from pydantic import BaseModel
from typing import Optional


class MarineData(BaseModel):
    latitude: float
    longitude: float
    value: Optional[float] = None
    unit: Optional[str] = None
    timestamp: Optional[str] = None
    source: str
    status: str
