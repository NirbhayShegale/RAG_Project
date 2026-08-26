from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.Graph.state import RAGState

from src.Graph.router import router
from src.Agent.RAG_Agent import RAG_Agent_node
from src.Tool.OrderLookUp import run_order_lookup
from src.Tool.run_retrival import run_retrival

graph = StateGraph(RAGState)

graph.add_node("Router", router)
graph.add_node("RetrivalTool", run_retrival)
graph.add_node("OrderLookupTool", run_order_lookup)
graph.add_node("RAG_Agent_node", RAG_Agent_node)

graph.add_edge(START, "Router")
graph.add_conditional_edges(
    "Router",
    lambda state: state["next_node"],
    {
        "RAG_node": "RetrivalTool",
        "order_lookup_tool_node": "OrderLookupTool",
    },
)
graph.add_edge("RetrivalTool", "RAG_Agent_node")
graph.add_edge("OrderLookupTool", "RAG_Agent_node")
graph.add_edge("RAG_Agent_node", END)

memory = MemorySaver()
workflow = graph.compile(checkpointer=memory)
