import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger

class BusinessConfigManager:
    def __init__(self):
        self.configs = {}
        self.default_config = {
            "business_name": "Perniagaan Demo",
            "business_type": "ecommerce",
            "primary_language": "Bahasa Malaysia",
            "supported_languages": ["Bahasa Malaysia", "English"],
            "business_hours": {
                "monday": {"start": "09:00", "end": "18:00", "is_open": True},
                "tuesday": {"start": "09:00", "end": "18:00", "is_open": True},
                "wednesday": {"start": "09:00", "end": "18:00", "is_open": True},
                "thursday": {"start": "09:00", "end": "18:00", "is_open": True},
                "friday": {"start": "09:00", "end": "18:00", "is_open": True},
                "saturday": {"start": "10:00", "end": "16:00", "is_open": True},
                "sunday": {"start": "10:00", "end": "16:00", "is_open": False}
            },
            "contact_info": {
                "phone": "+60-3-1234-5678",
                "email": "info@perniagaan.com",
                "address": "Kuala Lumpur, Malaysia",
                "website": "https://www.perniagaan.com"
            },
            "custom_responses": {
                "greeting": "Selamat datang! Bagaimana saya boleh membantu anda hari ini?",
                "goodbye": "Terima kasih kerana menghubungi kami. Semoga hari anda menyenangkan!",
                "escalation": "Saya akan menghubungkan anda dengan ejen manusia untuk bantuan lanjut.",
                "off_hours": "Maaf, kami sedang tutup. Sila hubungi kami pada waktu operasi: Isnin-Jumaat 9:00-18:00."
            },
            "escalation_rules": {
                "complaint_escalation": True,
                "billing_escalation": True,
                "technical_escalation": True,
                "escalation_threshold": 3  # Escalate after 3 failed attempts
            }
        }
    
    async def get_config(self, business_id: str = None) -> Dict[str, Any]:
        """Get business configuration"""
        try:
            if not business_id:
                return self.default_config
            
            # In production, this would query the database
            # For now, we'll use in-memory storage
            if business_id in self.configs:
                return self.configs[business_id]
            
            # Return default config if not found
            return self.default_config
            
        except Exception as e:
            logger.error(f"Error getting business config: {e}")
            return self.default_config
    
    async def save_config(self, config: Dict[str, Any]):
        """Save business configuration"""
        try:
            business_id = config.get("business_id")
            if not business_id:
                raise ValueError("Business ID is required")
            
            # Validate configuration
            validated_config = await self._validate_config(config)
            
            # Store configuration
            self.configs[business_id] = validated_config
            
            logger.info(f"Business config saved for {business_id}")
            
        except Exception as e:
            logger.error(f"Error saving business config: {e}")
            raise
    
    async def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business configuration"""
        try:
            validated = {}
            
            # Required fields
            required_fields = ["business_id", "business_name"]
            for field in required_fields:
                if field not in config or not config[field]:
                    raise ValueError(f"Field {field} is required")
                validated[field] = config[field]
            
            # Optional fields with defaults
            validated["business_type"] = config.get("business_type", "ecommerce")
            validated["primary_language"] = config.get("primary_language", "Bahasa Malaysia")
            validated["supported_languages"] = config.get("supported_languages", ["Bahasa Malaysia", "English"])
            validated["business_hours"] = config.get("business_hours", self.default_config["business_hours"])
            validated["contact_info"] = config.get("contact_info", self.default_config["contact_info"])
            validated["knowledge_base_url"] = config.get("knowledge_base_url")
            validated["api_key"] = config.get("api_key")
            validated["custom_responses"] = config.get("custom_responses", self.default_config["custom_responses"])
            validated["escalation_rules"] = config.get("escalation_rules", self.default_config["escalation_rules"])
            
            # Validate business hours
            validated["business_hours"] = await self._validate_business_hours(validated["business_hours"])
            
            # Validate supported languages
            validated["supported_languages"] = await self._validate_supported_languages(validated["supported_languages"])
            
            return validated
            
        except Exception as e:
            logger.error(f"Error validating config: {e}")
            raise
    
    async def _validate_business_hours(self, business_hours: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business hours configuration"""
        try:
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            validated_hours = {}
            
            for day in days:
                if day in business_hours:
                    day_config = business_hours[day]
                    validated_hours[day] = {
                        "start": day_config.get("start", "09:00"),
                        "end": day_config.get("end", "18:00"),
                        "is_open": day_config.get("is_open", True)
                    }
                else:
                    # Use default hours
                    validated_hours[day] = self.default_config["business_hours"][day]
            
            return validated_hours
            
        except Exception as e:
            logger.error(f"Error validating business hours: {e}")
            return self.default_config["business_hours"]
    
    async def _validate_supported_languages(self, languages: List[str]) -> List[str]:
        """Validate supported languages"""
        try:
            valid_languages = [
                "Bahasa Malaysia", "English", "Chinese", "Tamil", 
                "Hindi", "Thai", "Indonesian", "Filipino"
            ]
            
            validated_languages = []
            for lang in languages:
                if lang in valid_languages:
                    validated_languages.append(lang)
                else:
                    logger.warning(f"Unsupported language: {lang}")
            
            # Ensure at least one language is supported
            if not validated_languages:
                validated_languages = ["Bahasa Malaysia"]
            
            return validated_languages
            
        except Exception as e:
            logger.error(f"Error validating supported languages: {e}")
            return ["Bahasa Malaysia", "English"]
    
    async def get_business_types(self) -> List[Dict[str, str]]:
        """Get available business types"""
        return [
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
    
    async def get_language_templates(self) -> Dict[str, Dict[str, str]]:
        """Get language-specific response templates"""
        return {
            "Bahasa Malaysia": {
                "greeting": "Selamat datang! Bagaimana saya boleh membantu anda hari ini?",
                "goodbye": "Terima kasih kerana menghubungi kami. Semoga hari anda menyenangkan!",
                "escalation": "Saya akan menghubungkan anda dengan ejen manusia untuk bantuan lanjut.",
                "off_hours": "Maaf, kami sedang tutup. Sila hubungi kami pada waktu operasi: Isnin-Jumaat 9:00-18:00.",
                "processing": "Sila tunggu sebentar, saya sedang memproses permintaan anda...",
                "error": "Maaf, berlaku ralat. Sila cuba lagi atau hubungi kami untuk bantuan."
            },
            "English": {
                "greeting": "Welcome! How can I help you today?",
                "goodbye": "Thank you for contacting us. Have a great day!",
                "escalation": "I'll connect you with a human agent for further assistance.",
                "off_hours": "Sorry, we're currently closed. Please contact us during business hours: Monday-Friday 9:00-18:00.",
                "processing": "Please wait a moment, I'm processing your request...",
                "error": "Sorry, an error occurred. Please try again or contact us for assistance."
            },
            "Chinese": {
                "greeting": "欢迎！今天我能为您做些什么？",
                "goodbye": "感谢您联系我们。祝您有美好的一天！",
                "escalation": "我将为您连接人工客服以获得进一步帮助。",
                "off_hours": "抱歉，我们目前关闭。请在营业时间联系我们：周一至周五 9:00-18:00。",
                "processing": "请稍等，我正在处理您的请求...",
                "error": "抱歉，发生错误。请重试或联系我们寻求帮助。"
            },
            "Tamil": {
                "greeting": "வரவேற்கிறோம்! இன்று நான் உங்களுக்கு எவ்வாறு உதவ முடியும்?",
                "goodbye": "எங்களைத் தொடர்பு கொண்டதற்கு நன்றி. உங்கள் நாள் சிறப்பாக இருக்கட்டும்!",
                "escalation": "மேலும் உதவிக்காக மனித முகவருடன் உங்களை இணைக்கிறேன்.",
                "off_hours": "மன்னிக்கவும், நாங்கள் தற்போது மூடியிருக்கிறோம். வணிக நேரத்தில் எங்களைத் தொடர்பு கொள்ளவும்: திங்கள்-வெள்ளி 9:00-18:00.",
                "processing": "கொஞ்சம் காத்திருக்கவும், உங்கள் கோரிக்கையை நான் செயல்படுத்துகிறேன்...",
                "error": "மன்னிக்கவும், பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும் அல்லது உதவிக்காக எங்களைத் தொடர்பு கொள்ளவும்."
            }
        }
    
    async def is_business_open(self, business_id: str) -> bool:
        """Check if business is currently open"""
        try:
            config = await self.get_config(business_id)
            business_hours = config.get("business_hours", {})
            
            now = datetime.now()
            current_day = now.strftime("%A").lower()
            current_time = now.strftime("%H:%M")
            
            if current_day in business_hours:
                day_config = business_hours[current_day]
                if not day_config.get("is_open", False):
                    return False
                
                start_time = day_config.get("start", "09:00")
                end_time = day_config.get("end", "18:00")
                
                return start_time <= current_time <= end_time
            
            return True  # Default to open if no specific hours set
            
        except Exception as e:
            logger.error(f"Error checking business hours: {e}")
            return True
    
    async def get_escalation_message(self, business_id: str, language: str = "Bahasa Malaysia") -> str:
        """Get escalation message in specified language"""
        try:
            config = await self.get_config(business_id)
            custom_responses = config.get("custom_responses", {})
            
            # Check for custom escalation message
            if "escalation" in custom_responses:
                return custom_responses["escalation"]
            
            # Use language-specific template
            templates = await self.get_language_templates()
            if language in templates and "escalation" in templates[language]:
                return templates[language]["escalation"]
            
            # Default escalation message
            return "Saya akan menghubungkan anda dengan ejen manusia untuk bantuan lanjut."
            
        except Exception as e:
            logger.error(f"Error getting escalation message: {e}")
            return "Saya akan menghubungkan anda dengan ejen manusia untuk bantuan lanjut."
    
    async def delete_config(self, business_id: str) -> bool:
        """Delete business configuration"""
        try:
            if business_id in self.configs:
                del self.configs[business_id]
                logger.info(f"Business config deleted for {business_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting business config: {e}")
            return False