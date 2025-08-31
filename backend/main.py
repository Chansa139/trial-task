from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import asyncio
import json
import os
from datetime import datetime, timedelta
import uuid
from enum import Enum

# Import your agent framework
from agents.malaysian_customer_service import MalaysianCustomerServiceAgent
from models.states import MasterAgentState
from models.enums import Nodes
from models.exceptions import *
from langchain.chat_models.base import BaseChatModel
from langchain_openai import ChatOpenAI
from utils.database import DatabaseManager
from utils.analytics import AnalyticsManager
from utils.notifications import NotificationManager
from utils.business_config import BusinessConfigManager
from utils.malaysian_localization import MalaysianLocalizer

app = FastAPI(
    title="Sistem Agen Perkhidmatan Pelanggan Malaysia",
    description="Sistem AI yang canggih untuk perkhidmatan pelanggan multibahasa di Malaysia",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware untuk Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dalam production, tentukan domain Lovable anda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
agent_instance = None
db_manager = DatabaseManager()
analytics_manager = AnalyticsManager()
notification_manager = NotificationManager()
business_config_manager = BusinessConfigManager()
localizer = MalaysianLocalizer()

# Models untuk API
class ChatMessage(BaseModel):
    role: str = Field(..., description="Peranan: 'user' atau 'assistant'")
    content: str = Field(..., description="Kandungan mesej")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Masa mesej")
    detected_language: Optional[str] = Field(None, description="Bahasa yang dikesan")
    intent: Optional[str] = Field(None, description="Niat pelanggan")
    confidence: Optional[float] = Field(None, description="Tahap keyakinan AI")

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mesej daripada pelanggan")
    session_id: str = Field(..., description="ID sesi perbualan")
    business_id: Optional[str] = Field(None, description="ID perniagaan")
    customer_info: Optional[Dict[str, Any]] = Field(None, description="Maklumat pelanggan")

class ChatResponse(BaseModel):
    message: str = Field(..., description="Jawapan daripada agen")
    session_id: str = Field(..., description="ID sesi perbualan")
    detected_language: Optional[str] = Field(None, description="Bahasa yang dikesan")
    intent: Optional[str] = Field(None, description="Niat pelanggan")
    confidence: Optional[float] = Field(None, description="Tahap keyakinan AI")
    timestamp: datetime = Field(default_factory=datetime.now, description="Masa jawapan")
    agent_id: Optional[str] = Field(None, description="ID agen yang digunakan")
    processing_time: Optional[float] = Field(None, description="Masa pemprosesan (saat)")

class BusinessConfig(BaseModel):
    business_id: str = Field(..., description="ID unik perniagaan")
    business_name: str = Field(..., description="Nama perniagaan")
    business_type: str = Field(..., description="Jenis perniagaan")
    primary_language: str = Field(default="Bahasa Malaysia", description="Bahasa utama")
    supported_languages: List[str] = Field(default=["Bahasa Malaysia", "English"], description="Bahasa yang disokong")
    business_hours: Dict[str, Any] = Field(default_factory=dict, description="Waktu operasi")
    contact_info: Dict[str, Any] = Field(default_factory=dict, description="Maklumat hubungan")
    knowledge_base_url: Optional[str] = Field(None, description="URL pangkalan pengetahuan")
    api_key: Optional[str] = Field(None, description="Kunci API")
    custom_responses: Optional[Dict[str, str]] = Field(None, description="Jawapan tersuai")
    escalation_rules: Optional[Dict[str, Any]] = Field(None, description="Peraturan eskalasi")

class AnalyticsRequest(BaseModel):
    business_id: str = Field(..., description="ID perniagaan")
    date_from: Optional[datetime] = Field(None, description="Tarikh mula")
    date_to: Optional[datetime] = Field(None, description="Tarikh akhir")
    metric_type: Optional[str] = Field(None, description="Jenis metrik")

class NotificationRequest(BaseModel):
    business_id: str = Field(..., description="ID perniagaan")
    message: str = Field(..., description="Mesej notifikasi")
    notification_type: str = Field(..., description="Jenis notifikasi")
    recipients: List[str] = Field(..., description="Senarai penerima")

# Initialize agent
async def get_agent(business_id: str = None):
    global agent_instance
    if agent_instance is None or business_id:
        # Get business configuration
        business_config = await business_config_manager.get_config(business_id)
        
        # Initialize with OpenAI model
        model = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        )
        
        agent_instance = MalaysianCustomerServiceAgent(
            model=model, 
            business_config=business_config
        )
    
    return agent_instance

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Sistem Agen Perkhidmatan Pelanggan Malaysia",
        "status": "berjalan",
        "version": "2.0.0",
        "timestamp": datetime.now(),
        "bahasa": "Bahasa Malaysia"
    }

