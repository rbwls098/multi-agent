import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

class LLMClient:
     def __init__(self):
         self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
         self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini") # 기본값 설정

     def chat(self, prompt: str) -> str:
         try:
             response = self.client.chat.completions.create(
                 model=self.model,
                 messages=[{"role": "user", "content": prompt}]
             )
             return response.choices[0].message.content
         except Exception as e:
             return f"LLM Error: {e}"

# 싱글톤 인스턴스 생성 (다른 파일에서 import 해서 사용)
llm = LLMClient()