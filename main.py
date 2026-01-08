from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Union, List

class ComplexRoutingState(TypedDict):
    priority: int
    data_size: int
    processing_mode: str
    routes_taken: list

# 노드 정의
def initial_assessment(state: ComplexRoutingState) -> dict:
    """
    초기 평가 및 라우팅 준비 노드
    """
    # 복합 조건 평가
    if state["priority"] >= 8 and state["data_size"] < 1000:
        mode = "express"
    elif state["priority"] >= 5 and state["data_size"] < 10000:
        mode = "standard"
    elif state["data_size"] > 100000:
        mode = "batch"
    else:
        mode = "economy"

    return {
        "processing_mode": mode,
        "routes_taken": ["assessment"],
    }

def express_processing(state: ComplexRoutingState) -> dict:
    '''
    고속 처리 노드
    '''
    return {
        "routes_taken": state["routes_taken"] + ["express"],
        "processing_mode": "express_complete",
    }

def standard_processing(state: ComplexRoutingState) -> dict:
    '''
    표준 처리 노드
    '''
    return {
        "routes_taken": state["routes_taken"] + ["standard"],
        "processing_mode": "standard_complete",
    }

def batch_processing(state: ComplexRoutingState) -> dict:
    '''
    배치 처리 노드
    '''
    return {
        "routes_taken": state["routes_taken"] + ["batch"],
        "processing_mode": "batch_complete",
    }

def economy_processing(state: ComplexRoutingState) -> dict:
    '''
    경제 처리 노드
    '''
    return {
        "routes_taken": state["routes_taken"] + ["economy"],
        "processing_mode": "economy_complete",
    }

# 복잡한 라우팅 로직
def complex_router(state: ComplexRoutingState) -> Union[str, List[str]]:
    '''
    복잡한 라우팅 로직
    단일 노드 또는 여러 노드로 라우팅 가능
    '''
    mode = state["processing_mode"]

    # 단일 라우팅
    if mode in ["express", "standard", "batch", "economy"]:
        return mode
    
    # 다중 라우팅 (병렬 실행)
    if state["priority"] == 10:
        return ["express", "standard"] # 두 경로 모두 실행

    # 기본값
    return state['sentiment']

# 그래프 생성
graph = StateGraph(ComplexRoutingState)

# 노드 추가
graph.add_node("assessment", initial_assessment)
graph.add_node("express", express_processing)
graph.add_node("standard", standard_processing)
graph.add_node("batch", batch_processing)
graph.add_node("economy", economy_processing)
graph.add_node("router", complex_router)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "assessment")
graph.add_conditional_edges(
    "assessment",
    complex_router,
    {
        "express": "express",
        "standard": "standard",
        "batch": "batch",
        "economy": "economy",
    }
)
for node in ["express", "standard", "batch", "economy"]:
    graph.add_edge(node, END)

compiled_graph = graph.compile()

initial_state = {
    "priority": 10,
    "data_size": 20,
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"처리 방법: {result["processing_mode"]}")
print(f"처리 과정: {result["routes_taken"]}")