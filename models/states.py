from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime


class MasterAgentState(BaseModel):
    """State management for the master agent workflow"""
    messages: List[Dict[str, Any]]
    session_id: str
    detected_language: Optional[str] = None
    classified_intent: Optional[str] = None
    retrieved_knowledge: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        arbitrary_types_allowed = True