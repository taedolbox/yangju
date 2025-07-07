import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")

    menus = ["메뉴 선택", "조기재취업수당", "일용직(건설일용포함)"]

    # URL 쿼리 파라미터에서 메뉴 인덱스 가져오기
    # st.query_params를 사용하여 읽기
    menu_param = st.query_params.get("menu", None) # Changed to get a single string or None

    default_idx = 0
    if menu_param and menu_param.isdigit():
        parsed_menu_idx = int(menu_param) - 1
        if 0 <= parsed_menu_idx < len(menus):
            default_idx = parsed_menu_idx

    st.markdown("""
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
    """, unsafe_allow_html=True)

    # st.selectbox의 index를 초기화하기 위해 selected_menu 변수 사용
    selected_menu = st.selectbox("📋 메뉴 선택", menus, index=default_idx, key="main_menu_select")

    # 선택된 메뉴명으로 인덱스 변환
    selected_idx = menus.index(selected_menu)

    # URL 쿼리 파라미터 업데이트
    # st.query_params를 사용하여 쓰기 (할당)
    if selected_idx == 0:
        if "menu" in st.query_params: # 메뉴 선택(첫 항목)이면 URL 쿼리파라미터 삭제
            del st.query_params["menu"]
    else:
        st.query_params["menu"] = str(selected_idx + 1)
    
    # 세션 상태에 마지막 선택된 인덱스 저장 (선택 사항이지만 일관성을 위해 유지)
    st.session_state.last_selected_idx = selected_idx

    # 메뉴별 화면 출력
    if selected_idx == 0:
        st.info("메뉴를 선택하세요.")
    elif selected_idx == 1:
        early_reemployment_app()
    elif selected_idx == 2:
        daily_worker_eligibility_app()

if __name__ == "__main__":
    main()
