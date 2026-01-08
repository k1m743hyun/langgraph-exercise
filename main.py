from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class ControlFlowState(TypedDict):
    value: int
    path_taken: str
    result: str

# 노드 정의
def evaluate(state: ControlFlowState) -> dict:
    """
    값을 평가하는 노드
    """
    value = state["value"]

    if value > 100:
        path = "high"
    elif value > 50:
        path = "medium"
    else:
        path = "low"

    return {
        "path_taken": path,
        "result": f"Value {value} is {path}",
    }

def handle_high(state: ControlFlowState) -> dict:
    '''
    높은 값 처리 노드
    '''
    return {
        "result": f"HIGH: Special handling for {state['value']}",
    }

def handle_medium(state: ControlFlowState) -> dict:
    '''
    중간 값 처리 노드
    '''
    return {
        "result": f"MEDIUM: Standard handling for {state['value']}",
    }

def handle_low(state: ControlFlowState) -> dict:
    '''낮은 값 처리 노드'''
    return {
        "result": f"LOW: Basic handling for {state['value']}"
    }

def route_by_value(state: ControlFlowState) -> Literal["high", "medium", "low"]:
    '''상태에 따라 경로 결정'''
    return state["path_taken"]

# 그래프 생성
graph = StateGraph(ControlFlowState)

# 노드 추가
graph.add_node("evaluate", evaluate)
graph.add_node("handle_high", handle_high)
graph.add_node("handle_medium", handle_medium)
graph.add_node("handle_low", handle_low)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "evaluate")
graph.add_conditional_edges(
    "evaluate",
    route_by_value,
    {
        "high": "handle_high",
        "medium": "handle_medium",
        "low": "handle_low"
    }
)
graph.add_edge("handle_high", END)
graph.add_edge("handle_medium", END)
graph.add_edge("handle_low", END)

compiled_graph = graph.compile()

initial_state = {
    "value": 10,
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"최종 데이터: {result["value"]}")
print(f"완료된 단계: {result["path_taken"]}")
print(f"상태: {result["result"]}")