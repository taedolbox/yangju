import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app  # 만약 사용한다면

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )
    st.title("💼 실업급여 지원 시스템")

    menu = st.radio(
        "메뉴 선택",
        ["조기재취업수당", "일용직(건설일용포함)"],
        horizontal=True
    )

    if menu == "조기재취업수당":
        early_reemployment_app()
    else:
        daily_worker_eligibility_app()

    st.markdown("---")
    st.caption("ⓘ 참고용입니다. 실제 가능 여부는 고용센터 판단을 따르십시오.")

if __name__ == "__main__":
    main()
