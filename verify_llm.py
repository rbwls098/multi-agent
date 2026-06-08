from llm_client import llm

# 모듈이 잘 로드되는지 확인하고 테스트 메시지 발송
print("LLM 모듈 테스트 시작...")
response = llm.chat("사용 중인 모델 이름이 뭐야?")
print(f"LLM 응답: {response}")