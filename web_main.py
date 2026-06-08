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
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_profile(
    request: Request,
    name: str = Form(...),
    experience_years: int = Form(...),
    skills: str = Form(...),
    interests: str = Form(...)
):
    # 쉼표로 구분된 입력을 리스트로 변환
    interest_list = [i.strip() for i in interests.split(",")]
    skill_list = [s.strip() for s in skills.split(",")]

    # 1. 입력 데이터를 에이전트가 처리할 수 있는 형식으로 변환
    user_profile = {
        "profiles": [{
            "id": "web_user_1",
            "name": name,
            "experience": {"years": experience_years},
            "skills": {"main": skill_list},
            "interests": interest_list,
            "education": {"major": "알 수 없음"},
            "certifications": []
        }]
    }
    
    temp_profile_path = "temp_web_profile.json"
    with open(temp_profile_path, "w", encoding="utf-8") as f:
        json.dump(user_profile, f, ensure_ascii=False)

    try:
        # 2. 에이전트 실행 흐름 (검색 키워드 반영)
        
        # [정보 수집] 사용자가 입력한 관심 분야 키워드로 실시간 검색
        opportunities = collector.run(search_keywords=interest_list)
        
        # [역량 분석]
        web_analyzer = CompetencyAnalysisAgent(profile_path=temp_profile_path)
        analyzed_profiles = web_analyzer.run()
        
        # [매칭 전략]
        matched_profiles = matcher.run(analyzed_profiles, opportunities)
        
        # 결과 처리
        user_result = matched_profiles[0]
        
        # [자소서 코치]
        tips = []
        if user_result.get('matched_opportunities'):
            for opp in user_result['matched_opportunities']:
                tip = coach._generate_tip(opp['category'], user_result['experience_years'])
                tips.append(tip)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user_result,
                "tips": tips
            }
        )
    finally:
        if os.path.exists(temp_profile_path):
            os.remove(temp_profile_path)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
