import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict, Counter
import json
from loguru import logger

class AnalyticsManager:
    def __init__(self):
        self.metrics_cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def update_metrics(self, business_id: str, detected_language: str = None,
                           intent: str = None, processing_time: float = None):
        """Update analytics metrics"""
        try:
            timestamp = datetime.now()
            
            # Update language metrics
            if detected_language:
                await self._update_language_metrics(business_id, detected_language, timestamp)
            
            # Update intent metrics
            if intent:
                await self._update_intent_metrics(business_id, intent, timestamp)
            
            # Update performance metrics
            if processing_time:
                await self._update_performance_metrics(business_id, processing_time, timestamp)
            
            # Clear cache for this business
            if business_id in self.metrics_cache:
                del self.metrics_cache[business_id]
                
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    async def _update_language_metrics(self, business_id: str, language: str, timestamp: datetime):
        """Update language-specific metrics"""
        # This would typically update a database or cache
        # For now, we'll use in-memory storage
        pass
    
    async def _update_intent_metrics(self, business_id: str, intent: str, timestamp: datetime):
        """Update intent-specific metrics"""
        # This would typically update a database or cache
        pass
    
    async def _update_performance_metrics(self, business_id: str, processing_time: float, timestamp: datetime):
        """Update performance metrics"""
        # This would typically update a database or cache
        pass
    
    async def get_business_analytics(self, business_id: str, date_from: datetime = None,
                                   date_to: datetime = None) -> Dict[str, Any]:
        """Get comprehensive business analytics"""
        try:
            if not date_from:
                date_from = datetime.now() - timedelta(days=30)
            if not date_to:
                date_to = datetime.now()
            
            # Check cache first
            cache_key = f"{business_id}_{date_from.date()}_{date_to.date()}"
            if cache_key in self.metrics_cache:
                cached_data, cache_time = self.metrics_cache[cache_key]
                if (datetime.now() - cache_time).seconds < self.cache_ttl:
                    return cached_data
            
            # Get analytics data (this would typically come from database)
            analytics = await self._generate_analytics(business_id, date_from, date_to)
            
            # Cache the result
            self.metrics_cache[cache_key] = (analytics, datetime.now())
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting business analytics: {e}")
            return {}
    
    async def _generate_analytics(self, business_id: str, date_from: datetime, date_to: datetime) -> Dict[str, Any]:
        """Generate analytics data"""
        # This is a mock implementation - in production, this would query the database
        return {
            "business_id": business_id,
            "period": {
                "from": date_from.isoformat(),
                "to": date_to.isoformat()
            },
            "summary": {
                "total_conversations": 1250,
                "total_customers": 890,
                "average_response_time": 2.3,
                "customer_satisfaction": 4.2,
                "resolution_rate": 0.87
            },
            "languages": {
                "Bahasa Malaysia": 650,
                "English": 420,
                "Chinese": 120,
                "Tamil": 60
            },
            "intents": {
                "general": 300,
                "complaint": 250,
                "order": 200,
                "support": 180,
                "billing": 150,
                "product": 120,
                "delivery": 50
            },
            "performance": {
                "average_processing_time": 2.3,
                "peak_hours": ["10:00-12:00", "14:00-16:00", "20:00-22:00"],
                "busiest_days": ["Monday", "Tuesday", "Wednesday"],
                "response_accuracy": 0.92
            },
            "trends": {
                "conversation_growth": 0.15,  # 15% growth
                "language_diversity": 0.78,   # 78% language diversity
                "intent_complexity": 0.65     # 65% complex intents
            }
        }
    
    async def get_language_analytics(self, business_id: str) -> Dict[str, Any]:
        """Get language-specific analytics"""
        try:
            # Mock data - in production, this would come from database
            return {
                "business_id": business_id,
                "language_breakdown": {
                    "Bahasa Malaysia": {
                        "count": 650,
                        "percentage": 52.0,
                        "average_response_time": 2.1,
                        "satisfaction_score": 4.3
                    },
                    "English": {
                        "count": 420,
                        "percentage": 33.6,
                        "average_response_time": 2.4,
                        "satisfaction_score": 4.1
                    },
                    "Chinese": {
                        "count": 120,
                        "percentage": 9.6,
                        "average_response_time": 2.8,
                        "satisfaction_score": 4.0
                    },
                    "Tamil": {
                        "count": 60,
                        "percentage": 4.8,
                        "average_response_time": 3.1,
                        "satisfaction_score": 3.9
                    }
                },
                "language_trends": {
                    "Bahasa Malaysia": 0.12,  # 12% growth
                    "English": 0.08,          # 8% growth
                    "Chinese": 0.25,          # 25% growth
                    "Tamil": 0.18             # 18% growth
                },
                "recommendations": [
                    "Pertimbangkan untuk menambah sokongan bahasa Mandarin",
                    "Latihan tambahan diperlukan untuk agen Tamil",
                    "Bahasa Malaysia menunjukkan prestasi terbaik"
                ]
            }
        except Exception as e:
            logger.error(f"Error getting language analytics: {e}")
            return {}
    
    async def get_intent_analytics(self, business_id: str) -> Dict[str, Any]:
        """Get intent-specific analytics"""
        try:
            # Mock data - in production, this would come from database
            return {
                "business_id": business_id,
                "intent_breakdown": {
                    "general": {
                        "count": 300,
                        "percentage": 24.0,
                        "average_resolution_time": 1.8,
                        "escalation_rate": 0.05
                    },
                    "complaint": {
                        "count": 250,
                        "percentage": 20.0,
                        "average_resolution_time": 4.2,
                        "escalation_rate": 0.15
                    },
                    "order": {
                        "count": 200,
                        "percentage": 16.0,
                        "average_resolution_time": 2.1,
                        "escalation_rate": 0.08
                    },
                    "support": {
                        "count": 180,
                        "percentage": 14.4,
                        "average_resolution_time": 3.5,
                        "escalation_rate": 0.12
                    },
                    "billing": {
                        "count": 150,
                        "percentage": 12.0,
                        "average_resolution_time": 2.8,
                        "escalation_rate": 0.10
                    },
                    "product": {
                        "count": 120,
                        "percentage": 9.6,
                        "average_resolution_time": 2.3,
                        "escalation_rate": 0.06
                    },
                    "delivery": {
                        "count": 50,
                        "percentage": 4.0,
                        "average_resolution_time": 1.9,
                        "escalation_rate": 0.04
                    }
                },
                "intent_trends": {
                    "complaint": 0.20,    # 20% increase in complaints
                    "order": 0.15,        # 15% increase in orders
                    "support": 0.10,      # 10% increase in support
                    "billing": -0.05      # 5% decrease in billing issues
                },
                "insights": [
                    "Aduan pelanggan meningkat 20% - perlu perhatian",
                    "Pertanyaan pesanan menunjukkan trend positif",
                    "Isu bil menunjukkan penurunan - prestasi baik"
                ],
                "recommendations": [
                    "Tingkatkan latihan untuk menangani aduan",
                    "Sediakan FAQ untuk pertanyaan umum",
                    "Automasikan proses penjejakan pesanan"
                ]
            }
        except Exception as e:
            logger.error(f"Error getting intent analytics: {e}")
            return {}
    
    async def get_performance_analytics(self, business_id: str) -> Dict[str, Any]:
        """Get performance analytics"""
        try:
            return {
                "business_id": business_id,
                "response_times": {
                    "average": 2.3,
                    "median": 2.1,
                    "p95": 4.2,
                    "p99": 6.8
                },
                "accuracy_metrics": {
                    "language_detection": 0.96,
                    "intent_classification": 0.92,
                    "response_relevance": 0.89,
                    "customer_satisfaction": 4.2
                },
                "system_health": {
                    "uptime": 0.999,
                    "error_rate": 0.002,
                    "throughput": 45.2,  # conversations per hour
                    "concurrent_sessions": 12
                },
                "optimization_opportunities": [
                    "Mengurangkan masa respons untuk pertanyaan umum",
                    "Meningkatkan ketepatan klasifikasi niat",
                    "Mengoptimumkan cache untuk respons yang kerap"
                ]
            }
        except Exception as e:
            logger.error(f"Error getting performance analytics: {e}")
            return {}
    
    async def get_customer_insights(self, business_id: str) -> Dict[str, Any]:
        """Get customer insights"""
        try:
            return {
                "business_id": business_id,
                "customer_segments": {
                    "new_customers": {
                        "count": 450,
                        "percentage": 50.6,
                        "common_intents": ["general", "product", "order"],
                        "average_session_length": 3.2
                    },
                    "returning_customers": {
                        "count": 320,
                        "percentage": 36.0,
                        "common_intents": ["order", "support", "billing"],
                        "average_session_length": 4.8
                    },
                    "vip_customers": {
                        "count": 120,
                        "percentage": 13.4,
                        "common_intents": ["complaint", "support", "billing"],
                        "average_session_length": 6.2
                    }
                },
                "customer_journey": {
                    "first_contact": "general_inquiry",
                    "common_paths": [
                        "general → order → support",
                        "product → order → delivery",
                        "complaint → support → resolution"
                    ],
                    "drop_off_points": ["billing_inquiry", "technical_support"]
                },
                "satisfaction_analysis": {
                    "overall_satisfaction": 4.2,
                    "satisfaction_by_intent": {
                        "general": 4.5,
                        "order": 4.3,
                        "product": 4.2,
                        "support": 3.9,
                        "complaint": 3.6,
                        "billing": 4.1
                    },
                    "satisfaction_by_language": {
                        "Bahasa Malaysia": 4.3,
                        "English": 4.1,
                        "Chinese": 4.0,
                        "Tamil": 3.9
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error getting customer insights: {e}")
            return {}
    
    def clear_cache(self, business_id: str = None):
        """Clear analytics cache"""
        if business_id:
            keys_to_remove = [key for key in self.metrics_cache.keys() if key.startswith(business_id)]
            for key in keys_to_remove:
                del self.metrics_cache[key]
        else:
            self.metrics_cache.clear()
        
        logger.info(f"Analytics cache cleared for business: {business_id or 'all'}")