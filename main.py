import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app  # 필요 시 구현

# 페이지 설정
st.set_page_config(
    page_title="실업급여 지원 시스템",
    page_icon="💼",
    layout="centered"
)

# 헤더 크기 한 단계
st.header("💼 실업급여 지원 시스템")

# 메뉴 콤보박스
menu = st.selectbox(
    "메뉴 선택",
    ["조기재취업수당", "일용직(건설일용포함)"],
    index=0
)

if menu == "조기재취업수당":
    early_reemployment_app()
else:
    daily_worker_eligibility_app()

st.markdown("---")
st.caption("ⓘ 참고용입니다. 실제 판단은 고용센터의 공식 결과를 따르십시오.")
