import sqlite3
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
import aiosqlite
from loguru import logger

class DatabaseManager:
    def __init__(self, db_path: str = "malaysian_agent.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Conversations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        business_id TEXT,
                        user_message TEXT NOT NULL,
                        agent_response TEXT NOT NULL,
                        detected_language TEXT,
                        intent TEXT,
                        confidence REAL,
                        processing_time REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Business configurations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS business_configs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        business_id TEXT UNIQUE NOT NULL,
                        business_name TEXT NOT NULL,
                        business_type TEXT,
                        primary_language TEXT DEFAULT 'Bahasa Malaysia',
                        supported_languages TEXT, -- JSON array
                        business_hours TEXT, -- JSON object
                        contact_info TEXT, -- JSON object
                        knowledge_base_url TEXT,
                        api_key TEXT,
                        custom_responses TEXT, -- JSON object
                        escalation_rules TEXT, -- JSON object
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Analytics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        business_id TEXT NOT NULL,
                        metric_type TEXT NOT NULL,
                        metric_value TEXT NOT NULL,
                        metric_data TEXT, -- JSON object
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        date DATE DEFAULT (date('now'))
                    )
                """)
                
                # Error logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS error_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        business_id TEXT,
                        error_message TEXT NOT NULL,
                        error_type TEXT,
                        stack_trace TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Customer sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS customer_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        business_id TEXT,
                        customer_info TEXT, -- JSON object
                        first_message_at DATETIME,
                        last_message_at DATETIME,
                        total_messages INTEGER DEFAULT 0,
                        languages_used TEXT, -- JSON array
                        intents_detected TEXT, -- JSON array
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    async def check_connection(self) -> bool:
        """Check database connection"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return False
    
    async def store_conversation(self, session_id: str, user_message: str, agent_response: str,
                               detected_language: str = None, intent: str = None, 
                               confidence: float = None, processing_time: float = None,
                               business_id: str = None):
        """Store conversation in database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO conversations 
                    (session_id, business_id, user_message, agent_response, 
                     detected_language, intent, confidence, processing_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (session_id, business_id, user_message, agent_response,
                      detected_language, intent, confidence, processing_time))
                
                # Update customer session
                await self._update_customer_session(db, session_id, business_id, 
                                                  detected_language, intent)
                
                await db.commit()
                logger.info(f"Conversation stored for session {session_id}")
                
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
            raise
    
    async def _update_customer_session(self, db, session_id: str, business_id: str,
                                     detected_language: str, intent: str):
        """Update customer session information"""
        try:
            # Check if session exists
            cursor = await db.execute(
                "SELECT id, languages_used, intents_detected, total_messages FROM customer_sessions WHERE session_id = ?",
                (session_id,)
            )
            session = await cursor.fetchone()
            
            if session:
                # Update existing session
                session_id_db, languages_used, intents_detected, total_messages = session
                
                # Update languages and intents
                languages = json.loads(languages_used) if languages_used else []
                intents = json.loads(intents_detected) if intents_detected else []
                
                if detected_language and detected_language not in languages:
                    languages.append(detected_language)
                
                if intent and intent not in intents:
                    intents.append(intent)
                
                await db.execute("""
                    UPDATE customer_sessions 
                    SET total_messages = total_messages + 1,
                        languages_used = ?,
                        intents_detected = ?,
                        last_message_at = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """, (json.dumps(languages), json.dumps(intents), session_id))
            else:
                # Create new session
                languages = [detected_language] if detected_language else []
                intents = [intent] if intent else []
                
                await db.execute("""
                    INSERT INTO customer_sessions 
                    (session_id, business_id, languages_used, intents_detected, 
                     first_message_at, last_message_at, total_messages)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
                """, (session_id, business_id, json.dumps(languages), json.dumps(intents)))
                
        except Exception as e:
            logger.error(f"Error updating customer session: {e}")
    
    async def get_conversations(self, business_id: str = None, session_id: str = None,
                              limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get conversations from database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                query = "SELECT * FROM conversations WHERE 1=1"
                params = []
                
                if business_id:
                    query += " AND business_id = ?"
                    params.append(business_id)
                
                if session_id:
                    query += " AND session_id = ?"
                    params.append(session_id)
                
                query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting conversations: {e}")
            return []
    
    async def get_business_analytics(self, business_id: str, days: int = 30) -> Dict[str, Any]:
        """Get business analytics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Total conversations
                cursor = await db.execute("""
                    SELECT COUNT(*) as total_conversations
                    FROM conversations 
                    WHERE business_id = ? AND timestamp >= datetime('now', '-{} days')
                """.format(days), (business_id,))
                total_conversations = (await cursor.fetchone())['total_conversations']
                
                # Language distribution
                cursor = await db.execute("""
                    SELECT detected_language, COUNT(*) as count
                    FROM conversations 
                    WHERE business_id = ? AND detected_language IS NOT NULL 
                    AND timestamp >= datetime('now', '-{} days')
                    GROUP BY detected_language
                    ORDER BY count DESC
                """.format(days), (business_id,))
                language_distribution = [dict(row) for row in await cursor.fetchall()]
                
                # Intent distribution
                cursor = await db.execute("""
                    SELECT intent, COUNT(*) as count
                    FROM conversations 
                    WHERE business_id = ? AND intent IS NOT NULL 
                    AND timestamp >= datetime('now', '-{} days')
                    GROUP BY intent
                    ORDER BY count DESC
                """.format(days), (business_id,))
                intent_distribution = [dict(row) for row in await cursor.fetchall()]
                
                # Average processing time
                cursor = await db.execute("""
                    SELECT AVG(processing_time) as avg_processing_time
                    FROM conversations 
                    WHERE business_id = ? AND processing_time IS NOT NULL 
                    AND timestamp >= datetime('now', '-{} days')
                """.format(days), (business_id,))
                avg_processing_time = (await cursor.fetchone())['avg_processing_time'] or 0
                
                # Daily conversation count
                cursor = await db.execute("""
                    SELECT date(timestamp) as date, COUNT(*) as count
                    FROM conversations 
                    WHERE business_id = ? AND timestamp >= datetime('now', '-{} days')
                    GROUP BY date(timestamp)
                    ORDER BY date
                """.format(days), (business_id,))
                daily_conversations = [dict(row) for row in await cursor.fetchall()]
                
                return {
                    "total_conversations": total_conversations,
                    "language_distribution": language_distribution,
                    "intent_distribution": intent_distribution,
                    "average_processing_time": round(avg_processing_time, 2),
                    "daily_conversations": daily_conversations,
                    "period_days": days
                }
                
        except Exception as e:
            logger.error(f"Error getting business analytics: {e}")
            return {}
    
    async def log_error(self, session_id: str, error_message: str, 
                       business_id: str = None, error_type: str = None,
                       stack_trace: str = None):
        """Log error to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO error_logs 
                    (session_id, business_id, error_message, error_type, stack_trace)
                    VALUES (?, ?, ?, ?, ?)
                """, (session_id, business_id, error_message, error_type, stack_trace))
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error logging error: {e}")
    
    async def get_error_logs(self, business_id: str = None, days: int = 7) -> List[Dict[str, Any]]:
        """Get error logs"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                query = """
                    SELECT * FROM error_logs 
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days)
                params = []
                
                if business_id:
                    query += " AND business_id = ?"
                    params.append(business_id)
                
                query += " ORDER BY timestamp DESC"
                
                cursor = await db.execute(query, params)
                rows = await cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting error logs: {e}")
            return []