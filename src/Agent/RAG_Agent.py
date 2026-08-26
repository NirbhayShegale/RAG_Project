from src.Graph.state import RAGState
from langchain_classic.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
from src.Agent.RAG_Agent_prompt import RAG_AGENT_SYSTEM_PROMPT
from src.Config.models import get_llm
from src.Config.logger import get_logger

log = get_logger(__name__)


def RAG_Agent_node(state: RAGState) -> RAGState:
    current_query = state.get("Userquery", "")

    # System prompt carries the retrieved context + all guardrail rules
    formatted_system = RAG_AGENT_SYSTEM_PROMPT.format(
        context=state.get("Context", ""),
        history=state.get("messages", []),
    )

    # Pull previous Human/AI turns from state for conversational memory

    messages_to_send = [
        SystemMessage(content=formatted_system),
        HumanMessage(content=current_query),   # ← current question
    ]

    log.info(f"Agent: query='{current_query}' history={len(state.get('messages', []))} ctx={len(state.get('Context',''))}c")
    response = get_llm().invoke(messages_to_send)
    log.info(f"Agent: answer='{response.content[:80]}{'...' if len(response.content)>80 else ''}'")

    # Persist both sides of this turn into state["messages"]
    human_msg = HumanMessage(content=current_query)
    ai_msg    = AIMessage(content=response.content)  # plain text, not JSON dump

    return {"messages": [human_msg, ai_msg], "response": response}
