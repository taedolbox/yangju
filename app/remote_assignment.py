import streamlit as st
from app.questions import get_remote_assignment_questions

def remote_assignment_app():
    st.subheader("🟠 원거리 발령에 따른 판단")
    questions = get_remote_assignment_questions()

    if "remote_step" not in st.session_state:
        st.session_state.remote_step = 0
        st.session_state.remote_answers = []

    if st.session_state.remote_step < len(questions):
        q = questions[st.session_state.remote_step]
        st.write(f"**Q{st.session_state.remote_step + 1}. {q}**")
        ans = st.radio("답변", ["예", "아니요"], key=f"remote_{st.session_state.remote_step}")
        if st.button("다음", key=f"next_remote_{st.session_state.remote_step}"):
            st.session_state.remote_answers.append(ans)
            if st.session_state.remote_step == 0 and ans == "아니요":
                st.warning("❌ 통근시간 조건 불충족으로 지급 불가")
                st.session_state.remote_step = len(questions)
            else:
                st.session_state.remote_step += 1
            st.rerun()
    else:
        st.success("✅ 조건 충족 가능. 서류 지참 후 고용센터 방문하여 판단 받으세요.")

    if st.button("처음으로", key="reset_remote"):
        st.session_state.remote_step = 0
        st.session_state.remote_answers = []
        st.rerun()