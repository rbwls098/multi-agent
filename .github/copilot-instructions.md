# Copilot Instructions

이 저장소의 공통 작업 규칙은 루트의 `AGENTS.md`에 있다.

작업을 시작할 때 먼저 `AGENTS.md`, `context.md`, `todo.md`를 읽고 따른다.

## 프로젝트 개요

- **프로젝트**: 취업 안내 멀티에이전트
- **현재 진행**: Week 11 v0 완료 (함수 3개 구조)
- **주요 파일**: `career_agent.py`, `sample_career_profile.json`, `sample_data/opportunities.json`

## 기본 규칙

### 실행
- 기본 실행 명령: `python career_agent.py`
- 위치: `c:\multi-agent\` 디렉토리

### 개발 방식
- 파일을 수정하기 전에 먼저 **계획을 제시**한다.
- 한 번에 많은 파일을 바꾸지 않는다.
- 외부 패키지와 복잡한 프레임워크를 임의로 추가하지 않는다.
- Python 기본 코드로 시작해서 필요시에만 패키지 추가

### 기술 제약
- Playwright는 MCP가 아니라 CLI로만 사용한다.
- LangGraph, RAG, 복잡한 ML은 아직 사용하지 않음
- 외부 API는 모킹된 데이터로 먼저 구현

## 주요 파일

| 파일 | 용도 | 상태 |
|---|---|---|
| `career_agent.py` | 메인 에이전트 (3개 함수) | ✅ 완성 |
| `sample_career_profile.json` | 사용자 프로필 예시 | ✅ 완성 |
| `sample_data/opportunities.json` | 채용 공고 더미 데이터 | ✅ 완성 |
| `context.md` | 프로젝트 상세 문서 | ✅ 최신화 |
| `todo.md` | 작업 진행 상황 | ✅ 최신화 |

## Week 11 완료 사항

✅ 함수 3개 구조 완성
- `extract_profile()` - 사용자 프로필 추출
- `classify_user()` - 직무 분류 및 공고 매칭
- `write_recommendations()` - 추천안내문 작성

✅ 동작 확인
- 3명 사용자 프로필 테스트 완료
- 6개 채용 공고 매칭 완료
- 자소서 팁 생성 완료

## 다음 단계 (Week 12 ~)

기본 개선:
- 결과 파일 자동 저장
- CSV 입력 확장
- 매칭 알고리즘 개선

선택 확장:
- Groq API 연동
- 웹 폼 인터페이스
- 데이터베이스 저장
