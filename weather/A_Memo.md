# A. 직접 만든 MCP 서버 제출물 메모

## 1. 사용한 핵심 프롬프트 (Core Prompts)

- "weather_server.py에 도시 이름을 받아 OpenWeatherMap Current Weather API로 날씨를 조회하는 함수 `fetch_weather(city)`를 만들어줘. requests.get()에 timeout=10을 넣고 404, 401 오류를 구분해 줘."
- "이 프로젝트 기능 중 입출력을 분리해서 `fetch_weather()`(요청 담당)과 `parse_weather_response()`(응답 데이터 추출 담당)로 분할해줘."
- "네트워크/서버 응답 시간 초과와 같은 일시적 문제에 대비해 최대 2회까지 time.sleep(1)을 주고 재시도하는 로직을 추가해 줘. 그리고 에디터에서 볼 수 있도록 최소 수준으로 info, warning 로그를 남겨 줘."

## 2. 짧은 메모 (Short Memo)

- **어떤 에러 처리를 넣었는가**:
  - `API_KEY`가 없을 때 서버 구동 시점에 Fail-fast하도록 `ValueError` 예외 추가
  - HTTP 상태 코드(`401`, `404`)에 따른 명확한 에러 반환
  - `requests.exceptions.Timeout`, `requests.exceptions.ConnectionError`을 특정하여 일시적인 네트워크 오류에 대해 `time.sleep(1)`과 함께 2회 재시도(Retry)하는 루프 구조 구현
- **로그에 무엇을 남겼는가**:
  - 요청 시작 (`city` 인자) 확인
  - 요청 성공 시의 완료 여부 로깅
  - 실패 시 에러 사유 로깅 (민감한 `API_KEY`나 긴 JSON 응답 대신 결과 `{ "error": "사유" }` 형태만 로깅)
- **Copilot이 제안한 것 중 무엇을 수정했는가**:
  - 모든 예외를 `except Exception as e:`로 뭉뚱그리려는 경향을 세부적인 Exception(TimeOut, Connection, 등)으로 나누어 수정함.
  - Python 표준 로깅 방식을 따라 f-string을 `logger.info("... %s", var)` 스타일로 리팩토링함.

---
*(참고: 정상 동작 스크린샷과 오류 발생 스크린샷 2장은 사용자가 별도로 이 폴더에 캡처하여 이미지 파일로 추가해야 합니다.)*
