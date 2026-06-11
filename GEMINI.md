# GEMINI.md

이 저장소의 공통 작업 규칙은 루트의 `AGENTS.md`에 있다. 작업을 시작할 때 먼저 `AGENTS.md`, `context.md`, `todo.md`를 읽고 따른다.

## 요약

- **기본 실행 명령**: `python my_agent.py`
- **입력 파일**: `sample_input.txt` (사용자 프로필, JSON 형식)
- **출력 디렉토리**: `output/` 및 루트 디렉토리의 Markdown 파일들
- **주요 출력 파일**:
  - `output.md`: 분석된 정보 요약 표
  - `output_user_guide.md`: 맞춤형 채용 추천 및 자소서 팁
  - `review_report.md`: 에이전트 자가 검토 보고서
- **파일 수정 규칙**: 수정 전 계획 제시, 소규모 변경 지향, 외부 패키지 최소화
- **버전 관리 제외**: `docs/`(강의 자료), `weather/`(연습 폴더)는 `.gitignore`에 등록되어 관리 대상에서 제외됨

## 에이전트 간 데이터 흐름 (5개 에이전트 구조)

```
사용자 프로필 (JSON, sample_input.txt)
    ↓
[InformationGatheringAgent] (collector.py) → 실시간 채용 정보 수집 (사람인 크롤링 + 로컬 Fallback)
    ↓
[CompetencyAnalysisAgent] (analyzer.py) → 사용자 역량 분석 및 직무 분류
    ↓
[MatchingStrategyAgent] (matcher.py) → 규칙 + LLM 기반 적합도 산출 및 매칭
    ↓
[CoverLetterCoachAgent] (coach.py) → 맞춤형 자소서 작성 팁 생성
    ↓
[ReviewerAgent] (reviewer.py) → 최종 결과물 품질 및 정합성 검토
    ↓
최종 Markdown 출력 (output.md, output_user_guide.md, review_report.md)
```

## 개발 및 오류 방지 설정

1. **환경 변수**: `.env` 파일에 `OPENAI_API_KEY` (필수) 및 `GROQ_API_KEY` (선택) 설정 필요.
2. **의존성**: `pip install -r requirements.txt`로 필요한 패키지(requests, beautifulsoup4, python-dotenv, openai 등) 설치.
3. **Fallback 메커니즘**: 네트워크 또는 API 오류 발생 시 `sample_data/opportunities.json` 등의 로컬 데이터를 사용하도록 설계됨.
4. **Git 주의사항**: `docs/` 및 `weather/` 폴더는 로컬 작업용이므로 커밋하지 않도록 주의.