@app.get("/health")
async def health_check():
    try:
        # Check database connection
        db_status = await db_manager.check_connection()
        
        # Check agent status
        agent_status = agent_instance is not None
        
        # Check external services
        external_services = {
            "openai": os.getenv("OPENAI_API_KEY") is not None,
            "database": db_status,
            "agent": agent_status
        }
        
        overall_status = all(external_services.values())
        
        return {
            "status": "sihat" if overall_status else "masalah",
            "timestamp": datetime.now(),
            "services": external_services,
            "uptime": "berjalan"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Ralat kesihatan sistem: {str(e)}",
                "timestamp": datetime.now()
            }
        )

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    start_time = datetime.now()
    
    try:
        # Validate business ID
        if request.business_id:
            business_config = await business_config_manager.get_config(request.business_id)
            if not business_config:
                raise HTTPException(
                    status_code=404, 
                    detail="Perniagaan tidak dijumpai. Sila semak ID perniagaan anda."
                )
        
        # Get agent instance
        agent = await get_agent(request.business_id)
        
        # Create state for the agent
        state = MasterAgentState(
            messages=[{"role": "user", "content": request.message}],
            session_id=request.session_id,
            business_id=request.business_id,
            customer_info=request.customer_info
        )
        
        # Process the message through the agent
        result = await agent.select_agent(state)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Extract response
        if "messages" in result and result["messages"]:
            response_message = result["messages"][-1].content
        else:
            response_message = "Maaf, saya tidak dapat memproses permintaan anda pada masa ini. Sila cuba lagi."
        
        # Extract metadata from trace if available
        detected_language = None
        intent = None
        confidence = None
        agent_id = None
        
        if "trace" in result and result["trace"]:
            trace_data = result["trace"][0]
            if "output" in trace_data:
                output = trace_data["output"]
                if isinstance(output, dict):
                    detected_language = output.get("detected_language")
                    intent = output.get("intent")
                    confidence = output.get("confidence")
                    agent_id = output.get("agent_id")
        
        # Create response
        response = ChatResponse(
            message=response_message,
            session_id=request.session_id,
            detected_language=detected_language,
            intent=intent,
            confidence=confidence,
            timestamp=datetime.now(),
            agent_id=agent_id,
            processing_time=processing_time
        )
        
        # Store conversation in database (background task)
        background_tasks.add_task(
            store_conversation,
            request.session_id,
            request.message,
            response_message,
            detected_language,
            intent,
            confidence,
            processing_time,
            request.business_id
        )
        
        # Update analytics (background task)
        background_tasks.add_task(
            update_analytics,
            request.business_id,
            detected_language,
            intent,
            processing_time
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error
        await db_manager.log_error(
            session_id=request.session_id,
            error_message=str(e),
            business_id=request.business_id
        )
        
        raise HTTPException(
            status_code=500, 
            detail=f"Ralat dalam memproses perbualan: {str(e)}"
        )

# Business configuration endpoints
@app.post("/business/configure")
async def configure_business(config: BusinessConfig):
    """Konfigurasi perniagaan untuk agen"""
    try:
        # Validate configuration
        if not config.business_name:
            raise HTTPException(
                status_code=400,
                detail="Nama perniagaan diperlukan"
            )
        
        # Store configuration
        await business_config_manager.save_config(config)
        
        # Reinitialize agent with new configuration
        global agent_instance
        agent_instance = None
        
        return {
            "message": "Konfigurasi perniagaan berjaya disimpan",
            "business_id": config.business_id,
            "timestamp": datetime.now()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ralat dalam menyimpan konfigurasi: {str(e)}"
        )

@app.get("/business/{business_id}/config")
async def get_business_config(business_id: str):
    """Dapatkan konfigurasi perniagaan"""
    try:
        config = await business_config_manager.get_config(business_id)
        if not config:
            raise HTTPException(
                status_code=404,
                detail="Konfigurasi perniagaan tidak dijumpai"
            )
        
        return {
            "business_id": business_id,
            "config": config,
            "timestamp": datetime.now()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ralat dalam mendapatkan konfigurasi: {str(e)}"
        )

# Analytics endpoints
@app.get("/analytics/{business_id}")
async def get_analytics(business_id: str, date_from: datetime = None, date_to: datetime = None):
    """Dapatkan analitik perniagaan"""
    try:
        if not date_from:
            date_from = datetime.now() - timedelta(days=30)
        if not date_to:
            date_to = datetime.now()
        
        analytics = await analytics_manager.get_business_analytics(
            business_id=business_id,
            date_from=date_from,
            date_to=date_to
        )
        
        return {
            "business_id": business_id,
            "period": {
                "from": date_from,
                "to": date_to
            },
            "analytics": analytics,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ralat dalam mendapatkan analitik: {str(e)}"
        )

@app.get("/analytics/{business_id}/languages")
async def get_language_analytics(business_id: str):
    """Dapatkan analitik bahasa"""
    try:
        analytics = await analytics_manager.get_language_analytics(business_id)
        return {
            "business_id": business_id,
            "language_analytics": analytics,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ralat dalam mendapatkan analitik bahasa: {str(e)}"
        )

@app.get("/analytics/{business_id}/intents")
async def get_intent_analytics(business_id: str):
    """Dapatkan analitik niat pelanggan"""
    try:
        analytics = await analytics_manager.get_intent_analytics(business_id)
        return {
            "business_id": business_id,
            "intent_analytics": analytics,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ralat dalam mendapatkan analitik niat: {str(e)}"
        )

# Notification endpoints
@app.post("/notifications/send")
async def send_notification(request: NotificationRequest):
    """Hantar notifikasi"""
    try:
        await notification_manager.send_notification(
            business_id=request.business_id,
            message=request.message,
            notification_type=request.notification_type,
            recipients=request.recipients
        )
        
        return {
            "message": "Notifikasi berjaya dihantar",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ralat dalam menghantar notifikasi: {str(e)}"
        )

# System information endpoints
@app.get("/languages")
async def get_supported_languages():
    """Dapatkan senarai bahasa yang disokong"""
    return {
        "languages": [
            {"code": "ms", "name": "Bahasa Malaysia", "native_name": "Bahasa Malaysia"},
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "zh", "name": "Chinese", "native_name": "中文"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "th", "name": "Thai", "native_name": "ไทย"}
        ],
        "default_language": "ms",
        "timestamp": datetime.now()
    }

