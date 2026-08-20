from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import  InMemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Tool jo THODA khatarnak hai (paisa transfer)
@tool
def transfer_money(amount: int, to_account: str) -> str:
    """Paisa transfer karta hai account mein"""
    return f"{amount} rupaye {to_account} ko transfer ho gaye!"

tools = [transfer_money]

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatAnthropic(model="claude-sonnet-4-6")
llm_with_tools = llm.bind_tools(tools)

def llm_node(state: AgentState) -> AgentState:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "use_tool"
    return "khatam"

graph = StateGraph(AgentState)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue, {"use_tool": "tools", "khatam": END})
graph.add_edge("tools", "llm")

# 🔑 Ye hai naya part — Checkpointer aur Interrupt

checkpointer = InMemorySaver()
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["tools"]           # "Tools" :- node sew phele ruk jao 
)


# 🔑 config mein ek "thread_id" dena zaroori hai — ye batata hai konsi conversation hai
config = {"configurable": {"thread_id": "user-123"}}

# Step 1: Pehli baar chalao
result = app.invoke(
    {"messages": [HumanMessage(content="500 rupaye Ravi ke account mein transfer karo")]},
    config=config
)

# Yahan graph RUK JAYEGA (kyunki humne interrupt_before lagaya)
print("Graph ruk gaya hai! Ye tool call karna chahta hai:")
print(result["messages"][-1].tool_calls)

# User se pooch lo
user_input = input("Kya ye transfer karna sahi hai? (haan/nahi): ")

if user_input.lower() == "haan":
    # Step 2: Graph ko AAGE continue karo (wahin se jaha ruka tha)
    final_result = app.invoke(None, config=config)  # None = "jaisa hai waisa continue karo"
    print(final_result["messages"][-1].content)
else:
    print("Transfer cancel kar diya gaya!")


    
