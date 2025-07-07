import streamlit as st

def main():
    st.title("메뉴 선택 앱 (Radio 버튼)")

    menu_options = [
        "메뉴 선택",
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    selected_menu = st.radio(
        "메뉴를 선택하세요",
        menu_options,
        key="menu_selector",
        index=0
    )

    # 라디오 버튼 전체 글자색 파란색 스타일
    st.markdown(
        """
        <style>
        div.row-widget.stRadio > div {
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
