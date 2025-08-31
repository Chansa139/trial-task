from typing import Dict, Any, List, Optional
from datetime import datetime
import re

class MalaysianLocalizer:
    def __init__(self):
        self.language_mappings = {
            "ms": "Bahasa Malaysia",
            "en": "English", 
            "zh": "Chinese",
            "ta": "Tamil",
            "hi": "Hindi",
            "th": "Thai"
        }
        
        self.intent_mappings = {
            "ms": {
                "complaint": "aduan",
                "order": "pesanan", 
                "support": "sokongan",
                "billing": "bil",
                "general": "umum",
                "product": "produk",
                "delivery": "penghantaran",
                "return": "pemulangan"
            },
            "en": {
                "complaint": "complaint",
                "order": "order",
                "support": "support", 
                "billing": "billing",
                "general": "general",
                "product": "product",
                "delivery": "delivery",
                "return": "return"
            }
        }
        
        self.business_type_mappings = {
            "ms": {
                "ecommerce": "e-dagang",
                "retail": "runcit",
                "restaurant": "restoran",
                "hotel": "hotel",
                "banking": "perbankan",
                "telecom": "telekomunikasi",
                "healthcare": "kesihatan",
                "education": "pendidikan",
                "logistics": "logistik",
                "other": "lain-lain"
            }
        }
        
        self.time_formats = {
            "ms": "%d/%m/%Y %H:%M",
            "en": "%m/%d/%Y %H:%M",
            "zh": "%Y年%m月%d日 %H:%M",
            "ta": "%d/%m/%Y %H:%M"
        }
        
        self.currency_formats = {
            "ms": "RM {amount:.2f}",
            "en": "RM {amount:.2f}",
            "zh": "RM {amount:.2f}",
            "ta": "RM {amount:.2f}"
        }
    
    def get_language_name(self, language_code: str) -> str:
        """Get full language name from code"""
        return self.language_mappings.get(language_code, language_code)
    
    def get_language_code(self, language_name: str) -> str:
        """Get language code from full name"""
        for code, name in self.language_mappings.items():
            if name.lower() == language_name.lower():
                return code
        return "ms"  # Default to Bahasa Malaysia
    
    def localize_intent(self, intent: str, language: str = "ms") -> str:
        """Localize intent name to specified language"""
        if language in self.intent_mappings:
            return self.intent_mappings[language].get(intent, intent)
        return intent
    
    def localize_business_type(self, business_type: str, language: str = "ms") -> str:
        """Localize business type to specified language"""
        if language in self.business_type_mappings:
            return self.business_type_mappings[language].get(business_type, business_type)
        return business_type
    
    def format_datetime(self, dt: datetime, language: str = "ms") -> str:
        """Format datetime according to language preferences"""
        format_str = self.time_formats.get(language, self.time_formats["ms"])
        return dt.strftime(format_str)
    
    def format_currency(self, amount: float, language: str = "ms") -> str:
        """Format currency according to language preferences"""
        format_str = self.currency_formats.get(language, self.currency_formats["ms"])
        return format_str.format(amount=amount)
    
    def get_greeting(self, language: str = "ms") -> str:
        """Get greeting message in specified language"""
        greetings = {
            "ms": "Selamat datang! Bagaimana saya boleh membantu anda hari ini?",
            "en": "Welcome! How can I help you today?",
            "zh": "欢迎！今天我能为您做些什么？",
            "ta": "வரவேற்கிறோம்! இன்று நான் உங்களுக்கு எவ்வாறு உதவ முடியும்?",
            "hi": "स्वागत है! आज मैं आपकी कैसे मदद कर सकता हूं?",
            "th": "ยินดีต้อนรับ! วันนี้ฉันสามารถช่วยคุณได้อย่างไร?"
        }
        return greetings.get(language, greetings["ms"])
    
    def get_goodbye(self, language: str = "ms") -> str:
        """Get goodbye message in specified language"""
        goodbyes = {
            "ms": "Terima kasih kerana menghubungi kami. Semoga hari anda menyenangkan!",
            "en": "Thank you for contacting us. Have a great day!",
            "zh": "感谢您联系我们。祝您有美好的一天！",
            "ta": "எங்களைத் தொடர்பு கொண்டதற்கு நன்றி. உங்கள் நாள் சிறப்பாக இருக்கட்டும்!",
            "hi": "हमसे संपर्क करने के लिए धन्यवाद। आपका दिन शुभ हो!",
            "th": "ขอบคุณที่ติดต่อเรา ขอให้วันดีๆ!"
        }
        return goodbyes.get(language, goodbyes["ms"])
    
    def get_processing_message(self, language: str = "ms") -> str:
        """Get processing message in specified language"""
        messages = {
            "ms": "Sila tunggu sebentar, saya sedang memproses permintaan anda...",
            "en": "Please wait a moment, I'm processing your request...",
            "zh": "请稍等，我正在处理您的请求...",
            "ta": "கொஞ்சம் காத்திருக்கவும், உங்கள் கோரிக்கையை நான் செயல்படுத்துகிறேன்...",
            "hi": "कृपया एक क्षण प्रतीक्षा करें, मैं आपका अनुरोध संसाधित कर रहा हूं...",
            "th": "กรุณารอสักครู่ ฉันกำลังประมวลผลคำขอของคุณ..."
        }
        return messages.get(language, messages["ms"])
    
    def get_error_message(self, language: str = "ms") -> str:
        """Get error message in specified language"""
        messages = {
            "ms": "Maaf, berlaku ralat. Sila cuba lagi atau hubungi kami untuk bantuan.",
            "en": "Sorry, an error occurred. Please try again or contact us for assistance.",
            "zh": "抱歉，发生错误。请重试或联系我们寻求帮助。",
            "ta": "மன்னிக்கவும், பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும் அல்லது உதவிக்காக எங்களைத் தொடர்பு கொள்ளவும்.",
            "hi": "क्षमा करें, एक त्रुटि हुई। कृपया पुनः प्रयास करें या सहायता के लिए हमसे संपर्क करें।",
            "th": "ขออภัย เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้งหรือติดต่อเราเพื่อขอความช่วยเหลือ"
        }
        return messages.get(language, messages["ms"])
    
    def get_escalation_message(self, language: str = "ms") -> str:
        """Get escalation message in specified language"""
        messages = {
            "ms": "Saya akan menghubungkan anda dengan ejen manusia untuk bantuan lanjut.",
            "en": "I'll connect you with a human agent for further assistance.",
            "zh": "我将为您连接人工客服以获得进一步帮助。",
            "ta": "மேலும் உதவிக்காக மனித முகவருடன் உங்களை இணைக்கிறேன்.",
            "hi": "मैं आपको आगे की सहायता के लिए मानव एजेंट से जोड़ूंगा।",
            "th": "ฉันจะเชื่อมต่อคุณกับตัวแทนมนุษย์เพื่อความช่วยเหลือเพิ่มเติม"
        }
        return messages.get(language, messages["ms"])
    
    def get_off_hours_message(self, language: str = "ms") -> str:
        """Get off-hours message in specified language"""
        messages = {
            "ms": "Maaf, kami sedang tutup. Sila hubungi kami pada waktu operasi: Isnin-Jumaat 9:00-18:00.",
            "en": "Sorry, we're currently closed. Please contact us during business hours: Monday-Friday 9:00-18:00.",
            "zh": "抱歉，我们目前关闭。请在营业时间联系我们：周一至周五 9:00-18:00。",
            "ta": "மன்னிக்கவும், நாங்கள் தற்போது மூடியிருக்கிறோம். வணிக நேரத்தில் எங்களைத் தொடர்பு கொள்ளவும்: திங்கள்-வெள்ளி 9:00-18:00.",
            "hi": "क्षमा करें, हम वर्तमान में बंद हैं। कृपया व्यावसायिक घंटों के दौरान हमसे संपर्क करें: सोमवार-शुक्रवार 9:00-18:00।",
            "th": "ขออภัย เราปิดให้บริการในขณะนี้ กรุณาติดต่อเราตอนเวลาทำการ: จันทร์-ศุกร์ 9:00-18:00"
        }
        return messages.get(language, messages["ms"])
    
    def detect_language_from_text(self, text: str) -> str:
        """Detect language from text content"""
        # Simple language detection based on common words
        text_lower = text.lower()
        
        # Bahasa Malaysia indicators
        ms_indicators = ["saya", "anda", "kami", "mereka", "ini", "itu", "ada", "tidak", "boleh", "akan", "sudah", "belum"]
        if any(word in text_lower for word in ms_indicators):
            return "ms"
        
        # Chinese indicators
        zh_indicators = ["我", "你", "他", "她", "我们", "他们", "这", "那", "是", "不", "有", "没有"]
        if any(char in text for char in zh_indicators):
            return "zh"
        
        # Tamil indicators
        ta_indicators = ["நான்", "நீ", "அவர்", "அவள்", "நாங்கள்", "அவர்கள்", "இது", "அது", "உள்ளது", "இல்லை"]
        if any(word in text for word in ta_indicators):
            return "ta"
        
        # Hindi indicators
        hi_indicators = ["मैं", "तुम", "वह", "हम", "यह", "वह", "है", "नहीं", "हो", "था"]
        if any(word in text_lower for word in hi_indicators):
            return "hi"
        
        # Thai indicators
        th_indicators = ["ฉัน", "คุณ", "เขา", "เธอ", "เรา", "พวกเขา", "นี่", "นั่น", "เป็น", "ไม่", "มี", "ไม่มี"]
        if any(word in text for word in th_indicators):
            return "th"
        
        # Default to English if no other language detected
        return "en"
    
    def get_weekday_name(self, weekday: int, language: str = "ms") -> str:
        """Get weekday name in specified language"""
        weekdays = {
            "ms": ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"],
            "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "zh": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
            "ta": ["திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்", "வெள்ளி", "சனி", "ஞாயிறு"],
            "hi": ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"],
            "th": ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
        }
        
        if language in weekdays and 0 <= weekday < 7:
            return weekdays[language][weekday]
        return weekdays["ms"][weekday]
    
    def get_month_name(self, month: int, language: str = "ms") -> str:
        """Get month name in specified language"""
        months = {
            "ms": ["Januari", "Februari", "Mac", "April", "Mei", "Jun", 
                   "Julai", "Ogos", "September", "Oktober", "November", "Disember"],
            "en": ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"],
            "zh": ["一月", "二月", "三月", "四月", "五月", "六月",
                   "七月", "八月", "九月", "十月", "十一月", "十二月"],
            "ta": ["ஜனவரி", "பிப்ரவரி", "மார்ச்", "ஏப்ரல்", "மே", "ஜூன்",
                   "ஜூலை", "ஆகஸ்ட்", "செப்டம்பர்", "அக்டோபர்", "நவம்பர்", "டிசம்பர்"],
            "hi": ["जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून",
                   "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"],
            "th": ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
                   "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
        }
        
        if language in months and 1 <= month <= 12:
            return months[language][month - 1]
        return months["ms"][month - 1]
    
    def format_phone_number(self, phone: str, language: str = "ms") -> str:
        """Format phone number according to Malaysian standards"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Malaysian phone number formatting
        if digits.startswith('60'):
            # International format: +60-3-1234-5678
            if len(digits) == 12:  # +60-3-1234-5678
                return f"+{digits[:2]}-{digits[2:3]}-{digits[3:7]}-{digits[7:]}"
            elif len(digits) == 11:  # +60-12-345-6789
                return f"+{digits[:2]}-{digits[2:4]}-{digits[4:7]}-{digits[7:]}"
        elif digits.startswith('0'):
            # Local format: 03-1234-5678
            if len(digits) == 10:
                return f"{digits[:2]}-{digits[2:6]}-{digits[6:]}"
            elif len(digits) == 11:
                return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
        
        return phone  # Return original if can't format
    
    def get_currency_symbol(self, language: str = "ms") -> str:
        """Get currency symbol for specified language"""
        return "RM"  # Malaysian Ringgit is standard across all languages
    
    def localize_number(self, number: float, language: str = "ms") -> str:
        """Localize number formatting"""
        if language == "ms":
            # Malaysian format: 1,234.56
            return f"{number:,.2f}"
        elif language == "zh":
            # Chinese format: 1,234.56
            return f"{number:,.2f}"
        else:
            # Default format
            return f"{number:,.2f}"