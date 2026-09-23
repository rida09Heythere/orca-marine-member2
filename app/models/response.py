from pydantic import BaseModel
from typing import Optional, Any


class Evidence(BaseModel):
    source: Optional[str] = None
    tool: Optional[str] = None
    status: Optional[str] = None
    data: Optional[Any] = None
    message: Optional[str] = None


class SafetyAlert(BaseModel):
    level: str
    type: str
    message: str


class SafetyStatus(BaseModel):
    overall_status: str
    alerts: list[SafetyAlert] = []


class AgentInfo(BaseModel):
    name: str
    tools_used: list[str] = []


class ORCAResponse(BaseModel):
    query: str
    location: Optional[str] = None
    language: str
    user_type: Optional[str] = None
    agent: AgentInfo
    answer: str
    safety: Optional[SafetyStatus] = None
    evidence: list[Evidence] = []
