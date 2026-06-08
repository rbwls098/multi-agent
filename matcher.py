from llm_client import llm

class MatchingStrategyAgent:
     def run(self, profiles, opportunities):
         print("[매칭 전략 에이전트] 정밀 시맨틱 매칭 및 랭킹 산출 중...")
         
         if not opportunities:
             return profiles

         matched_profiles = []
         for profile in profiles:
             scored_items = []
             for opp in opportunities:
                 # AI 기반 정밀 점수 계산
                 score = self._calculate_ai_score(profile, opp)
                 scored_items.append({
                     'opp_id': opp['id'],
                     'title': opp['title'],
                     'company': opp['company'],
                     'match_score': round(score, 2),
                     'category': opp['category'],
                     'deadline': opp.get('deadline', '확인 필요'),
                     'source': opp.get('source', '알 수 없음'),
                     'qualifications': opp.get('qualifications', '공고 참조'),
                     'preferred': opp.get('preferred', '공고 참조'),
                     'url': opp.get('url', '#')
                 })
                
             # 점수 높은 순(사용자 스펙과 일치할수록)으로 정렬
             scored_items.sort(key=lambda x: x['match_score'], reverse=True)
             profile['matched_opportunities'] = scored_items[:5] # 상위 5개
             matched_profiles.append(profile)
             
         print("✓ 사용자 맞춤형 랭킹 작성을 완료했습니다.\n")
         return matched_profiles

     def _calculate_ai_score(self, profile, opportunity):
         user_context = f"보유기술: {', '.join(profile['skills'])}, 관심분야: {', '.join(profile['interests'])}"
         job_context = f"공고제목: {opportunity['title']}, 자격요건: {opportunity.get('qualifications', '')}, 우대사항: {opportunity.get('preferred', '')}"
         
         prompt = f"""
         너는 전문 리크루팅 매칭 AI야. 
         지원자의 스펙이 해당 공고의 자격요건 및 우대사항과 얼마나 일치하는지 분석해서 점수를 줘.
         
         [지원자 스펙]
         {user_context}
         
         [공고 상세 정보]
         {job_context}
         
         규칙:
         1. 지원자의 기술 스택이나 관심사가 공고의 자격요건/우대사항에 구체적으로 언급될수록 높은 점수를 줘.
         2. 0.0에서 1.0 사이의 숫자 하나만 응답해.
         """
         
         try:
             response = llm.chat(prompt)
             import re
             match = re.search(r"\d+\.\d+", response)
             return float(match.group()) if match else 0.5
         except:
             return 0.5
