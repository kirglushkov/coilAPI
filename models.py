from datetime import datetime
from pydantic import BaseModel

class Coil(BaseModel):
    id: int
    length: float
    weight: float
    deleted_at: datetime = None
