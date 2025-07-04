import streamlit as st
from app.questions import get_employment_questions, get_self_employment_questions

def early_reemployment_app():
    st.subheader("🟢 조기재취업수당 요건 판단")

    if "early_step" not in st.session_state:
        st.session_state.early_step = 0
        st.session_state.early_answers = []
        st.session_state.employment_type = None
        st.session_state.early_questions = []
        st.session_state.show_results = False

    # First question
    if st.session_state.early_step == 0:
        q = "새 일자리가 일반 회사 취업인가요, 자영업/특수고용직(예: 예술인, 노무제공자)인가요?"
        st.write(f"**질문: {q}**")
        ans = st.radio("답변", ["일반 회사 취업", "자영업/특수고용직/예술인"], key="early_q0")
        if st.button("다음", key="early_next_0"):
            st.session_state.employment_type = ans
            st.session_state.early_answers.append(ans)
            st.session_state.early_questions = get_employment_questions() if ans == "일반 회사 취업" else get_self_employment_questions()
            st.session_state.early_step += 1
            st.rerun()
    elif st.session_state.early_step <= len(st.session_state.early_questions):
        q_idx = st.session_state.early_step - 1
        q = st.session_state.early_questions[q_idx]
        # Debugging output
        st.write(f"**디버깅**: 경로: {st.session_state.employment_type}, "
                 f"문항 수: {len(st.session_state.early_questions)}, "
                 f"early_step: {st.session_state.early_step}, "
                 f"현재 문항: {q}, "
                 f"답변: {st.session_state.early_answers}")
        st.write(f"**Q{st.session_state.early_step}: {q}**")
        ans = st.radio("답변", ["예", "아니요"], key=f"early_q{st.session_state.early_step}")
        if st.button("다음", key=f"early_next_{st.session_state.early_step}"):
            st.session_state.early_answers.append(ans)
            st.session_state.early_step += 1
            st.rerun()
    elif not st.session_state.show_results:
        st.write("**모든 문항에 답변하였습니다. 결과를 확인하려면 아래 버튼을 클릭하세요.**")
        if st.button("결과 보기", key="early_show_result"):
            st.session_state.show_results = True
            st.rerun()
    else:
        questions = st.session_state.early_questions
        answers = st.session_state.early_answers[1:]  # Exclude first answer (employment type)
        if st.session_state.employment_type == "일반 회사 취업":
            required_answers = ["예", "예", "예", "예", "아니요", "아니요", "아니요", "아니요", "아니요", "아니요"]
        else:
            required_answers = ["예", "예", "예", "아니요", "예", "아니요"]

        mismatches = [
            (i + 1, q, a, r) for i, (q, a, r) in enumerate(zip(questions, answers, required_answers)) if a != r
        ]

        if not mismatches:
            st.success("✅ 질문에 대한 조건이 모두 충족하였습니다. 고용센터에 확인 및 청구를 진행하세요.")
        else:
            st.warning("❌ 아래 조건을 충족하지 못했습니다:")
            for i, q, a, r in mismatches:
                st.write(f"- Q{i+1}: {q} (답변: {a}, 요구: {r})")
            st.write("고용센터에 문의하여 추가 확인이 필요합니다.")

    if st.button("처음으로", key="early_reset"):
        for key in ["early_step", "early_answers", "employment_type", "early_questions", "show_results"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
