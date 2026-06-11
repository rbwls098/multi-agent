import json
import requests
import os
import re
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime

class InformationGatheringAgent:
    def __init__(self, fallback_data_path="sample_data/opportunities.json"):
        self.fallback_data_path = fallback_data_path
        self.current_year = 2026 # 시스템 기준 현재 연도

    def run(self, search_keywords=None):
        if not search_keywords:
            search_keywords = ["개발", "기획", "디자인"]
            
        print(f"[정보수집 에이전트] {', '.join(search_keywords)} 키워드로 채용 데이터를 수집합니다.")
        opportunities = []

        for keyword in search_keywords:
            opportunities.extend(self._collect_jobkorea(keyword))
            opportunities.extend(self._collect_saramin(keyword))

        # 1. 날짜 기반 필터링 (현재 시점 이후 공고만)
        current_date = datetime(2026, 6, 11) # 시스템 기준 현재 날짜
        filtered_opps = []
        for opp in opportunities:
            deadline = opp.get('deadline', '')
            if self._is_active_deadline(deadline, current_date):
                filtered_opps.append(opp)
        
        opportunities = filtered_opps

        # 2. 중복 제거 (제목+회사명 기준)
        unique_opps = {}
        for opp in opportunities:
            key = f"{opp['title']}_{opp['company']}"
            if key not in unique_opps:
                unique_opps[key] = opp
        
        opportunities = list(unique_opps.values())

        if not opportunities:
            print("⚠️ 실시간 수집 결과가 없어 최신 가상 데이터를 제공합니다.")
            for kw in search_keywords:
                opportunities.append({
                    "id": f"ai_gen_{kw}",
                    "title": f"{kw} 분야 전문 인재 채용 (2026 하반기)",
                    "company": "AI 추천 유망 기업",
                    "category": kw,
                    "required_skills": [kw],
                    "qualifications": "해당 분야 전공 또는 유관 경험 보유자",
                    "preferred": "관련 자격증 소지자, 원활한 커뮤니케이션 가능자",
                    "experience_years": 0,
                    "deadline": "2026.06.30 까지",
                    "url": "https://www.saramin.co.kr",
                    "source": "AI 추천"
                })

        os.makedirs("output", exist_ok=True)
        with open("output/collected_opportunities.json", "w", encoding="utf-8-sig") as f:
            json.dump({"opportunities": opportunities}, f, ensure_ascii=False, indent=2)

        print(f"✓ 총 {len(opportunities)}개의 유효한 채용 데이터를 확보했습니다.\n")
        return opportunities

    def _is_active_deadline(self, deadline_str, current_date):
        """마감일이 현재 날짜 이후인지 확인"""
        if "마감" in deadline_str or "상시" in deadline_str or "채용시" in deadline_str:
            return True
        
        # 날짜 추출 (MM/DD 또는 YYYY.MM.DD)
        date_match = re.search(r"(\d{4})?[./-]?(\d{1,2})[./-]?(\d{1,2})", deadline_str)
        if date_match:
            groups = date_match.groups()
            year = int(groups[0]) if groups[0] else self.current_year
            month = int(groups[1])
            day = int(groups[2])
            
            try:
                deadline_date = datetime(year, month, day)
                # 연도가 없어서 과거로 오해받는 경우 보정 (6월인데 마감이 1월이면 내년으로 간주하거나, 이미 지난 것)
                if not groups[0] and deadline_date < current_date:
                    # 마감일이 지났는데 연도가 안적혀있으면 올해가 아닐 수 있음
                    # 하지만 크롤링 결과는 보통 현재 공고이므로, 
                    # 한 달 이상 차이 나면 과거 공고로 보고 필터링
                    if (current_date - deadline_date).days > 30:
                        return False
                return deadline_date >= current_date
            except:
                return True
        return True

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
