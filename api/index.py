from http.server import BaseHTTPRequestHandler
import sys
import os

# 부모 디렉토리(루트)의 모듈을 참조하기 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import InformationGatheringAgent
from analyzer import CompetencyAnalysisAgent
from matcher import MatchingStrategyAgent
from coach import CoverLetterCoachAgent

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # 웹 브라우저에서 한글이 깨지지 않도록 헤더 설정
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        
        try:
            # 1. 정보 수집 로직
            collector = InformationGatheringAgent()
            opportunities = collector.run()
            
            # 2. 프로필 분석
            analyzer = CompetencyAnalysisAgent()
            profiles = analyzer.run()
            
            # 3. 공고 매칭
            matcher = MatchingStrategyAgent()
            matched_profiles = matcher.run(profiles, opportunities)
            
            # 4. 자소서 팁 및 결과 생성
            coach = CoverLetterCoachAgent()
            recommendations = coach.run(matched_profiles)
            
            # 최종 텍스트웹 화면에 응답 (크롤링된 마크다운 결과물 출력)
            self.wfile.write(recommendations.encode('utf-8'))
        except Exception as e:
            self.wfile.write(f"에러가 발생했습니다: {e}".encode('utf-8'))
        return