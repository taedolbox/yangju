import streamlit as st

from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.daily_worker_eligibility_mobile import daily_worker_eligibility_mobile_app
from app.early_reemployment import early_reemployment_app
from app.questions import (
    get_employment_questions,
    get_self_employment_questions,
    get_daily_worker_eligibility_questions
)

def update_selected_menu(filtered_menus, all_menus):
    selected_menu = st.session_state.menu_selector
    if selected_menu in filtered_menus:
        st.session_state.selected_menu = selected_menu
        menu_id = all_menus.index(selected_menu) + 1
        st.query_params["menu"] = str(menu_id)

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="wide"
    )

    # ✅ styles.css 불러오기
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # ✅ 외부 폰트 Preload 추가
    st.markdown("""
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" as="style">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap">
    """, unsafe_allow_html=True)

    # ✅ user_agent 파라미터로 디바이스 구분
    user_agent = st.query_params.get("user_agent", [""])[0]

    if not user_agent:
        st.components.v1.html(
            """
            <script>
            const ua = navigator.userAgent;
            const url = new URL(window.location);
            if (!url.searchParams.has('user_agent')) {
                url.searchParams.set('user_agent', ua);
                window.location.href = url.toString();
            }
            </script>
            """,
            height=0,
        )
        st.info("디바이스 정보를 확인 중입니다. 잠시만 기다려주세요...")
        st.stop()

    is_mobile = False
    mobile_indicators = ["Android", "iPhone", "iPad", "iPod", "Mobile"]
    for indicator in mobile_indicators:
        if indicator in user_agent:
            is_mobile = True
            break

    all_menus = [
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    if is_mobile:
        menu_functions = {
            "조기재취업수당": early_reemployment_app,
            "일용직(건설일용포함)": daily_worker_eligibility_mobile_app
        }
    else:
        menu_functions = {
            "조기재취업수당": early_reemployment_app,
            "일용직(건설일용포함)": daily_worker_eligibility_app
        }

    all_questions = {
        "조기재취업수당": get_employment_questions() + get_self_employment_questions(),
        "일용직(건설일용포함)": get_daily_worker_eligibility_questions()
    }

    with st.sidebar:
        st.markdown("### 🔍 검색")
        search_query = st.text_input("메뉴 또는 질문을 검색하세요", key="search_query")

        filtered_menus = all_menus
        if search_query:
            search_query = search_query.lower()
            filtered_menus = [
                menu for menu in all_menus
                if search_query in menu.lower() or
                any(search_query in q.lower() for q in all_questions.get(menu, []))
            ]

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

        if filtered_menus:
            selected_menu = st.radio(
                "📋 메뉴",
                filtered_menus,
                index=filtered_menus.index(st.session_state.selected_menu)
                if st.session_state.selected_menu in filtered_menus else 0,
                key="menu_selector",
                on_change=lambda: update_selected_menu(filtered_menus, all_menus)
            )
            if selected_menu != st.session_state.selected_menu:
                st.session_state.selected_menu = selected_menu
                menu_id = all_menus.index(selected_menu) + 1
                st.query_params["menu"] = str(menu_id)
        else:
            st.warning("검색 결과에 해당하는 메뉴가 없습니다.")
            st.session_state.selected_menu = None

        st.markdown("---")
        st.markdown("[📌 고용센터 찾기](https://www.work24.go.kr/cm/c/d/0190/retrieveInstSrchLst.do)")

    st.markdown("---")

    if st.session_state.selected_menu:
        menu_functions.get(
            st.session_state.selected_menu,
            lambda: st.info("메뉴를 선택하세요.")
        )()
    else:
        st.info("왼쪽 사이드바에서 메뉴를 선택하거나 검색어를 입력하세요.")

if __name__ == "__main__":
    main()


