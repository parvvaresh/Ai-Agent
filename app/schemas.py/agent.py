from pydantic import BaseModel
from typing import Optional

class AskRequest(BaseModel):
    """Request model for asking the agent"""
    query: str
    session_id: Optional[str] = "default_session"

class AskResponse(BaseModel):
    """Response model from the agent"""
    response: str
    session_id: str