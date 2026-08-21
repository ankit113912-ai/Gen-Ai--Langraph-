from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str   # supervisor yahan decide karke likhega

llm = ChatAnthropic(model="claude-sonnet-4-6")

# 🧑‍💼 SUPERVISOR — decide karta hai kaunsa agent chalega
def supervisor_node(state: AgentState) -> AgentState:
    user_message = state["messages"][-1].content
    
    decision_prompt = f"""User ne ye poocha: "{user_message}"
    Agar ye MATH/calculation sawaal hai, to sirf 'math' likho.
    Agar ye GENERAL KNOWLEDGE sawaal hai, to sirf 'research' likho.
    Sirf ek word likho: math ya research"""
    
    response = llm.invoke([HumanMessage(content=decision_prompt)])
    decision = response.content.strip().lower()
    print(f"👨‍💼 Supervisor decide kar raha hai: {decision}")
    return {"next_agent": decision}

# 🧮 MATH AGENT — sirf calculation karta hai
def math_agent_node(state: AgentState) -> AgentState:
    print("🧮 Math Agent kaam kar raha hai...")
    system = SystemMessage(content="Tum ek math expert ho. Sirf calculation aur numbers pe focus karo.")
    response = llm.invoke([system] + state["messages"])
    return {"messages": [response]}

# 📚 RESEARCH AGENT — general knowledge deta hai
def research_agent_node(state: AgentState) -> AgentState:
    print("📚 Research Agent kaam kar raha hai...")
    system = SystemMessage(content="Tum ek general knowledge expert ho. Facts aur information do.")
    response = llm.invoke([system] + state["messages"])
    return {"messages": [response]}

# Routing function — supervisor ke decision ke hisaab se node choose karo
def route_karo(state: AgentState) -> str:
    return state["next_agent"]

# Graph banate hain
graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("math", math_agent_node)
graph.add_node("research", research_agent_node)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_karo,
    {
        "math": "math",
        "research": "research"
    }
)
graph.add_edge("math", END)
graph.add_edge("research", END)

app = graph.compile()

# Test 1: Math sawaal
result1 = app.invoke({
    "messages": [HumanMessage(content="25 * 17 kitna hota hai?")],
    "next_agent": ""
})
print("Final Answer:", result1["messages"][-1].content)

print("\n---\n")

# Test 2: General knowledge sawaal
result2 = app.invoke({
    "messages": [HumanMessage(content="Taj Mahal kisne banwaya tha?")],
    "next_agent": ""
})
print("Final Answer:", result2["messages"][-1].content)