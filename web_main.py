import json
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# 기존 에이전트 클래스 임포트
from collector import InformationGatheringAgent
from analyzer import CompetencyAnalysisAgent
from matcher import MatchingStrategyAgent
from coach import CoverLetterCoachAgent

app = FastAPI()

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 에이전트 인스턴스 생성
collector = InformationGatheringAgent()
analyzer = CompetencyAnalysisAgent()
matcher = MatchingStrategyAgent()
coach = CoverLetterCoachAgent()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_profile(
    request: Request,
    name: str = Form(...),
    experience_years: int = Form(...),
    skills: str = Form(...),
    interests: str = Form(...)
):
    # 1. 입력 데이터를 에이전트가 처리할 수 있는 형식으로 변환
    user_profile = {
        "profiles": [{
            "id": "web_user_1",
            "name": name,
            "experience": {"years": experience_years},
            "skills": {"main": [s.strip() for s in skills.split(",")]},
            "interests": [i.strip() for i in interests.split(",")],
            "education": {"major": "알 수 없음"},
            "certifications": []
        }]
    }
    
    # 임시 파일로 저장 (기존 analyzer가 파일을 읽도록 되어 있으므로 최소한의 수정으로 연동)
    temp_profile_path = "temp_web_profile.json"
    with open(temp_profile_path, "w", encoding="utf-8") as f:
        json.dump(user_profile, f, ensure_ascii=False)

    try:
        # 2. 에이전트 실행 흐름 (기존 main.py 로직)
        
        # 정보 수집
        opportunities = collector.run()
        
        # 역량 분석 (임시 파일 경로 전달)
        web_analyzer = CompetencyAnalysisAgent(profile_path=temp_profile_path)
        analyzed_profiles = web_analyzer.run()
        
        # 매칭 전략
        matched_profiles = matcher.run(analyzed_profiles, opportunities)
        
        # 결과 처리
        user_result = matched_profiles[0]
        
        # 자소서 팁 생성 (개별 팁 추출을 위해 coach 내부 로직 활용 또는 개별 생성)
        tips = []
        if user_result.get('matched_opportunities'):
            for opp in user_result['matched_opportunities']:
                tip = coach._generate_tip(opp['category'], user_result['experience_years'])
                tips.append(tip)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "user": user_result,
            "tips": tips
        })
    finally:
        if os.path.exists(temp_profile_path):
            os.remove(temp_profile_path)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 커리어 매칭 에이전트 웹 서버를 시작합니다.")
    print("접속 주소: http://127.0.0.1:8000")
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)
