from langgraph.graph import StateGraph, START, END
from src.Graph.state import RAGState

graph = StateGraph(RAGState)

graph.add_node("Orchestrator", orchestrator_work)
graph.add_node("Synthesis", synthesis_node)

graph.add_edge(START, "Orchestrator")
graph.add_edge("Orchestrator", "Synthesis")
graph.add_edge("Synthesis", END)

workflow = graph.compile()