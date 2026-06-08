import json
import requests
import os
import re
import urllib.parse
from bs4 import BeautifulSoup

class InformationGatheringAgent:
    def __init__(self, fallback_data_path="sample_data/opportunities.json"):
        self.fallback_data_path = fallback_data_path

    def run(self, search_keywords=None):
        if not search_keywords:
            search_keywords = ["개발", "기획", "디자인"]
            
        print(f"[정보수집 에이전트] {', '.join(search_keywords)} 키워드로 채용 데이터를 수집합니다.")
        opportunities = []

        for keyword in search_keywords:
            opportunities.extend(self._collect_jobkorea(keyword))
            opportunities.extend(self._collect_saramin(keyword))

        # 중복 제거 (제목+회사명 기준)
        unique_opps = {}
        for opp in opportunities:
            key = f"{opp['title']}_{opp['company']}"
            if key not in unique_opps:
                unique_opps[key] = opp
        
        opportunities = list(unique_opps.values())

        if not opportunities:
            print("⚠️ 실시간 수집 결과가 없어 기본 데이터를 제공합니다.")
            for kw in search_keywords:
                opportunities.append({
                    "id": f"ai_gen_{kw}",
                    "title": f"{kw} 분야 전문 인재 채용",
                    "company": "AI 추천 유망 기업",
                    "category": kw,
                    "required_skills": [kw],
                    "qualifications": "해당 분야 전공 또는 유관 경험 보유자",
                    "preferred": "관련 자격증 소지자, 원활한 커뮤니케이션 가능자",
                    "experience_years": 0,
                    "deadline": "채용 시 마감",
                    "url": "https://www.jobkorea.co.kr",
                    "source": "AI 추천"
                })

        os.makedirs("output", exist_ok=True)
        with open("output/collected_opportunities.json", "w", encoding="utf-8-sig") as f:
            json.dump({"opportunities": opportunities}, f, ensure_ascii=False, indent=2)

        print(f"✓ 총 {len(opportunities)}개의 상세 채용 데이터를 확보했습니다.\n")
        return opportunities

    def _collect_jobkorea(self, keyword):
        results = []
        try:
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://www.jobkorea.co.kr/Search/?stext={encoded_keyword}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select('.list-default .list-post')
                for idx, item in enumerate(items[:10]):
                    title_elem = item.select_one('.post-list-info .title')
                    if not title_elem: continue
                    title = title_elem.text.strip()
                    link = "https://www.jobkorea.co.kr" + title_elem.get('href', '')
                    
                    corp_elem = item.select_one('.post-list-corp a')
                    company = corp_elem.text.strip() if corp_elem else "기업"
                    
                    # 마감일
                    date_elem = item.select_one('.post-list-info .option .date')
                    deadline = date_elem.text.strip() if date_elem else "확인 필요"
                    
                    # 자격요건/우대사항 (간단 추출)
                    exp_elem = item.select_one('.post-list-info .option .exp')
                    edu_elem = item.select_one('.post-list-info .option .edu')
                    qual = f"{exp_elem.text if exp_elem else ''} / {edu_elem.text if edu_elem else ''}".strip(' /')
                    
                    results.append({
                        "id": f"jobkorea_{keyword}_{idx}",
                        "title": title,
                        "company": company,
                        "category": keyword,
                        "required_skills": [keyword],
                        "qualifications": qual if qual else "공고 참조",
                        "preferred": "상세 페이지 우대사항 확인",
                        "experience_years": 0,
                        "deadline": deadline,
                        "url": link,
                        "source": "잡코리아"
                    })
        except Exception as e:
            print(f"✗ 잡코리아 수집 실패: {e}")
        return results

    def _collect_saramin(self, keyword):
        results = []
        try:
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchword={encoded_keyword}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select('.item_recruit')
                for idx, item in enumerate(items[:10]):
                    title_elem = item.select_one('.job_tit a')
                    if not title_elem: continue
                    title = title_elem.get('title', '').strip()
                    link = "https://www.saramin.co.kr" + title_elem.get('href', '')
                    
                    corp_elem = item.select_one('.corp_name a')
                    company = corp_elem.text.strip() if corp_elem else "기업"
                    
                    deadline_elem = item.select_one('.job_date .date')
                    deadline = deadline_elem.text.strip() if deadline_elem else "확인 필요"
                    
                    # 섹터 기반으로 자격요건 흉내
                    sectors = [a.text.strip() for a in item.select('.job_sector a')]
                    
                    results.append({
                        "id": f"saram_{keyword}_{idx}",
                        "title": title,
                        "company": company,
                        "category": keyword,
                        "required_skills": sectors,
                        "qualifications": ", ".join(sectors[:2]) + " 역량 보유자",
                        "preferred": "관련 분야 전공 및 자격증 우대",
                        "experience_years": 0,
                        "deadline": deadline,
                        "url": link,
                        "source": "사람인"
                    })
        except:
            pass
        return results
