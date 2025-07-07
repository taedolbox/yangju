import streamlit as st

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    # ✅ 콤보박스 테두리 + 선택 텍스트 파란색 CSS
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
        key="menu_selector"
    )

    # ✅ 선택에 따라 링크만 표시
    if selected_menu == "조기재취업수당":
        st.markdown(
            '<a href="https://example.com/early_reemployment" target="_blank" style="color:#007bff; font-weight:bold;">조기재취업수당 바로가기</a>',
            unsafe_allow_html=True
        )
    elif selected_menu == "일용직(건설일용포함)":
        st.markdown(
            '<a href="https://example.com/daily_worker" target="_blank" style="color:#007bff; font-weight:bold;">일용직(건설일용 포함) 바로가기</a>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("ⓘ 참고용입니다. 실제 판단은 고용센터의 공식 결과를 따르십시오.")

if __name__ == "__main__":
    main()

