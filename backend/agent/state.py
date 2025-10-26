from typing import TypedDict, Literal, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    The state for our agent.

    Attributes:
        messages: The history of messages (Human, AI)
        intent: The classified intent of the user's last message
        response: The AI's response to be added to history
        context_data: Additional context data from tools
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    intent: Literal[
        "search_recommendation",
        "compare",
        "details",
        "query",
        "chitchat",
        "irrelevant",
        "adversarial",
    ] | None
    response: str
    context_data: list | dict | None