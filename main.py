from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. State: 카운터를 저장하는 상자
class CountState(TypedDict):
    count: int

# 2. Node: 카운터를 증가시키는 함수
def increment(state):
    print(f"현재 카운트: {state['count']}")
    new_count = state['count'] + 1
    print(f"새로운 카운트: {new_count}")
    return {"count": new_count}

# 3. Edge: 노드를 연결하는 그래프
graph = StateGraph(CountState)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_edge("increment", END)

# 실행해보기
app = graph.compile()
result = app.invoke({"count": 0})
print(f"최종 결과: {result}")