from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# .env 파일에서 환경 변수 로드
load_dotenv()

# GPT-4.1-mini 설정
gpt4_mini = ChatOpenAI(
    model_name="gpt-4.1-mini", # GPT-4.1-mini에 해당하는 모델명
    temperature=0.7,
    max_tokens=150,
)

# GPT-4.1 설정
gpt4 = ChatOpenAI(
    model_name="gpt-4.1", # GPT-4.1에 해당하는 모델명
    temporature=0.7,
    max_tokens=300,
)

# GPT-4.1-mini 사용
response_mini = gpt4_mini.invoke([HumanMessage(content="Hello, how are you?")])
print(response_mini)

# GPT-4.1 사용
response_full = gpt4.invoke([HumanMessage(content="Explain the concept of machine learning.")])
print(response_full)