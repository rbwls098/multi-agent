import streamlit as st
import os
from my_agent import run_pipeline

# Streamlit 화면 구성 가이드라인 준수

st.set_page_config(page_title="AI 커리어 매칭 시스템", layout="wide")

st.title("🚀 AI 커리어 매칭 및 자소서 코칭 시스템")
st.markdown("""
사용자의 역량을 분석하여 최적의 채용 공고를 추천하고, 맞춤형 자소서 작성 가이드와 검토 보고서를 제공합니다.
""")

# 입력 섹션
st.subheader("📋 입력 자료")
st.markdown("""
**작성 예시:** 
> "저는 3년차 백엔드 개발자 홍길동입니다. Java와 Spring Boot를 주로 사용하며, 최근에는 대용량 트래픽 처리와 인프라 자동화에 관심이 많습니다."
""")
default_text = "이름: 홍길동\n경력: 5년차\n기술: Python, AWS, Docker\n관심분야: 인프라 엔지니어링, 백엔드"
input_text = st.text_area("위 예시를 참고하여 정보를 입력하세요:", value=default_text, height=150)

if st.button("에이전트 실행"):
    with st.spinner("에이전트들이 협업 중입니다..."):
        # 핵심 로직 호출
        profile, guides, review = run_pipeline(input_text)
        
        st.success("분석 완료!")
        
        # 결과 화면 출력 (3개 탭으로 구분)
        tab1, tab2, tab3 = st.tabs(["📊 역량 분석 결과", "📝 맞춤형 취업 가이드", "🔍 최종 검토 보고서"])
        
        with tab1:
            st.markdown("### 사용자 역량 정보 추출 및 분류")
            st.json(profile)
            st.info("파일 저장 위치: output.md")
            
        with tab2:
            st.markdown("### 맞춤형 커리어 전략 가이드")
            st.markdown(guides)
            st.info("파일 저장 위치: output_user_guide.md")
            
        with tab3:
            st.markdown("### 시스템 최종 품질 검토")
            st.markdown(review)
            st.warning("⚠️ 이 보고서는 AI 검토자의 의견이며 최종 확인은 사용자의 몫입니다.")
            st.info("파일 저장 위치: review_report.md")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 서비스 프로세스")
    st.info("""
    **결과 도출 과정:**
    1. **정보 추출**: 입력된 텍스트에서 이름, 경력, 기술 등을 AI가 정밀 분석합니다.
    2. **공고 수집/분류**: 추출된 키워드를 바탕으로 실시간 채용 공고를 수집하여 직무별로 분류합니다.
    3. **가이드 작성**: 분석된 데이터로 최적의 추천 공고와 상세 자소서 팁을 생성합니다.
    4. **AI 검토**: 생성된 모든 내용의 품질과 정합성을 최종 점검합니다.
    """)
    
    st.header("💡 입력 가이드")
    st.markdown("""
    **어떤 내용을 넣어야 하나요?**
    - 성함 및 실무 경력
    - 보유 기술 스택 (예: Python, Java, Figma)
    - 관심 있는 직무나 산업 분야
    
    **어떻게 입력해야 하나요?**
    - 문장형으로 자유롭게 적으시거나, 항목별로 나열해도 AI가 잘 이해합니다.
    """)
    
    # API 키 확인 로직
    has_api_key = False
    if "OPENAI_API_KEY" in st.secrets:
        has_api_key = True
    elif os.path.exists(".env"):
        with open(".env", "r") as f:
            if "OPENAI_API_KEY=" in f.read():
                has_api_key = True

    if has_api_key:
        st.success("✅ 시스템 정상 작동 중")
    else:
        st.error("❌ 설정 오류: API 키가 등록되지 않았습니다.")
