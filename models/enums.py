from enum import Enum


class Nodes(str, Enum):
    """Enumeration of workflow nodes"""
    supervisor = "supervisor"
    execute_agent = "execute_agent"
    language_detector = "language_detector"
    intent_classifier = "intent_classifier"
    knowledge_retriever = "knowledge_retriever"
    response_generator = "response_generator"