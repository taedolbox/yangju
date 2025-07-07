import streamlit as st

from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app  # 없으면 이 줄 지워도 됨

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    st.header("💼 실업급여 지원 시스템")

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
    st.caption("ⓘ 참고용입니다. 실제 판단은 고용센터의 공식 결과를 따릅니다.")

if __name__ == "__main__":
    main()
