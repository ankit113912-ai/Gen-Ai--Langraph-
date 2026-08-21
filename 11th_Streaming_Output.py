# Two types of Straming Output in langgraph 1st -values Streamig , 2nd - Tokens Streaming  

# 1st  Values Streaming ( node by node )

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    step: str

def node1(state: MyState) -> MyState:
    return {"step": "Node 1 complete"}

def node2(state: MyState) -> MyState:
    return {"step": "Node 2 complete"}

def node3(state: MyState) -> MyState:
    return {"step": "Node 3 complete"}

graph = StateGraph(MyState)
graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", "node3")
graph.add_edge("node3", END)

app = graph.compile()

# 🔑 invoke() ki jagah stream() use karo
for chunk in app.stream({"step": ""}):
    print(chunk)




# 2nd :- Tokens Streaming 

from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatAnthropic(model="claude-sonnet-4-6")

def chat_node(state: ChatState) -> ChatState:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)
app = graph.compile()

# 🔑 stream_mode="messages" se token-by-token milta hai
for chunk, metadata in app.stream(
    {"messages": [HumanMessage(content="LangGraph ke baare mein 3 lines batao")]},
    stream_mode="messages"
):
    if chunk.content:
        print(chunk.content, end="", flush=True)
