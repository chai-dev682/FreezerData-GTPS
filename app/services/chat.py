from typing import List, Dict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from app.core.config import settings, ModelType
from app.services.graph.graph_state import GraphState, DatabaseEnum
from app.services.graph.graph_nodes import (
    query_transformation_node,
    determine_database,
    txt2sql_node,
    data_retrieval_node,
    visualization_node
)

class ChatService:
    def __init__(self):
        self.data_retrieval_graph = self._build_data_retrieval_graph()
        self.model = ChatOpenAI(
            model=ModelType.gpt4o,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def _build_data_retrieval_graph(self):
        workflow = StateGraph(state_schema=GraphState)
        
        # Add nodes
        workflow.add_node("query_transformation", query_transformation_node)
        workflow.add_node("txt2sql", txt2sql_node)
        workflow.add_node("data_retrieval", data_retrieval_node)
        workflow.add_node("visual_show", visualization_node)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "query_transformation",
            determine_database,
            {
                DatabaseEnum.MYSQL: "txt2sql",
                DatabaseEnum.VECTORDB: "data_retrieval"
            }
        )

        # Add edges
        workflow.add_edge("txt2sql", "data_retrieval")
        workflow.add_edge("data_retrieval", "visual_show")

        workflow.set_entry_point("query_transformation")
        workflow.set_finish_point("visual_show")
        
        return workflow.compile()

    def process_message(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        messages = conversation_history + [{"role": "user", "content": query}]
        initial_state = GraphState(messages=messages, query=query)
        
        final_state = self.data_retrieval_graph.invoke(initial_state)
        
        # Check if visualization is needed
        # if "compare" in query.lower() or "chart" in query.lower():
        return {"response": final_state["messages"][-1]["content"],
                "visualization": final_state["visualization"]}
        # return {"response": final_state["messages"][-1]["content"]}

chat_service = ChatService()