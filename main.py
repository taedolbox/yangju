import streamlit as st

# 필요한 모든 앱 함수와 질문 함수를 임포트합니다.
# 이 함수들은 'app' 폴더 안의 각 파일에서 가져옵니다.
from app.daily_worker_eligibility import daily_worker_eligibility_app_original_ui
from app.early_reemployment import early_reemployment_app
from app.questions import (
    get_employment_questions,
    get_daily_worker_eligibility_questions,
    get_self_employment_questions
)

# --- 메뉴 선택 및 URL 동기화 관련 함수 ---
def update_selected_menu(filtered_menus, all_menus):
    """
    사이드바 메뉴 선택 시 세션 상태를 업데이트하고 URL 쿼리 파라미터를 설정합니다.
    """
    selected_menu = st.session_state.menu_selector
    if selected_menu in filtered_menus:
        st.session_state.selected_menu = selected_menu
        # 메뉴 ID를 쿼리 파라미터로 설정하여 URL에 반영
        menu_id = all_menus.index(selected_menu) + 1
        st.query_params["menu"] = str(menu_id)

# --- Streamlit 앱의 메인 로직 함수 ---
def main():
    """
    Streamlit 앱의 메인 진입점 함수입니다.
    페이지 설정, CSS 적용, 사이드바 메뉴 및 메인 콘텐츠 표시를 담당합니다.
    """
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    # --- CSS 적용 ---
    try:
        with open("static/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("경고: 'static/styles.css' 파일을 찾을 수 없습니다. CSS 스타일이 적용되지 않을 수 있습니다.")

    # --- 전체 메뉴 목록 정의 ---
    all_menus = [
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    # --- 각 메뉴에 연결될 함수 매핑 ---
    # 이 부분이 중요합니다: '일용직(건설일용포함)' 메뉴에 'daily_worker_eligibility_app_original_ui' 함수를 연결합니다.
    menu_functions = {
        "조기재취업수당": early_reemployment_app,
        "일용직(건설일용포함)": daily_worker_eligibility_app_original_ui # <-- 이 함수 이름이 정확히 일치해야 합니다!
    }

    # --- 각 메뉴에 해당하는 질문 목록 정의 (검색 기능에 사용) ---
    all_questions = {
        "조기재취업수당": get_employment_questions() + get_self_employment_questions(),
        "일용직(건설일용포함)": get_daily_worker_eligibility_questions()
    }

    # --- 사이드바 구성 ---
    with st.sidebar:
        st.markdown("### 🔍 검색")
        search_query = st.text_input("메뉴 또는 질문을 검색하세요", key="search_query")

        # 검색 쿼리에 따라 메뉴 필터링
        filtered_menus = all_menus
        if search_query:
            search_query = search_query.lower()
            filtered_menus = [
                menu for menu in all_menus
                if search_query in menu.lower() or
                any(search_query in q.lower() for q in all_questions.get(menu, []))
            ]

        # 세션 상태 초기화 및 URL 쿼리 파라미터 처리
        if "selected_menu" not in st.session_state:
            query_params = st.query_params
            url_menu_id = query_params.get("menu", [None])[0]
            default_menu = None
            if url_menu_id:
                try:
                    menu_idx = int(url_menu_id) - 1
                    if 0 <= menu_idx < len(all_menus):
                        default_menu = all_menus[menu_idx]
                except ValueError:
                    pass
            st.session_state.selected_menu = default_menu if default_menu in all_menus else filtered_menus[0] if filtered_menus else None

        # 필터링된 메뉴를 라디오 버튼으로 표시
        if filtered_menus:
            selected_menu = st.radio(
                "📋 메뉴",
                filtered_menus,
                index=filtered_menus.index(st.session_state.selected_menu)
                if st.session_state.selected_menu in filtered_menus else 0,
                key="menu_selector",
                on_change=lambda: update_selected_menu(filtered_menus, all_menus)
            )
        else:
            st.warning("검색 결과에 해당하는 메뉴가 없습니다.")
            st.session_state.selected_menu = None

    st.markdown("---")

    # --- 메인 콘텐츠 영역: 선택된 메뉴에 따라 해당 함수 실행 ---
    if st.session_state.selected_menu:
        # 딕셔너리에 매핑된 함수를 호출합니다.
        menu_functions.get(
            st.session_state.selected_menu,
            lambda: st.info("메뉴를 선택하세요.") # 선택된 메뉴가 없거나 매핑되지 않았을 때 기본 메시지
        )()
    else:
        st.info("왼쪽 사이드바에서 메뉴를 선택하거나 검색어를 입력하세요.")

    st.markdown("---")
    st.caption("ⓒ 2025 실업급여 도우미는 도움을 드리기 위한 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.")
    st.markdown("[📌 고용센터 찾기](https://www.work24.go.kr/cm/c/d/0190/retrieveInstSrchLst.do)")

# --- 스크립트 실행 진입점 ---
if __name__ == "__main__":
    main()
