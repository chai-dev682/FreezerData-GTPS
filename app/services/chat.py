from typing import List, Dict, Optional
from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI

from app.core.config import settings, ModelType
from app.core.logging import logger
from app.schemas.freezer_data import ObjectDB
from app.services.graph.graph_state import GraphState
from app.services.graph.graph_nodes import (
    data_retrieval_node,
    extract_object_id_node,
    has_object_id,
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
        workflow.add_node("extract_object_id", extract_object_id_node)
        workflow.add_node("data_retrieval", data_retrieval_node)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            START,
            has_object_id,
            {
                "extract_object_id": "extract_object_id",
                "data_retrieval": "data_retrieval",
            }
        )
        
        workflow.set_finish_point("data_retrieval")
        workflow.set_finish_point("extract_object_id")
        
        return workflow.compile()

    def process_message(self, query: str, messages: List[Dict[str, str]], obj: Optional[ObjectDB] = None) -> Dict[str, str]:
        """
        Process an incoming chat message through the workflow graph.
        
        Args:
            query: The user's input query
            messages: The conversation history
            
        Returns:
            Dict containing the response and any additional information
        """
        try:
            # Initialize graph state
            state = GraphState(
                messages=messages.copy(),
                query=query,
                object=obj
            )
            
            # Add user message to state
            state.messages.append({
                "role": "user",
                "content": query
            })
            
            # Run the workflow graph
            result = self.data_retrieval_graph.invoke({
                "messages": state.messages,
                "query": query,
                "object": state.object
            })
            
            # Extract the last assistant message as the response
            assistant_messages = [
                msg["content"] for msg in result["messages"] 
                if msg["role"] == "assistant"
            ]
            
            response = assistant_messages[-1] if assistant_messages else "I apologize, but I couldn't process your request."
            
            return {
                "response": response,
                "state": result
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "response": "I encountered an error while processing your request. Please try again.",
                "state": None
            }

chat_service = ChatService()