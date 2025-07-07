import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app
from app.early_reemployment import early_reemployment_app

def main():
    st.set_page_config(
        page_title="실업급여 지원 시스템",
        page_icon="💼",
        layout="centered"
    )

    st.markdown(
        """
        <style>
        .custom-select {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            background: #f0f4f8 url('https://cdn-icons-png.flaticon.com/512/54/54712.png') no-repeat 8px center;
            background-size: 20px 20px;
            border: 2px solid #2196F3;
            border-radius: 6px;
            padding: 8px 12px 8px 40px;
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
        }
        .custom-select:focus {
            border-color: #0d47a1;
            outline: none;
            box-shadow: 0 0 0 2px rgba(33,150,243,0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    selected_menu = st.selectbox(
        label="",
        options=["조기재취업수당", "일용직(건설일용포함)"],
        index=0,
        key="menu_selector"
    )

    if selected_menu == "조기재취업수당":
        early_reemployment_app()
    else:
        daily_worker_eligibility_app()

    st.markdown("---")
    st.caption("ⓘ 참고용입니다. 실제 판단은 고용센터의 공식 결과를 따르십시오.")

if __name__ == "__main__":
    main()
