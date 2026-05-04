import os
import time
import json
import logging
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 환경 변수 로드 (.env 파일에서 읽어오기)
load_dotenv()

# OpenWeatherMap API 키 가져오기
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not API_KEY:
    raise ValueError("OPENWEATHERMAP_API_KEY가 필요합니다. .env 파일을 확인해주세요.")

def fetch_weather(city: str) -> dict:
    """
    OpenWeatherMap API를 호출하여 지정된 도시의 날씨 데이터를 가져오는 함수 (HTTP 요청만 담당).
    
    Args:
        city (str): 날씨를 조회할 도시 이름 (예: "Seoul")
        
    Returns:
        dict: API에서 반환된 원본 JSON 응답 데이터
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 401:
                return {"error": "API 키가 유효하지 않습니다"}
            elif response.status_code == 404:
                return {"error": "도시를 찾을 수 없습니다"}

            response.raise_for_status()
            return response.json()

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            logger.warning(f"네트워크/타임아웃 오류 발생 (시도 {attempt + 1}/{max_retries + 1}): {e}")
            if attempt == max_retries:
                return {"error": "서버 응답 시간 초과 및 재시도 실패"}
            time.sleep(1)  # 짧은 대기 후 재시도
        except requests.exceptions.RequestException as e:
            return {"error": f"API 호출 중 네트워크 오류 발생: {str(e)}"}

def parse_weather_response(response: dict) -> dict:
    """
    OpenWeatherMap 원본 응답 JSON에서 필요한 정보만 추출하는 함수
    
    Args:
        response (dict): API에서 반환된 원본 JSON 데이터
        
    Returns:
        dict: 핵심 날씨 정보만 포함된 딕셔너리
    """
    if "error" in response:
        return response
        
    try:
        return {
            "temperature": response["main"]["temp"],
            "humidity": response["main"]["humidity"],
            "description": response["weather"][0]["description"]
        }
    except KeyError:
        return {"error": "응답 데이터에서 필수 항목을 찾을 수 없습니다"}

# MCP 서버 초기화
mcp = FastMCP("weather")

@mcp.tool()
def get_weather(city: str) -> str:
    """
    도시 이름을 입력받아 현재 온도, 습도, 날씨 상태 등의 정보를 반환합니다.
    에러 발생 시 JSON 형태로 에러 설명을 포함하여 반환합니다.
    
    Args:
        city (str): 날씨를 조회할 도시 이름 (예: "Seoul")
    """
    logger.info("weather request started: city=%s", city)
    
    weather_data = fetch_weather(city)
    result = parse_weather_response(weather_data)
    
    if "error" in result:
        logger.warning("weather request failed: city=%s, reason=%s", city, result['error'])
    else:
        logger.info("weather request successful: city=%s", city)
        
    # output 폴더 생성 및 저장 (스크립트 위치 기준)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, f"weather_result_{city}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    # JSON 형태로 결과 반환 (에러 역시 JSON 형태로 반환됨)
    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    # MCP 서버 실행
    mcp.run()
