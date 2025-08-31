import os
from typing import Dict, Any

class Config:
    """Configuration class for Malaysian Customer Service Agent"""
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "malaysian_agent.db")
    DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    
    # Business Configuration
    DEFAULT_BUSINESS_NAME = os.getenv("DEFAULT_BUSINESS_NAME", "Perniagaan Demo")
    DEFAULT_PRIMARY_LANGUAGE = os.getenv("DEFAULT_PRIMARY_LANGUAGE", "Bahasa Malaysia")
    DEFAULT_SUPPORTED_LANGUAGES = os.getenv("DEFAULT_SUPPORTED_LANGUAGES", "Bahasa Malaysia,English").split(",")
    
    # Notification Configuration
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    
    # Analytics Configuration
    ANALYTICS_CACHE_TTL = int(os.getenv("ANALYTICS_CACHE_TTL", "300"))  # 5 minutes
    ANALYTICS_RETENTION_DAYS = int(os.getenv("ANALYTICS_RETENTION_DAYS", "365"))
    
    # Security Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_BURST = int(os.getenv("RATE_LIMIT_BURST", "100"))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "malaysian_agent.log")
    
    # Malaysian Specific Configuration
    MALAYSIA_TIMEZONE = "Asia/Kuala_Lumpur"
    MALAYSIA_CURRENCY = "MYR"
    MALAYSIA_PHONE_PREFIX = "+60"
    
    # Business Hours (Malaysian Standard)
    DEFAULT_BUSINESS_HOURS = {
        "monday": {"start": "09:00", "end": "18:00", "is_open": True},
        "tuesday": {"start": "09:00", "end": "18:00", "is_open": True},
        "wednesday": {"start": "09:00", "end": "18:00", "is_open": True},
        "thursday": {"start": "09:00", "end": "18:00", "is_open": True},
        "friday": {"start": "09:00", "end": "18:00", "is_open": True},
        "saturday": {"start": "10:00", "end": "16:00", "is_open": True},
        "sunday": {"start": "10:00", "end": "16:00", "is_open": False}
    }
    
    # Supported Languages
    SUPPORTED_LANGUAGES = [
        {"code": "ms", "name": "Bahasa Malaysia", "native_name": "Bahasa Malaysia"},
        {"code": "en", "name": "English", "native_name": "English"},
        {"code": "zh", "name": "Chinese", "native_name": "中文"},
        {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"},
        {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
        {"code": "th", "name": "Thai", "native_name": "ไทย"}
    ]
    
    # Supported Intents
    SUPPORTED_INTENTS = [
        {"code": "complaint", "name": "Aduan", "description": "Aduan atau masalah pelanggan"},
        {"code": "order", "name": "Pesanan", "description": "Pertanyaan berkaitan pesanan"},
        {"code": "support", "name": "Sokongan", "description": "Permintaan sokongan teknikal"},
        {"code": "billing", "name": "Bil", "description": "Pertanyaan bil dan pembayaran"},
        {"code": "general", "name": "Umum", "description": "Soalan atau maklumat umum"},
        {"code": "product", "name": "Produk", "description": "Pertanyaan tentang produk"},
        {"code": "delivery", "name": "Penghantaran", "description": "Pertanyaan tentang penghantaran"},
        {"code": "return", "name": "Pemulangan", "description": "Permintaan pemulangan barang"}
    ]
    
    # Business Types
    BUSINESS_TYPES = [
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
    ]
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            "api": {
                "host": cls.API_HOST,
                "port": cls.API_PORT,
                "debug": cls.API_DEBUG
            },
            "openai": {
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL,
                "temperature": cls.OPENAI_TEMPERATURE
            },
            "database": {
                "url": cls.DATABASE_URL,
                "pool_size": cls.DATABASE_POOL_SIZE
            },
            "business": {
                "default_name": cls.DEFAULT_BUSINESS_NAME,
                "default_primary_language": cls.DEFAULT_PRIMARY_LANGUAGE,
                "default_supported_languages": cls.DEFAULT_SUPPORTED_LANGUAGES,
                "default_business_hours": cls.DEFAULT_BUSINESS_HOURS
            },
            "notification": {
                "smtp_host": cls.SMTP_HOST,
                "smtp_port": cls.SMTP_PORT,
                "smtp_username": cls.SMTP_USERNAME,
                "smtp_password": cls.SMTP_PASSWORD
            },
            "analytics": {
                "cache_ttl": cls.ANALYTICS_CACHE_TTL,
                "retention_days": cls.ANALYTICS_RETENTION_DAYS
            },
            "security": {
                "secret_key": cls.SECRET_KEY,
                "access_token_expire_minutes": cls.ACCESS_TOKEN_EXPIRE_MINUTES
            },
            "rate_limiting": {
                "per_minute": cls.RATE_LIMIT_PER_MINUTE,
                "burst": cls.RATE_LIMIT_BURST
            },
            "logging": {
                "level": cls.LOG_LEVEL,
                "file": cls.LOG_FILE
            },
            "malaysia": {
                "timezone": cls.MALAYSIA_TIMEZONE,
                "currency": cls.MALAYSIA_CURRENCY,
                "phone_prefix": cls.MALAYSIA_PHONE_PREFIX
            },
            "supported_languages": cls.SUPPORTED_LANGUAGES,
            "supported_intents": cls.SUPPORTED_INTENTS,
            "business_types": cls.BUSINESS_TYPES
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration"""
        errors = []
        
        # Check required configurations
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your-openai-api-key":
            errors.append("OPENAI_API_KEY is required")
        
        if not cls.SECRET_KEY or cls.SECRET_KEY == "your-secret-key-here":
            errors.append("SECRET_KEY is required")
        
        # Check port range
        if not (1 <= cls.API_PORT <= 65535):
            errors.append("API_PORT must be between 1 and 65535")
        
        # Check temperature range
        if not (0.0 <= cls.OPENAI_TEMPERATURE <= 2.0):
            errors.append("OPENAI_TEMPERATURE must be between 0.0 and 2.0")
        
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True