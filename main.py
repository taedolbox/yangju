import streamlit as st
import os

# 앱 모듈 불러오기
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app
from app.unemployment_recognition import unemployment_recognition_app

def load_css(file_name):
    """CSS 파일을 읽어 Streamlit에 적용"""
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    # 스타일 로드 및 상단 안내 텍스트
    load_css("static/styles.css")
    st.markdown('<div class="custom-header">실업급여 도우미</div>', unsafe_allow_html=True)

    # 메뉴 구성
    menus = ["메뉴 선택", "실업인정", "조기재취업수당", "일용직(건설일용포함)"]
    menu_titles = {
        "메뉴 선택": "실업급여 지원 시스템",
        "실업인정": "실업인정",
        "조기재취업수당": "조기재취업수당 요건 판단",
        "일용직(건설일용포함)": "일용직(건설일용포함)"
    }
    menu_functions = {
        "실업인정": unemployment_recognition_app,
        "조기재취업수당": early_reemployment_app,
        "일용직(건설일용포함)": daily_worker_eligibility_app
    }

    # URL 파라미터 초기화
    menu_param = st.query_params.get("menu", None)
    if "current_menu_idx" not in st.session_state:
        st.session_state.current_menu_idx = int(menu_param) - 1 if menu_param and menu_param.isdigit() else 0

    def on_menu_change():
        selected = st.session_state.main_menu_select_key
        st.session_state.current_menu_idx = menus.index(selected)
        if st.session_state.current_menu_idx == 0:
            st.query_params.clear()
        else:
            st.query_params["menu"] = str(st.session_state.current_menu_idx + 1)

    # 메뉴 선택 UI
    st.selectbox(
        "📋 메뉴 선택",
        menus,
        index=st.session_state.current_menu_idx,
        key="main_menu_select_key",
        on_change=on_menu_change
    )

    st.markdown("---")
    selected = menus[st.session_state.current_menu_idx]
    st.markdown(f"<span style='font-size:22px; font-weight:600;'>🏗️ {menu_titles[selected]}</span>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; font-weight:700;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 기능 실행
    if selected == "메뉴 선택":
        st.markdown("""
        <div style="background-color:#f0f8ff;padding:20px;border-radius:10px;">
            <h3 style="color:#0d47a1;">🌟 환영합니다! 아래에서 기능을 선택해 주세요.</h3>
            <ul style="font-size:15px;">
                <li>🔹 <b>실업인정</b>: 실업인정 신청 및 정보 확인</li>
                <li>🔹 <b>조기재취업수당</b>: 신청 가능 여부 판단</li>
                <li>🔹 <b>일용직</b>: 신청 가능 시점 확인</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        menu_functions[selected]()

if __name__ == "__main__":
    main()
