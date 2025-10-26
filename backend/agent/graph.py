import json
import logging
from typing import Dict, Any

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.prompts.intent_classification import INTENT_CLASSIFICATION_PROMPT
from agent.prompts.tool_selection import TOOL_SELECTION_PROMPT
from agent.prompts.chitchat_intent import CHITCHAT_INTENT_PROMPT
from agent.prompts.query_intent import QUERY_INTENT_PROMPT
from agent.prompts.irrelevant_intent import IRRELEVANT_INTENT_PROMPT
from agent.prompts.adversarial_intent import ADVERSARIAL_INTENT_PROMPT
from agent.prompts.details_intent import DETAILS_INTENT_PROMPT
from agent.prompts.compare_intent import COMPARE_INTENT_PROMPT
from agent.prompts.search_recommendation_intent import (
    SEARCH_RECOMMENDATION_INTENT_PROMPT,
)

from agent.tools.supabase_tools import (
    fetch_phone_details,
    fetch_recommendations,
    compare_phones,
)

from agent.models.intent_classification_response import IntentClassificationResponse

from agent.state import AgentState

logger = logging.getLogger(__name__)

# CHAT MODELS
intent_classification_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
).with_structured_output(schema=IntentClassificationResponse, method="json_mode")

string_response_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

tool_selection_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash").bind_tools(
    [fetch_phone_details, fetch_recommendations, compare_phones]
)


# NODES
def intent_classification(state: AgentState) -> AgentState:
    """Classify the intent of the user's message"""
    system_prompt = SystemMessage(content=INTENT_CLASSIFICATION_PROMPT)
    response: IntentClassificationResponse = intent_classification_model.invoke(
        [system_prompt] + state["messages"]
    )
    classified_intent = response.intent
    logger.info(f"Classified intent: {classified_intent}")
    return {"intent": classified_intent}


def handle_chitchat_intent(state: AgentState) -> AgentState:
    """Handle chitchat intent"""
    system_prompt = SystemMessage(content=CHITCHAT_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "response": response.content, "context_data": None}


def handle_query_intent(state: AgentState) -> AgentState:
    """Handle query intent"""
    system_prompt = SystemMessage(content=QUERY_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "response": response.content, "context_data": None}


def handle_irrelevant_intent(state: AgentState) -> AgentState:
    """Handle irrelevant intent"""
    system_prompt = SystemMessage(content=IRRELEVANT_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "response": response.content, "context_data": None}


def handle_adversarial_intent(state: AgentState) -> AgentState:
    """Handle adversarial intent"""
    system_prompt = SystemMessage(content=ADVERSARIAL_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "response": response.content, "context_data": None}


