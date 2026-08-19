from langgraph.graph import StateGraph, END
from typing import TypedDict

# Step 1: State define karo (hamara "bag" kaisa dikhega)
class MyState(TypedDict):
    message: str

# Step 2: Node banao (ek kaam karne wala function)
def hello_node(state: MyState) -> MyState:
    print("Node chal raha hai!")
    state["message"] = "Namaste duniya! 🙏"
    return state

# Step 3: Graph banao aur node add karo
graph = StateGraph(MyState)
graph.add_node("hello", hello_node)

# Step 4: Bataao graph kahan se start hoga aur kahan khatam
graph.set_entry_point("hello")
graph.add_edge("hello", END)

# Step 5: Graph ko "compile" karo (ready karo chalne ke liye)
app = graph.compile()

# Step 6: Graph ko chalao!
result = app.invoke({"message": ""})
print(result)



"""  


 Har LangGraph mein ye 5 steps hamesha hote hain:

1   State define karo
2   Node(s) banao
3   Graph banao + nodes add karo
4   Entry point aur Edges set karo
5   Compile karke invoke karo          


"""
