# Todo

## Phase 1: 기초 설정 ✅ (완료)
- [x] `sample_career_profile.json` 샘플 데이터 작성 (사용자 3명)
- [x] 모킹된 채용 공고 데이터셋 준비 (`sample_data/opportunities.json` - 공고 6개)
- [x] 프로젝트 구조 및 폴더 설정 완료
- [ ] 환경 변수 설정 (`.env.example` 작성) - 필요시 나중에

## Phase 2: 에이전트 구현 ✅ (완료 - 함수 3개)
- [x] 정보수집 에이전트 함수 구현 → `extract_profile()`
- [x] 역량 분석 에이전트 함수 구현 → `classify_user()` + 매칭 점수
- [x] 매칭 전략 에이전트 함수 구현 → `calculate_match_score()`
- [x] 자소서 코치 에이전트 함수 구현 → `write_recommendations()`

## Phase 3: 통합 및 출력 ✅ (완료 - Week 11 v0)
- [x] 전체 흐름을 실행하는 main 함수 작성
- [ ] 결과를 Markdown 파일로 자동 저장 (output/ 디렉토리)
- [x] 분석 리포트 및 추천 목록 생성 (터미널 출력)
- [x] 자소서 피드백 생성 (분야별 팁)

## Phase 4: 검증 및 문서화 (진행 중)
- [x] 실행 결과 검증 완료 (3명 사용자 정상 작동)
- [ ] README 작성 (사용 방법, API 연동 가이드)
- [ ] 테스트 케이스 작성
- [ ] 브라우저에서 결과 확인 (필요시 Playwright CLI 사용)

---

## Week 12 개선 사항 (선택)

### 기본 개선 (권장)
- [ ] 결과를 `output/career_recommendations.md` 파일로 자동 저장
- [ ] CSV 파일로 사용자 프로필 입력 받기 (career_agent.py 확장)
- [ ] 매칭 점수 알고리즘 개선 (가중치 세밀 조정)
- [ ] 박매니저처럼 매칭이 안 되는 경우 처리 (쿠팡 BD 공고 추가 또는 로직 개선)

### 확장 기능 (선택)
- [ ] Groq API 연동 (자소서 피드백 고도화)
- [ ] 외부 도구 API 1개 추가 (예: 채용 정보 수집)
- [ ] 웹 폼 인터페이스 추가 (Flask 또는 Streamlit)
- [ ] 데이터베이스 연결 (SQLite)

---

## Week 11 완료 체크리스트

- [x] 준비 파일 4개 확인 (copilot-instructions.md, context.md, todo.md 있음)
- [x] 일정공지 예시를 취업 안내 에이전트로 변환
- [x] `career_agent.py` 작성 완료
- [x] 외부 패키지 없이 실행 가능 (Python 기본만 사용)
- [x] 최소 3개 함수 역할별 분리 (extract, classify, write)
- [x] 중간 결과 출력 (Step 1, 2, 3)
- [x] `python career_agent.py` 실행 성공
- [x] context.md, todo.md, copilot-instructions.md 갱신
