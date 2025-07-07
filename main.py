import streamlit as st

from app.early_reemployment import early_reemployment_app
from app.daily_worker_eligibility import daily_worker_eligibility_app

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    # ✅ 콤보박스 테두리 & 선택값 색상 파란색 CSS
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] > div {
            border: 2px solid #007bff !important;
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

    # ✅ 콤보박스 옵션
    menu_options = [
        "메뉴 선택",
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    selected_menu = st.selectbox(
        label="",
        options=menu_options,
        index=0
    )

    # ✅ 메뉴에 따라 앱 함수 연결
    if selected_menu == "조기재취업수당":
        early_reemployment_app()
    elif selected_menu == "일용직(건설일용포함)":
        daily_worker_eligibility_app()
    # "메뉴 선택"이면 아무것도 실행 안 함

if __name__ == "__main__":
    main()

