import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app  # 조기재취업수당 페이지용

# 페이지 설정
st.set_page_config(
    page_title="실업급여 지원 시스템",
    page_icon="💼",
    layout="centered"
)

# 상단 헤더를 한 단계 작게
st.header("💼 실업급여 지원 시스템")

# 메뉴 선택을 콤보박스(selectbox)로 변경
menu = st.selectbox(
    "메뉴 선택",
    ["조기재취업수당", "일용직(건설일용포함)"],
    index=0
)

# 메뉴별 기능 연결
if menu == "조기재취업수당":
    early_reemployment_app()
elif menu == "일용직(건설일용포함)":
    daily_worker_eligibility_app()

# 하단 참고문구
st.markdown("---")
st.caption("ⓘ 본 도우미는 참고용입니다. 실제 판단은 고용센터의 공식 결과를 따르십시오.")
