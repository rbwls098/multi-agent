from llm_client import llm

class CoverLetterCoachAgent:
    def run(self, matched_profiles):
        print("[자소서 코치 에이전트] 추천 기회별 고도화된 자소서 팁과 가이드를 생성합니다.")
        
        final_output = ""
        
        for user in matched_profiles:
            user_name = user.get('name', '사용자')
            experience = user.get('experience_years', 0)
            skills = ", ".join(user.get('skills', []))
            matches = user.get('matched_opportunities', [])
            
            if not matches:
                continue

            # LLM을 사용하여 전체 가이드 작성
            prompt = f"""
            당신은 최고의 시니어 커리어 코치입니다. 아래 사용자의 프로필과 매칭된 채용 공고를 바탕으로 
            [사용자 맞춤형 취업 전략 보고서]를 Markdown 형식으로 작성하세요.
            
            [사용자 정보]
            - 성함: {user_name}
            - 경력: {experience}년차
            - 보유 기술: {skills}
            
            [추천 채용 공고 정보]
            {self._format_matches(matches)}
            
            [작성 지침]
            1. 각 공고별로 왜 이 공고가 사용자에게 추천되었는지 '매칭 포인트'를 설명하세요.
            2. 각 공고별로 자소서 작성 시 강조해야 할 '핵심 키워드'와 '구체적인 작성 팁'을 300자 이상 상세히 적으세요.
            3. 공고의 [마감일]과 [상세페이지 링크]를 반드시 포함하세요.
            4. 마지막에 사용자가 즉시 실행해야 할 'To-Do List'를 단계별로 아주 구체적으로 제시하세요.
            5. 문체는 신뢰감 있고 친절하며, 단정적인 표현보다는 "~을 권장합니다", "~에 도움이 될 것입니다"와 같은 제안형 어조를 사용하세요.
            
            결과물은 충분한 분량으로 풍부하게 작성해 주세요.
            """
            
            final_output += llm.chat(prompt)
            final_output += "\n\n---\n\n"
            
        print("✓ 고도화된 자소서 가이드 생성을 완료했습니다.\n")
        return final_output
        
    def _format_matches(self, matches):
        formatted = ""
        for idx, m in enumerate(matches, 1):
            formatted += f"{idx}. {m['title']} ({m['company']})\n"
            formatted += f"   - 지원분야: {m['category']}\n"
            formatted += f"   - 매칭점수: {int(m['match_score']*100)}%\n"
            formatted += f"   - 마감일: {m['deadline']}\n"
            formatted += f"   - 링크: {m['url']}\n"
            formatted += f"   - 자격요건: {m['qualifications']}\n\n"
        return formatted
