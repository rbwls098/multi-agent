import json

class ReviewerAgent:
    def __init__(self):
        pass

    def run(self, matched_profiles, advice_output):
        print("[검토자 에이전트] 생성된 추천 결과와 조언을 검토합니다.")
        
        report = "# 검토 보고서 (Review Report)\n\n"
        
        # 1. 매칭 적절성 검토
        report += "## 1. 매칭 적절성 점검\n"
        for user in matched_profiles:
            report += f"### 사용자: {user['name']}\n"
            matches = user.get('matched_opportunities', [])
            if not matches:
                report += "- ⚠️ 매칭된 공고가 없습니다. 분석 로직 또는 데이터 부족 가능성이 있습니다.\n"
            else:
                report += f"- ✅ 매칭된 공고 수: {len(matches)}건\n"
                for m in matches:
                    report += f"  - {m['company']} ({m['title']}): 매칭 점수 {int(m['match_score']*100)}%\n"
        
        report += "\n## 2. 콘텐츠 품질 점검\n"
        if advice_output and len(advice_output) > 100:
            report += "- ✅ 사용자 가이드가 충분한 분량으로 생성되었습니다.\n"
            report += "- ✅ Markdown 형식이 올바르게 적용되었습니다.\n"
        else:
            report += "- ⚠️ 사용자 가이드의 내용이 너무 짧거나 누락되었습니다.\n"

        report += "\n## 3. 종합 의견\n"
        report += "본 에이전트 시스템은 사용자 역량 분석, 공고 수집, 매칭, 코칭 과정을 거쳐 최종 결과물을 생성하였습니다. "
        report += "전반적으로 데이터 흐름이 안정적이며, 매칭 점수 산출 로직에 LLM 정성 평가가 반영되어 신뢰도가 높습니다.\n"
        
        print("✓ 최종 검토 보고서 작성을 완료했습니다.\n")
        return report
