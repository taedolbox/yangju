import sys
import os

sys.path.append(os.path.abspath("."))

import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
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
    elif menu == "일용직(건설일용포함)":
        daily_worker_eligibility_app()

if __name__ == "__main__":
    main()
