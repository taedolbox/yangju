# main.py

import streamlit as st
from app.daily_worker_eligibility ipport daily_worker-eligibility_app
from app.early_reemployment import early_reemployment_app

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")

    menus = ["메뉴 선택", "조기재취업수당", "일용직(건설일용포함)"]

    # 1. 초기 메뉴 인덱스 결정 (URL 또는 세션 상태)
    menu_param_from_url = st.query_params.get("menu", None)

    if "current_menu_idx" not in st.session_state:
        if menu_param_from_url and menu_param_from_url.isdigit():
            parsed_menu_idx = int(menu_param_from_url) - 1
            if 0 <= parsed_menu_idx < len(menus):
                st.session_state.current_menu_idx = parsed_menu_idx
            else:
                st.session_state.current_menu_idx = 0
        else:
            st.session_state.current_menu_idx = 0

    # CSS 스타일
    st.markdown("""
    <style>
    /* 콤보박스 선택 영역 (현재 선택된 값 표시되는 부분) */
    div[data-baseweb="select"] > div:first-child {
        border: 2px solid #2196F3 !important; /* 기존 테두리 유지 */
        color: #2196F3 !important;             /* 기존 텍스트 색상 유지 */
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
        selected_menu_name = st.session_state.main_menu_select_key
        st.session_state.current_menu_idx = menus.index(selected_menu_name)

        if st.session_state.current_menu_idx == 0:
            if "menu" in st.query_params:
                del st.query_params["menu"] # "메뉴 선택" 시 URL 파라미터 제거
        else:
            st.query_params["menu"] = str(st.session_state.current_menu_idx + 1) # 선택된 메뉴의 인덱스를 URL 파라미터로 저장

    # 메뉴 선택 콤보박스
    st.selectbox(
        "📋 메뉴 선택",
        menus,
        index=st.session_state.current_menu_idx,
        key="main_menu_select_key",
        on_change=on_menu_change
    )

    # --- 동적 타이틀을 추가합니다 ---
    selected_menu_title = menus[st.session_state.current_menu_idx]
    
    if selected_menu_title == "메뉴 선택":
        # 초기 화면이므로 별도의 타이틀을 넣지 않거나, 환영 메시지 안에 포함
        pass 
    else:
        # 선택된 메뉴 이름으로 동적 타이틀 생성
        display_title = selected_menu_title + " 요건 판단" if selected_menu_title != "일용직(건설일용포함)" else "일용직(건설일용포함) 실업급여 요건 판단"
        st.markdown(
            f"<span style='font-size:22px; font-weight:600;'>🏗️ {display_title}</span>",
            unsafe_allow_html=True
        )

    # 모든 페이지에 공통으로 표시될 안내 문구
    st.markdown(
        "<p style='font-size:18px; font-weight:700; margin-bottom:10px;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )
    # --- 동적 타이틀 추가 종료 ---

    # 3. 세션 상태의 current_menu_idx에 따라 화면 출력
    selected_idx = st.session_state.current_menu_idx

    if selected_idx == 0:
        # "메뉴 선택" 시 보여줄 초기 화면 내용
        st.markdown("---") # 시각적 구분선 추가
        st.markdown(
            """
            <div style="padding: 20px; border-radius: 10px; background-color: #f0f8ff; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color: #0d47a1; margin-bottom: 15px;">🌟 실업급여 지원 시스템에 오신 것을 환영합니다!</h3>
                <p style="font-size: 16px; line-height: 1.6; color: #333333;">  이 시스템은 <b>실업급여 수급 자격</b> 및 <b>조기재취업수당</b>과 관련된 정보를 쉽고 빠르게 확인하실 수 있도록 돕습니다.
                    <br><br>
                    궁금한 기능을 위에 있는 <b>'📋 메뉴 선택' 콤보박스에서 선택</b>해 주세요.
                </p>
                <ul style="font-size: 15px; line-height: 1.8; margin-top: 15px; color: #333333;"> <li>🔹 <b>조기재취업수당:</b> 조기재취업수당 신청 가능 여부를 판단합니다.</li>
                    <li>🔹 <b>일용직(건설일용포함):</b> 일용직 근로자의 실업급여 신청 가능 시점을 판단합니다.</li>
                </ul>
                <p style="font-size: 14px; color: #555; margin-top: 20px;">
                    💡 <b>주의:</b> 본 시스템의 결과는 참고용이며, 최종적인 실업급여 수급 여부는 관할 고용센터의 판단에 따릅니다.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown("---") # 또 다른 시각적 구분선
    elif selected_idx == 1:
        early_reemployment_app() # 조기재취업수당 페이지 함수 호출
    elif selected_idx == 2:
        daily_worker_eligibility_app() # 일용직 페이지 함수 호출

if __name__ == "__main__":
    main()
