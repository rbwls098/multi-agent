from llm_client import llm

class MatchingStrategyAgent:
     def run(self, profiles, opportunities):
         print("[매칭 전략 에이전트] 사용자 역량과 채용 기회를 매칭합니다.")
         
         matched_profiles = []
         for profile in profiles:
             matched = []
             for opp in opportunities:
                 score = self._calculate_match_score(profile, opp)
                 if score >= 0.5:
                     matched.append({
                            'opp_id': opp['id'],
                         'title': opp['title'],
                         'company': opp['company'],
                         'match_score': round(score, 2),
                         'category': opp['category']
                     })
                
             matched.sort(key=lambda x: x['match_score'], reverse=True)
             profile['matched_opportunities'] = matched[:3]
             matched_profiles.append(profile)
             
         print("✓ 모든 사용자 대상 매칭 추천 목록 작성을 완료했습니다.\n")
         return matched_profiles

     def _calculate_match_score(self, profile, opportunity):
         # 1. 규칙 기반 기본 점수 계산 (기존 로직)
         score = 0.0
         required_skills = opportunity['required_skills']
         user_skills = profile['skills']
         
         matching_skills = sum(
             1 for req in required_skills 
             if any(req.lower() in u.lower() or u.lower() in req.lower() for u in user_skills)
         )
         skill_score = (matching_skills / len(required_skills)) if required_skills else 0
         score += skill_score * 0.6
         
         category = opportunity['category'].lower()
         interests_match = any(category in i.lower() or i.lower() in category for i in
      profile['interests'])
         if interests_match:
             score += 0.4
             
         if profile['experience_years'] >= opportunity['experience_years']:
             score *= 1.1

         # 2. LLM을 통한 정성적 매칭 점수 추가
         prompt = f"""
         사용자 역량: {', '.join(user_skills)}
         공고 필수 역량: {', '.join(required_skills)}
         이 공고에 대한 사용자의 적합도를 0에서 1 사이의 숫자로만 평가해서 숫자 하나만 응답해줘.
         다른 말은 하지 말고 숫자만 응답해.
         """
         llm_score_str = llm.chat(prompt)
         try:
             # LLM 응답에서 숫자만 추출 시도
             import re
             numbers = re.findall(r"[-+]?\d*\.\d+|\d+", llm_score_str)
             llm_score = float(numbers[0]) if numbers else 0.5
         except:
             llm_score = 0.5
             
         # 규칙 기반 점수(0.7) + LLM 정성 점수(0.3) 조합
         final_score = (score * 0.7) + (llm_score * 0.3)
         return min(final_score, 1.5) # 최대점수 보정