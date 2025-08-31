#!/bin/bash

# Malaysian Customer Service Agent - Deployment Script
# Skrip Pemasangan Sistem Agen Perkhidmatan Pelanggan Malaysia

set -e  # Exit on any error

echo "🇲🇾 Memulakan pemasangan Sistem Agen Perkhidmatan Pelanggan Malaysia..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Python is installed
check_python() {
    print_status "Memeriksa Python..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION ditemui"
    else
        print_error "Python 3 tidak ditemui. Sila pasang Python 3.8 atau lebih tinggi."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Memeriksa pip..."
    if command -v pip3 &> /dev/null; then
        print_status "pip3 ditemui"
    else
        print_error "pip3 tidak ditemui. Sila pasang pip3."
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Membuat persekitaran maya..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_status "Persekitaran maya dicipta"
    else
        print_warning "Persekitaran maya sudah wujud"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Mengaktifkan persekitaran maya..."
    source venv/bin/activate
    print_status "Persekitaran maya diaktifkan"
}

# Install dependencies
install_dependencies() {
    print_status "Memasang dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_status "Dependencies berjaya dipasang"
}

# Check environment variables
check_env_vars() {
    print_status "Memeriksa pembolehubah persekitaran..."
    
    if [ -z "$OPENAI_API_KEY" ]; then
        print_warning "OPENAI_API_KEY tidak ditetapkan"
        echo "Sila set kunci API OpenAI:"
        echo "export OPENAI_API_KEY='your-openai-api-key-here'"
        echo ""
        read -p "Masukkan kunci API OpenAI anda: " OPENAI_API_KEY
        export OPENAI_API_KEY
    fi
    
    if [ -z "$SECRET_KEY" ]; then
        print_warning "SECRET_KEY tidak ditetapkan"
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
        export SECRET_KEY
        print_status "SECRET_KEY dijana secara automatik"
    fi
    
    print_status "Pembolehubah persekitaran OK"
}

# Create .env file
create_env_file() {
    print_status "Membuat fail .env..."
    cat > .env << EOF
# Malaysian Customer Service Agent Configuration
OPENAI_API_KEY=$OPENAI_API_KEY
SECRET_KEY=$SECRET_KEY
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False
LOG_LEVEL=INFO
DATABASE_URL=malaysian_agent.db
DEFAULT_BUSINESS_NAME=Perniagaan Demo
DEFAULT_PRIMARY_LANGUAGE=Bahasa Malaysia
EOF
    print_status "Fail .env dicipta"
}

# Initialize database
init_database() {
    print_status "Memulakan pangkalan data..."
    python3 -c "
import asyncio
from utils.database import DatabaseManager

async def init_db():
    db = DatabaseManager()
    if await db.check_connection():
        print('Pangkalan data berjaya dimulakan')
    else:
        print('Ralat dalam memulakan pangkalan data')
        exit(1)

asyncio.run(init_db())
"
    print_status "Pangkalan data siap"
}

# Create systemd service file
create_systemd_service() {
    print_status "Membuat fail perkhidmatan systemd..."
    
    CURRENT_DIR=$(pwd)
    USER=$(whoami)
    
    sudo tee /etc/systemd/system/malaysian-agent.service > /dev/null << EOF
[Unit]
Description=Malaysian Customer Service Agent
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/venv/bin
ExecStart=$CURRENT_DIR/venv/bin/python start.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    print_status "Fail perkhidmatan systemd dicipta"
}

# Start systemd service
start_service() {
    print_status "Memulakan perkhidmatan systemd..."
    sudo systemctl daemon-reload
    sudo systemctl enable malaysian-agent
    sudo systemctl start malaysian-agent
    print_status "Perkhidmatan systemd dimulakan"
}

# Check service status
check_service() {
    print_status "Memeriksa status perkhidmatan..."
    sudo systemctl status malaysian-agent --no-pager
}

