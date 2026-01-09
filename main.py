from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Optional
from datetime import datetime
from operator import add

class WorkflowState(TypedDict):
    input_data: str
    processing_stage: str
    results: Annotated[list, add]
    error: Optional[str]
    metadata: dict

# 노드 함수들 정의
def validate_input(state: WorkflowState) -> dict:
    """
    입력 검증 노드
    """
    input_data = state['input_data']

    if not input_data:
        return {
            "error": "입력 데이터가 비었습니다.",
            "processing_stage": "validation_failed",
        }
    
    if len(input_data) > 1000:
        return {
            "error": "입력 데이터가 너무 깁니다.",
            "processing_stage": "validation_failed",
        }
    
    return {
        "processing_stage": "validated",
        "results": ["입력 검증 완료"],
    }

def process_data(state: WorkflowState) -> dict:
    '''
    데이터 처리 노드
    '''
    # 실제 처리 로직
    processed = state["input_data"].upper()
    
    return {
        "processing_stage": "processed",
        "results": [f"처리 결과: {processed}"],
        "metadata": {
            **state.get("metadata", {}),
            "processed_at": datetime.now().isoformat(),
        }
    }

def generate_output(state: WorkflowState) -> dict:
    '''
    출력 생성 노드
    '''
    final_output = "\n".join(state["results"])

    return {
        "processing_stage": "completed",
        "results": [f"최종 출력: {final_output}"],
        "metadata": {
            **state["metadata"],
            "completed_at": datetime.now().isoformat(),
        }
    }

def handle_error(state: WorkflowState) -> dict:
    '''
    에러 처리 노드
    '''
    return {
        "processing_stage": "error_handled",
        "results": [f"에러 처리: {state['error']}"],
    }

# 라우팅 함수
def route_after_validation(state: WorkflowState) -> str:
    '''
    검증 후 라우팅 노드
    '''
    if state.get("error"):
        return "error"
    
    return "process"

# 그래프 구성
graph = StateGraph(WorkflowState)

# 노드 추가
graph.add_node("validate", validate_input)
graph.add_node("process", process_data)
graph.add_node("output", generate_output)
graph.add_node("error_handler", handle_error)
graph.add_node("route_after_validation", route_after_validation)

# 엣지 추가
graph.add_edge(START, "validate")
graph.add_conditional_edges(
    "validate",
    route_after_validation,
    {
        "process": "process",
        "error": "error_handler",
    }
)
graph.add_edge("process", "output")
graph.add_edge("output", END)
graph.add_edge("error_handler", END)

compiled_graph = graph.compile()

initial_state = {
    "input_data": "",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"처리 과정: {result['processing_stage']}")
print(f"결과: {result['results']}")
print(f"에러: {result.get("error")}")
print(f"메타데이터: {result.get('metadata')}")