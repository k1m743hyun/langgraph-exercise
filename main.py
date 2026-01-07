from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
from langchain_core.runnables import RunnableConfig
from functools import wraps
import time
import asyncio

class State(TypedDict):
    text: str
    uppercase_text: str
    numbers: list[int]
    scores: list[int]
    total_score: int

def create_processing_node(node_type: str, **kwargs):
    """
    노드 팩토리 함수
    다양한 타입의 노드를 동적으로 생성
    """

    if node_type == "transformer":
        def transformer_node(state: State) -> Dict[str, Any]:
            transform_func = kwargs.get("transform_func", lambda x: x)
            input_field = kwargs.get("input_field", "input")
            output_field = kwargs.get("output_field", "output")

            transformed = transform_func(state[input_field])
            return {output_field: transformed}

        return transformer_node

    elif node_type == "filter":
        def filter_node(state: State) -> Dict[str, Any]:
            filter_func = kwargs.get("filter_func", lambda x: True)
            items_field = kwargs.get("items_field", "items")

            filtered = [item for item in state[items_field] if filter_func(item)]
            return {items_field: filtered}

        return filter_node

    elif node_type == "aggregator":
        def aggregator_node(state: State) -> Dict[str, Any]:
            agg_func = kwargs.get("agg_func", sum)
            values_field = kwargs.get("values_field", "values")
            result_field = kwargs.get("result_field", "result")

            aggregated = agg_func(state[values_field])
            return {result_field: aggregated}

        return aggregator_node

    else:
        raise ValueError(f"Unknown node type: {node_type}")

# 팩토리로 노드 생성
uppercase_node = create_processing_node(
    "transformer",
    transform_func=lambda x: x.upper(),
    input_field="text",
    output_field="uppercase_text"
)

positive_filter = create_processing_node(
    "filter",
    filter_func=lambda x: x > 0,
    items_field="numbers"
)

sum_aggregator = create_processing_node(
    "aggregator",
    agg_func=sum,
    values_field="scores",
    result_field="total_score"
)

graph = StateGraph(State)
graph.add_node("uppercase", uppercase_node)
graph.add_node("filter_positive", positive_filter)
graph.add_node("calculate_sum", sum_aggregator)

graph.add_edge(START, "filter_positive")
graph.add_edge("filter_positive", END)

compiled_graph = graph.compile()

initial_state = {
    #"text": "hello",
    "numbers": [2, -3, 4, 5],
    #"scores": [1, 2, 3, 4],
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
#print(f"결과: {result["uppercase_text"]}")
print(f"결과: {result["numbers"]}")
#print(f"결과: {result["total_score"]}")