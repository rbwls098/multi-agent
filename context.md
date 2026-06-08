# 취업 안내 멀티에이전트 프로젝트

## 현재 상태 (Week 14 최종 완료)

✅ **Week 14 최종 완성** - 5개 에이전트 클래스 구조로 고도화 및 최종 제출 요건 충족

## 목표

사용자의 역량과 관심사를 분석하고, 채용 사이트(사람인)에서 실시간으로 채용 기회를 수집한 뒤, 규칙과 LLM을 결합한 최적의 매칭을 제시하고 맞춤형 자소서 팁을 제공한다. 최종적으로 에이전트가 생성한 결과물을 스스로 검토하여 신뢰도를 확보한다.

## 입력

- `sample_input.txt` - 사용자의 프로필 (JSON 형식)

## 출력

1. **output.md** - 핵심 정보 추출 결과 요약 표
2. **output_user_guide.md** - 사용자별 맞춤형 추천 및 자소서 팁
3. **review_report.md** - 에이전트 자가 검토 보고서

## 에이전트 구조 (최종)

**5개 에이전트 클래스 구조:**

1. **InformationGatheringAgent**: 채용 정보 수집
   - 사람인 웹사이트 실시간 크롤링 (Requests/BS4)
   - 실패 시 로컬 데이터(opportunities.json) 활용 (Fallback)

2. **CompetencyAnalysisAgent**: 사용자 역량 분석
   - 입력 프로필 파싱 및 직무 유형 분류

3. **MatchingStrategyAgent**: 매칭 전략 수립
   - 규칙 기반 점수와 LLM 정성 평가 점수를 결합하여 적합도 산출

4. **CoverLetterCoachAgent**: 자소서 코칭
   - 매칭된 공고별 맞춤형 작성 팁 및 안내문 생성

5. **ReviewerAgent**: 최종 검토
   - 생성된 결과물의 품질, 매칭 정합성, Markdown 형식 준수 여부 검토

## 파일 구조

```
c:\multi-agent\
├── my_agent.py                        # 메인 실행 파일 (최종)
├── collector.py                       # 정보 수집 에이전트
├── analyzer.py                        # 역량 분석 에이전트
├── matcher.py                         # 매칭 전략 에이전트
├── coach.py                           # 자소서 코치 에이전트
├── reviewer.py                        # 검토자 에이전트
├── sample_input.txt                   # 입력 데이터
├── README.md                          # 프로젝트 설명서
├── context.md                         # 프로젝트 목표 및 구조
├── todo.md                            # 작업 진행 내역
├── tool_usage_log.md                  # 도구 사용 기록
├── presentation.md                    # 발표 자료
└── .env.example                       # 환경변수 예시
```

## 제약 & 규칙

- `python my_agent.py` 명령어로 전체 프로세스 실행
- 외부 API 실패 시에도 기본 동작이 가능하도록 Fallback 로직 유지
- 모든 결과물은 Markdown 형식으로 저장
