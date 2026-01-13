from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from typing import TypedDict, Annotated, List, Optional, Literal
from operator import add

class SubgraphState(TypedDict):
    '''서브그래프의 상태를 정의하는 클래스'''
    messages: Annotated[List[AnyMessage], add]
    context: str

def process_node(state: SubgraphState):
    '''입력 메세지를 처리하는 노드'''
    current_message = state["messages"][-1]
    # 메세지 처리 로직
    processed_result = f"Processed: {current_message.content}"
    return {"context": processed_result}

def respond_node(state: SubgraphState):
    '''응답을 생성하는 노드'''
    context = state["context"]
    # 응답 생성 로직
    response  = AIMessage(content=f"Response based on: {context}")
    return {"messages": [response]}

# 서브그래프 인스턴스 생성
subgraph_builder = StateGraph(SubgraphState)

# 노드 추가
subgraph_builder.add_node("process", process_node)
subgraph_builder.add_node("respond", respond_node)

# 엣지 추가
subgraph_builder.add_edge(START, "process")
subgraph_builder.add_edge("process", "respond")
subgraph_builder.add_edge("respond", END)

# 서브그래프 컴파일
subgraph = subgraph_builder.compile()

# subgraph_image = subgraph.get_graph().draw_mermaid_png()
# display(Image(subgraph_image))

# 초기 상태 설정
# initial_state = {
#     "messages": [HumanMessage(content="Hello!")],
#     "context": ""
# }

# 서브그래프 실행
# result = subgraph.invoke(initial_state)

# 결과 확인
# for message in result["messages"]:
#     print(f"Message: {message.content}")

class MainState(TypedDict):
    messages: Annotated[List[AnyMessage], add]  # 메세지 히스토리
    context: str                                # 컨텍스트 정보
    subgraph_result: Optional[str]
    processing_state: str

def preprocessing(state: MainState) -> MainState:
    '''데이터 전처리를 수행하는 노드'''
    return {
        "context": f"Context from: {state['messages'][-1].content}",
        "processing_state": "preprocessing_complete"
    }

def postprocessing(state: MainState) -> MainState:
    '''서브그래프 실행 결과를 후처리하는 노드'''
    context = state.get("context", "")
    return {
        "subgraph_result": f"Final result based on context: {context}",
        "processing_state": "complete"
    }

def route_next(state: MainState) -> Literal["postprocessing", "reprocess"]:
    '''다음 단계를 결정하는 라우터'''
    if state['processing_state'] == "preprocessing_complete":
        return "postprocessing"
    return "reprocess"

# 메인 그래프 구성
main_graph = StateGraph(MainState)

# 노드 추가
main_graph.add_node("preprocessing", preprocessing)
main_graph.add_node("subgraph", subgraph) # 기존 서브 그래프
main_graph.add_node("postprocessing", postprocessing)

# 엣지 추가
main_graph.add_edge(START, "preprocessing")
main_graph.add_edge("preprocessing", "subgraph")
main_graph.add_conditional_edges(
    "subgraph",
    route_next,
    {
        "postprocessing": "postprocessing",
        "reprocess": "preprocessing"
    }
)
main_graph.add_edge("postprocessing", END)

# 그래프 컴파일
compiled_main_graph = main_graph.compile()

# 그래프 시각화 (ASCII)
#print(compiled_main_graph.get_graph(xray=True).draw_ascii())

initial_state = {
    "messages": [HumanMessage(content="Hello!")],
    "processing_state": "started"
}

try:
    result = compiled_main_graph.invoke(initial_state)
    print("실행 결과:")
    print(f"처리 상태: {result['processing_state']}")
    print(f"최종 결과: {result['subgraph_result']}")
except Exception as e:
    print(f"그래프 실행 실패: {e}")