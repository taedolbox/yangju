import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")

    menus = ["메뉴 선택", "조기재취업수당", "일용직(건설일용포함)"]

    # 1. 초기 메뉴 인덱스 결정 (URL 또는 세션 상태)
    # URL 쿼리 파라미터에서 메뉴 인덱스 가져오기 (앱 최초 로드 시)
    menu_param_from_url = st.query_params.get("menu", None)
    
    # 세션 상태에 'current_menu_idx'가 없으면 URL 파라미터에서 초기값 설정
    if "current_menu_idx" not in st.session_state:
        if menu_param_from_url and menu_param_from_url.isdigit():
            parsed_menu_idx = int(menu_param_from_url) - 1
            if 0 <= parsed_menu_idx < len(menus):
                st.session_state.current_menu_idx = parsed_menu_idx
            else:
                st.session_state.current_menu_idx = 0 # 유효하지 않으면 기본값
        else:
            st.session_state.current_menu_idx = 0 # URL 파라미터 없으면 기본값
    
    # 스타일은 그대로 유지
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

    # 2. st.selectbox에서 값 변경 시 세션 상태 업데이트
    # on_change 콜백 함수 정의
    def on_menu_change():
        selected_menu_name = st.session_state.main_menu_select_key # key로 접근
        st.session_state.current_menu_idx = menus.index(selected_menu_name)
        
        # 메뉴 변경 시 URL 쿼리 파라미터도 업데이트 (옵션)
        # 이 부분은 즉시 화면 전환에 영향을 주지 않고, URL 공유 시 유용
        if st.session_state.current_menu_idx == 0:
            if "menu" in st.query_params:
                del st.query_params["menu"]
        else:
            st.query_params["menu"] = str(st.session_state.current_menu_idx + 1)

    # st.selectbox의 index를 현재 세션 상태 값으로 설정
    # on_change 콜백을 사용하여 선택 변경 시 세션 상태 업데이트
    st.selectbox(
        "📋 메뉴 선택", 
        menus, 
        index=st.session_state.current_menu_idx, # 현재 세션 상태에 따라 초기화
        key="main_menu_select_key", # 콜백에서 접근할 키
        on_change=on_menu_change # 변경 시 콜백 함수 실행
    )

    # 3. 세션 상태의 current_menu_idx에 따라 화면 출력
    selected_idx = st.session_state.current_menu_idx

    if selected_idx == 0:
        st.info("메뉴를 선택하세요.")
    elif selected_idx == 1:
        early_reemployment_app()
    elif selected_idx == 2:
        daily_worker_eligibility_app()

if __name__ == "__main__":
    main()
