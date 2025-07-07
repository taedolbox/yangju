import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")

    # 메뉴 리스트 (조기재취업수당, 일용직(건설일용포함)만)
    menus = ["조기재취업수당", "일용직(건설일용포함)"]

    # 콤보박스에 메뉴 출력 (파란색 텍스트는 CSS로)
    menu_css = """
    <style>
    div[data-baseweb="select"] > div {
        border: 2px solid #2196F3 !important;
        color: #2196F3 !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] span {
        color: #2196F3 !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] ul[role="listbox"] li {
        color: #2196F3 !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] ul[role="listbox"] li:hover {
        background-color: #2196F3 !important;
        color: white !important;
    }
    </style>
    """
    st.markdown(menu_css, unsafe_allow_html=True)

    selected_menu = st.selectbox("📋 메뉴 선택", menus, index=0)

    if selected_menu == "조기재취업수당":
        early_reemployment_app()
    elif selected_menu == "일용직(건설일용포함)":
        daily_worker_eligibility_app()

if __name__ == "__main__":
    main()

