__all__ = ["AgentCPMAgent"]


def __getattr__(name):
    if name == "AgentCPMAgent":
        from .agentcpm_agent import AgentCPMAgent

        return AgentCPMAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
