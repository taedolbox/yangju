import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app

# 페이지 기본 세팅
st.set_page_config(
    page_title="실업급여 도우미",
    page_icon="🏗️",
    layout="centered",
)

# 상단 메뉴 - 선택 박스 대신 버튼 or 라디오 등으로 바꿔도 됩니다.
menu = st.selectbox(
    "메뉴 선택",
    ("일용근로자 수급자격 판단",),
    index=0
)

# 선택된 메뉴에 따라 함수 실행
if menu == "일용근로자 수급자격 판단":
    daily_worker_eligibility_app()

# 하단 고지 문구
st.markdown("---")
st.caption("ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터의 판단을 따릅니다.")