def handle_details_intent(state: AgentState) -> AgentState:
    """Handle details intent with tool data"""
    system_prompt = SystemMessage(content=DETAILS_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    last_message: ToolMessage = state["messages"][-1]
    output_data = json.loads(last_message.content)
    if isinstance(output_data, dict) and "error" in output_data:
        output_data = None
    return {
        "messages": [response],
        "response": response.content,
        "context_data": output_data,
    }


def handle_search_recommendation_intent(state: AgentState) -> AgentState:
    """Handle search/recommendation intent with tool data"""
    system_prompt = SystemMessage(content=SEARCH_RECOMMENDATION_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    last_message: ToolMessage = state["messages"][-1]
    output_data = json.loads(last_message.content)
    if isinstance(output_data, dict) and "error" in output_data:
        output_data = None
    return {
        "messages": [response],
        "response": response.content,
        "context_data": output_data,
    }


def handle_compare_intent(state: AgentState) -> AgentState:
    """Handle compare intent with tool data"""
    system_prompt = SystemMessage(content=COMPARE_INTENT_PROMPT)
    response = string_response_model.invoke([system_prompt] + state["messages"])
    last_message: ToolMessage = state["messages"][-1]
    output_data = json.loads(last_message.content)
    if isinstance(output_data, dict) and "error" in output_data:
        output_data = None
    return {
        "messages": [response],
        "response": response.content,
        "context_data": output_data,
    }


def prepare_tool_call(state: AgentState) -> AgentState:
    """Prepare tool call based on user intent"""
    system_prompt = SystemMessage(content=TOOL_SELECTION_PROMPT)
    response = tool_selection_model.invoke([system_prompt] + state["messages"])
    return {"messages": [response], "response": response.content, "context_data": None}


def handle_simple_intent(state: AgentState) -> AgentState:
    """Pass through for simple intents"""
    return state


# CONDITIONAL EDGES
def should_proceed_with_tool_call(state: AgentState) -> str:
    """Check if tool call should proceed"""
    if state.get("messages")[-1].tool_calls:
        return "Have Clarity"
    else:
        return "Need Clarity"


def redirect_to_intent_type_handler(state: AgentState) -> str:
    """Route to simple or data-based intent handlers"""
    if state.get("intent") in ["chitchat", "query", "irrelevant", "adversarial"]:
        return "Simple Intents"
    else:
        return "Data Based Intents"


def redirect_to_specific_intent_handler(state: AgentState) -> str:
    """Route to specific intent handler"""
    return state.get("intent")


# BUILD THE GRAPH
def create_graph():
    """Create and compile the agent graph"""
    graph = StateGraph(AgentState)
    tool_node = ToolNode(
        tools=[fetch_phone_details, fetch_recommendations, compare_phones]
    )

    # ADD NODES
    graph.add_node("Fetch Data", tool_node)
    graph.add_node("Database API Call Preparation", prepare_tool_call)
    graph.add_node("Intent Classifier", intent_classification)
    graph.add_node("Handle Simple Intent", handle_simple_intent)

    # SIMPLE RESPONSE INTENT NODES
    graph.add_node("Handle ChitChat Intent", handle_chitchat_intent)
    graph.add_node("Handle Query Intent", handle_query_intent)
    graph.add_node("Handle Irrelevant Intent", handle_irrelevant_intent)
    graph.add_node("Handle Adversarial Intent", handle_adversarial_intent)

    # DATA BASED RESPONSE INTENT NODES
    graph.add_node("Handle Details Intent", handle_details_intent)
    graph.add_node(
        "Handle Search/Recommendation Intent", handle_search_recommendation_intent
    )
    graph.add_node("Handle Compare Intent", handle_compare_intent)

    # ADD EDGES
    graph.add_edge(START, "Intent Classifier")
    graph.add_conditional_edges(
        "Intent Classifier",
        redirect_to_intent_type_handler,
        {
            "Simple Intents": "Handle Simple Intent",
            "Data Based Intents": "Database API Call Preparation",
        },
    )

    graph.add_conditional_edges(
        "Handle Simple Intent",
        redirect_to_specific_intent_handler,
        {
            "chitchat": "Handle ChitChat Intent",
            "query": "Handle Query Intent",
            "irrelevant": "Handle Irrelevant Intent",
            "adversarial": "Handle Adversarial Intent",
        },
    )

    graph.add_conditional_edges(
        "Database API Call Preparation",
        should_proceed_with_tool_call,
        {
            "Have Clarity": "Fetch Data",
            "Need Clarity": END,
        },
    )

    graph.add_conditional_edges(
        "Fetch Data",
        redirect_to_specific_intent_handler,
        {
            "details": "Handle Details Intent",
            "search_recommendation": "Handle Search/Recommendation Intent",
            "compare": "Handle Compare Intent",
        },
    )

    graph.add_edge("Handle ChitChat Intent", END)
    graph.add_edge("Handle Query Intent", END)
    graph.add_edge("Handle Irrelevant Intent", END)
    graph.add_edge("Handle Adversarial Intent", END)
    graph.add_edge("Handle Details Intent", END)
    graph.add_edge("Handle Search/Recommendation Intent", END)
    graph.add_edge("Handle Compare Intent", END)

    return graph.compile()


# Create the compiled graph
app = create_graph()


async def process_message(message: str, conversation_history: list) -> Dict[str, Any]:
    """
    Process a user message through the agent graph

    Args:
        message: The user's message
        conversation_history: List of previous messages in the conversation

    Returns:
        Dictionary containing intent, response, context_data, and updated messages
    """
    try:
        # Convert conversation history to proper message format
        messages = conversation_history.copy()
        messages.append(HumanMessage(content=message))

        # Initial state
        initial_state = {
            "messages": messages,
            "intent": None,
            "response": "",
            "context_data": None,
        }

        # Run the graph
        result = await app.ainvoke(initial_state)

        return {
            "intent": result.get("intent"),
            "response": result.get("response", ""),
            "context_data": result.get("context_data"),
            "messages": result.get("messages", []),
        }

    except Exception as e:
        logger.error(f"Error in process_message: {e}", exc_info=True)
        raise
