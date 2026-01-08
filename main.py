from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from operator import add

class ConditionalState(TypedDict):
    user_input: str
    sentiment: str
    response: str

# 노드 정의
def analyze_sentiment(state: ConditionalState) -> dict:
    """
    감정 분석 노드
    """
    text = state["user_input"].lower()

    # 간단한 감정 분석 (실제로는 ML 모델 사용)
    if any(word in text for word in ["happy", "great", "awesome", "love"]):
        sentiment = "positive"
    elif any(word in text for word in ["sad", "bad", "hate", "terrible"]):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
    }

def positive_response(state: ConditionalState) -> dict:
    '''
    긍정적인 응답 생성 노드
    '''
    return {
        "response": f"😊 That's wonderful! I'm glad you feel that way about: {state['user_input']}",
    }

def negative_response(state: ConditionalState) -> dict:
    '''
    부정적인 응답 생성 노드
    '''
    return {
        "response": f"😔 I understand that's difficult. Let me help with: {state['user_input']}",
    }

def neutral_response(state: ConditionalState) -> dict:
    '''
    중립적인 응답 생성 노드
    '''
    return {
        "response": f"📝 I see. Let me process your request: {state['user_input']}",
    }

# 라우팅 함수
def sentiment_router(state: ConditionalState) -> Literal["positive", "negative", "neutral"]:
    '''감정에 따라 라우팅'''
    return state['sentiment']

# 그래프 생성
graph = StateGraph(ConditionalState)

# 노드 추가
graph.add_node("analyze", analyze_sentiment)
graph.add_node("positive", positive_response)
graph.add_node("negative", negative_response)
graph.add_node("neutral", neutral_response)
graph.add_node("router", sentiment_router)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "analyze")
graph.add_conditional_edges(
    "analyze",
    sentiment_router,
    {
        "positive": "positive",
        "negative": "negative",
        "neutral": "neutral",
    }
)
graph.add_edge("positive", END)
graph.add_edge("negative", END)
graph.add_edge("neutral", END)

compiled_graph = graph.compile()

initial_state = {
    "user_input": "happy",
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"감정: {result["sentiment"]}")
print(f"결과: {result["response"]}")