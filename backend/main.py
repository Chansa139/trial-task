from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
from datetime import datetime

# Import your agent framework
from agents.malaysian_customer_service import MalaysianCustomerServiceAgent
from models.states import MasterAgentState
from models.enums import Nodes
from langchain.chat_models.base import BaseChatModel
from langchain_openai import ChatOpenAI

app = FastAPI(title="Malaysian Customer Service Agent API", version="1.0.0")

# CORS middleware for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent_instance = None

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    session_id: str
    business_config: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    detected_language: Optional[str] = None
    intent: Optional[str] = None
    confidence: Optional[float] = None
    timestamp: datetime

class BusinessConfig(BaseModel):
    business_name: str
    primary_language: str = "Bahasa Malaysia"
    supported_languages: List[str] = ["Bahasa Malaysia", "English"]
    knowledge_base_url: Optional[str] = None
    api_key: Optional[str] = None

# Initialize agent
async def get_agent():
    global agent_instance
    if agent_instance is None:
        # Initialize with OpenAI model
        model = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key="your-openai-api-key"  # Replace with actual key
        )
        
        # Default business configuration
        default_config = {
            "business_name": "Demo Business",
            "primary_language": "Bahasa Malaysia",
            "supported_languages": ["Bahasa Malaysia", "English", "Chinese", "Tamil"],
            "knowledge_base_url": "https://api.example.com/knowledge",
            "api_key": "demo-api-key"
        }
        
        agent_instance = MalaysianCustomerServiceAgent(model=model, business_config=default_config)
    
    return agent_instance

@app.get("/")
async def root():
    return {"message": "Malaysian Customer Service Agent API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        agent = await get_agent()
        
        # Create state for the agent
        state = MasterAgentState(
            messages=[{"role": "user", "content": request.message}],
            session_id=request.session_id
        )
        
        # Process the message through the agent
        result = await agent.select_agent(state)
        
        # Extract response
        if "messages" in result and result["messages"]:
            response_message = result["messages"][-1].content
        else:
            response_message = "I apologize, but I couldn't process your request at the moment."
        
        # Extract metadata from trace if available
        detected_language = None
        intent = None
        confidence = None
        
        if "trace" in result and result["trace"]:
            trace_data = result["trace"][0]
            if "output" in trace_data:
                output = trace_data["output"]
                if isinstance(output, dict):
                    detected_language = output.get("detected_language")
                    intent = output.get("intent")
                    confidence = output.get("confidence")
        
        return ChatResponse(
            message=response_message,
            session_id=request.session_id,
            detected_language=detected_language,
            intent=intent,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/configure")
async def configure_business(config: BusinessConfig):
    """Configure the agent for a specific business"""
    try:
        global agent_instance
        
        # Reinitialize agent with new configuration
        model = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key="your-openai-api-key"  # Replace with actual key
        )
        
        business_config = {
            "business_name": config.business_name,
            "primary_language": config.primary_language,
            "supported_languages": config.supported_languages,
            "knowledge_base_url": config.knowledge_base_url,
            "api_key": config.api_key
        }
        
        agent_instance = MalaysianCustomerServiceAgent(model=model, business_config=business_config)
        
        return {"message": "Business configuration updated successfully", "config": business_config}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error configuring business: {str(e)}")

@app.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "ms", "name": "Bahasa Malaysia", "native_name": "Bahasa Malaysia"},
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "zh", "name": "Chinese", "native_name": "中文"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"}
        ]
    }

@app.get("/intents")
async def get_supported_intents():
    """Get list of supported intents"""
    return {
        "intents": [
            {"code": "complaint", "name": "Complaint", "description": "Customer complaints or issues"},
            {"code": "order", "name": "Order", "description": "Order-related inquiries"},
            {"code": "support", "name": "Support", "description": "Technical support requests"},
            {"code": "billing", "name": "Billing", "description": "Billing and payment inquiries"},
            {"code": "general", "name": "General", "description": "General questions or information"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)