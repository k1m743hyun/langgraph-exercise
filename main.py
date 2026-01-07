from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated
from datetime import datetime
from operator import add

class State(TypedDict):
    input: str
    output: str

def sync_node(state: State) -> Dict[str, Any]:
    '''
    동기 노드 - 일반적인 노드 타입
    순차적으로 실행되며 결과를 즉시 반환
    '''
    # 동기 작업 수행
    result = perform_sync_operation(state["input"])

    return {
        "output": result,
    }

def perform_sync_operation(data):
    '''동기 작업'''
    import time
    time.sleep(0.1) # 시뮬레이션
    return f"Sync: result: {data}"

graph = StateGraph(State)
graph.add_node("node", sync_node)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
        "input": "안녕하세요",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"결과: {result['output']}")