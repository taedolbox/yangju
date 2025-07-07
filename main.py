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
        /* 콤보박스 외곽 테두리 */
        div[data-baseweb="select"] > div {
            border: 2px solid #007bff !important;
            border-radius: 6px !important;
        }

        /* 콤보박스 선택된 값 텍스트 색상 */
        div[data-baseweb="select"] span {
            color: #007bff !important;
            font-weight: 600;
        }

        /* 드롭다운 옵션들 텍스트 색상 */
        div[data-baseweb="select"] ul[role="listbox"] li {
            color: #007bff !important;
            font-weight: 600;
        }

        /* 드롭다운 옵션 마우스 오버 색상 */
        div[data-baseweb="select"] ul[role="listbox"] li:hover {
            background-color: #cce4ff !important;
            color: #004a99 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write(f"선택된 메뉴: {selected_menu}")

if __name__ == "__main__":
    main()
