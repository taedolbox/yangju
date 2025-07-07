import sys
import os

# 작업 경로를 sys.path에 추가 (현재 폴더)
sys.path.append(os.path.abspath("."))

import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app  # 필요시 사용

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="wide"
    )

    # 메뉴 리스트
    all_menus = [
        "조기재취업수당",
        "일용직(건설일용포함)"
    ]

    # 메뉴별 함수 매핑
    menu_functions = {
        "조기재취업수당": early_reemployment_app,
        "일용직(건설일용포함)": daily_worker_eligibility_app
    }

    # 상단 메뉴 표시
    selected_menu = st.selectbox("📋 메뉴 선택", all_menus)

    st.markdown("---")

    # 선택된 메뉴에 맞는 함수 실행
    if selected_menu in menu_functions:
        menu_functions[selected_menu]()
    else:
        st.info("메뉴를 선택하세요.")

if __name__ == "__main__":
    main()
