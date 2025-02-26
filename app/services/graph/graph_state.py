from typing import List, Dict, Optional
from pydantic import BaseModel
from app.schemas.freezer_data import ObjectDB

class Message(BaseModel):
    role: str
    content: str

class GraphState(BaseModel):
    messages: List[Dict[str, str]]
    query: Optional[str] = None
    object: Optional[ObjectDB] = None
