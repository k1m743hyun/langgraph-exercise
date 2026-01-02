from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated, List
from operator import add

class BasicState(TypedDict):
    # 단순 값들 - 덮어쓰기 방식
    current_step: str
    user_id: str

    # 누적되는 값들 - 추가 방식
    messages: Annotated[List[str], add]
    processing_log: Annotated[List[str], add]

# 노드 1 실행
def node1(state: BasicState):
    return {
        "messages": ["어떻게 도와드릴까요?"],
        "processing_log": ["사용 인사 감지"],
    }

# 노드 2 실행
def node2(state: BasicState):
    return {
        "messages": ["무엇을 도와드릴까요?"],
        "processing_log": ["응답 생성 완료"],
    }

# 그래프 구성
graph = StateGraph(BasicState)
graph.add_node("node1", node1)
graph.add_node("node2", node2)

# 연결: START -> first -> second -> END
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# 실행
state = {
    "messages": ["안녕하세요"],
    "processing_log": ["시작"],
}

app = graph.compile()
result = app.invoke(state)
print(f"최종 결과: {result}")