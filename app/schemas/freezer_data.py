from pydantic import BaseModel
from datetime import date
from typing import Optional

class ObjectDB(BaseModel):
    id: int
    object_id: int
    created_at: date
    updated_at: date

class Manuals(BaseModel):
    id: int
    manual_id: int
    created_at: date
    updated_at: date

class ObjectManual(BaseModel):
    id: int
    object_id: int
    manual_id: int
    created_at: date
    updated_at: date
    