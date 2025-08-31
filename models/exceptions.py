class UnknownAgentTypeException(Exception):
    """Exception raised when an unknown agent type is encountered"""
    pass


class AgentNotFoundError(Exception):
    """Exception raised when a requested agent is not found"""
    pass


class NoToolCallsError(Exception):
    """Exception raised when no tool calls are found in agent response"""
    pass


class AgentUnavailableError(Exception):
    """Exception raised when an agent is unavailable"""
    pass