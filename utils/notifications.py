import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
from loguru import logger

class NotificationManager:
    def __init__(self):
        self.smtp_config = {
            "host": "smtp.gmail.com",
            "port": 587,
            "username": None,  # Set via environment variable
            "password": None   # Set via environment variable
        }
        self.notification_templates = {
            "escalation": {
                "subject": "Eskalasi Perbualan Pelanggan - {business_name}",
                "body": """
                Eskalasi Perbualan Pelanggan
                
                Perniagaan: {business_name}
                Sesi ID: {session_id}
                Masa: {timestamp}
                Bahasa: {language}
                Niat: {intent}
                
                Mesej Pelanggan:
                {customer_message}
                
                Sila ambil tindakan segera.
                """
            },
            "error": {
                "subject": "Ralat Sistem - {business_name}",
                "body": """
                Ralat Sistem Dikesan
                
                Perniagaan: {business_name}
                Masa: {timestamp}
                Jenis Ralat: {error_type}
                
                Butiran Ralat:
                {error_message}
                
                Sila semak sistem anda.
                """
            },
            "daily_report": {
                "subject": "Laporan Harian - {business_name}",
                "body": """
                Laporan Harian Sistem Agen
                
                Perniagaan: {business_name}
                Tarikh: {date}
                
                Statistik:
                - Jumlah Perbualan: {total_conversations}
                - Bahasa Terbanyak: {top_language}
                - Niat Terbanyak: {top_intent}
                - Masa Respons Purata: {avg_response_time}s
                - Kadar Kepuasan: {satisfaction_rate}%
                
                Analisis:
                {analysis}
                """
            },
            "threshold_alert": {
                "subject": "Amaran Ambang - {business_name}",
                "body": """
                Amarab Ambang Sistem
                
                Perniagaan: {business_name}
                Masa: {timestamp}
                Jenis Ambang: {threshold_type}
                Nilai Semasa: {current_value}
                Ambang: {threshold_value}
                
                {message}
                """
            }
        }
    
    async def send_notification(self, business_id: str, message: str, 
                              notification_type: str, recipients: List[str]):
        """Send notification to recipients"""
        try:
            # Get business configuration
            from utils.business_config import BusinessConfigManager
            config_manager = BusinessConfigManager()
            business_config = await config_manager.get_config(business_id)
            
            # Prepare notification data
            notification_data = {
                "business_name": business_config.get("business_name", "Perniagaan"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": message
            }
            
            # Get notification template
            template = self.notification_templates.get(notification_type, {})
            if not template:
                logger.warning(f"No template found for notification type: {notification_type}")
                return
            
            # Format notification
            subject = template["subject"].format(**notification_data)
            body = template["body"].format(**notification_data)
            
            # Send notification
            await self._send_email(recipients, subject, body)
            
            logger.info(f"Notification sent to {len(recipients)} recipients for business {business_id}")
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            raise
    
    async def _send_email(self, recipients: List[str], subject: str, body: str):
        """Send email notification"""
        try:
            # In production, you would use actual SMTP configuration
            # For now, we'll just log the notification
            logger.info(f"Email notification:")
            logger.info(f"To: {', '.join(recipients)}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body: {body}")
            
            # Mock email sending
            await asyncio.sleep(0.1)  # Simulate email sending delay
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise
    
    async def send_escalation_notification(self, business_id: str, session_id: str,
                                         customer_message: str, language: str, intent: str):
        """Send escalation notification"""
        try:
            # Get business configuration
            from utils.business_config import BusinessConfigManager
            config_manager = BusinessConfigManager()
            business_config = await config_manager.get_config(business_id)
            
            # Get escalation recipients
            contact_info = business_config.get("contact_info", {})
            recipients = [contact_info.get("email", "admin@perniagaan.com")]
            
            # Prepare escalation data
            escalation_data = {
                "business_name": business_config.get("business_name", "Perniagaan"),
                "session_id": session_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "language": language,
                "intent": intent,
                "customer_message": customer_message
            }
            
            # Get escalation template
            template = self.notification_templates["escalation"]
            subject = template["subject"].format(**escalation_data)
            body = template["body"].format(**escalation_data)
            
            # Send notification
            await self._send_email(recipients, subject, body)
            
            logger.info(f"Escalation notification sent for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error sending escalation notification: {e}")
    
    async def send_error_notification(self, business_id: str, error_type: str, error_message: str):
        """Send error notification"""
        try:
            # Get business configuration
            from utils.business_config import BusinessConfigManager
            config_manager = BusinessConfigManager()
            business_config = await config_manager.get_config(business_id)
            
            # Get error notification recipients
            contact_info = business_config.get("contact_info", {})
            recipients = [contact_info.get("email", "admin@perniagaan.com")]
            
            # Prepare error data
            error_data = {
                "business_name": business_config.get("business_name", "Perniagaan"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error_type": error_type,
                "error_message": error_message
            }
            
            # Get error template
            template = self.notification_templates["error"]
            subject = template["subject"].format(**error_data)
            body = template["body"].format(**error_data)
            
            # Send notification
            await self._send_email(recipients, subject, body)
            
            logger.info(f"Error notification sent for business {business_id}")
            
        except Exception as e:
            logger.error(f"Error sending error notification: {e}")
    
    async def send_daily_report(self, business_id: str, analytics_data: Dict[str, Any]):
        """Send daily report"""
        try:
            # Get business configuration
            from utils.business_config import BusinessConfigManager
            config_manager = BusinessConfigManager()
            business_config = await config_manager.get_config(business_id)
            
            # Get report recipients
            contact_info = business_config.get("contact_info", {})
            recipients = [contact_info.get("email", "admin@perniagaan.com")]
            
            # Prepare report data
            report_data = {
                "business_name": business_config.get("business_name", "Perniagaan"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "total_conversations": analytics_data.get("total_conversations", 0),
                "top_language": analytics_data.get("top_language", "Bahasa Malaysia"),
                "top_intent": analytics_data.get("top_intent", "general"),
                "avg_response_time": analytics_data.get("avg_response_time", 0),
                "satisfaction_rate": analytics_data.get("satisfaction_rate", 0),
                "analysis": analytics_data.get("analysis", "Tiada analisis tersedia")
            }
            
            # Get report template
            template = self.notification_templates["daily_report"]
            subject = template["subject"].format(**report_data)
            body = template["body"].format(**report_data)
            
            # Send notification
            await self._send_email(recipients, subject, body)
            
            logger.info(f"Daily report sent for business {business_id}")
            
        except Exception as e:
            logger.error(f"Error sending daily report: {e}")
    
    async def send_threshold_alert(self, business_id: str, threshold_type: str,
                                 current_value: float, threshold_value: float, message: str):
        """Send threshold alert"""
        try:
            # Get business configuration
            from utils.business_config import BusinessConfigManager
            config_manager = BusinessConfigManager()
            business_config = await config_manager.get_config(business_id)
            
            # Get alert recipients
            contact_info = business_config.get("contact_info", {})
            recipients = [contact_info.get("email", "admin@perniagaan.com")]
            
            # Prepare alert data
            alert_data = {
                "business_name": business_config.get("business_name", "Perniagaan"),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "threshold_type": threshold_type,
                "current_value": current_value,
                "threshold_value": threshold_value,
                "message": message
            }
            
            # Get alert template
            template = self.notification_templates["threshold_alert"]
            subject = template["subject"].format(**alert_data)
            body = template["body"].format(**alert_data)
            
            # Send notification
            await self._send_email(recipients, subject, body)
            
            logger.info(f"Threshold alert sent for business {business_id}")
            
        except Exception as e:
            logger.error(f"Error sending threshold alert: {e}")
    
    async def send_whatsapp_notification(self, phone_number: str, message: str):
        """Send WhatsApp notification (mock implementation)"""
        try:
            # In production, you would integrate with WhatsApp Business API
            logger.info(f"WhatsApp notification to {phone_number}: {message}")
            
            # Mock WhatsApp sending
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp notification: {e}")
    
    async def send_sms_notification(self, phone_number: str, message: str):
        """Send SMS notification (mock implementation)"""
        try:
            # In production, you would integrate with SMS service provider
            logger.info(f"SMS notification to {phone_number}: {message}")
            
            # Mock SMS sending
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error sending SMS notification: {e}")
    
    def get_notification_templates(self) -> Dict[str, Dict[str, str]]:
        """Get available notification templates"""
        return self.notification_templates
    
    async def create_custom_template(self, template_name: str, subject: str, body: str):
        """Create custom notification template"""
        try:
            self.notification_templates[template_name] = {
                "subject": subject,
                "body": body
            }
            
            logger.info(f"Custom notification template created: {template_name}")
            
        except Exception as e:
            logger.error(f"Error creating custom template: {e}")
            raise