import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드 (로컬 환경용)
load_dotenv()

def get_api_key():
    # 1. Streamlit Secrets 확인 (클라우드 환경)
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    # 2. 환경 변수 확인 (로컬 환경)
    return os.getenv("OPENAI_API_KEY")

class LLMClient:
     def __init__(self):
         api_key = get_api_key()
         self.client = OpenAI(api_key=api_key)
         self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini") # 기본값 설정

     def chat(self, prompt: str) -> str:
         if not self.client.api_key:
             return "LLM Error: API Key is missing."
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