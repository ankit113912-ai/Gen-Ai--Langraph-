from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    sawaal: str
    number1: int
    number2: int
    result: int

# 🔧 Ye hai hamara TOOL — ek simple function
def calculator_tool(a: int, b: int) -> int:
    print(f"Tool chal raha hai: {a} + {b} calculate ho raha hai")
    return a + b

# Node jo tool ko CALL karta hai
def use_tool_node(state: MyState) -> MyState:
    # LLM ki jagah abhi hum manually decide kar rahe hain ki tool use karna hai
    result = calculator_tool(state["number1"], state["number2"])
    state["result"] = result
    return state

graph = StateGraph(MyState)
graph.add_node("use_tool", use_tool_node)
graph.add_edge(START, "use_tool")
graph.add_edge("use_tool", END)

app = graph.compile()
result = app.invoke({"sawaal": "5 aur 10 ka sum?", "number1": 10, "number2": 10, "result": 0})
print(result)