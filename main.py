import streamlit as st

def main():
    st.title("메뉴 선택 앱")

    st.markdown(
        "<span style='color:#007bff; font-weight:700; font-size:18px;'>메뉴 선택</span>",
        unsafe_allow_html=True
    )

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

    # 콤보박스 테두리 파란색 스타일
    st.markdown(
        """
        <style>
        div[data-baseweb="select"] > div {
            border: 2px solid #007bff !important;
            border-radius: 6px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write(f"선택된 메뉴: {selected_menu}")

if __name__ == "__main__":
    main()
