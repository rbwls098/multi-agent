# Todo

## Phase 1: 기초 설정 및 환경 정비 ✅ (완료)
- [x] `sample_input.txt` 데이터 작성 및 연동
- [x] 채용 공고 데이터셋 준비 (로컬 Fallback용)
- [x] 프로젝트 구조 및 폴더 설정 완료
- [x] 환경 변수 예시 (`.env.example`) 작성 및 `.env` 설정 안내
- [x] `.gitignore` 업데이트: `docs/`(강의자료) 및 `weather/`(연습폴더) 제외 완료

## Phase 2: 에이전트 고도화 (5개 에이전트) ✅ (완료)
- [x] **InformationGatheringAgent**: 사람인 실시간 크롤링 및 날짜 필터링(2026년 기준) 구현 (`collector.py`)
- [x] **CompetencyAnalysisAgent**: 사용자 역량 파싱 및 직무 자동 분류 (`analyzer.py`)
- [x] **MatchingStrategyAgent**: 규칙 기반 점수 + LLM 정성 평가 결합 매칭 (`matcher.py`)
- [x] **CoverLetterCoachAgent**: LLM 기반 고도화된 자소서 작성 가이드 생성 로직 최적화 (`coach.py`)
- [x] **ReviewerAgent**: 에이전트 생성 결과물 최종 검토 및 정합성 확인 (`reviewer.py`)

## Phase 3: 시스템 통합 및 출력 최적화 ✅ (완료)
- [x] `my_agent.py` 통합 실행 스크립트 고도화 (에이전트 파이프라인 구조)
- [x] `output.md`: 핵심 데이터 추출 및 요약 표 생성
- [x] `output_user_guide.md`: 풍부한 상세 정보와 구체적 팁을 포함한 보고서 생성
- [x] `review_report.md`: 시스템 신뢰도 확보를 위한 검토 보고서 생성

## Phase 4: 문서화 및 최종 유지보수 ✅ (완료)
- [x] `GEMINI.md`, `AGENTS.md`, `context.md` 최신 상태로 업데이트
- [x] `README.md` 구조 개선 및 한글 인코딩 문제 해결
- [x] `llm_client.py` Streamlit Cloud & CLI 호환성 강화
- [x] GitHub 배포 및 실시간 서비스 안정화 확인

---

## 최종 점검 리스트 ✅
- [x] `python my_agent.py` 정상 실행 및 결과 도출 (2026년 공고 필터링 확인)
- [x] 출력 파일 3종 세트 정상 생성 및 내용 충실도 확인
- [x] API 키 노출 방지 및 보안 수칙 준수 (Streamlit Secrets 활용)
- [x] `.gitignore` 설정에 따른 불필요 파일 커밋 제외 확인
