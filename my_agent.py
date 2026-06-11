import json
import os
from llm_client import llm
from collector import InformationGatheringAgent
from matcher import MatchingStrategyAgent
from coach import CoverLetterCoachAgent
from reviewer import ReviewerAgent

# [중요] 14주차 고도화된 멀티에이전트 시스템 메인 파이프라인

def extract_facts(text):
    """[에이전트 1] 입력 자료에서 핵심 정보를 정밀하게 추출"""
    print("[1/5] 정보 추출 에이전트 가동...")
    prompt = f"""
    당신은 전문 데이터 추출 전문가입니다. 아래 사용자의 입력 텍스트에서 핵심 정보를 JSON 형식으로 추출하세요.
    
    [입력 텍스트]
    {text}
    
    [추출 규칙]
    - name: 성함 (없으면 '사용자')
    - experience_years: 숫자만 (신입은 0)
    - skills: 구체적인 기술 스택 리스트
    - interests: 관심 직무 또는 분야 리스트
    
    형식: {{"name": "", "experience_years": 0, "skills": [], "interests": []}}
    """
    try:
        response = llm.chat(prompt)
        import re
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return {"name": "사용자", "experience_years": 0, "skills": ["미지정"], "interests": ["미지정"]}

def run_pipeline(input_text):
    """전체 에이전트 흐름 실행 (표준 멀티에이전트 구조)"""
    
    # 1. 정보 추출
    profile = extract_facts(input_text)
    
    # 2. 정보 수집 (InformationGatheringAgent)
    collector = InformationGatheringAgent()
    opportunities = collector.run(search_keywords=profile['interests'])
    
    # 3. 매칭 및 랭킹 (MatchingStrategyAgent)
    # MatchingStrategyAgent는 리스트 형태를 받으므로 변환
    matcher = MatchingStrategyAgent()
    matched_profiles = matcher.run([profile], opportunities)
    
    # 4. 자소서 코칭 가이드 생성 (CoverLetterCoachAgent)
    coach = CoverLetterCoachAgent()
    final_guide = coach.run(matched_profiles)
    
    # 5. 최종 검토 (ReviewerAgent)
    reviewer = ReviewerAgent()
    final_review = reviewer.run(matched_profiles, final_guide)
    
    # 6. 결과 저장
    save_all_results(profile, final_guide, final_review)
    
    return profile, final_guide, final_review

def save_all_results(profile, guides, review):
    """표준 파일 저장 (프로젝트 가이드 준수)"""
    os.makedirs("output", exist_ok=True)
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(f"# 추출 데이터\n\n{json.dumps(profile, ensure_ascii=False, indent=2)}")
    with open("output_user_guide.md", "w", encoding="utf-8") as f:
        f.write(guides)
    with open("review_report.md", "w", encoding="utf-8") as f:
        f.write(review)

if __name__ == "__main__":
    test_input = "홍길동, 3년차 백엔드, Java/Spring 활용 가능, 클라우드 아키텍처 관심"
    run_pipeline(test_input)
