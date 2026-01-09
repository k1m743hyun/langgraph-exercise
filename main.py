from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State: 숫자 하나만 저장
class CounterState(TypedDict):
    count:int

# Node: 숫자를 1 증가
def count_up(state):
    return {"count": state["count"] + 1}

# Graph: 시작 -> 카운트 -> 끝
graph = StateGraph(CounterState)
graph.add_node("count_up", count_up)
graph.add_edge(START, "count_up")
graph.add_edge("count_up", END)

# 실행
app = graph.compile()
result = app.invoke({"count": 0})
print(f"결과: {result}")