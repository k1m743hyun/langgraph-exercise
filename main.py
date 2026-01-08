from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
from langchain_core.runnables import RunnableConfig
from functools import wraps
import time
import asyncio

class State(TypedDict):
    counter: int
    message: str

# 노드 정의
def increment(state: State) -> dict:
    """
    카운터를 증가시키는 노드
    """
    return {
        "counter": state["counter"] + 1,
        "message": f"카운터 증가: {state['counter']} -> {state['counter'] + 1}"
    }

def double(state: State) -> dict:
    '''
    카운터를 두 배로 만드는 노드
    '''
    return {
        "counter": state["counter"] * 2,
        "message": f"카운터 두 배: {state['counter']} -> {state['counter'] * 2}"
    }

# 그래프 생성
graph = StateGraph(State)

# 노드 추가
graph.add_node("increment", increment)
graph.add_node("double", double)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "increment")      # 시작 -> increment
graph.add_edge("increment", "double")   # increment -> double
graph.add_edge("double", END)           # double -> 종료

compiled_graph = graph.compile()

initial_state = {
    "counter": 1,
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"카운터: {result["counter"]}")
print(f"메세지: {result["message"]}")