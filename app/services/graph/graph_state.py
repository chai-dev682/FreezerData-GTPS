from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel

class DatabaseEnum(str, Enum):
    MYSQL = "mysql"
    VECTORDB = "vectordb"

class Message(BaseModel):
    role: str
    content: str

class GraphState(BaseModel):
    messages: List[Dict[str, str]]
    database: Optional[DatabaseEnum] = DatabaseEnum.VECTORDB
    query: Optional[str] = None
    sql_query: Optional[str] = None
    raw_data: Optional[List[Dict]] = None
    visualization: Optional[Dict] = None