@app.get("/intents")
async def get_supported_intents():
    """Dapatkan senarai niat yang disokong"""
    return {
        "intents": [
            {"code": "complaint", "name": "Aduan", "description": "Aduan atau masalah pelanggan"},
            {"code": "order", "name": "Pesanan", "description": "Pertanyaan berkaitan pesanan"},
            {"code": "support", "name": "Sokongan", "description": "Permintaan sokongan teknikal"},
            {"code": "billing", "name": "Bil", "description": "Pertanyaan bil dan pembayaran"},
            {"code": "general", "name": "Umum", "description": "Soalan atau maklumat umum"},
            {"code": "product", "name": "Produk", "description": "Pertanyaan tentang produk"},
            {"code": "delivery", "name": "Penghantaran", "description": "Pertanyaan tentang penghantaran"},
            {"code": "return", "name": "Pemulangan", "description": "Permintaan pemulangan barang"}
        ],
        "timestamp": datetime.now()
    }

@app.get("/business-types")
async def get_business_types():
    """Dapatkan senarai jenis perniagaan"""
    return {
        "business_types": [
            {"code": "ecommerce", "name": "E-dagang", "description": "Perdagangan dalam talian"},
            {"code": "retail", "name": "Runcit", "description": "Peruncitan"},
            {"code": "restaurant", "name": "Restoran", "description": "Restoran dan makanan"},
            {"code": "hotel", "name": "Hotel", "description": "Penginapan dan hospitaliti"},
            {"code": "banking", "name": "Perbankan", "description": "Perkhidmatan kewangan"},
            {"code": "telecom", "name": "Telekomunikasi", "description": "Perkhidmatan telekomunikasi"},
            {"code": "healthcare", "name": "Kesihatan", "description": "Perkhidmatan kesihatan"},
            {"code": "education", "name": "Pendidikan", "description": "Institusi pendidikan"},
            {"code": "logistics", "name": "Logistik", "description": "Perkhidmatan penghantaran"},
            {"code": "other", "name": "Lain-lain", "description": "Jenis perniagaan lain"}
        ],
        "timestamp": datetime.now()
    }

# Background task functions
async def store_conversation(session_id: str, user_message: str, agent_response: str, 
                           detected_language: str, intent: str, confidence: float, 
                           processing_time: float, business_id: str):
    """Simpan perbualan dalam pangkalan data"""
    try:
        await db_manager.store_conversation(
            session_id=session_id,
            user_message=user_message,
            agent_response=agent_response,
            detected_language=detected_language,
            intent=intent,
            confidence=confidence,
            processing_time=processing_time,
            business_id=business_id
        )
    except Exception as e:
        print(f"Ralat dalam menyimpan perbualan: {e}")

async def update_analytics(business_id: str, detected_language: str, intent: str, processing_time: float):
    """Kemaskini analitik"""
    try:
        await analytics_manager.update_metrics(
            business_id=business_id,
            detected_language=detected_language,
            intent=intent,
            processing_time=processing_time
        )
    except Exception as e:
        print(f"Ralat dalam mengemaskini analitik: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)