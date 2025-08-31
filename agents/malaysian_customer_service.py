from typing import Any, Dict
from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from loguru import logger

from agents.base import BaseMasterAgent
from models.states import MasterAgentState
from utils.tracing import trace_execution_time


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
                    "system_prompt": """You are a language detection expert. Detect the language of the input text and return the result in JSON format.
                    
                    Supported languages:
                    - Bahasa Malaysia (ms)
                    - English (en) 
                    - Chinese (zh)
                    - Tamil (ta)
                    
                    Return format: {"language": "language_code", "confidence": 0.95}""",
                    "tools": ["language_detection"]
                }
            },
            {
                "name": "intent_classifier_agent", 
                "type": "gen_ai",
                "id": "intent_class_001",
                "agent_schema": {
                    "model": "gpt-4",
                    "system_prompt": """You are a customer intent classification expert. Classify the customer's intent from their message.
                    
                    Intent categories:
                    - complaint: Customer complaints or issues
                    - order: Order-related inquiries (status, tracking, etc.)
                    - support: Technical support requests
                    - billing: Billing and payment inquiries
                    - general: General questions or information requests
                    
                    Return format: {"intent": "intent_category", "confidence": 0.90, "entities": ["relevant_entities"]}""",
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
                    "system_prompt": f"""You are a helpful customer service representative for {business_config.get('business_name', 'our company')}.
                    
                    Guidelines:
                    - Respond in the customer's detected language
                    - Be helpful, professional, and empathetic
                    - Use the retrieved knowledge to provide accurate information
                    - If you don't know something, offer to connect them with a human agent
                    - Keep responses concise but complete
                    
                    Primary language: {business_config.get('primary_language', 'Bahasa Malaysia')}
                    Supported languages: {', '.join(business_config.get('supported_languages', ['Bahasa Malaysia', 'English']))}""",
                    "tools": ["response_generation"]
                }
            }
        ]
        super().__init__(model=model, agents=agents)
        self.business_config = business_config
        self._current_step = 0
        self._max_steps = len(agents)

    async def select_agent(self, state: MasterAgentState):
        """Intelligent agent selection based on conversation state"""
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
                logger.info(f"Step 1: Detecting language for message")
                
            elif self._current_step == 1:
                # Step 2: Intent Classification
                agent_to_execute = self._agents_to_bind_to_llm[1]
                logger.info(f"Step 2: Classifying intent for message")
                
            elif self._current_step == 2:
                # Step 3: Knowledge Retrieval
                agent_to_execute = self._agents_to_bind_to_llm[2]
                logger.info(f"Step 3: Retrieving relevant knowledge")
                
            elif self._current_step == 3:
                # Step 4: Response Generation
                agent_to_execute = self._agents_to_bind_to_llm[3]
                logger.info(f"Step 4: Generating response")
                
            else:
                # All steps completed, generate final response
                return self._create_completion_response(state, trace)

            # Execute the selected agent
            async with trace_execution_time(trace=trace):
                response = await self._execute_agent_step(agent_to_execute, messages, state)
            
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
            error_message = f"Error in Malaysian Customer Service Agent: {e}"
            logger.exception(error_message)

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
                # Simulate knowledge retrieval
                mock_knowledge = {
                    "complaint": "For complaints, please provide your order number and describe the issue. We'll investigate and get back to you within 24 hours.",
                    "order": "You can track your order status by providing your order number. Orders typically take 3-5 business days to arrive.",
                    "support": "For technical support, please describe the issue you're experiencing. Our support team is available 24/7.",
                    "billing": "For billing inquiries, please provide your account number. You can also check your billing history in your account dashboard.",
                    "general": "Thank you for contacting us. How can I help you today?"
                }
                
                # Return mock knowledge based on intent (if available)
                intent = getattr(state, 'detected_intent', 'general')
                knowledge = mock_knowledge.get(intent, mock_knowledge['general'])
                
                return AIMessage(content=knowledge)
                
            else:
                raise ValueError(f"Unsupported agent type: {agent_to_execute['type']}")
                
        except Exception as e:
            logger.error(f"Error executing agent step: {e}")
            return AIMessage(content=f"I apologize, but I encountered an error processing your request: {e}")

    def _create_completion_response(self, state: MasterAgentState, trace: Dict[str, Any]):
        """Create final response when all steps are completed"""
        # Generate a comprehensive response based on all gathered information
        final_response = "Thank you for contacting us. I've processed your request and gathered all necessary information. How else can I assist you today?"
        
        trace.update({
            "output": final_response,
            "is_success": True
        })
        
        return {"messages": [AIMessage(content=final_response)], "trace": [trace]}

    def reset_conversation(self):
        """Reset the conversation state"""
        self._current_step = 0