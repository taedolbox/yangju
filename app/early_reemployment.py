import streamlit as st
from app.questions import get_employment_questions, get_self_employment_questions

def early_reemployment_app():


    if "early_step" not in st.session_state:
        st.session_state.early_step = 0
        st.session_state.early_answers = []
        st.session_state.employment_type = None
        st.session_state.early_questions = []

    # 1단계: 취업 형태 선택
    if st.session_state.early_step == 0:
        q = "새 일자리가 일반 회사 취업인가요,\n자영업/특수고용직(예: 예술인, 노무제공자)인가요?"
        st.write(f"**{q}**")
        ans = st.radio(
            "선택하세요",
            ["일반 회사 취업", "자영업/특수고용직/예술인"],
            key="early_q0"
        )
        if st.button("➡️ 다음"):
            st.session_state.employment_type = ans
            st.session_state.early_answers.append(ans)
            st.session_state.early_questions = (
                get_employment_questions() if ans == "일반 회사 취업"
                else get_self_employment_questions()
            )
            st.session_state.early_step += 1
            st.rerun()

    # 2단계 이후 질문
    elif st.session_state.early_step <= len(st.session_state.early_questions):
        idx = st.session_state.early_step - 1
        q = st.session_state.early_questions[idx]
        st.write(f"**Q{st.session_state.early_step}. {q}**")
        ans = st.radio(
            "선택하세요",
            ["예", "아니요"],
            key=f"early_q{st.session_state.early_step}"
        )
        if st.button("➡️ 다음", key=f"early_next_{st.session_state.early_step}"):
            st.session_state.early_answers.append(ans)
            st.session_state.early_step += 1
            st.rerun()

    # 모든 질문 완료 → 바로 결과 표시
    else:
        answers = st.session_state.early_answers[1:]  # 첫번째는 employment type
        if st.session_state.employment_type == "일반 회사 취업":
            required = ["예", "예", "예", "예", "아니요", "아니요", "아니요", "아니요", "아니요", "아니요"]
            questions = get_employment_questions()
        else:
            required = ["예", "예", "예", "아니요", "예", "아니요"]
            questions = get_self_employment_questions()

        mismatches = [
            (i+1, q, a, r)
            for i, (q, a, r) in enumerate(zip(questions, answers, required))
            if a != r
        ]

        if not mismatches:
            st.success("✅ 모든 조건을 충족했습니다.\n고용센터에 문의하여 청구를 진행하세요.")
        else:
            st.warning("❌ 아래 조건이 충족되지 않았습니다:")
            for i, q, a, r in mismatches:
                st.write(f"- Q{i}: {q} (답변: {a} / 필요: {r})")
            st.info("위 조건에 대해 고용센터에 추가 문의가 필요할 수 있습니다.")

    if st.button("🔄 처음부터 다시 시작"):
        for key in ["early_step", "early_answers", "employment_type", "early_questions"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

