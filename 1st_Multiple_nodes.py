# Multiple nodes ko connect karna  :- 

from langgraph.graph import StateGraph, END
from typing import TypedDict


# State design 

class Mystate (TypedDict):
    Question :str
    Think    :str 
    Answer   :str


# Node 1 : Question Read 

def Read_node (State:Mystate) -> Mystate:
    print ("step 1 : Question Read kar raha hu ! ")
    State["Question"] = "What is Langgraph ? "
    return State



# Node 2 : Thinking 

def Think_node (state:Mystate) -> Mystate:
    print ("step 2 : soch raha huu... ")
    state["Think"] = "This is a graph based Ai Framwork  "
    return state



# Node 3 : Answer node 

def Answer_node (state:Mystate) -> Mystate:
    print ("step 3 : Answer de raha huu...")
    state["Answer"] = f"{state['Think']} - ye most powerful hai !" 
    return state


# Graph banate hai 

graph = StateGraph(Mystate)

# Teeno  nodes add karo 

graph.add_node("Read",   Read_node)
graph.add_node("Think",  Think_node)
graph.add_node("Answer", Answer_node)


# Entery point set karo 

graph.set_entry_point("Read")

# abb teeno ko chain sew join karo (train ke coaches join karne jesa )

graph.add_edge("Read","Think")
graph.add_edge("Think","Answer")
graph.add_edge("Answer",END)


# Compile and Run 

app = graph.compile()
result = app.invoke({"Question": "", "Think": "", "Answer": ""})
print ( result )
















