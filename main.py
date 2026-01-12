from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# 서브 그래프 정의
class SubgraphState(TypedDict):
    foo: str    # 부모 그래프와 공유하는 키
    bar: str    # 서브그래프에서만 사용하는 프라이빗 키

def subgraph_node_1(state: SubgraphState):
    return {"bar": "bar"}

def subgraph_node_2(state: SubgraphState):
    # 프라이빗 키(bar)를 사용하여 공유 키(foo)를 업데이트
    return {"foo": state["foo"] + state["bar"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()

# 부모 그래프 정의
class ParentState(TypedDict):
    foo: str

def node_1(state: ParentState):
    return {"foo": "hi! " + state["foo"]}

builder = StateGraph(ParentState)

# 노드 추가
builder.add_node("node_1", node_1)
builder.add_node("node_2", subgraph)    # 컴파일된 서브 그래프를 직접 추가

# 엣지 연결
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")

# 실행
graph = builder.compile()
for chunk in graph.stream({"foo": "foo"}):
    print(chunk)