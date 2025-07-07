import streamlit as st

from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app

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
        layout="centered"
    )

    # 스타일 직접 삽입
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
        unsafe_allow_html=True,
    )

    # 👉 필요한 메뉴만 유지
    all_menus = [
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    menu_functions = {
        "조기재취업수당": early_reemployment_app,
        "일용직(건설일용포함)": daily_worker_eligibility_app
    }

    with st.sidebar:
        st.markdown("### 📋 메뉴 선택")

        # 세션 초기화
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
            st.session_state.selected_menu = default_menu if default_menu in all_menus else all_menus[0]

        selected_index = all_menus.index(st.session_state.selected_menu) if st.session_state.selected_menu in all_menus else 0
        selected_menu = st.selectbox(
            "",
            all_menus,
            index=selected_index,
            key="menu_selector",
            on_change=lambda: update_selected_menu(all_menus, all_menus)
        )

        if selected_menu != st.session_state.selected_menu:
            st.session_state.selected_menu = selected_menu
            menu_id = all_menus.index(selected_menu) + 1
            st.query_params["menu"] = str(menu_id)

        st.markdown("---")
        st.markdown("[📌 고용센터 찾기](https://www.work24.go.kr/cm/c/d/0190/retrieveInstSrchLst.do)")

    st.markdown("---")

    if st.session_state.selected_menu:
        menu_functions.get(
            st.session_state.selected_menu,
            lambda: st.info("메뉴를 선택하세요.")
        )()
    else:
        st.info("왼쪽에서 메뉴를 선택하세요.")

if __name__ == "__main__":
    main()
