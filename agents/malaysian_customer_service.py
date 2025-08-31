from typing import Any, Dict, List, Optional
from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from loguru import logger
import asyncio
import json
from datetime import datetime

from agents.base import BaseMasterAgent
from models.states import MasterAgentState
from utils.tracing import trace_execution_time
from utils.malaysian_localization import MalaysianLocalizer
from utils.business_config import BusinessConfigManager
from utils.notifications import NotificationManager

class MalaysianCustomerServiceAgent(BaseMasterAgent):
    def __init__(self, model: BaseChatModel, business_config: Dict[str, Any]) -> None:
        # Define agents for Malaysian customer service
        agents = [
            {
                "name": "language_detector_agent",
                "type": "gen_ai",
                "id": "lang_detect_001",
                "agent_schema": {
                    "model": "gpt-4",
                    "system_prompt": """Anda adalah pakar pengesanan bahasa. Kesan bahasa input teks dan kembalikan hasil dalam format JSON.

Bahasa yang disokong:
- Bahasa Malaysia (ms)
- English (en) 
- Chinese (zh)
- Tamil (ta)
- Hindi (hi)
- Thai (th)

Format pulangan: {"language": "kod_bahasa", "confidence": 0.95, "reasoning": "alasan_pengesanan"}""",
                    "tools": ["language_detection"]
                }
            },
            {
                "name": "intent_classifier_agent", 
                "type": "gen_ai",
                "id": "intent_class_001",
                "agent_schema": {
                    "model": "gpt-4",
                    "system_prompt": """Anda adalah pakar klasifikasi niat pelanggan. Klasifikasikan niat pelanggan dari mesej mereka.

Kategori niat:
- complaint: Aduan atau masalah pelanggan
- order: Pertanyaan berkaitan pesanan (status, penjejakan, dll)
- support: Permintaan sokongan teknikal
- billing: Pertanyaan bil dan pembayaran
- general: Soalan atau maklumat umum
- product: Pertanyaan tentang produk
- delivery: Pertanyaan tentang penghantaran
- return: Permintaan pemulangan barang

Format pulangan: {"intent": "kategori_niat", "confidence": 0.90, "entities": ["entiti_relevan"], "urgency": "tinggi/sederhana/rendah"}""",
                    "tools": ["intent_classification"]
                }
            },
            {
                "name": "knowledge_retriever_agent",
                "type": "mcp",
                "id": "knowledge_001", 
                "url": business_config.get("knowledge_base_url", "https://api.example.com/knowledge"),
                "agent_schema": {
                    "endpoint": "/search",
                    "auth": business_config.get("api_key", "demo-key")
                }
            },
            {
                "name": "response_generator_agent",
                "type": "gen_ai",
                "id": "response_gen_001",
                "agent_schema": {
                    "model": "gpt-4",
                    "system_prompt": f"""Anda adalah wakil perkhidmatan pelanggan yang membantu untuk {business_config.get('business_name', 'perniagaan kami')}.

Panduan:
- Balas dalam bahasa yang dikesan pelanggan
- Bersikap membantu, profesional, dan empati
- Gunakan pengetahuan yang diperoleh untuk memberikan maklumat yang tepat
- Jika anda tidak tahu sesuatu, tawarkan untuk menghubungkan mereka dengan ejen manusia
- Pastikan respons ringkas tetapi lengkap
- Gunakan maklumat perniagaan yang relevan

Bahasa utama: {business_config.get('primary_language', 'Bahasa Malaysia')}
Bahasa yang disokong: {', '.join(business_config.get('supported_languages', ['Bahasa Malaysia', 'English']))}

Maklumat perniagaan:
- Nama: {business_config.get('business_name', 'Perniagaan')}
- Jenis: {business_config.get('business_type', 'ecommerce')}
- Waktu operasi: {business_config.get('business_hours', {})}
- Maklumat hubungan: {business_config.get('contact_info', {})}""",
                    "tools": ["response_generation"]
                }
            }
        ]
        super().__init__(model=model, agents=agents)
        self.business_config = business_config
        self.localizer = MalaysianLocalizer()
        self.business_config_manager = BusinessConfigManager()
        self.notification_manager = NotificationManager()
        self._current_step = 0
        self._max_steps = len(agents)
        self._conversation_context = {}

    async def select_agent(self, state: MasterAgentState):
        """Pemilihan agen pintar berdasarkan keadaan perbualan"""
        messages = state.messages
        trace = {
            "name": "MalaysianCustomerServiceAgent",
            "input": messages[-1].model_dump() if hasattr(messages[-1], 'model_dump') else str(messages[-1]),
        }

        try:
            # Determine which agent to use based on current state
            if self._current_step == 0:
                # Step 1: Language Detection
                agent_to_execute = self._agents_to_bind_to_llm[0]
                logger.info(f"Langkah 1: Mengesan bahasa untuk mesej")
                
            elif self._current_step == 1:
                # Step 2: Intent Classification
                agent_to_execute = self._agents_to_bind_to_llm[1]
                logger.info(f"Langkah 2: Mengklasifikasikan niat untuk mesej")
                
            elif self._current_step == 2:
                # Step 3: Knowledge Retrieval
                agent_to_execute = self._agents_to_bind_to_llm[2]
                logger.info(f"Langkah 3: Mengambil pengetahuan yang relevan")
                
            elif self._current_step == 3:
                # Step 4: Response Generation
                agent_to_execute = self._agents_to_bind_to_llm[3]
                logger.info(f"Langkah 4: Menjana respons")
                
            else:
                # All steps completed, generate final response
                return self._create_completion_response(state, trace)

            # Execute the selected agent
            async with trace_execution_time(trace=trace):
                response = await self._execute_agent_step(agent_to_execute, messages, state)
            
            # Process response and update context
            await self._process_agent_response(agent_to_execute, response, state)
            
            # Move to next step
            self._current_step += 1
            
            # If this is the final step, return the response
            if self._current_step >= self._max_steps:
                self._current_step = 0  # Reset for next conversation
                trace.update({
                    "output": response.model_dump() if hasattr(response, 'model_dump') else str(response),
                    "is_success": True
                })
                return {"messages": [response], "trace": [trace]}
            else:
                # Continue to next step
                return await self.select_agent(state)

        except Exception as e:
            error_message = f"Ralat dalam Agen Perkhidmatan Pelanggan Malaysia: {e}"
            logger.exception(error_message)

            # Send error notification
            await self._send_error_notification(state, str(e))

            trace.update({
                "output": error_message,
                "is_success": False
            })
            return {"messages": [AIMessage(content=error_message)], "trace": [trace]}

    async def _execute_agent_step(self, agent_to_execute: Dict[str, Any], messages: list, state: MasterAgentState):
        """Execute a single agent step"""
        try:
            # For GenAI agents, use the model directly
            if agent_to_execute["type"] == "gen_ai":
                system_prompt = agent_to_execute["agent_schema"]["system_prompt"]
                user_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
                
                # Create messages for the model
                model_messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
                
                # Get response from the model
                response = await self.model.ainvoke(model_messages)
                return response
                
            # For MCP agents, simulate API call
            elif agent_to_execute["type"] == "mcp":
                # Simulate knowledge retrieval based on business type
                knowledge = await self._get_business_knowledge(state)
                return AIMessage(content=knowledge)
                
            else:
                raise ValueError(f"Jenis agen tidak disokong: {agent_to_execute['type']}")
                
        except Exception as e:
            logger.error(f"Ralat dalam melaksanakan langkah agen: {e}")
            return AIMessage(content=f"Maaf, saya menghadapi ralat dalam memproses permintaan anda: {e}")

    async def _get_business_knowledge(self, state: MasterAgentState) -> str:
        """Get business-specific knowledge"""
        try:
            business_type = self.business_config.get("business_type", "ecommerce")
            intent = self._conversation_context.get("intent", "general")
            
            # Business-specific knowledge base
            knowledge_base = {
                "ecommerce": {
                    "complaint": "Untuk aduan, sila berikan nombor pesanan anda dan terangkan masalahnya. Kami akan menyiasat dan menghubungi anda dalam masa 24 jam.",
                    "order": "Anda boleh menjejaki status pesanan dengan memberikan nombor pesanan anda. Pesanan biasanya mengambil masa 3-5 hari bekerja untuk sampai.",
                    "support": "Untuk sokongan teknikal, sila terangkan masalah yang anda hadapi. Pasukan sokongan kami tersedia 24/7.",
                    "billing": "Untuk pertanyaan bil, sila berikan nombor akaun anda. Anda juga boleh menyemak sejarah bil dalam dashboard akaun anda.",
                    "general": "Terima kasih kerana menghubungi kami. Bagaimana saya boleh membantu anda hari ini?",
                    "product": "Kami mempunyai pelbagai produk berkualiti tinggi. Bolehkah anda beritahu saya produk mana yang anda minati?",
                    "delivery": "Kami menyediakan perkhidmatan penghantaran ke seluruh Malaysia. Kos penghantaran bergantung pada lokasi dan saiz pesanan.",
                    "return": "Kami menerima pemulangan dalam masa 30 hari dari tarikh pembelian. Sila pastikan barang dalam keadaan asal."
                },
                "restaurant": {
                    "complaint": "Kami meminta maaf atas ketidakselesaan. Sila berikan butiran pesanan dan masalah yang dihadapi. Kami akan menyiasat dengan segera.",
                    "order": "Anda boleh membuat tempahan melalui telefon atau aplikasi kami. Waktu tempahan: 10:00-22:00 setiap hari.",
                    "support": "Untuk pertanyaan tentang menu atau alergi, sila hubungi kami. Chef kami akan membantu anda.",
                    "billing": "Kami menerima tunai, kad kredit, dan pembayaran digital. Tiada caj perkhidmatan dikenakan.",
                    "general": "Selamat datang ke restoran kami! Bagaimana saya boleh membantu anda hari ini?",
                    "product": "Kami menawarkan masakan tempatan dan antarabangsa. Menu kami dikemas kini setiap bulan.",
                    "delivery": "Kami menyediakan perkhidmatan penghantaran dalam radius 10km. Masa penghantaran: 30-45 minit.",
                    "return": "Jika ada masalah dengan makanan, sila hubungi kami dengan segera. Kami akan menggantikan atau memulangkan wang."
                },
                "hotel": {
                    "complaint": "Kami meminta maaf atas ketidakselesaan. Sila berikan nombor tempahan dan terangkan masalahnya. Kami akan menyelesaikannya dengan segera.",
                    "order": "Anda boleh membuat tempahan melalui laman web kami atau hubungi resepsi. Kami menawarkan kadar istimewa untuk tempahan awal.",
                    "support": "Untuk pertanyaan tentang kemudahan hotel atau aktiviti, sila hubungi concierge kami. Mereka tersedia 24/7.",
                    "billing": "Semua bil akan dikenakan pada kad kredit yang didaftarkan. Anda boleh menyemak bil dalam akaun anda.",
                    "general": "Selamat datang ke hotel kami! Bagaimana saya boleh membantu anda hari ini?",
                    "product": "Kami menawarkan bilik mewah dengan kemudahan moden. Semua bilik dilengkapi dengan WiFi percuma dan TV kabel.",
                    "delivery": "Kami menyediakan perkhidmatan room service 24/7. Menu dan masa penghantaran boleh didapati di bilik anda.",
                    "return": "Jika anda tidak berpuas hati dengan penginapan, sila hubungi pengurus hotel. Kami akan menyelesaikan masalah anda."
                }
            }
            
            # Get knowledge based on business type and intent
            business_knowledge = knowledge_base.get(business_type, knowledge_base["ecommerce"])
            return business_knowledge.get(intent, business_knowledge["general"])
            
        except Exception as e:
            logger.error(f"Ralat dalam mendapatkan pengetahuan perniagaan: {e}")
            return "Terima kasih kerana menghubungi kami. Bagaimana saya boleh membantu anda hari ini?"

    async def _process_agent_response(self, agent: Dict[str, Any], response: AIMessage, state: MasterAgentState):
        """Process agent response and update conversation context"""
        try:
            agent_name = agent["name"]
            response_content = response.content
            
            # Parse JSON responses
            if agent_name == "language_detector_agent":
                try:
                    # Try to parse JSON response
                    if response_content.startswith("{") and response_content.endswith("}"):
                        parsed = json.loads(response_content)
                        self._conversation_context["detected_language"] = parsed.get("language", "ms")
                        self._conversation_context["language_confidence"] = parsed.get("confidence", 0.0)
                    else:
                        # Fallback to simple language detection
                        self._conversation_context["detected_language"] = self.localizer.detect_language_from_text(response_content)
                        self._conversation_context["language_confidence"] = 0.8
                except json.JSONDecodeError:
                    # Fallback to simple language detection
                    self._conversation_context["detected_language"] = self.localizer.detect_language_from_text(response_content)
                    self._conversation_context["language_confidence"] = 0.8
                    
            elif agent_name == "intent_classifier_agent":
                try:
                    # Try to parse JSON response
                    if response_content.startswith("{") and response_content.endswith("}"):
                        parsed = json.loads(response_content)
                        self._conversation_context["intent"] = parsed.get("intent", "general")
                        self._conversation_context["intent_confidence"] = parsed.get("confidence", 0.0)
                        self._conversation_context["urgency"] = parsed.get("urgency", "sederhana")
                    else:
                        # Fallback to simple intent detection
                        self._conversation_context["intent"] = "general"
                        self._conversation_context["intent_confidence"] = 0.5
                        self._conversation_context["urgency"] = "sederhana"
                except json.JSONDecodeError:
                    # Fallback to simple intent detection
                    self._conversation_context["intent"] = "general"
                    self._conversation_context["intent_confidence"] = 0.5
                    self._conversation_context["urgency"] = "sederhana"
                    
            elif agent_name == "knowledge_retriever_agent":
                self._conversation_context["retrieved_knowledge"] = response_content
                
            elif agent_name == "response_generator_agent":
                # Check if escalation is needed
                if self._should_escalate():
                    await self._handle_escalation(state)
                
        except Exception as e:
            logger.error(f"Ralat dalam memproses respons agen: {e}")

    def _should_escalate(self) -> bool:
        """Check if conversation should be escalated"""
        try:
            intent = self._conversation_context.get("intent", "general")
            urgency = self._conversation_context.get("urgency", "sederhana")
            confidence = self._conversation_context.get("intent_confidence", 1.0)
            
            # Escalate if high urgency or low confidence
            if urgency == "tinggi" or confidence < 0.5:
                return True
                
            # Escalate for certain intents
            escalation_intents = ["complaint", "billing", "support"]
            if intent in escalation_intents and confidence < 0.7:
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Ralat dalam menentukan eskalasi: {e}")
            return False

    async def _handle_escalation(self, state: MasterAgentState):
        """Handle conversation escalation"""
        try:
            business_id = getattr(state, 'business_id', None)
            session_id = getattr(state, 'session_id', 'unknown')
            detected_language = self._conversation_context.get("detected_language", "ms")
            intent = self._conversation_context.get("intent", "general")
            
            # Get customer message
            customer_message = ""
            if state.messages:
                customer_message = state.messages[-1].content if hasattr(state.messages[-1], 'content') else str(state.messages[-1])
            
            # Send escalation notification
            await self.notification_manager.send_escalation_notification(
                business_id=business_id,
                session_id=session_id,
                customer_message=customer_message,
                language=detected_language,
                intent=intent
            )
            
            logger.info(f"Eskalasi dihantar untuk sesi {session_id}")
            
        except Exception as e:
            logger.error(f"Ralat dalam mengendalikan eskalasi: {e}")

    async def _send_error_notification(self, state: MasterAgentState, error_message: str):
        """Send error notification"""
        try:
            business_id = getattr(state, 'business_id', None)
            if business_id:
                await self.notification_manager.send_error_notification(
                    business_id=business_id,
                    error_type="agent_error",
                    error_message=error_message
                )
        except Exception as e:
            logger.error(f"Ralat dalam menghantar notifikasi ralat: {e}")

    def _create_completion_response(self, state: MasterAgentState, trace: Dict[str, Any]):
        """Create final response when all steps are completed"""
        try:
            # Generate a comprehensive response based on all gathered information
            detected_language = self._conversation_context.get("detected_language", "ms")
            intent = self._conversation_context.get("intent", "general")
            knowledge = self._conversation_context.get("retrieved_knowledge", "")
            
            # Create personalized response
            if knowledge:
                final_response = knowledge
            else:
                final_response = self.localizer.get_greeting(detected_language)
            
            # Add escalation message if needed
            if self._should_escalate():
                escalation_msg = self.localizer.get_escalation_message(detected_language)
                final_response += f"\n\n{escalation_msg}"
            
            trace.update({
                "output": final_response,
                "is_success": True,
                "detected_language": detected_language,
                "intent": intent,
                "confidence": self._conversation_context.get("intent_confidence", 0.0)
            })
            
            return {"messages": [AIMessage(content=final_response)], "trace": [trace]}
            
        except Exception as e:
            logger.error(f"Ralat dalam mencipta respons penyiapan: {e}")
            return {"messages": [AIMessage(content="Terima kasih kerana menghubungi kami. Bagaimana saya boleh membantu anda hari ini?")], "trace": [trace]}

    def reset_conversation(self):
        """Reset the conversation state"""
        self._current_step = 0
        self._conversation_context = {}

    async def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation"""
        return {
            "current_step": self._current_step,
            "max_steps": self._max_steps,
            "context": self._conversation_context,
            "business_config": {
                "name": self.business_config.get("business_name", "Perniagaan"),
                "type": self.business_config.get("business_type", "ecommerce"),
                "primary_language": self.business_config.get("primary_language", "Bahasa Malaysia")
            }
        }