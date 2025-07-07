import sys
import os
sys.path.append(os.path.abspath('.'))

import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")

    # 📌 CSS 임포트
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # 메뉴
    all_menus = ["일용직(건설일용포함)"]
    selected = st.sidebar.radio("메뉴 선택", all_menus)

    if selected == "일용직(건설일용포함)":
        daily_worker_eligibility_app()
    else:
        st.write("준비 중")

if __name__ == "__main__":
    main()
