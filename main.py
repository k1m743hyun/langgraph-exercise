from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from operator import add

class State(TypedDict):
    message_count: int                          # 기본 리듀서 (덮어쓰기)
    conversation: Annotated[list[str], add]     # add 리듀서 (리스트 연결)

# 노드 1 실행
def node1(state: State) -> State:
    '''
    첫 번째 노드: 대화 시작
    - message_count를 1로 설정
    - conversation에 인사말 추가
    '''
    print(f"Node 1 - 현재 대화: {state.get('conversation', [])}")
    return {
        "message_count": 1,
        "conversation": ["안녕하세요!"],
    }

# 노드 2 실행
def node2(state: State) -> State:
    '''
    두 번째 노드: 대화 이어가기
    - message_count는 업데이트 하지 않음 (이전 값 유지)
    - conversation에 새 메세지 추가 (add 리듀서로 누적)
    '''
    print(f"Node 2 - 현재 대화: {state['conversation']}")
    return {
        "conversation": ["어떻게 도와드릴까요?"],
    }

# 그래프 구성
graph = StateGraph(State)
graph.add_node("node1", node1)
graph.add_node("node2", node2)

# 연결: START -> first -> second -> END
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

compiled_graph = graph.compile()

# 실행
initial_tate = {
    "message_count": 0,
    "conversation": [],
}
result = compiled_graph.invoke(initial_tate)
print("\n=== 최종 결과 ===")
print(f"메세지 수: {result['message_count']}")
print(f"대화 내용: {result['conversation']}")