# Create nginx configuration
create_nginx_config() {
    print_status "Membuat konfigurasi nginx..."
    
    sudo tee /etc/nginx/sites-available/malaysian-agent > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;  # Ganti dengan domain anda
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    
    sudo ln -sf /etc/nginx/sites-available/malaysian-agent /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    
    print_status "Konfigurasi nginx siap"
}

# Main deployment function
main() {
    print_header "╔══════════════════════════════════════════════════════════════╗"
    print_header "║                                                              ║"
    print_header "║    🇲🇾 SISTEM AGEN PERKHIDMATAN PELANGGAN MALAYSIA 🇲🇾      ║"
    print_header "║                                                              ║"
    print_header "║    Skrip Pemasangan Automatik                                ║"
    print_header "║                                                              ║"
    print_header "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Check system requirements
    check_python
    check_pip
    
    # Setup environment
    create_venv
    activate_venv
    install_dependencies
    
    # Configuration
    check_env_vars
    create_env_file
    init_database
    
    # Ask for deployment type
    echo ""
    print_status "Pilih jenis pemasangan:"
    echo "1) Pemasangan tempatan (untuk ujian)"
    echo "2) Pemasangan production (dengan systemd dan nginx)"
    read -p "Pilihan anda (1 atau 2): " DEPLOYMENT_TYPE
    
    if [ "$DEPLOYMENT_TYPE" = "1" ]; then
        print_status "Pemasangan tempatan dipilih"
        print_status "Untuk menjalankan sistem:"
        echo "  source venv/bin/activate"
        echo "  python start.py"
        
    elif [ "$DEPLOYMENT_TYPE" = "2" ]; then
        print_status "Pemasangan production dipilih"
        
        # Check if running as root for systemd
        if [ "$EUID" -eq 0 ]; then
            print_error "Jangan jalankan skrip ini sebagai root untuk pemasangan production"
            exit 1
        fi
        
        create_systemd_service
        start_service
        check_service
        
        # Ask for nginx setup
        read -p "Adakah anda mahu memasang nginx? (y/n): " INSTALL_NGINX
        if [ "$INSTALL_NGINX" = "y" ] || [ "$INSTALL_NGINX" = "Y" ]; then
            create_nginx_config
        fi
        
    else
        print_error "Pilihan tidak sah"
        exit 1
    fi
    
    echo ""
    print_header "╔══════════════════════════════════════════════════════════════╗"
    print_header "║                                                              ║"
    print_header "║    ✅ PEMASANGAN BERJAYA DISELESAIKAN! ✅                    ║"
    print_header "║                                                              ║"
    print_header "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    print_status "Maklumat Pemasangan:"
    echo "  - Direktori: $(pwd)"
    echo "  - Persekitaran maya: venv/"
    echo "  - Pangkalan data: malaysian_agent.db"
    echo "  - Log: malaysian_agent.log"
    echo "  - Konfigurasi: .env"
    echo ""
    
    if [ "$DEPLOYMENT_TYPE" = "1" ]; then
        print_status "Untuk menjalankan sistem:"
        echo "  source venv/bin/activate"
        echo "  python start.py"
        echo ""
        print_status "Sistem akan berjalan di: http://localhost:8000"
        
    elif [ "$DEPLOYMENT_TYPE" = "2" ]; then
        print_status "Perkhidmatan systemd:"
        echo "  sudo systemctl status malaysian-agent"
        echo "  sudo systemctl restart malaysian-agent"
        echo "  sudo systemctl stop malaysian-agent"
        echo ""
        print_status "Sistem berjalan sebagai perkhidmatan systemd"
    fi
    
    echo ""
    print_status "Dokumentasi API: http://localhost:8000/docs"
    print_status "Semakan kesihatan: http://localhost:8000/health"
    echo ""
    print_status "Selamat menggunakan Sistem Agen Perkhidmatan Pelanggan Malaysia! 🇲🇾"
}

# Run main function
main "$@"