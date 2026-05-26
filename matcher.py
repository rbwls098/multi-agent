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
                        'match_score': round(score, 2), # 소수점 둘째 자리까지 표시
                        'category': opp['category']
                    })
            
            # 매칭 점수순으로 내림차순 정렬 후 상위 3개 선별
            matched.sort(key=lambda x: x['match_score'], reverse=True)
            profile['matched_opportunities'] = matched[:3]
            matched_profiles.append(profile)
            
        print("✓ 모든 사용자 대상 매칭 추천 목록 작성을 완료했습니다.\n")
        return matched_profiles

    def _calculate_match_score(self, profile, opportunity):
        score = 0.0
        
        # 1. 기술 매칭 (기본 점수 비중: 0.6)
        required_skills = opportunity['required_skills']
        user_skills = profile['skills']
        
        matching_skills = sum(
            1 for req in required_skills 
            if any(req.lower() in u.lower() or u.lower() in req.lower() for u in user_skills)
        )
        skill_score = (matching_skills / len(required_skills)) if required_skills else 0
        score += skill_score * 0.6
        
        # 2. 관심사 매칭 (기본 점수 비중: 0.4)
        category = opportunity['category'].lower()
        interests_match = any(category in i.lower() or i.lower() in category for i in profile['interests'])
        if interests_match:
            score += 0.4
            
        # 3. 경력 요구사항 (충족 시 1.1배 보너스 적용)
        # 2번 피드백 반영: 1.0 클리핑(제한) 삭제. 경력 보너스가 정상적으로 전체 매칭 점수에 반영되게 함.
        if profile['experience_years'] >= opportunity['experience_years']:
            score *= 1.1
            
        return score
