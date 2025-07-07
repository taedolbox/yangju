import streamlit as st

def main():
    st.title("메뉴 선택 앱")

    menu_options = [
        "메뉴 선택",
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    selected_menu = st.selectbox(
        "",
        menu_options,
        key="menu_selector"
    )

    # 콤보박스 테두리 및 글자색 파란색 스타일 적용
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

    st.write(f"선택된 메뉴: {selected_menu}")

if __name__ == "__main__":
    main()
