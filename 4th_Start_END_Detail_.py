""" from langgraph.graph import StateGraph, START, END

graph = StateGraph(MyState)
graph.add_node("padho", padho_node)
graph.add_node("socho", socho_node)              

# Purana tareeka:
# graph.set_entry_point("padho")

# Naya tareeka (better!):
graph.add_edge(START, "padho")   # START se "padho" tak edge banao
graph.add_edge("padho", "socho")
graph.add_edge("socho", END)


# whats the difference  :- 

#purana

graph.set_entry_point("padho")

#NAya 

graph.add_edge(START,"padho")
"""