import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app

# 페이지 설정
st.set_page_config(
    page_title="실업급여 지원 시스템",
    page_icon="💼",
    layout="centered"
)

# 상단 메뉴 (필요 시 항목 추가)
menu = st.radio(
    "메뉴 선택",
    ["조기재취업수당", "일용직(건설일용포함)"],
    horizontal=True
)

# 메뉴별 기능 연결
if menu == "조기재취업수당":
    # early_reemployment_app()  # 추후 구현
    st.info("조기재취업수당 페이지 준비 중입니다.")
elif menu == "일용직(건설일용포함)":
    daily_worker_eligibility_app()

# 하단 참고문구
st.markdown("---")
st.caption("ⓘ 본 도우미는 참고용입니다. 실제 판단은 고용센터를 따르십시오.")
