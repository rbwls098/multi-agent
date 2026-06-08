import json
import os
from llm_client import llm

# 13.1 가이드라인에 따른 완성형 핵심 함수 정의

def extract_facts(text):
    """[에이전트 1] 입력 자료에서 핵심 정보를 정밀하게 추출"""
    print("[1/4] 정보 추출 에이전트 가동...")
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

def classify_items(profile):
    """[에이전트 2] 실시간 공고 수집 및 직무별 분류"""
    print("[2/4] 분류 및 수집 에이전트 가동...")
    from collector import InformationGatheringAgent
    collector = InformationGatheringAgent()
    opportunities = collector.run(search_keywords=profile['interests'])
    
    grouped = {}
    for opp in opportunities:
        cat = opp['category']
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(opp)
    
    return {"profile": profile, "grouped_opps": grouped}

def write_user_guides(data):
    """[에이전트 3] 완성형 가이드 작성 (모든 피드백이 내재화된 Single-pass 로직)"""
    print("[3/4] 완성형 가이드 작성 에이전트 가동...")
    profile = data['profile']
    grouped = data['grouped_opps']
    
    # 그동안의 검토 피드백(단정 표현 금지, 구체적 To-Do, 상세 정보 등)을 프롬프트에 직접 녹여냄
    prompt = f"""
    당신은 시니어 커리어 컨설턴트입니다. 아래 데이터를 바탕으로 [최종 커리어 가이드]를 작성하세요.
    
    [데이터]
    - 사용자: {profile['name']} ({profile['experience_years']}년차)
    - 주요역량: {', '.join(profile['skills'])}
    - 수집된 공고: {json.dumps(grouped, ensure_ascii=False)}
    
    [작성 원칙 - 필독]
    1. **완곡한 표현**: "반드시 합격", "높은 연관성" 등 단정적인 단어를 절대 사용하지 마세요. "~할 가능성이 있습니다", "도움이 될 것으로 예상됩니다"와 같이 신중하게 표현하세요.
    2. **데이터 기반**: 입력 자료에 없는 정보를 임의로 지어내지 마세요.
    3. **상세 정보 노출**: 추천 공고마다 [마감일], [출처], [상세페이지 링크]를 명확히 포함하세요.
    4. **실행 중심**: 하단에 사용자가 즉시 실천할 수 있는 구체적인 To-Do List를 단계별로 제시하세요.
    
    응답은 가독성 좋은 Markdown 형식으로만 작성하세요.
    """
    return llm.chat(prompt)

def review_guides(guides):
    """[에이전트 4] 최종 품질 검토 (체크리스트 기반)"""
    print("[4/4] 최종 검토 에이전트 가동...")
    prompt = f"""
    당신은 최종 품질 검수자입니다. 아래 안내문이 가이드라인을 준수하는지 점검하고 보고서를 작성하세요.
    
    [체크리스트]
    - 단정적/과장된 표현이 제거되었는가?
    - 마감일과 링크 등 핵심 정보가 포함되었는가?
    - To-Do List가 실질적인 도움이 되는가?
    
    가이드 내용:
    {guides}
    """
    return llm.chat(prompt)

def save_all_results(profile, guides, review):
    """표준 파일 저장 (13.1 가이드 준수)"""
    os.makedirs("output", exist_ok=True)
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(f"# 추출 데이터\n\n{json.dumps(profile, ensure_ascii=False, indent=2)}")
    with open("output_user_guide.md", "w", encoding="utf-8") as f:
        f.write(guides)
    with open("review_report.md", "w", encoding="utf-8") as f:
        f.write(review)

def run_pipeline(input_text):
    """전체 에이전트 흐름 실행 (단일 실행 완성형)"""
    # 1. 정보 추출
    profile = extract_facts(input_text)
    
    # 2. 공고 수집 및 분류
    data = classify_items(profile)
    
    # 3. 완성형 가이드 작성 (피드백이 이미 반영된 단일 생성)
    final_guide = write_user_guides(data)
    
    # 4. 품질 검토
    final_review = review_guides(final_guide)
    
    # 5. 저장
    save_all_results(profile, final_guide, final_review)
    
    return profile, final_guide, final_review

if __name__ == "__main__":
    test_input = "홍길동, 3년차 백엔드, Java/Spring 활용 가능, 클라우드 아키텍처 관심"
    run_pipeline(test_input)
