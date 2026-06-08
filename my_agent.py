import os
import json
from collector import InformationGatheringAgent
from analyzer import CompetencyAnalysisAgent
from matcher import MatchingStrategyAgent
from coach import CoverLetterCoachAgent
from reviewer import ReviewerAgent

def main():
    print("=" * 60)
    print("취업 안내 멀티에이전트 시스템 (최종 제출용)")
    print("=" * 60)
    print()
    
    # 입력 파일 확인 (sample_input.txt 사용)
    input_file = "sample_input.txt"
    if not os.path.exists(input_file):
        # 만약 없으면 기존 JSON에서 복사 (최초 1회)
        if os.path.exists("sample_career_profile.json"):
            with open("sample_career_profile.json", "r", encoding="utf-8") as f:
                content = f.read()
            with open(input_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            print(f"오류: {input_file}이 존재하지 않습니다.")
            return

    # 1. 정보 수집 (수집 에이전트)
    collector = InformationGatheringAgent()
    opportunities = collector.run()
    
    # 2. 사용자 역량 분석 (역량 분석 에이전트) - sample_input.txt 사용하도록 변경
    analyzer = CompetencyAnalysisAgent(profile_path=input_file)
    profiles = analyzer.run()
    
    # 3. 공고 매칭 (매칭 전략 에이전트)
    matcher = MatchingStrategyAgent()
    matched_profiles = matcher.run(profiles, opportunities)
    
    # 4. 자소서 팁 작성 (자소서 코치 에이전트)
    coach = CoverLetterCoachAgent()
    user_guide = coach.run(matched_profiles)
    
    # 5. 최종 검토 (검토자 에이전트)
    reviewer = ReviewerAgent()
    review_report = reviewer.run(matched_profiles, user_guide)
    
    # 6. 결과 저장 (요구사항에 맞춘 파일명)
    os.makedirs('output', exist_ok=True)
    
    # output.md (핵심 정보 추출 결과 표)
    with open('output.md', 'w', encoding='utf-8') as f:
        f.write("# 핵심 정보 추출 결과\n\n")
        f.write("| 이름 | 직무 유형 | 경력 | 매칭 공고 수 | 최고 매칭 점수 |\n")
        f.write("|------|-----------|------|--------------|----------------|\n")
        for p in matched_profiles:
            max_score = max([m['match_score'] for m in p['matched_opportunities']]) if p['matched_opportunities'] else 0
            f.write(f"| {p['name']} | {p['job_type']} | {p['experience_years']}년 | {len(p['matched_opportunities'])}건 | {int(max_score*100)}% |\n")
    
    # output_user_guide.md (사용자 가이드)
    with open('output_user_guide.md', 'w', encoding='utf-8') as f:
        f.write(user_guide)
        
    # review_report.md (검토 보고서)
    with open('review_report.md', 'w', encoding='utf-8') as f:
        f.write(review_report)
        
    print("============================================================")
    print("최종 결과 저장 완료")
    print("============================================================")
    print("- output.md: 추출 결과 표")
    print("- output_user_guide.md: 사용자별 맞춤 추천 및 팁")
    print("- review_report.md: 시스템 자가 검토 보고서")
    print("============================================================\n")

if __name__ == "__main__":
    main()
