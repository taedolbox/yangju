import streamlit as st

def main():
    menu_options = [
        "메뉴 선택",
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    selected_menu = st.selectbox("", menu_options, key="menu_selector")

    # 콤보박스 테두리 및 선택된 텍스트 파란색 스타일
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

    # 선택 메뉴별로 아래에 링크 또는 내용 표시
    if selected_menu == "메뉴 선택":
        st.write("")  # 빈칸
    elif selected_menu == "조기재취업수당":
        st.markdown(
            '<a href="https://example.com/early_reemployment" target="_blank" style="color:#007bff; font-weight:bold;">조기재취업수당 바로가기</a>',
            unsafe_allow_html=True
        )
    elif selected_menu == "일용직(건설일용포함)":
        st.markdown(
            '<a href="https://example.com/daily_worker" target="_blank" style="color:#007bff; font-weight:bold;">일용직(건설일용 포함) 바로가기</a>',
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
