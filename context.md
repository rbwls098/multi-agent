# 취업 안내 멀티에이전트 프로젝트

## 현재 상태 (Week 11 완료)

✅ **Week 11 v0 완성** - 함수 3개 구조로 기본 동작 확인됨

## 목표

사용자의 역량과 관심사를 분석하고, 공모전/인턴/정규직 채용 기회를 자동으로 수집한 뒤, 최적의 매칭을 제시하고 자소서 작성을 지원한다.

## 입력

**현재 (Week 11):**
- `sample_career_profile.json` - 사용자 프로필 3개 예시
- `sample_data/opportunities.json` - 채용 공고 6개 더미 데이터

**향후 (Week 12~):**
- CSV 파일 (Excel 호환)
- 웹 폼 입력
- 데이터베이스

**데이터 구조:**
- 개인정보 (이름, 학력)
- 경력 정보 (경력년수, 직무 경험)
- 기술 스택 (프로그래밍 언어, 도구, 프레임워크)
- 자격증 및 수상 경력
- 관심 분야 및 직무

## 출력

**현재 (Week 11):**
- 터미널 출력: 사용자별 추천 공고 및 자소서 팁

**향후:**
1. **career_opportunities.md** - 수집된 채용 기회 목록
2. **matched_recommendations.md** - 사용자별 맞춤형 추천 (우선순위 포함)
3. **cover_letter_feedback.md** - 각 기회별 자소서 작성 팁 및 검토
4. **analysis_report.md** - 역량 분석 리포트 및 보완 제안

## 에이전트 구조 (Week 11)

**3개 함수 구조:**

1. **extract_profile()**: 사용자 프로필 추출
   - sample_career_profile.json 파싱
   - 핵심 정보 추출 (이름, 경력, 기술, 관심사)
   - 출력: 정제된 프로필 리스트

2. **classify_user()**: 직무 분류 및 공고 매칭
   - 사용자 기술 & 공고 요구사항 매칭
   - 매칭 점수 계산 (기술, 관심사, 경력 기반)
   - 출력: 사용자별 매칭 공고 (상위 3개)

3. **write_recommendations()**: 추천안내문 작성
   - 사용자별 추천 공고 정렬
   - 분야별 자소서 작성 팁 제시
   - 출력: Markdown 형식의 최종 추천문

**향후 확장 (Week 12~):**
- LLM 기반 자소서 피드백
- 외부 API 연동 (실제 채용 공고)
- 데이터베이스 저장

## 파일 구조

```
c:\multi-agent\
├── career_agent.py                    # 메인 에이전트 (Week 11)
├── sample_career_profile.json         # 사용자 프로필 예시 3개
├── sample_data/
│   └── opportunities.json             # 채용 공고 더미 데이터 6개
├── context.md                         # 프로젝트 문서
├── todo.md                            # 작업 진행 상황
└── .github/
    └── copilot-instructions.md        # Copilot 규칙
```

## 제약 & 규칙

- Python 기본 코드로 시작 (외부 패키지 최소화)
- `career_agent.py` 하나에서 시작
- 실제 API 연동 전까지는 모킹된 데이터 사용
- 민감한 정보(API 키, 개인정보)는 `.env` 파일로 관리
- 한 번에 한 단계씩 개선 (과도한 기능 추가 금지)
