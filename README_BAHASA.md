# 🇲🇾 Sistem Agen Perkhidmatan Pelanggan Malaysia

Sistem AI yang canggih untuk perkhidmatan pelanggan multibahasa di Malaysia, dibangunkan khusus untuk memenuhi keperluan perniagaan Malaysia.

## 🚀 Ciri-ciri Utama

- **Sokongan Multibahasa**: Bahasa Malaysia, English, Chinese, Tamil, Hindi, Thai
- **Klasifikasi Niat Pintar**: Mengenal pasti niat pelanggan secara automatik
- **Analitik Komprehensif**: Laporan terperinci dalam Bahasa Malaysia
- **Konfigurasi Perniagaan**: Mudah disesuaikan untuk pelbagai jenis perniagaan
- **Notifikasi Automatik**: Sistem notifikasi untuk eskalasi dan ralat
- **Penyetempatan Malaysia**: Direka khusus untuk pasaran Malaysia

## 🏗️ Arkitektur Sistem

### Backend (FastAPI + Framework Agen Anda)
- **BaseMasterAgent**: Enjin orkestrasi teras
- **MalaysianCustomerServiceAgent**: Pelaksanaan khusus untuk Malaysia
- **API RESTful**: Endpoint yang bersih untuk integrasi frontend
- **Pemprosesan Multi-langkah**: Pengesanan bahasa → Klasifikasi niat → Pengambilan pengetahuan → Penjanaan respons

### Ciri-ciri Teknikal
- **Pangkalan Data SQLite**: Penyimpanan perbualan dan analitik
- **Sistem Notifikasi**: Email, SMS, WhatsApp (mock)
- **Cache Analitik**: Prestasi yang dioptimumkan
- **Logging Komprehensif**: Pengekodan ralat dan pemantauan

## 🛠️ Panduan Pemasangan

### 1. Keperluan Sistem
```bash
# Python 3.8 atau lebih tinggi
python --version

# Dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi Persekitaran
```bash
# Set kunci API OpenAI
export OPENAI_API_KEY="your-openai-api-key-here"

# Set kunci rahsia
export SECRET_KEY="your-secret-key-here"

# Konfigurasi pilihan
export API_HOST="0.0.0.0"
export API_PORT="8000"
export LOG_LEVEL="INFO"
```

### 3. Menjalankan Sistem
```bash
# Cara mudah - gunakan skrip permulaan
python start.py

# Atau secara manual
cd backend
python main.py
```

Sistem akan berjalan di `http://localhost:8000`

## 📊 Ciri-ciri Perniagaan

### Jenis Perniagaan yang Disokong
- **E-dagang**: Perdagangan dalam talian
- **Runcit**: Peruncitan
- **Restoran**: Restoran dan makanan
- **Hotel**: Penginapan dan hospitaliti
- **Perbankan**: Perkhidmatan kewangan
- **Telekomunikasi**: Perkhidmatan telekomunikasi
- **Kesihatan**: Perkhidmatan kesihatan
- **Pendidikan**: Institusi pendidikan
- **Logistik**: Perkhidmatan penghantaran

### Bahasa yang Disokong
- 🇲🇾 **Bahasa Malaysia** (Utama)
- 🇺🇸 **English**
- 🇨🇳 **Chinese**
- 🇮🇳 **Tamil**
- 🇮🇳 **Hindi**
- 🇹🇭 **Thai**

### Kategori Niat Pelanggan
- **Aduan**: Aduan atau masalah pelanggan
- **Pesanan**: Pertanyaan berkaitan pesanan
- **Sokongan**: Permintaan sokongan teknikal
- **Bil**: Pertanyaan bil dan pembayaran
- **Umum**: Soalan atau maklumat umum
- **Produk**: Pertanyaan tentang produk
- **Penghantaran**: Pertanyaan tentang penghantaran
- **Pemulangan**: Permintaan pemulangan barang

## 🔧 API Endpoints

### Perbualan
```http
POST /chat
Content-Type: application/json

{
  "message": "Saya ada masalah dengan pesanan saya",
  "session_id": "session_123",
  "business_id": "business_456"
}
```

### Konfigurasi Perniagaan
```http
POST /business/configure
Content-Type: application/json

{
  "business_id": "business_456",
  "business_name": "Perniagaan Saya",
  "business_type": "ecommerce",
  "primary_language": "Bahasa Malaysia",
  "supported_languages": ["Bahasa Malaysia", "English"],
  "contact_info": {
    "phone": "+60-3-1234-5678",
    "email": "info@perniagaan.com"
  }
}
```

### Analitik
```http
GET /analytics/business_456?date_from=2024-01-01&date_to=2024-01-31
```

## 📈 Analitik dan Laporan

### Metrik yang Tersedia
- **Jumlah Perbualan**: Bilangan perbualan harian/bulanan
- **Pengagihan Bahasa**: Bahasa yang paling kerap digunakan
- **Klasifikasi Niat**: Niat pelanggan yang paling biasa
- **Masa Respons**: Purata masa respons agen
- **Kadar Kepuasan**: Tahap kepuasan pelanggan
- **Trend Pertumbuhan**: Analisis trend penggunaan

### Laporan Automatik
- **Laporan Harian**: Statistik harian perniagaan
- **Laporan Bulanan**: Analisis prestasi bulanan
- **Amaran Ambang**: Notifikasi apabila metrik melebihi ambang
- **Eskalasi**: Notifikasi untuk perbualan yang memerlukan perhatian

## 🔔 Sistem Notifikasi

