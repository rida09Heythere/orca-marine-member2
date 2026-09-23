from pydantic import BaseModel
from typing import Any, Optional


class ToolResult(BaseModel):
    tool: str
    status: str
    data: Optional[Any] = None
    message: str
    source: Optional[str] = None
