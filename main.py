from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any
from datetime import datetime

class CalculationState(TypedDict):
    numbers: list[float]
    operation: str
    result: float
    history: list[dict]

def calculator_node(state: CalculationState) -> Dict[str, Any]:
    '''
    비즈니스 로직 실행 노드
    수학 연산을 수행하고 결과를 저장
    '''
    numbers = state["numbers"]
    operation = state["operation"]

    # 연산 수행
    if operation == "sum":
        result = sum(numbers)
    elif operation == "multiply":
        result = 1
        for num in numbers:
            result *= num
    elif operation == "average":
        result = sum(numbers) / len(numbers) if numbers else 0
    else:
        raise ValueError(f"Unknown operation: {operation}")

    # 히스토리 업데이트
    history_entry = {
        "operation": operation,
        "inputs": numbers,
        "result": result,
        "timestamp": datetime.now().isoformat(),
    }

    return {
        "result": result,
        "history": [history_entry], # 리듀서가 있다면 누적됨
    }