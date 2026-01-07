from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
from langchain_core.runnables import RunnableConfig
from functools import wraps
import time
import asyncio

class State(TypedDict):
    input: str
    output: str
    processor_type: str
    total_processed: int
    from_cache: bool

def timing_decorator(func):
    '''노드 실행 시간 측정 데코레이터'''
    @wraps(func)
    def wrapper(state):
        start_time = time.time()
        result = func(state)
        execution_time = time.time() - start_time

        # 실행 시간 추가
        if isinstance(result, dict):
            result["execution_time"] = execution_time

        print(f"{func.__name__} executed in {execution_time:.3f} seconds")
        return result
    
    return wrapper

def error_handling_decorator(func):
    '''에러 처리 데코레이터'''
    @wraps(func)
    def wrapper(state):
        try:
            return func(state)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return {
                "error": str(e),
                "error_node": func.__name__,
                "status": "failed",
            }
    
    return wrapper

@timing_decorator
@error_handling_decorator
def decorated_node(state: State) -> Dict[str, Any]:
    '''
    데코레이터가 적용된 노드
    자동으로 시간 측정과 에러 처리가 됨
    '''
    # 의도적으로 느린 작업
    time.sleep(0.1)

    # 비즈니스 로직
    result = state["input"].upper() if isinstance(state["input"], str) else str(state["input"])

    return {"output":  result}

graph = StateGraph(State)
graph.add_node("node", decorated_node)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
    "input": "hello",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"결과: {result["output"]}")