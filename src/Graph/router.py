from typing import Literal
from pydantic import BaseModel

from src.Graph.state import RAGState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.Config.models import get_llm
from src.Config.logger import get_logger

log = get_logger(__name__)


class router_model(BaseModel):
    next_node: Literal["RAG_node", "order_lookup_tool_node"]


parser = PydanticOutputParser(pydantic_object=router_model)


def router(state: RAGState) -> RAGState:
    user_query = state['Userquery'].lower()
    log.info(f"Router: '{user_query}'")

    prompt = ChatPromptTemplate.from_template(
    """
    You are an expert at classifying user queries for a customer-support agent.
    You do NOT answer the question yourself. You ONLY classify the query into one of two categories.

    Capabilities:
    - RAG_node: retrieves general policy, product, or how-to information
    - order_lookup_tool_node: retrieves data for ONE specific existing order (status, tracking, items, delivery estimate, cancellation-window eligibility). Requires an order ID.

    User query: {Userquery}

    {format_instructions}
    """)

    chain = prompt | get_llm() | parser
    response = chain.invoke({"Userquery": user_query, "format_instructions": parser.get_format_instructions()})

    log.info(f"Router -> {response.next_node}")
    return {"next_node": response.next_node}
