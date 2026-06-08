import streamlit as st
import os
from my_agent import run_pipeline

# 13.5 Streamlit 화면 구성 가이드라인 준수

st.set_page_config(page_title="커리어 에이전트 - Week 13", layout="wide")

st.title("🚀 커리어 매칭 에이전트 (13주차 표준)")
st.markdown("""
입력 자료를 바탕으로 정보를 추출하고, 맞춤형 가이드 작성 및 검토를 수행합니다.
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
        tab1, tab2, tab3 = st.tabs(["📊 추출/분류 결과", "📝 맞춤형 안내문", "🔍 검토 보고서"])
        
        with tab1:
            st.markdown("### 12주차 기반 정보 추출")
            st.json(profile)
            st.info("파일 저장 위치: output.md")
            
        with tab2:
            st.markdown("### 최종 사용자 가이드")
            st.markdown(guides)
            st.info("파일 저장 위치: output_user_guide.md")
            
        with tab3:
            st.markdown("### 에이전트 검토 결과")
            st.markdown(review)
            st.warning("⚠️ 이 보고서는 AI 검토자의 의견이며 최종 확인은 사용자의 몫입니다.")
            st.info("파일 저장 위치: review_report.md")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 에이전트 워크플로우")
    st.info("""
    **결과 도출 과정:**
    1. **정보 추출**: 입력된 텍스트에서 이름, 경력, 기술 등을 AI가 분석합니다.
    2. **공고 수집/분류**: 추출된 키워드를 바탕으로 실제 채용 사이트에서 공고를 가져와 직무별로 나눕니다.
    3. **가이드 작성**: 분석된 데이터로 맞춤형 추천 및 주의사항 안내문을 작성합니다.
    4. **AI 검토**: 작성된 안내문에 누락된 정보나 잘못된 표현이 없는지 최종 점검합니다.
    """)
    
    st.header("💡 입력 가이드")
    st.markdown("""
    **어떤 내용을 넣어야 하나요?**
    - 자신의 성함
    - 실무 경력 (년수)
    - 보유 중인 기술 스택 (예: Python, Java, Figma)
    - 관심 있는 직무나 분야
    
    **어떻게 입력해야 하나요?**
    - 문장형으로 자유롭게 적으시거나, 항목별로 나열해도 AI가 잘 이해합니다.
    """)
    
    if os.path.exists(".env"):
        st.success("✅ API 키 로드됨")
    else:
        st.error("❌ API 키가 없습니다. .env 파일을 확인해주세요.")