### Jenis Notifikasi
- **Eskalasi**: Apabila perbualan perlu dihantar kepada ejen manusia
- **Ralat**: Notifikasi ralat sistem
- **Laporan Harian**: Laporan statistik harian
- **Amaran Ambang**: Apabila metrik melebihi had yang ditetapkan

### Saluran Notifikasi
- **Email**: Notifikasi melalui email
- **SMS**: Notifikasi melalui SMS (mock)
- **WhatsApp**: Notifikasi melalui WhatsApp (mock)

## 🎯 Model Perniagaan

### Pakej Harga
- **Pakej SME**: RM 500-1,500/bulan (1,000 interaksi)
- **Pakej Perniagaan**: RM 2,000-5,000/bulan (10,000 interaksi)
- **Pakej Enterprise**: RM 10,000-50,000/bulan (tanpa had)

### Projeksi Pendapatan
- **Bulan 3**: RM 7,500/bulan (10 pelanggan)
- **Bulan 6**: RM 100,000/bulan (50 pelanggan)
- **Bulan 12**: RM 525,000/bulan (150 pelanggan)

## 🚀 Strategi Go-to-Market

### Fasa 1: MVP (Bulan 1-3)
- Membina agen perkhidmatan pelanggan multibahasa asas
- Sasaran 5-10 pelanggan SME
- Fokus pada Bahasa Malaysia + English
- Harga: RM 500-1,000/bulan

### Fasa 2: Skala (Bulan 4-8)
- Menambah sokongan Chinese dan Tamil
- Sasaran 50-100 perniagaan
- Menambah ciri enterprise
- Harga: RM 1,000-5,000/bulan

### Fasa 3: Enterprise (Bulan 9-12)
- Sasaran syarikat besar Malaysia
- Menambah integrasi tersuai
- Mengembangkan ke pasaran Asia Tenggara
- Harga: RM 10,000-50,000/bulan

## 🔧 Penyesuaian dan Integrasi

### Konfigurasi Perniagaan
```python
# Contoh konfigurasi perniagaan
business_config = {
    "business_id": "restoran_123",
    "business_name": "Restoran Nasi Lemak",
    "business_type": "restaurant",
    "primary_language": "Bahasa Malaysia",
    "supported_languages": ["Bahasa Malaysia", "English", "Chinese"],
    "business_hours": {
        "monday": {"start": "07:00", "end": "22:00", "is_open": True},
        "tuesday": {"start": "07:00", "end": "22:00", "is_open": True},
        # ... hari lain
    },
    "contact_info": {
        "phone": "+60-3-1234-5678",
        "email": "info@restoran.com",
        "address": "Kuala Lumpur, Malaysia"
    }
}
```

### Integrasi dengan Sistem Sedia Ada
- **API RESTful**: Mudah diintegrasikan dengan sistem sedia ada
- **Webhook**: Notifikasi masa nyata untuk eskalasi
- **Export Data**: Eksport analitik dalam format CSV/JSON
- **Single Sign-On**: Integrasi dengan sistem autentikasi sedia ada

## 📱 Frontend (Lovable)

Sistem ini direka untuk berfungsi dengan frontend Lovable. Frontend akan menyediakan:

- **Antaramuka Perbualan**: Chat yang responsif dan mudah digunakan
- **Dashboard Analitik**: Visualisasi data dalam Bahasa Malaysia
- **Konfigurasi Perniagaan**: Antaramuka untuk mengkonfigurasi perniagaan
- **Pemantauan Masa Nyata**: Status sistem dan metrik prestasi

## 🛡️ Keselamatan dan Privasi

### Langkah Keselamatan
- **Enkripsi Data**: Semua data disulitkan dalam transit dan rehat
- **Autentikasi API**: Sistem autentikasi yang selamat
- **Rate Limiting**: Perlindungan daripada serangan DDoS
- **Log Audit**: Log semua aktiviti untuk audit

### Pematuhan Privasi
- **PDPA Malaysia**: Mematuhi Akta Perlindungan Data Peribadi Malaysia
- **Penyimpanan Data**: Data disimpan di Malaysia
- **Hak Pelanggan**: Pelanggan boleh meminta data mereka dipadamkan

## 🔍 Penyelesaian Masalah

### Masalah Biasa
1. **Ralat API OpenAI**: Pastikan kunci API sah dan ada kredit
2. **Pangkalan Data**: Semak sambungan pangkalan data
3. **Port Terpakai**: Tukar port jika 8000 sudah digunakan
4. **Memory**: Pastikan sistem mempunyai RAM yang mencukupi

### Log dan Debugging
```bash
# Semak log sistem
tail -f malaysian_agent.log

# Semak status kesihatan
curl http://localhost:8000/health

# Semak konfigurasi
curl http://localhost:8000/
```

## 📞 Sokongan

### Dokumentasi
- **API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Log Sistem**: `malaysian_agent.log`

### Bantuan
- Semak log sistem untuk ralat
- Gunakan endpoint `/health` untuk semakan status
- Rujuk dokumentasi API untuk integrasi

## 🎯 Langkah Seterusnya

1. **Pemasangan**: Ikuti panduan pemasangan di atas
2. **Konfigurasi**: Set kunci API dan konfigurasi perniagaan
3. **Ujian**: Uji sistem dengan mesej dalam pelbagai bahasa
4. **Integrasi**: Integrasikan dengan frontend Lovable
5. **Pelanggan**: Cari 3-5 pelanggan pilot
6. **Skala**: Kembangkan berdasarkan maklum balas pelanggan

---

**Siap untuk merevolusikan perkhidmatan pelanggan di Malaysia! 🇲🇾**