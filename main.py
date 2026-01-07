from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any, Annotated
from datetime import datetime
from operator import add

class UpdateState(TypedDict):
    counter: int
    items: Annotated[list, add] # 리듀서 적용
    flag: dict

def update_node(state: UpdateState) -> Dict[str, Any]:
    '''
    상태 업데이트 노드
    다양한 업데이트 패턴 시연
    '''
    # 1. 단순 덮어쓰기
    new_counter = state["counter"] + 1

    # 2. 리스트에 추가 (리듀서 활용)
    new_items = ["new_item"]

    # 3. 딕셔너리 부분 업데이트
    updated_flags = state["flags"].copy()
    updated_flags["processed"] = True
    updated_flags["node_name"] = "update_node"

    return {
        "counter": new_counter, # 덮어쓰기
        "items": new_items,     # 리듀서로 추가
        "flags": updated_flags, # 전체 교체
    }