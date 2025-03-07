from langgraph.pregel.remote import RemoteGraph
from langgraph_sdk import get_sync_client
url = "http://127.0.0.1:2024"
graph_name = "simple-devops-agent"
sync_client = get_sync_client(url=url)
remote_graph = RemoteGraph(graph_name, url=url)

# create a thread (or use an existing thread instead)
thread = sync_client.threads.create()

# invoke the graph with the thread config
config = {"configurable": {"thread_id": thread["thread_id"]}}
result = remote_graph.invoke({
    "messages": [{"role": "user", "content": "what's the weather in sf"}]
}, config=config)

# verify that the state was persisted to the thread
thread_state = remote_graph.get_state(config)
print(thread_state)