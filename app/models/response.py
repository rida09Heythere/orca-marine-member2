from pydantic import BaseModel
from typing import Optional


class Evidence(BaseModel):
    source: str
    tool: Optional[str] = None
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance_to_boundary_m: Optional[float] = None
    message: Optional[str] = None


class AgentInfo(BaseModel):
    name: str
    tool_used: Optional[str] = None


class ORCAResponse(BaseModel):
    query: str
    location: Optional[str] = None
    language: str
    user_type: Optional[str] = None
    agent: AgentInfo
    answer: str
    evidence: Optional[Evidence] = None
