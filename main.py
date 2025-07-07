import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered",
    )

    st.title("💼 실업급여 지원 시스템")
    st.sidebar.title("메뉴")
    menu = st.sidebar.radio("메뉴 선택", ["일용직(건설일용포함)"])

    if menu == "일용직(건설일용포함)":
        daily_worker_eligibility_app()

if __name__ == "__main__":
    main()
