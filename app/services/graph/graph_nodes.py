from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import pandas as pd

from app.core.config import settings, ModelType
from app.db.vectordb import vector_db
from app.db.mysql import mysql_db
from app.core.logging import logger
from app.core.prompt_templates.query_transformation import query_transformation
from app.core.prompt_templates.sql_vector import sql_vector
from app.core.prompt_templates.generate_sql import generate_sql
from app.core.prompt_templates.generate_response import generate_response
from app.core.function_templates.sql_vector import sql_vector_tool
from .graph_state import GraphState, DatabaseEnum

model = ChatOpenAI(
    model=ModelType.gpt4o,
    openai_api_key=settings.OPENAI_API_KEY
)

def extract_function_params(prompt, function):
    function_name = function[0]["function"]["name"]
    arg_name = list(function[0]["function"]["parameters"]['properties'].keys())[0]
    model_ = model.bind_tools(function, tool_choice=function_name)
    messages = [SystemMessage(prompt)]
    tool_call = model_.invoke(messages).tool_calls
    prop = tool_call[0]['args'][arg_name]

    return prop

def format_conversation_history(messages: List[Dict[str, str]]) -> str:
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

def query_transformation_node(state: GraphState) -> GraphState:
    # response = model.invoke([state.messages + SystemMessage(query_transformation.format(
    #     query=state.messages[-1]["content"]
    # ))])
    
    # state.query = response.content
    return state

def determine_database(state: GraphState) -> DatabaseEnum:
    is_sql = extract_function_params(prompt=sql_vector.format(
        query=state.query,
        conversation=format_conversation_history(state.messages)
    ), function=sql_vector_tool)
    if is_sql == "yes":
        return DatabaseEnum.MYSQL
    else:
        return DatabaseEnum.VECTORDB

def txt2sql_node(state: GraphState) -> GraphState:
    state.database = DatabaseEnum.MYSQL
    response = model.invoke(state.messages + [SystemMessage(generate_sql.format(
        query=state.query
    ))])
    state.sql_query = response.content.strip().replace('``sql', '').replace('`', '')
    return state

def data_retrieval_node(state: GraphState) -> GraphState:
    try:
        if state.database == DatabaseEnum.MYSQL:
            print(state.sql_query)
            results = mysql_db.query(state.sql_query)
        else:
            print(state.query)
            results = vector_db.query(state.query, top_k=3)
            results = [result.model_dump() for result in results]

        state.raw_data = results
        
        # Dynamically build context string using only available fields
        context = "\n\n".join(
            "\n".join([
                f"{key.replace('_', ' ').title()}: {value}"
                for key, value in lease.items()
                if value is not None
            ]) for lease in results
        )
        prompt = generate_response.format(
            context=context,
        )

        response = model.invoke(state.messages + [HumanMessage(prompt)])
        state.messages.append({"role": "assistant", "content": response.content})

    except Exception as e:
        logger.error(f"Error in data retrieval: {str(e)}")
        state.messages.append({
            "role": "assistant",
            "content": "I apologize, but I encountered an error while retrieving the information. Could you please rephrase your question?"
        })

    return state

def visualization_node(state: GraphState) -> GraphState:
    if not state.raw_data:
        state.visualization = {"show": False}
        return state

    # Define visualization function
    visualization_function = {
        "name": "determine_visualization",
        "description": "Determine the best visualization type for the given data and query",
        "parameters": {
            "type": "object",
            "properties": {
                "visualization_type": {
                    "type": "string",
                    "enum": ["bar", "line", "table", "none"],
                    "description": "Type of visualization to show. 'bar' for comparisons, 'line' for trends, 'table' for raw data, 'none' for no visualization"
                },
                "x_axis": {
                    "type": "string",
                    "description": "Field to use for x-axis"
                },
                "y_axis": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to use for y-axis"
                }
            },
            "required": ["visualization_type"]
        }
    }

    # Get visualization recommendation from LLM
    model_with_tools = model.bind_tools([visualization_function])
    response = model_with_tools.invoke(state.messages + [HumanMessage(f"Query: {state.query}\nAvailable fields: {list(state.raw_data[0].keys())}")])

    # Parse the function call
    if response.tool_calls:
        args = response.tool_calls[0]['args']
        state.visualization = {
            "show": args["visualization_type"] != "none",
            "type": args["visualization_type"],
            "data": pd.DataFrame(state.raw_data),
            "x": args.get("x_axis", ""),
            "y": args.get("y_axis", [])
        }
    else:
        state.visualization = {"show": False}
    
    return state