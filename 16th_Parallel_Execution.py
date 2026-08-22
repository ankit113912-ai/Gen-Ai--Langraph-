#  Parallel Node code :- 

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
import time

class MyState(TypedDict):
    results: Annotated[list, operator.add]   # 🔑 Reducer zaroori hai parallel ke liye!

def check_weather(state: MyState) -> MyState:
    print("🌤️ Weather check ho raha hai...")
    time.sleep(2)   # simulate karte hain ki isme time lagta hai
    return {"results": ["Weather: 32°C, dhoop"]}

def check_news(state: MyState) -> MyState:
    print("📰 News check ho raha hai...")
    time.sleep(2)
    return {"results": ["News: Aaj koi badi khabar nahi"]}

def check_stocks(state: MyState) -> MyState:
    print("📈 Stocks check ho raha hai...")
    time.sleep(2)
    return {"results": ["Stocks: Sensex 500 points upar"]}

graph = StateGraph(MyState)
graph.add_node("weather", check_weather)
graph.add_node("news", check_news)
graph.add_node("stocks", check_stocks)

# 🔑 Yahi hai PARALLEL ka jaadu — START se teeno ko edge do!
graph.add_edge(START, "weather")
graph.add_edge(START, "news")
graph.add_edge(START, "stocks")

# Teeno khatam hone ke baad END pe jao
graph.add_edge("weather", END)
graph.add_edge("news", END)
graph.add_edge("stocks", END)

app = graph.compile()

start_time = time.time()
result = app.invoke({"results": []})
print(f"\nTotal time: {time.time() - start_time:.2f} seconds")
print("Results:", result["results"])