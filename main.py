import os
from collector import InformationGatheringAgent
from analyzer import CompetencyAnalysisAgent
from matcher import MatchingStrategyAgent
from coach import CoverLetterCoachAgent

def main():
    print("=" * 60)
    print("취업 안내 멀티에이전트 시스템 (피드백 반영)")
    print("=" * 60)
    print()
    
    # 1. 정보 수집 (수집 에이전트) - 4번 피드백 반영 (웹 수집 흉내내기 + 로컬 데이터 로딩)
    collector = InformationGatheringAgent()
    opportunities = collector.run()
    
    # 2. 사용자 역량 분석 (역량 분석 에이전트)
    analyzer = CompetencyAnalysisAgent()
    profiles = analyzer.run()
    
    # 3. 공고 매칭 (매칭 전략 에이전트) - 2번 피드백 반영 (매칭점수 클리핑 제거)
    matcher = MatchingStrategyAgent()
    matched_profiles = matcher.run(profiles, opportunities)
    
    # 4. 자소서 팁 작성 (자소서 코치 에이전트) - 3번 피드백 반영 (for문 오류 해결)
    coach = CoverLetterCoachAgent()
    recommendations = coach.run(matched_profiles)
    
    # 5. 결과 출력 및 저장
    print("============================================================")
    print("최종 결과 요약")
    print("============================================================\n")
    print(recommendations)
    
    os.makedirs('output', exist_ok=True)
    out_file = 'output/matched_recommendations.md'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(recommendations)
    print(f"\n[안내] 최종 추천 결과가 '{out_file}'에 성공적으로 저장되었습니다.\n")

if __name__ == "__main__":
    main()
