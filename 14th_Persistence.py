# Conversatation  ko Permently Save karna database main :- 

from langgraph.graph import  StateGraph , START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_anthropic import ChatAnthropic
from langchain_core.messages  import HumanMessage
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
import sqlite3


class Chatstate(TypedDict):
    messages: Annotated[list,add_messages]

    llm = ChatAnthropic(model="claude-sonnet-4-6")

def chat_node (State:Chatstate) -> Chatstate:
    response = llm.invoke (State["messages"])
    return {"messages":[response]}


graph = StateGraph(Chatstate)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# 🔑 Yahi hai naya part — InMemorySaver ki jagah SqliteSaver
conn = sqlite3.connect("my_chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

app = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "rahul-ki-chat"}}

result = app.invoke(
    {"messages": [HumanMessage(content="Mera naam Rahul hai")]},
    config=config
)
print("AI:", result["messages"][-1].content)