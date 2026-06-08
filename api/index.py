import sys
import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 프로젝트 루트 경로 추가 (에이전트 모듈 임포트용)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import InformationGatheringAgent
from analyzer import CompetencyAnalysisAgent
from matcher import MatchingStrategyAgent
from coach import CoverLetterCoachAgent

app = FastAPI()

# Vercel 서버리스 환경을 위한 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 에이전트 인스턴스 생성
collector = InformationGatheringAgent()
matcher = MatchingStrategyAgent()
coach = CoverLetterCoachAgent()

@app.get("/")
@app.get("/api")
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze")
@app.post("/api/analyze")
async def analyze_profile(
    request: Request,
    name: str = Form(...),
    experience_years: int = Form(...),
    skills: str = Form(...),
    interests: str = Form(...)
):
    # 1. 입력 데이터를 에이전트 형식으로 변환
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
    
    # 서버리스 환경이므로 /tmp 디렉토리 사용 (Vercel 권장)
    temp_profile_path = "/tmp/temp_web_profile.json"
    with open(temp_profile_path, "w", encoding="utf-8") as f:
        json.dump(user_profile, f, ensure_ascii=False)

    try:
        # 2. 에이전트 실행
        opportunities = collector.run()
        web_analyzer = CompetencyAnalysisAgent(profile_path=temp_profile_path)
        analyzed_profiles = web_analyzer.run()
        matched_profiles = matcher.run(analyzed_profiles, opportunities)
        
        user_result = matched_profiles[0]
        
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

# Vercel은 'app' 객체를 엔트리 포인트로 사용합니다.
� 'app' 객체를 엔트리 포인트로 사용합니다.
