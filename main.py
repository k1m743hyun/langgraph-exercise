from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated, List
from operator import add
from IPython.display import Image, display

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
initial_state = {
    "messages": [HumanMessage(content="Hello!")],
    "context": ""
}

# 서브그래프 실행
result = subgraph.invoke(initial_state)

# 결과 확인
for message in result["messages"]:
    print(f"Message: {message.content}")