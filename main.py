import streamlit as st

def main():
    menu_options = [
        "메뉴 선택",
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    selected_menu = st.selectbox("", menu_options, key="menu_selector")

    st.markdown(
        """
        <style>
        /* 콤보박스 테두리 파란색 */
        div[data-baseweb="select"] > div {
            border: 2px solid #007bff !important;
            border-radius: 6px !important;
        }

        /* 선택된 텍스트 색상 파란색 */
        div[data-baseweb="select"] span {
            color: #007bff !important;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
