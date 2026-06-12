# 취업 안내 멀티에이전트 시스템

사용자의 역량과 관심사를 분석하여 최적의 채용 공고를 추천하고, 맞춤형 자기소개서 작성 가이드를 제공하는 지능형 멀티에이전트 시스템입니다.

## 🚀 주요 기능
- **실시간 정보 수집**: 사람인(Saramin) 사이트 크롤링 및 로컬 데이터 Fallback 지원
- **사용자 역량 분석**: 기술 스택 및 경력 기반의 정교한 직무 분류
- **지능형 매칭**: 규칙 기반 점수화와 LLM의 정성 평가를 결합한 최적화된 매칭 전략
- **맞춤형 코칭**: 공고별 핵심 키워드 및 자소서 작성 팁 자동 생성
- **자가 검토 시스템**: `ReviewerAgent`를 통한 결과물의 품질 및 정합성 최종 검증

## 🛠️ 실행 방법
1. **환경 설정**:
   - `.env.example` 파일을 참고하여 `.env` 파일을 생성하고 `OPENAI_API_KEY`를 설정합니다.
   - 필요 시 `GROQ_API_KEY`를 추가로 설정할 수 있습니다.
2. **의존성 설치**:
   ```bash
   pip install -r requirements.txt
   ```
3. **시스템 실행**:
   ```bash
   python my_agent.py
   ```

## 📂 파일 구조
- `my_agent.py`: 전체 에이전트 워크플로우를 제어하는 메인 스크립트
- `collector.py`: 정보수집 에이전트 클래스
- `analyzer.py`: 역량 분석 에이전트 클래스
- `matcher.py`: 매칭 전략 에이전트 클래스
- `coach.py`: 자소서 코치 에이전트 클래스
- `reviewer.py`: 검토자 에이전트 클래스
- `sample_input.txt`: 사용자 프로필 데이터 (JSON)
- `output.md`: 결과 요약 보고서
- `output_user_guide.md`: 사용자 맞춤 가이드
- `review_report.md`: 에이전트 품질 검토 보고서

## 🤖 에이전트 구성
| 역할 | 클래스명 | 설명 |
|---|---|---|
| 정보 수집 | `InformationGatheringAgent` | 사람인 크롤링 및 로컬 데이터 수집 |
| 역량 분석 | `CompetencyAnalysisAgent` | 프로필 분석 및 직무 유형 분류 |
| 매칭 전략 | `MatchingStrategyAgent` | 정적/동적 평가를 통한 최적 공고 매칭 |
| 자소서 코치 | `CoverLetterCoachAgent` | 맞춤형 작성 팁 및 피드백 생성 |
| 검토자 | `ReviewerAgent` | 최종 결과물의 신뢰도 검증 |

## ⚠️ 주의 사항
- `docs/` (강의 자료) 및 `weather/` (연습용 폴더)는 `.gitignore`에 등록되어 있어 버전 관리에서 제외됩니다.
- 실시간 크롤링은 웹사이트 구조 변경에 따라 동작이 달라질 수 있으며, 이 경우 로컬 데이터를 활용합니다.
