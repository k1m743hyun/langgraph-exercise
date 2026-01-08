from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import TypedDict, Literal

class StudentState(TypedDict):
    name: str
    score: int
    grade: str
    feedback: str
    retry_count: int

# 조건부 엣지 방식
def evaluate_score_traditional(state: StudentState) -> dict:
    """
    전통적인 방식 노드 - 점수만 평가
    """
    score = state['score']

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "F"
    
    return {"grade": grade}

def route_by_grade(state: StudentState) -> Literal["excellent", "good", "average", "need_help"]:
    '''
    조건부 엣지용 라우터 노드
    '''
    grade = state["grade"]

    if grade == "A":
        return "excellent"
    elif grade == "B":
        return "good"
    elif grade == "C":
        return "average"
    else:
        return "need_help"

# Command 방식
def evaluate_score_smart(state: StudentState) -> Command[Literal["excellent", "good", "average", "need_help", END]]:
    '''
    Command 방식 노드 - 평가와 동시에 피드백까지 생성
    '''
    score = state["score"]
    name = state["name"]
    retry_count = state.get("retry_count", 0)

    if score >= 90:
        return Command(
            goto="excellent",
            update={
                "grade": "A",
                "feedback": f"{name}님, 훌륭합니다! {score}점은 정말 대단해요!",
                "retry_count": 0 # 성공하면 재시도 카운트 리셋
            }
        )
    elif score >= 80:
        return Command(
            goto="good",
            update={
                "grade": "B",
                "feedback": f"{name}님, 잘했어요! {score}점이네요.",
                "retry_count": 0
            }
        )
    elif score >= 70:
        return Command(
            goto="average",
            update={
                "grade": "C",
                "feedback": f"{name}님, 괜찮아요. {score}점입니다.",
                "retry_count": retry_count
            }
        )
    else:
        # F 학점이면서 재시도가 3번 미만이면 재도전 기회 제공
        if retry_count < 3:
            return Command(
                goto="need_help",
                update={
                    "grade": "F",
                    "feedback": f"{name}님, 다시 도전해보세요! (재시도 {retry_count + 1}/3)",
                    "retry_count": retry_count + 1
                }
            )
        else:
            return Command(
                goto=END,
                update={
                    "grade": "F",
                    "feedback": f"{name}님, 추가 도움이 필요해 보입니다. 선생님과 상담하세요.",
                    "retry_count": retry_count
                }
            )

def excellent_handler(state: StudentState) -> dict:
    '''
    우수 학생 처리 노드
    '''
    return {
        "feedback": state['feedback'] + " 상장을 받으세요!"
    }

def need_help_handler(state: StudentState) -> Command[Literal["evaluate_score_smart", END]]:
    '''
    도움이 필요한 학생 처리 노드
    '''
    retry_count = state['retry_count']

    if retry_count < 3:
        return Command(
            goto="evaluate_score_smart",
            update={
                "score": state["score"] + 10, # 도움을 받아 점수 향상
                "feedback": state["feedback"] + " 추가 공부 후 재시험!"
            }
        )
    else:
        return Command(
            goto=END,
            update={}
        )

# 그래프 생성
graph = StateGraph(StudentState)

# 핸들러 노드들
def excellent_handler(state: StudentState) -> dict:
    return {"feedback": f"{state['name']}님, 훌륭합니다! A등급!"}

def good_handler(state: StudentState) -> dict:
    return {"feedback": f"{state['name']}님, 잘했어요! B등급!"}

def average_handler(state: StudentState) -> dict:
    return {"feedback": f"{state['name']}님, 괜찮아요. C등급입니다."}

def need_help_handler(state: StudentState) -> dict:
    return {"feedback": f"{state['name']}님, 추가 도움이 필요해요."}

# 노드 추가
graph.add_node("evaluate_score_smart", evaluate_score_smart)
graph.add_node("excellent", excellent_handler)
graph.add_node("good", good_handler)
graph.add_node("average", average_handler)
graph.add_node("need_help", need_help_handler)

# 엣지 추가
graph.add_edge(START, "evaluate_score_smart")
graph.add_conditional_edges(
    "evaluate_score_smart",
    route_by_grade,
    {
        "excellent": "excellent",
        "good": "good",
        "average": "average",
        "need_help": "need_help"
    }
)
graph.add_edge("excellent", END)
graph.add_edge("good", END)
graph.add_edge("average", END)
graph.add_edge("need_help", END)

compiled_graph = graph.compile()

initial_state = {
    "name": "김태현",
    "score": 90,
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"학생 명: {result['name']}")
print(f"점수: {result['score']}")
print(f"등급: {result['grade']}")
print(f"피드백: {result['feedback']}")
# for message in result['messages']:
#     print(f"    - {message}")