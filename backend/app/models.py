from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class CallLog(BaseModel):
    id: str
    agent_id: str
    lead_phone: str
    status: str
    duration: int
    timestamp: datetime
    transcription: Optional[str] = None
    summary: Optional[str] = None

class Script(BaseModel):
    id: str
    name: str
    content: List[dict] # Simplified for now
    created_at: datetime
