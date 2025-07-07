import streamlit as st

from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    st.markdown(
        """
        <style>
        div[data-baseweb="select"] {
            border: 2px solid #2196F3 !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="select"] span {
            color: #007bff !important;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_menu = st.selectbox(
        label="",
        options=["조기재취업수당", "일용직(건설일용포함)"],
        index=0
    )

    if selected_menu == "조기재취업수당":
        early_reemployment_app()
    else:
        daily_worker_eligibility_app()

if __name__ == "__main__":
    main()

