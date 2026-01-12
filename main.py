from langchain_core.messages import AnyMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated

# 서브 그래프 상태 - 다른 스키마
class SubgraphMessageState(TypedDict):
    subgraph_message: Annotated[list[AnyMessage], add_messages]

def call_model(state: SubgraphMessageState):
    response = model.invoke(state["subgraph_message"])
    return {"subgraph_message": response}

subgraph_builder = StateGraph(SubgraphMessageState)
subgraph_builder.add_node("call_model_from_subgraph", call_model)
subgraph_builder.add_edge(START, "call_model_from_subgraph")
subgraph = subgraph_builder.compile()

# 부모 그래프 - 상태 변환 함수 정의
def call_subgraph(state: MessagesState):
    # 부모 상태 -> 서브그래프 상태로 변환
    response = subgraph.invoke({"subgraph_message": state["messages"]})
    # 서브그래프 상태 -> 부모 상태로 변환하여 변환
    return {"messages": response["subgraph_messages"]}

builder = StateGraph(MessagesState)

# 노드 추가
builder.add_node("subgraph_node", call_subgraph)

# 엣지 연결
builder.add_edge(START, "subgraph_node")

# 실행
graph = builder.compile()

graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})