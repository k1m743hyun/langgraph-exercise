from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add

class StateTransferExample(TypedDict):
    '''상태 전달 예시'''
    accumulator: Annotated[list, add]
    current_value: int
    transformations: list

# 노드 정의
def transform_add_10(state: StateTransferExample) -> dict:
    """
    값에 10을 더하고 변환 기록 노드
    """
    new_value = state["current_value"] + 10
    return {
        "current_value": new_value,
        "accumulator": [new_value],
        "transformations": state.get("transformations", []) + ["add_10"],
    }

def transform_multiply_2(state: StateTransferExample) -> dict:
    '''
    값을 2배로 만들고 변환 기록 노드
    '''
    new_value = state["current_value"] * 2
    return {
        "current_value": new_value,
        "accumulator": [new_value],
        "transformations": state.get("transformations", []) + ["multiply_2"],
    }

def transform_square(state: StateTransferExample) -> dict:
    '''
    값을 제곱하고 변환 기록 노드
    '''
    new_value = state["current_value"] ** 2
    return {
        "current_value": new_value,
        "accumulator": [new_value],
        "transformations": state.get("transformations", []) + ["square"],
    }


# 그래프 생성
graph = StateGraph(StateTransferExample)

# 노드 추가
graph.add_node("add_10", transform_add_10)
graph.add_node("multiply_2", transform_multiply_2)
graph.add_node("square", transform_square)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "add_10")
graph.add_edge("add_10", "multiply_2")
graph.add_edge("multiply_2", "square")
graph.add_edge("square", END)

compiled_graph = graph.compile()

initial_state = {
    "accumulator": [],
    "current_value": 5,
    "transformations": [],
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"변환 과정: {result["accumulator"]}")
print(f"완료된 단계: {result["current_value"]}")
print(f"적용된 변환: {result["transformations"]}")