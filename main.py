from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State: 더 많은 정보 저장
class TeamworkState(TypedDict):
    number:int
    doubled: int
    message: str

# Node 1: 숫자를 2배로 만들기
def doubler(state):
    double_value = state['number'] * 2
    print(f"2배 계산: {state['number']} X 2 = {double_value}")
    return {"doubled": double_value}

# Node 2: 메세지 만들기
def messenger(state):
    message = f"원래 숫자 {state['number']}가 {state['doubled']}가 되었습니다!"
    print(f"메세지 생성: {message}")
    return {"message": message}

# Graph 구성
graph = StateGraph(TeamworkState)

# 노드 추가
graph.add_node("doubler", doubler)
graph.add_node("messenger", messenger)

# 엣지 연결
graph.add_edge(START, "doubler")
graph.add_edge("doubler", "messenger")
graph.add_edge("messenger", END)

# 실행
app = graph.compile()
result = app.invoke({"number": 5, "doubled": 0, "message": ""})
print(f"최종 결과: {result}")