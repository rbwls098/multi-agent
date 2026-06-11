# AGENTS.md

이 파일은 GitHub Copilot, Gemini CLI 등에서 공통으로 참고할 프로젝트 규칙이다.

## 프로젝트 개요

- **이름**: 취업 안내 멀티에이전트 시스템
- **목표**: 실시간 채용 정보 수집, 사용자 역량 분석, 최적 기회 추천 및 자소서 가이드 제공
- **메인 실행 파일**: `my_agent.py`
- **입력 데이터**: `sample_input.txt` (JSON 형식 사용자 프로필)
- **주요 출력**: `output.md`, `output_user_guide.md`, `review_report.md`

## 에이전트 역할 및 파일 매핑

1. **정보수집 에이전트 (`InformationGatheringAgent` / `collector.py`)**: 사람인 실시간 크롤링 및 로컬 데이터(Fallback) 수집
2. **역량 분석 에이전트 (`CompetencyAnalysisAgent` / `analyzer.py`)**: 사용자 프로필 분석 및 직무 분류
3. **매칭 전략 에이전트 (`MatchingStrategyAgent` / `matcher.py`)**: 규칙 기반 점수와 LLM 정성 평가를 결합한 매칭
4. **자소서 코치 에이전트 (`CoverLetterCoachAgent` / `coach.py`)**: 공고별 맞춤형 작성 팁 및 피드백 생성
5. **검토자 에이전트 (`ReviewerAgent` / `reviewer.py`)**: 생성된 모든 결과물의 품질 및 정합성 최종 검토

## 작업 가이드라인

1. **변경 전 계획 수립**: 모든 수정 전에는 먼저 의도를 설명하고 계획을 제시한다.
2. **최소 단위 수정**: 한 번에 한 가지 기능이나 파일만 수정하며, 대규모 리팩터링은 피한다.
3. **안정성 우선**: 네트워크 오류나 API 제한을 대비한 Fallback 로직을 유지한다.
4. **환경 설정**: API 키 등 민감 정보는 `.env` 파일에서 관리하며 절대 코드에 하드코딩하지 않는다.
5. **버전 관리**: `docs/`, `weather/` 폴더는 버전 관리에서 제외되어 있으므로 관련 파일이 스테이징되지 않도록 주의한다.

## 데이터 표준

- **내부 데이터 인터페이스**: Python `dict` 또는 `list`를 사용하여 에이전트 간 데이터를 전달한다.
- **최종 출력**: 모든 사용자 대상 결과물은 Markdown 형식을 준수한다.
