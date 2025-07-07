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
        div[data-baseweb="select"] {
            border: 2px solid #2196F3 !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="select"]:focus-within {
            border: 2px solid #0d47a1 !important;
            box-shadow: 0 0 0 2px rgba(33,150,243,0.3);
        }
        .menu-label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-label">'
        '<img src="https://cdn-icons-png.flaticon.com/512/54/54712.png" width="24"/>'
        '<span>메뉴 선택</span>'
        '</div>',
        unsafe_allow_html=True
    )

    selected_menu = st.selectbox(
        label="",  # 👉 라벨 제거
        options=["조기재취업수당", "일용직(건설일용포함)"],
        index=0
    )

    if selected_menu == "조기재취업수당":
        early_reemployment_app()
    else:
        daily_worker_eligibility_app()

    st.markdown("---")
    st.caption("ⓘ 참고용입니다. 실제 판단은 고용센터의 공식 결과를 따르십시오.")

if __name__ == "__main__":
    main()
