# State Update Reducers (Data kese merge hota hai )

from typing import Annotated
from langgraph.graph import StateGraph, START,END
import operator
from typing import TypedDict

class MyState (TypedDict):
    # Annotated ka matlab hai : "is field ko is REDUCER sew update karo "
    messages: Annotated[list, operator.add]

def node1 (state:MyState) -> MyState:
    return {"messages":["Doodh"]}       # sirf naya data return karo 

def node2 (state:MyState)  -> MyState:
    return{"messages":["Bread"]}


graph = StateGraph(MyState)

graph.add_node("node1",node1)
graph.add_node("node2",node2)
graph.add_edge(START,"node1")
graph.add_edge("node1","node2")
graph.add_edge("node2",END)

app = graph.compile()
result = app.invoke ({"messages":[]})

print(result)

