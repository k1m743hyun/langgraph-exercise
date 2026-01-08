from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import TypedDict, Literal

class OrderState(TypedDict):
    customer_name: str
    item: str
    quantity: int
    price: float
    status: str
    messages: list

# 노드 정의
def check_inventory(state: OrderState) -> Command[Literal["process_payment", "out_of_stock", END]]:
    """
    재고 확인 후 다음 단계 결정 노드
    """
    item = state['item']
    quantity = state['quantity']

    # 간단한 재고 확인 (실제로는 DB 조회)
    available_stock = {"사과": 10, "바나나": 5, "오렌지": 0}
    stock = available_stock.get(item, 0)

    if stock >= quantity:
        # 재고 충분 - 결제 처리로 이동
        return Command(
            goto="process_payment",
            update={
                "status": "재고 확인 완료",
                "messages": state['messages'] + [f"{item} {quantity}개 재고 확인됨"]
            }
        )
    else:
        # 재고 부족 - 품절 처리로 이동
        return Command(
            goto="out_of_stock",
            update={
                "status": "재고 부족",
                "messages": state['messages'] + [f"{item} 재고 부족 (요청: {quantity}개, 보유: {stock}개)"]
            }
        )

def process_payment(state: OrderState) -> Command[Literal["send_confirmation", END]]:
    '''
    결제 처리 노드
    '''
    total_price = state["quantity"] * state["price"]

    return Command(
        goto="send_confirmation",
        update={
            "status": "결제 완료",
            "messages": state["messages"] + [f"결제 완료: {total_price}원"]
        }
    )

def out_of_stock(state: OrderState) -> Command[Literal[END]]:
    '''
    품절 처리 노드
    '''
    return Command(
        goto=END,
        update={
            "status": "주문 취소됨",
            "messages": state["messages"] + ["죄송합니다. 품절로 인해 주문이 취소되었습니다."]
        }
    )

def send_confirmation(state: OrderState) -> Command[Literal[END]]:
    '''
    주문 확인 메세지 발송 노드
    '''
    customer = state["customer_name"]

    return Command(
        goto=END,
        update={
            "status": "주문 완료",
            "messages": state["messages"] + [f"{customer}님께 주문 확인 메세지를 발송했습니다."]
        }
    )

# 그래프 생성
graph = StateGraph(OrderState)

# 노드 추가
graph.add_node("check_inventory", check_inventory)
graph.add_node("process_payment", process_payment)
graph.add_node("out_of_stock", out_of_stock)
graph.add_node("send_confirmation", send_confirmation)

# 엣지 추가 - 기본 패턴
graph.add_edge(START, "check_inventory")

compiled_graph = graph.compile()

initial_state = {
    "customer_name": "김태현",
    "item": "사과",
    "quantity": 20,
    "price": 10000,
    "status": "",
    "messages": [],
}

result = compiled_graph.invoke(initial_state)
print("\n=== 최종 결과 ===")
print(f"고객 명: {result["customer_name"]}")
print(f"최종 상태: {result["status"]}")
for message in result['messages']:
    print(f"    - {message}")