import streamlit as st
from app.questions import get_wage_delay_questions

def wage_delay_app():
    st.subheader("🔴 임금 체불에 의한 판단")
    questions = get_wage_delay_questions()

    if "wage_step" not in st.session_state:
        st.session_state.wage_step = 0
        st.session_state.wage_answers = []

    if st.session_state.wage_step < len(questions):
        q = questions[st.session_state.wage_step]
        st.write(f"**Q{st.session_state.wage_step + 1}. {q}**")
        ans = st.radio("답변", ["예", "아니요"], key=f"wage_{st.session_state.wage_step}")
        if st.button("다음", key=f"next_wage_{st.session_state.wage_step}"):
            st.session_state.wage_answers.append(ans)
            if (st.session_state.wage_step == 0 or st.session_state.wage_step == 2) and ans == "아니요":
                st.warning("❌ 수급 요건이 부족할 수 있습니다.\n임금 체불을 명확히 입증하거나 추가 상담 필요.")
                st.session_state.wage_step = len(questions)
            else:
                st.session_state.wage_step += 1
            st.rerun()
    else:
        st.success("✅ 실업급여 수급 가능성이 있습니다.\n체불 입증 자료와 함께 고용노동청 또는 고용센터에 문의하세요.")

    if st.button("처음으로", key="reset_wage"):
        st.session_state.wage_step = 0
        st.session_state.wage_answers = []
        st.rerun()