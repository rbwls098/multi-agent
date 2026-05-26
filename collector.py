import json
import requests
import os
import re
from bs4 import BeautifulSoup

class InformationGatheringAgent:
    def __init__(self, fallback_data_path="sample_data/opportunities.json"):
        self.fallback_data_path = fallback_data_path

    def run(self):
        print("[정보수집 에이전트] 채용 기회 데이터를 수집합니다.")
        opportunities = []

        try:
            # 사람인 '개발자' 대상 검색
            search_url = "https://www.saramin.co.kr/zf_user/search/recruit?searchword=개발자&recruitSort=relation&recruitPageCount=20"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select('.item_recruit')
                print(f"✓ 외부 채용 검색 페이지 파싱 성공 (추출된 공고 수: {len(items)}건)")
                
                os.makedirs("output", exist_ok=True)
                
                for idx, item in enumerate(items[:15]): # 상위 15개 가져오기
                    title_elem = item.select_one('.job_tit a')
                    if not title_elem: continue
                    title = title_elem.get('title', '').strip()
                    
                    corp_elem = item.select_one('.corp_name a')
                    company = corp_elem.text.strip() if corp_elem else "알 수 없는 기업"
                    
                    conds = [c.text for c in item.select('.job_condition span')]
                    exp_text = next((c for c in conds if '경력' in c or '신입' in c), "")
                    
                    # 경력 숫자 추출
                    exp_years = 0
                    if '경력' in exp_text:
                        match = re.search(r'\d+', exp_text)
                        if match:
                            exp_years = int(match.group())
                    
                    # 기술 스택 및 카테고리 추출
                    sectors = [a.text.strip() for a in item.select('.job_sector a')]
                    
                    category = "개발"
                    if any("웹" in s.lower() or "프론트" in s or "백엔드" in s or "react" in s.lower() for s in sectors):
                        category = "웹개발"
                    elif any("ai" in s.lower() or "데이터" in s or "딥러닝" in s for s in sectors):
                        category = "데이터/AI"
                    elif any("기획" in s or "pm" in s.lower() for s in sectors):
                        category = "비즈니스개발"

                    opportunities.append({
                        "id": f"saram_auto_{idx}",
                        "title": title,
                        "company": company,
                        "category": category,
                        "required_skills": sectors, # 핵심 기술 스킬로 대체
                        "experience_years": exp_years
                    })
        except Exception as e:
            print(f"✗ 웹 수집 중 예외 발생: {e}")

        # 백업 데이터 추가 로직 (만약 수집된 것이 없을 경우 등)
        if len(opportunities) < 3:
            print("✗ 충분한 데이터를 수집하지 못하여 기본 로컬 데이터를 추가합니다.")
            try:
                with open(self.fallback_data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    opportunities.extend(data.get('opportunities', []))
            except FileNotFoundError:
                pass

        # 수집 결과를 JSON으로 저장
        os.makedirs("output", exist_ok=True)
        with open("output/collected_opportunities.json", "w", encoding="utf-8") as f:
            json.dump({"opportunities": opportunities}, f, ensure_ascii=False, indent=2)

        print(f"✓ 총 {len(opportunities)}개의 실제 채용 기회를 수집 완료하였습니다.\n")
        return opportunities
