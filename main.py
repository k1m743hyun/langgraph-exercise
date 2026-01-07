from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, Any, Annotated, Optional
from datetime import datetime
from operator import add
from langchain_core.runnables import RunnableConfig
import asyncio

class State(TypedDict):
    input: str
    output: str
    processor_type: str
    total_processed: int
    from_cache: bool

class DataProcessorNode:
    '''
    클래스 기반 노드
    상태를 가지고 복잡한 로직을 구현할 때 유용
    '''

    def __init__(self, processor_type: str = "standard"):
        self.processor_type = processor_type
        self.processing_count = 0
        self.cache = {}
    
    def __call__(self, state: State) -> Dict[str, Any]:
        '''
        노드 실행 메서드
        클래스 인스턴스를 호출 가능하게 만듦
        '''
        input_data = state["input"]

        # 캐시 확인
        cache_key = f"{self.processor_type}:{input_data}"
        if cache_key in self.cache:
            print(f"Cache hit for {cache_key}")
            return {"output": self.cache[cache_key], "from_cache": True}
        
        # 처리 수행
        if self.processor_type == "standard":
            result = self._standard_process(input_data)
        elif self.processor_type == "advanced":
            result = self._advanced_process(input_data)
        else:
            result = self._default_process(input_data)
        
        # 통계 업데이트
        self.processing_count += 1

        return {
            "output": result,
            "processor_type": self.processor_type,
            "total_processed": self.processing_count,
            "from_cache": False,
        }
    
    def _standard_process(self, data):
        return f"Standard processed: {data}"
    
    def _advanced_process(self, data):
        return f"Advanced processed: {data}"

    def _default_process(self, data):
        return f"Default processed: {data}"

processor = DataProcessorNode(processor_type="advanced")

graph = StateGraph(State)
graph.add_node("node", processor)

graph.add_edge(START, "node")
graph.add_edge("node", END)

compiled_graph = graph.compile()

initial_state = {
    "input": "hello",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"결과: {result["output"]}")
print(f"타입: {result["processor_type"]}")
print(f"횟수: {result["total_processed"]}")
print(f"캐시: {result["from_cache"]}")