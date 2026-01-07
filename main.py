from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any

# 상태 정의
class State(TypedDict):
    counter: int
    messages: list
    status: str

# 기본 노드 함수
def increment(state: State) -> Dict[str, Any]:
    '''
    가장 간단한 형태의 노드

    Args:
        state: 현재 그래프 상태
    
    Returns:
        업데이트할 상태 딕셔너리
    '''
    # 현재 카운터 값 가져오기
    current_counter = state["counter"]

    # 비즈니스 로직 수행
    new_counter = current_counter + 1

    # 상태 업데이트 반환
    return {
        "counter": new_counter,
        "messages": [f"카운터가 {new_counter}로 증가했습니다."],
        "status": "incremented",
    }

# 그래프 생성 및 노드 추가
graph = StateGraph(state)
graph.add_node("increment", increment) # 노드 이름과 함수 매핑