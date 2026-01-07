from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated
from datetime import datetime
from operator import add
import asyncio

class State(TypedDict):
    input: str
    output: str
    additional_data: list

async def async_node(state: State) -> Dict[str, Any]:
    '''
    비동기 노드 - I/O 작업에 효율적
    동시에 여러 작업을 처리할 수 있음
    '''
    # 비동기 작업 수행
    result = await perform_async_operation(state["input"])

    # 여러 비동기 작업 동시 실행
    results = await asyncio.gather(
        fetch_data_1(),
        fetch_data_2(),
        fetch_data_3(),
    )

    return {
        "output": result,
        "additional_data": results
    }

async def perform_async_operation(data):
    '''비동기 작업'''
    await asyncio.sleep(0.1) # 시뮬레이션
    return f"Async: result: {data}"

async def fetch_data_1():
    await asyncio.sleep(0.05)
    return "data_1"

async def fetch_data_2():
    await asyncio.sleep(0.05)
    return "data_2"

async def fetch_data_3():
    await asyncio.sleep(0.05)
    return "data_3"

graph = StateGraph(State)
graph.add_node("node", async_node)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
        "input": "안녕하세요",
}

result = asyncio.run(compiled_graph.ainvoke(initial_state))
print("\n=== 최종 결과 ===")
print(f"결과: {result['output']}")