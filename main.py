from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
from langchain_core.runnables import RunnableConfig
import asyncio

class State(TypedDict):
    input: str
    output: str
    config_used: Dict

def configurable_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    '''
    구성 가능한 노드
    런타임에 동작을 조정할 수 있음

    Args:
        state: 현재 상태
        config: 런타임 구성
    '''
    # 구성에서 값 가져오기
    model_name = config.get("configurable", {}).get("model", "default")
    temperature = config.get("configurable",  {}).get("temperature", 0.7)
    max_retries = config.get("configurable", {}).get("max_retries", 3)

    print(f"Using model: {model_name}, temperature: {temperature}")

    # 구성에 따른 처리
    result = None
    for attempt in range(max_retries):
        try:
            result = process_with_model(
                state["input"],
                model=model_name,
                temperature=temperature
            )
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                result = "Failed after all retries"
    
    return {
        "output":  result,
        "config_used": {
            "model": model_name,
            "temperature": temperature,
            "retries": max_retries
        }
    }

def process_with_model(input_data, model, temperature):
    '''모델을 사용한 처리 (시뮬레이션)'''
    return f"Processed with {model} at temperature {temperature}: {input_data}"

graph = StateGraph(State)
graph.add_node("node", configurable_node)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
    "input": "hello",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"결과: {result["output"]}")
print(f"구성: {result["config_used"]}")