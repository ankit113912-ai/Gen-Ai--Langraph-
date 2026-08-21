from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# ===== SUBGRAPH: Research Team =====
class ResearchState(TypedDict):
    query: str
    search_result: str
    summary: str

def search_node(state: ResearchState) -> ResearchState:
    print("  🔍 Subgraph: Search kar raha hoon...")
    state["search_result"] = f"'{state['query']}' ke baare mein info mil gayi"
    return state

def summarize_node(state: ResearchState) -> ResearchState:
    print("  📝 Subgraph: Summarize kar raha hoon...")
    state["summary"] = f"Summary: {state['search_result']}"
    return state

# Subgraph banate hain (ye poora normal graph hai)
research_graph = StateGraph(ResearchState)
research_graph.add_node("search", search_node)
research_graph.add_node("summarize", summarize_node)
research_graph.add_edge(START, "search")
research_graph.add_edge("search", "summarize")
research_graph.add_edge("summarize", END)

research_subgraph = research_graph.compile()   # 🔑 Compile kar diya - ab ye ek "unit" hai


# ===== MAIN GRAPH: Customer Support =====
class SupportState(TypedDict):
    query: str
    search_result: str
    summary: str
    final_response: str

def greet_node(state: SupportState) -> SupportState:
    print("👋 Main Graph: User ko greet kar raha hoon")
    return state

def final_response_node(state: SupportState) -> SupportState:
    print("✅ Main Graph: Final response bana raha hoon")
    state["final_response"] = f"Yahan hai aapka jawab: {state['summary']}"
    return state

main_graph = StateGraph(SupportState)
main_graph.add_node("greet", greet_node)

# 🔑 Yahi hai magic — subgraph ko ek NORMAL NODE ki tarah add karo!
main_graph.add_node("research_team", research_subgraph)

main_graph.add_node("final_response", final_response_node)

main_graph.add_edge(START, "greet")
main_graph.add_edge("greet", "research_team")     # subgraph call ho raha hai yahan
main_graph.add_edge("research_team", "final_response")
main_graph.add_edge("final_response", END)

app = main_graph.compile()

result = app.invoke({
    "query": "LangGraph kaise seekhein",
    "search_result": "",
    "summary": "",
    "final_response": ""
})
print("\nFinal Result:", result["final_response"])
