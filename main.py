from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
from langchain_core.runnables import RunnableConfig
from functools import wraps
import time
import asyncio

class WorkflowState(TypedDict):
    data: str
    steps_completed: list
    status: str

# 노드 정의
def step1(state: WorkflowState) -> dict:
    """
    첫 번째 처리 노드
    """
    return {
        "data": state["data"] + " -> Step 1",
        "steps_completed": state.get("steps_completed", []) + ["step1"],
        "status": "step1_complete",
    }

def step2(state: WorkflowState) -> dict:
    '''
    두 번째 처리 노드
    '''
    return {
        "data": state["data"] + " -> Step 2",
        "steps_completed": state.get("steps_completed", []) + ["step2"],
        "status": "step2_complete",
    }

def step3(state: WorkflowState) -> dict:
    '''
    세 번째 처리 노드
    '''
    return {
        "data": state["data"] + " -> Step 3",
        "steps_completed": state.get("steps_completed", []) + ["step3"],
        "status": "step3_complete",
    }

# 그래프 생성
graph = StateGraph(WorkflowState)

# 노드 추가
graph.add_node("step1", step1)
graph.add_node("step2", step2)
graph.add_node("step3", step3)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "step1")     # 시작 -> step1
graph.add_edge("step1", "step2")   # step1 -> step2
graph.add_edge("step2", "step3")   # step2 -> step3
graph.add_edge("step3", END)       # step3 -> 종료

compiled_graph = graph.compile()

initial_state = {
    "data": "Start",
    "steps_completed": [],
    "status": "initialized",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"최종 데이터: {result["data"]}")
print(f"완료된 단계: {result["steps_completed"]}")
print(f"상태: {result["status"]}")