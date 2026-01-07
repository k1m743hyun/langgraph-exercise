from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated
from datetime import datetime
from operator import add
import asyncio

class State(TypedDict):
    mode: str
    input: str
    result: dict
    execution_time: str
    mode_used: str

def conditional_node(state: State) -> Dict[str, Any]:
    '''
    조건부 노드 - 상태에 따라 다른 처리 수행
    '''
    mode = state.get("mode", "default")

    if mode == "fast":
        # 빠른 처리
        result = quick_process(state)
        execution_time = "fast"
    elif mode == "thorough":
        # 정밀 처리
        result = thorough_process(state)
        execution_time = "slow"
    else:
        # 기본 처리
        result = default_process(state)
        execution_time = "normal"

    return {
        "result": result,
        "execution_time": execution_time,
        "mode_used": mode
    }

def quick_process(state):
    return {
        "status": "quick",
        "data": state.get("input", "")[:10],
    }

def thorough_process(state):
    return {
        "status": "thorough",
        "data": analyze_deeply(state.get("input", "")),
    }

def default_process(state):
    return {
        "status": "default",
        "data": state.get("input", ""),
    }

def analyze_deeply(data):
    # 심층 분석 로직
    return f"Deeply analyzed: {data}"

graph = StateGraph(State)
graph.add_node("node", conditional_node)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
    "mode": "fast",
    "input": "안녕하세요",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"결과: {result["result"]}")