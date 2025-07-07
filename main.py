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

    # --- CSS 스타일 변경 ---
    st.markdown("""
    <style>
    /* 콤보박스 선택 영역 (현재 선택된 값 표시되는 부분) */
    div[data-baseweb="select"] > div:first-child {
        border: 2px solid #2196F3 !important; /* 기존 테두리 유지 */
        color: #2196F3 !important;           /* 기존 텍스트 색상 유지 */
        font-weight: 600 !important;
        background-color: #E3F2FD !important; /* 콤보박스 배경색 변경 (밝은 파랑) */
    }
    
    /* 콤보박스 내부 텍스트 (현재 선택된 값) */
    div[data-baseweb="select"] span {
        color: #2196F3 !important;
        font-weight: 600 !important;
    }
    
    /* 드롭다운 리스트 컨테이너 */
    div[data-baseweb="popover"] {
        z-index: 9999 !important; /* 다른 요소 위에 오도록 z-index 높임 */
        background-color: #FFFFFF !important; /* 드롭다운 배경색 하얀색으로 명확하게 */
        border: 1px solid #2196F3 !important; /* 테두리 추가 */
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important; /* 그림자 추가 */
    }

    /* 드롭다운 리스트 항목 */
    div[data-baseweb="select"] ul[role="listbox"] li {
        color: #2196F3 !important;
        font-weight: 600 !important;
        padding: 10px 15px !important; /* 패딩 조정 */
    }
    
    /* 드롭다운 리스트 항목 호버 시 */
    div[data-baseweb="select"] ul[role="listbox"] li:hover {
        background-color: #2196F3 !important;
        color: white !important;
    }
    
    /* 스크롤바 스타일링 (선택 사항, 깔끔하게 보이게) */
    div[data-baseweb="popover"]::-webkit-scrollbar {
        width: 8px;
    }
    div[data-baseweb="popover"]::-webkit-scrollbar-thumb {
        background-color: #bbdefb; /* 연한 파랑 */
        border-radius: 4px;
    }
    div[data-baseweb="popover"]::-webkit-scrollbar-track {
        background-color: #f1f1f1;
    }

    </style>
    """, unsafe_allow_html=True)

    # 2. st.selectbox에서 값 변경 시 세션 상태 업데이트
    def on_menu_change():
        selected_menu_name = st.session_state.main_menu_select_key # key로 접근
        st.session_state.current_menu_idx = menus.index(selected_menu_name)
        
        # 메뉴 변경 시 URL 쿼리 파라미터도 업데이트 (옵션)
        if st.session_state.current_menu_idx == 0:
            if "menu" in st.query_params:
                del st.query_params["menu"]
        else:
            st.query_params["menu"] = str(st.session_state.current_menu_idx + 1)

    # st.selectbox의 index를 현재 세션 상태 값으로 설정
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
