
from langgraph.graph import StateGraph, END
from typing import TypedDict
import random

class MyState(TypedDict):
    target: int      # sahi number jo dhundna hai
    guess: int        # abhi ka guess
    tries: int         # kitni baar try kiya

# Node: Guess karo
def guess_node(state: MyState) -> MyState:
    state["guess"] = random.randint(1, 10)
    state["tries"] += 1
    print(f"Try {state['tries']}: Guess kiya {state['guess']}")
    return state

# Decision function: Sahi mila ya nahi?
def check_karo(state: MyState) -> str:
    if state["guess"] == state["target"]:
        return "sahi_mila"
    else:
        return "phir_try_karo"

# Graph banate hain
graph = StateGraph(MyState)
graph.add_node("guess", guess_node)

graph.set_entry_point("guess")

# 🔑 Yahi hai LOOP ka jaadu
graph.add_conditional_edges(
    "guess",
    check_karo,
    {
        "sahi_mila": END,          # agar sahi mila, khatam karo
        "phir_try_karo": "guess"   # 🔁 agar galat, WAPAS "guess" node pe jao!
    }
)

app = graph.compile()

result = app.invoke({"target": 7, "guess": 0, "tries": 0})
print("\nFinal Result:", result)