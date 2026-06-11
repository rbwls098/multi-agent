# 프로젝트 컨텍스트

## 현재 상태 (Week 14 최종 완료)

- ✅ **멀티에이전트 고도화**: 5개 에이전트 클래스 구조 (`InformationGathering`, `CompetencyAnalysis`, `MatchingStrategy`, `CoverLetterCoach`, `Reviewer`) 완성.
- ✅ **안정성 강화**: 실시간 크롤링 실패 시 로컬 데이터를 활용하는 Fallback 로직 구현.
- ✅ **검증 프로세스**: `ReviewerAgent`를 통한 최종 결과물 자가 검토 단계 추가.
- ✅ **환경 설정**: `.gitignore`를 통해 `docs/`(강의자료) 및 `weather/`(연습폴더)를 버전 관리에서 제외.

## 프로젝트 목표

사용자의 역량(기술 스택, 경력 등)과 관심사를 분석하여, 사람인 등 채용 사이트의 실시간 공고와 매칭하고 맞춤형 취업 전략(자소서 팁 등)을 제공하는 지능형 시스템 구축.

## 시스템 아키텍처 및 데이터 흐름

1. **입력**: `sample_input.txt` (사용자 프로필 JSON)
2. **처리 단계**:
    - **수집**: `collector.py`가 실시간/로컬 공고 수집.
    - **분석**: `analyzer.py`가 사용자 역량 파싱 및 분류.
    - **매칭**: `matcher.py`가 규칙 점수 + LLM 평가로 추천 순위 산출.
    - **코칭**: `coach.py`가 공고별 맞춤 자소서 가이드 생성.
    - **검토**: `reviewer.py`가 전체 결과의 일관성 및 품질 검수.
3. **출력**:
    - `output.md`: 추출 정보 요약.
    - `output_user_guide.md`: 사용자 맞춤 추천 가이드.
    - `review_report.md`: 에이전트 품질 검토 보고서.

## 주요 파일 구조

```
c:\multi-agent\
├── my_agent.py          # 메인 실행 스크립트 (통합 프로세스 제어)
├── collector.py         # 정보 수집 에이전트 클래스
├── analyzer.py          # 역량 분석 에이전트 클래스
├── matcher.py           # 매칭 전략 에이전트 클래스
├── coach.py             # 자소서 코치 에이전트 클래스
├── reviewer.py          # 검토자 에이전트 클래스
├── llm_client.py        # LLM(OpenAI/Groq) 연동 유틸리티
├── sample_input.txt     # 테스트용 사용자 프로필
├── .env                 # API 키 등 환경 변수 (로컬 전용)
├── .gitignore           # 버전 관리 제외 설정 (docs/, weather/ 포함)
└── output/              # 결과물 저장 디렉토리 (선택 사항)
```

## 실행 및 제약 사항

- **실행**: `python my_agent.py`
- **필수 설정**: `.env` 파일에 `OPENAI_API_KEY` 등록 필수.
- **의존성**: `requests`, `beautifulsoup4`, `python-dotenv`, `openai` 등 필요.
- **품질 관리**: `ReviewerAgent`의 검토 결과에 따라 결과물의 신뢰도를 판단함.
