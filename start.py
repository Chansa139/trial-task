#!/usr/bin/env python3
"""
Malaysian Customer Service Agent - Startup Script
Sistem Agen Perkhidmatan Pelanggan Malaysia - Skrip Permulaan
"""

import os
import sys
import asyncio
import uvicorn
from loguru import logger
from config import Config

def setup_logging():
    """Setup logging configuration"""
    logger.remove()  # Remove default handler
    
    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=Config.LOG_LEVEL,
        colorize=True
    )
    
    # Add file handler
    logger.add(
        Config.LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=Config.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

def check_environment():
    """Check environment setup"""
    logger.info("Memeriksa persekitaran sistem...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 atau lebih tinggi diperlukan")
        sys.exit(1)
    
    # Check required environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Pembolehubah persekitaran yang diperlukan tidak ditemui: {', '.join(missing_vars)}")
        logger.info("Sila set pembolehubah berikut:")
        for var in missing_vars:
            logger.info(f"  export {var}=your_value_here")
        sys.exit(1)
    
    logger.success("Persekitaran sistem OK")

def validate_config():
    """Validate configuration"""
    logger.info("Mengesahkan konfigurasi...")
    
    if not Config.validate_config():
        logger.error("Konfigurasi tidak sah")
        sys.exit(1)
    
    logger.success("Konfigurasi sah")

async def initialize_database():
    """Initialize database"""
    logger.info("Memulakan pangkalan data...")
    
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        # Check database connection
        if await db_manager.check_connection():
            logger.success("Pangkalan data berjaya disambung")
        else:
            logger.error("Gagal menyambung ke pangkalan data")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Ralat dalam memulakan pangkalan data: {e}")
        sys.exit(1)

async def initialize_services():
    """Initialize all services"""
    logger.info("Memulakan perkhidmatan...")
    
    try:
        # Initialize business config manager
        from utils.business_config import BusinessConfigManager
        business_config_manager = BusinessConfigManager()
        logger.info("Pengurus konfigurasi perniagaan dimulakan")
        
        # Initialize analytics manager
        from utils.analytics import AnalyticsManager
        analytics_manager = AnalyticsManager()
        logger.info("Pengurus analitik dimulakan")
        
        # Initialize notification manager
        from utils.notifications import NotificationManager
        notification_manager = NotificationManager()
        logger.info("Pengurus notifikasi dimulakan")
        
        # Initialize Malaysian localizer
        from utils.malaysian_localization import MalaysianLocalizer
        localizer = MalaysianLocalizer()
        logger.info("Penyetempatan Malaysia dimulakan")
        
        logger.success("Semua perkhidmatan berjaya dimulakan")
        
    except Exception as e:
        logger.error(f"Ralat dalam memulakan perkhidmatan: {e}")
        sys.exit(1)

def print_startup_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🇲🇾 SISTEM AGEN PERKHIDMATAN PELANGGAN MALAYSIA 🇲🇾      ║
    ║                                                              ║
    ║    Sistem AI yang canggih untuk perkhidmatan pelanggan      ║
    ║    multibahasa di Malaysia                                   ║
    ║                                                              ║
    ║    Versi: 2.0.0                                              ║
    ║    Bahasa: Bahasa Malaysia                                   ║
    ║    Dibangunkan untuk pasaran Malaysia                        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_configuration_info():
    """Print configuration information"""
    logger.info("Maklumat Konfigurasi:")
    logger.info(f"  - Host: {Config.API_HOST}")
    logger.info(f"  - Port: {Config.API_PORT}")
    logger.info(f"  - Debug: {Config.API_DEBUG}")
    logger.info(f"  - Model OpenAI: {Config.OPENAI_MODEL}")
    logger.info(f"  - Suhu: {Config.OPENAI_TEMPERATURE}")
    logger.info(f"  - Pangkalan Data: {Config.DATABASE_URL}")
    logger.info(f"  - Tahap Log: {Config.LOG_LEVEL}")
    logger.info(f"  - Zon Masa: {Config.MALAYSIA_TIMEZONE}")
    logger.info(f"  - Mata Wang: {Config.MALAYSIA_CURRENCY}")

def print_supported_features():
    """Print supported features"""
    logger.info("Ciri-ciri yang Disokong:")
    logger.info(f"  - Bahasa: {len(Config.SUPPORTED_LANGUAGES)} bahasa")
    for lang in Config.SUPPORTED_LANGUAGES:
        logger.info(f"    * {lang['native_name']} ({lang['code']})")
    
    logger.info(f"  - Niat: {len(Config.SUPPORTED_INTENTS)} kategori")
    for intent in Config.SUPPORTED_INTENTS:
        logger.info(f"    * {intent['name']} ({intent['code']})")
    
    logger.info(f"  - Jenis Perniagaan: {len(Config.BUSINESS_TYPES)} jenis")
    for business_type in Config.BUSINESS_TYPES:
        logger.info(f"    * {business_type['name']} ({business_type['code']})")

def print_api_endpoints():
    """Print API endpoints information"""
    logger.info("Endpoint API yang Tersedia:")
    logger.info("  - GET  /                    - Maklumat sistem")
    logger.info("  - GET  /health              - Semakan kesihatan")
    logger.info("  - POST /chat                - Perbualan dengan agen")
    logger.info("  - POST /business/configure  - Konfigurasi perniagaan")
    logger.info("  - GET  /business/{id}/config - Dapatkan konfigurasi")
    logger.info("  - GET  /analytics/{id}      - Analitik perniagaan")
    logger.info("  - GET  /languages           - Bahasa yang disokong")
    logger.info("  - GET  /intents             - Niat yang disokong")
    logger.info("  - GET  /business-types      - Jenis perniagaan")
    logger.info("  - POST /notifications/send  - Hantar notifikasi")

async def main():
    """Main startup function"""
    try:
        # Print startup banner
        print_startup_banner()
        
        # Setup logging
        setup_logging()
        logger.info("Memulakan Sistem Agen Perkhidmatan Pelanggan Malaysia...")
        
        # Check environment
        check_environment()
        
        # Validate configuration
        validate_config()
        
        # Initialize database
        await initialize_database()
        
        # Initialize services
        await initialize_services()
        
        # Print configuration info
        print_configuration_info()
        
        # Print supported features
        print_supported_features()
        
        # Print API endpoints
        print_api_endpoints()
        
        logger.success("Sistem siap untuk digunakan!")
        logger.info(f"Server akan berjalan di http://{Config.API_HOST}:{Config.API_PORT}")
        logger.info("Tekan Ctrl+C untuk berhenti")
        
        # Start the server
        uvicorn.run(
            "backend.main:app",
            host=Config.API_HOST,
            port=Config.API_PORT,
            reload=Config.API_DEBUG,
            log_level=Config.LOG_LEVEL.lower()
        )
        
    except KeyboardInterrupt:
        logger.info("Menerima isyarat berhenti...")
        logger.info("Sistem dihentikan dengan selamat")
    except Exception as e:
        logger.error(f"Ralat dalam memulakan sistem: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())