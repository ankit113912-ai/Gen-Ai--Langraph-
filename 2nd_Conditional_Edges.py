
# Conditional Example :-  Check karega ki number positive hai ya negative 

from langgraph.graph import StateGraph, END
from typing import TypedDict

# State Design 

class MyState (TypedDict):

    number : int 
    result : str 

# Node 1 :- number set karo 

def input_node (state:MyState) -> MyState:
    print ("number check kar raha hain :", state["number"])
    return state

# Node 2 :- Positive wala message 

def positive_node (state:MyState) -> MyState:
    state["result"] = "ye number POSITIVE  hain ! "
    return state 

# Node 3 :- Negative wala message 

def Negative_node (state:MyState) -> MyState:
    state["result"] = "ye number NEGATIVE hai ! "
    return state


# ye hai DECISION FUNCTION -> ye batayega konsa rasta lena hai 

def decide_karo (state:MyState) -> str :
    if state ["number"] >= 0 :

        return "positive_path"    # ye ek label hai node ka naam nahi 

    else :
        return "negative_path"


# Graph banate hain

graph = StateGraph(MyState)

graph.add_node ("input", input_node)
graph.add_node ("positive",positive_node)
graph.add_node ("negative",Negative_node)

graph.set_entry_point("input")



# ye hain conditional edge

graph.add_conditional_edges(
    "input",              # kis node ke baad decide karna hai
    decide_karo,          # kaunsa function decide karega
    {
        "positive_path": "positive",   # agar "positive_path" mila to "positive" node pe jao
        "negative_path": "negative"    # agar "negative_path" mila to "negative" node pe jao
    }

)


graph.add_edge("positive",END)
graph.add_edge("negative",END)


app = graph.compile()


# Test karte hai chalo 

result1 = app.invoke({"number": 5, "result": ""})
print(result1)

result2 = app.invoke({"number": -3, "result": ""})
print(result2)


                


