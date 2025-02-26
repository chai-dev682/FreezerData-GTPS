from pydantic import BaseModel
from typing import Optional

class ObjectDB(BaseModel):
    id: int
    object_id: int
    max_working_pressure_bar: int
    description: str
    location: str
    complex: str
    building_data: str
    servicecontract_nr: str
    sla: str
    brand: str
    model: str
    refrigerant: str
    refrigerant_filling_kg: float
    config_file: Optional[str] = None

class Manuals(BaseModel):
    id: int
    pdf_file_name: str
    tech_specification: Optional[str] = None
    manual_structure: Optional[str] = None

class ObjectManual(BaseModel):
    id: int
    object_id: int
    manual_id: int
    