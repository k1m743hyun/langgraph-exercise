from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State: 숫자 하나만 저장
class ConditionalState(TypedDict):
    count:int
    message: str

# Node 1: 카운트 증가
def increment(state):
    new_count = state['count'] + 1
    print(f"카운트 증가: {state['count']} -> {new_count}")
    return {"count": new_count}

# Node 2: 완료 메세지
def finish(state):
    print("카운팅 완료!")
    return {"message": "완료되었습니다!"}

# 조건 함수: 다음에 어디로 갈지 결정
def should_continue(state):
    if state['count'] < 3:
        return "continue"
    else:
        return "finish"

# Graph: 시작 -> 카운트 -> 끝
graph = StateGraph(ConditionalState)

# 노드 추가
graph.add_node("increment", increment)
graph.add_node("finish", finish)

# 엣지 연결
graph.add_edge(START, "increment")
graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue": "increment",
        "finish": "finish"
    }
)
graph.add_edge("finish", END)

# 실행
app = graph.compile()
result = app.invoke({"count": 0, "message": ""})
print(f"최종 결과: {result}")