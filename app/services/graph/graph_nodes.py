from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings, ModelType
from app.core.logging import logger
from app.core.prompt_templates.troubleshoot import troubleshoot
from app.core.function_templates.extract_object_id import extract_object_id_tool
from app.db.mysql import mysql_db
from app.db.vectordb import vector_db
from app.schemas.freezer_data import ObjectDB
from .graph_state import GraphState

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

def has_object_id(state: GraphState) -> str:
    return "extract_object_id" if state.object is None else "data_retrieval"

def extract_object_id_node(state: GraphState) -> GraphState:
    try:
        user_query = state.query

        extracted_id = extract_function_params(
            prompt=f"Extract the object ID from the following user query. user_query: {user_query}",
            function=extract_object_id_tool
        )

        if extracted_id is not None:
            # Query object details from MySQL database
            sql_query = f"SELECT * FROM ObjectDB WHERE object_id = {extracted_id}"
            results = mysql_db.query(sql_query)
            
            if results and len(results) > 0:
                obj_info = results[0]
                state.object = ObjectDB(**obj_info)
                info_message = f"""I'll help you with information about object #{extracted_id}.\n
                    Here are the detailed specifications:\n
                    - Maximum Working Pressure: {obj_info['max_working_pressure_bar']} bar\n
                    - Location: {obj_info['location']}\n
                    - Complex: {obj_info['complex']}\n
                    - Building Data: {obj_info['building_data']}\n
                    - Service Contract Number: {obj_info['servicecontract_nr']}\n
                    - SLA: {obj_info['sla']}\n
                    - Brand: {obj_info['brand']}\n
                    - Model: {obj_info['model']}\n
                    - Refrigerant: {obj_info['refrigerant']}\n
                    - Refrigerant Filling: {obj_info['refrigerant_filling_kg']} kg\n
                """
                
                state.messages.append({
                    "role": "assistant",
                    "content": info_message
                })
            else:
                state.messages.append({
                    "role": "assistant",
                    "content": f"I found object #{extracted_id}, but couldn't retrieve its details. Please try again."
                })
        else:
            state.messages.append({
                "role": "assistant",
                "content": "Unfortunately I couldn't extract your object id from your query. Please try again."
            })
        
    except Exception as e:
        logger.error(f"Error in object ID extraction: {str(e)}")
        state.object = None
    
    return state

def data_retrieval_node(state: GraphState) -> GraphState:
    try:
        # Get relevant context from vector database using the user's query
        context_results = vector_db.query(state.query, state.object.object_id)
        
        # Format conversation history for context
        conversation_history = format_conversation_history(state.messages)
        
        # Prepare system message with context from vector DB
        system_message = troubleshoot.format(context_results=context_results, object_info=state.object, conversation_history=conversation_history)
        
        # Generate response using the model
        response = model.invoke([
            SystemMessage(content=system_message),
            HumanMessage(content=state.query)
        ])
        
        # Add response to conversation history
        state.messages.append({
            "role": "assistant",
            "content": response.content
        })
        
    except Exception as e:
        logger.error(f"Error in data retrieval: {str(e)}")
        state.messages.append({
            "role": "assistant",
            "content": "I apologize, but I encountered an error while processing your request. Could you please rephrase your question?"
        })
    
    return state
