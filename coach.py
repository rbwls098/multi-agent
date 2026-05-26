class CoverLetterCoachAgent:
    def run(self, classified_users):
        print("[자소서 코치 에이전트] 추천 기회별 자소서 팁과 안내문을 검토 및 생성합니다.")
        
        output = "# 취업 안내 - 맞춤형 추천\n\n"
        
        # 3번 피드백 반영: for user in classified_users: 반복문 제대로 적용
        for user in classified_users:
            output += f"## {user['name']} - {user['job_type']} 직무\n\n"
            output += f"**경력:** {user['experience_years']}년\n\n"
            
            if not user.get('matched_opportunities'):
                output += "현재 적합한 공고가 없습니다. 추가 기술 확보(자격증, 포트폴리오 등)를 권장합니다.\n\n"
                continue
            
            output += "### 추천 공고 및 자소서 팁\n\n"
            for idx, opp in enumerate(user['matched_opportunities'], 1):
                output += f"{idx}. **{opp['title']}** ({opp['company']})\n"
                output += f"   - 지원 분야: {opp['category']}\n"
                output += f"   - 역량 매칭도: {int(opp['match_score']*100)}%\n"
                
                tip = self._generate_tip(opp['category'], user['experience_years'])
                output += f"   - 💡 **자소서 팁**: {tip}\n\n"
            
            output += "---\n\n"
            
        print("✓ 자소서 팁 및 최종 안내문(Markdown) 구성 완료했습니다.\n")
        return output
        
    def _generate_tip(self, category, exp_years):
        tip = ""
        category_lower = category.lower()
        if '비즈니스' in category_lower or '기획' in category_lower:
            tip += "리더십, 전략적 사고, 그리고 팀워크 기반의 협업 성과를 위주로 작성해보세요."
        elif '개발' in category_lower:
            tip += "구체적인 기술 스택을 활용한 프로젝트 경험과 문제 해결 과정을 강조하세요."
        elif 'ai' in category_lower or '데이터' in category_lower:
            tip += "데이터 파이프라인 구축 또는 머신러닝 프로세스 관련 성과를 부각하세요."
        else:
            tip += "직무 관련 핵심 역량과 지원 동기를 명확하게 드러내어 작성해보세요."
            
        if exp_years == 0:
            tip += " 덧붙여, 신입이므로 성장 가능성과 지속적인 학습 열정을 보여주는 것이 핵심입니다."
        else:
            tip += f" 덧붙여, {exp_years}년의 실무 경험에서 어떠한 가치를 창출했는지 수치화하여 포함하면 좋습니다."
        return tip
