# Two Level pr error handling hoti hain 1st :- Node ke andar (try/except) use kar, 2nd :- poore graph main

# 1st :-  Node ke andar error handling.


from langgraph.graph import StateGraph,START,END
from typing import TypedDict

class Mystate (TypedDict):
    number: int
    result: str


def risky_node(state: Mystate)  -> Mystate:
    try:
        # ek risky operation - Divide by Zero ho sakta hain 
        result = 100 / state["number"]
        state["result"] = f"Result: {result}"

    except ZeroDivisionError:
        print ("Error Ayi :  number zero nahi ho sakta ! ")
        state["result"] = "Error: 0  se divide nahi ho sakta , default value use kar raha hoon "

    except Exception as e :
        print (f" koi or error : {e}")
        state ["result"] = "kuch galat ho gya , lekin app crash nahi hua !"

    return state 

graph = StateGraph(Mystate)
graph.add_node("risky",risky_node)
graph.add_edge(START,"risky")
graph.add_edge("risky",END)

app = graph.compile ()


# Test karte hain
result1 = app.invoke({"number": 5, "result": ""})
print(result1)

result2 = app.invoke({"number": 0, "result": ""})   # Ye error create karega
print(result2)





# 2nd :- Retry policy 
from langgraph.graph import StateGraph, START, END
from langgraph.pregel import RetryPolicy
from typing import TypedDict
import random

class MyState(TypedDict):
    attempt: int
    result: str

def unreliable_node(state: MyState) -> MyState:
    state["attempt"] = state.get("attempt", 0) + 1
    print(f"Try #{state['attempt']}...")
    
    # Simulate karte hain ek unreliable API jo kabhi-kabhi fail hoti hai
    if random.random() < 0.7:   # 70% chance of failure
        raise Exception("API abhi fail ho gaya, phir try karo!")
    
    state["result"] = "Success!"
    return state

graph = StateGraph(MyState)

# 🔑 Yahi hai retry policy — node ke saath attach karo
graph.add_node(
    "unreliable",
    unreliable_node,
    retry=RetryPolicy(max_attempts=5)   # 5 baar tak automatic retry karega
)
graph.add_edge(START, "unreliable")
graph.add_edge("unreliable", END)

app = graph.compile()
result = app.invoke({"attempt": 0, "result": ""})
print("Final:", result)



# Retry Policy ke important paramerers 

RetryPolicy(
    max_attempts=5,           # kitni baar tak try kare
    initial_interval=1.0,     # pehli retry se pehle kitna ruke (seconds)
    backoff_factor=2.0,       # har retry pe wait time double ho jaaye
    max_interval=60.0         # max kitna ruk sakta hai retries ke beech
)



# Combo try expect and retry policy dono ek sath use karo :-


def smart_node(state: MyState) -> MyState:
    try:
        # risky operation
        result = call_external_api(state["query"])
        state["result"] = result
    except ValueError as e:
        # Ye retry se theek nahi hoga (permanent problem), isliye graceful fallback
        state["result"] = "Invalid input diya gaya, kripya sahi format mein bhejo"
    return state

# Sirf network/timeout jaisi errors ke liye retry lagao
graph.add_node("smart", smart_node, retry=RetryPolicy(max_attempts=3))
