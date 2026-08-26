from typing import Annotated, Any, TypedDict
from langchain_classic.schema import BaseMessage
from langgraph.graph import add_messages

class RAGState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_node: str
    Context: str
    Userquery: str
    response: str
