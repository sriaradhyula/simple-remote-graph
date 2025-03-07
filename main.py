from langgraph_sdk import get_sync_client
from langgraph.graph import StateGraph, MessagesState, START
from typing import TypedDict
from langgraph.pregel.remote import RemoteGraph

url = "http://127.0.0.1:2024"
graph_name = "simple-devops-agent"
remote_graph = RemoteGraph(graph_name, url=url)

# define parent graph
builder = StateGraph(MessagesState)
# add remote graph directly as a node
builder.add_node("child", remote_graph)
builder.add_edge(START, "child")
graph = builder.compile()

# invoke the graph
async def invoke_graph():
    result = await graph.ainvoke({
        "messages": [{"role": "user", "content": "what's the weather in sf"}]
    })
    print(result)

    # stream outputs from the graph
    async for chunk in graph.astream({
        "messages": [{"role": "user", "content": "what's the weather in la"}]
    }):
        print(chunk)

import asyncio
asyncio.run(invoke_graph())