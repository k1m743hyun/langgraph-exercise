from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
import asyncio

class ValidationState(TypedDict):
    input_data: Any
    validation_errors: list[str]
    is_valid: bool

def validation_node(state: ValidationState) -> Dict[str, Any]:
    '''
    검증 노드 - 데이터 유효성 검사
    '''
    input_data = state["input_data"]
    errors = []

    # 다양한 검증 수행
    if not input_data:
        errors.append("입력 데이터가 비어있습니다.")

    if isinstance(input_data, str):
        if len(input_data) < 3:
            errors.append("문자열이 너무 짧습니다. (최소 3자)")
        if len(input_data) > 1000:
            errors.append("문자열이 너무 깁니다. (최대 1000자)")
        if not input_data.isascii():
            errors.append("ASCII 문자만 허용됩니다.")

    elif isinstance(input_data, (int, float)):
        if input_data < 0:
            errors.append("음수는 허용되지 않습니다.")
        if input_data > 1000000:
            errors.append("값이 너무 큽니다. (최대 1,000,000)")
    
    elif isinstance(input_data, list):
        if len(input_data) == 0:
            errors.append("리스트가 비어있습니다.")
        if len(input_data) > 100:
            errors.append("리스트 항목이 너무 많습니다. (최대 100개)")

    # 검증 결과 반환
    return {
        "validation_errors": errors,
        "is_valid": len(errors) == 0,
    }

graph = StateGraph(ValidationState)
graph.add_node("node", validation_node)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
    "input_data": "hello",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"에러: {result["validation_errors"]}")
print(f"결과: {result["is_valid"]}")