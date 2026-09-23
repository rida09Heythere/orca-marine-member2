from pydantic import BaseModel
from typing import Optional


class UserQuery(BaseModel):
    query: str
    location: Optional[str] = None
    language: str = "en"
    user_type: Optional[str] = None