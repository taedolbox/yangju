import streamlit as st
from datetime import date
from app.questions import get_employment_questions, get_self_employment_questions

def early_reemployment_app():
    # 👉 아이콘 및 제목 통일
    st.markdown(
        "<h2 style='font-size: 1.8em;'>🏗️ 조기재취업수당 요건 판단</h2>",
        unsafe_allow_html=True
    )

    # ▶️ 상태 초기화
    if "early_step" not in st.session_state:
        st.session_state.early_step = 0
        st.session_state.early_answers = []
        st.session_state.employment_type = None
        st.session_state.early_questions = []
        st.session_state.report_date = None
        st.session_state.reemployment_date = None

    # ▶️ 1단계: 기본 입력 정보
    if st.session_state.early_step == 0:
        st.markdown("### 📋 기본 정보 입력")

        col1, col2 = st.columns(2)
        with col1:
            report_date = st.date_input(
                "📅 실업 신고일",
                value=date.today()
            )
        with col2:
            reemployment_date = st.date_input(
                "📅 재취업 날짜",
                value=date.today()
            )

        st.markdown("#### 📌 취업 형태 선택")
        employment_type = st.radio(
            "",
            ["일반 회사 취업", "자영업/특수고용직/예술인"]
        )

        if st.button("➡️ 다음"):
            st.session_state.report_date = report_date
            st.session_state.reemployment_date = reemployment_date
            st.session_state.employment_type = employment_type
            st.session_state.early_answers.append(employment_type)
            st.session_state.early_questions = (
                get_employment_questions() if employment_type == "일반 회사 취업"
                else get_self_employment_questions()
            )
            st.session_state.early_step += 1
            st.rerun()

    # ▶️ 2단계: 조건 질문 흐름
    elif st.session_state.early_step <= len(st.session_state.early_questions):
        idx = st.session_state.early_step - 1
        q = st.session_state.early_questions[idx]
        st.markdown(f"### ✅ Q{st.session_state.early_step}. {q}")
        ans = st.radio(
            "선택하세요",
            ["예", "아니요"],
            key=f"early_q{st.session_state.early_step}"
        )
        if st.button("➡️ 다음", key=f"early_next_{st.session_state.early_step}"):
            st.session_state.early_answers.append(ans)
            st.session_state.early_step += 1
            st.rerun()

    # ▶️ 3단계: 결과 자동 출력
    else:
        answers = st.session_state.early_answers[1:]  # 첫번째는 취업 형태
        if st.session_state.employment_type == "일반 회사 취업":
            required = ["예", "예", "예", "예", "아니요", "아니요", "아니요", "아니요", "아니요", "아니요"]
            questions = get_employment_questions()
        else:
            required = ["예", "예", "예", "아니요", "예", "아니요"]
            questions = get_self_employment_questions()

        st.markdown("### 📄 입력 정보")
        st.write(f"**📅 실업 신고일:** `{st.session_state.report_date}`")
        st.write(f"**📅 재취업 날짜:** `{st.session_state.reemployment_date}`")
        st.write(f"**📌 취업 형태:** `{st.session_state.employment_type}`")

        mismatches = [
            (i+1, q, a, r)
            for i, (q, a, r) in enumerate(zip(questions, answers, required))
            if a != r
        ]

        st.markdown("---")

        if not mismatches:
            st.success("✅ 모든 조건이 충족되었습니다.\n고용센터에 문의하여 청구를 진행하세요.")
        else:
            st.warning("❌ 아래 조건이 충족되지 않았습니다:")
            for i, q, a, r in mismatches:
                st.write(f"- Q{i}: {q} (답변: `{a}` / 필요: `{r}`)")
            st.info("조건이 다르면 고용센터에 추가 문의하세요.")

    # ▶️ 초기화
    if st.button("🔄 처음부터 다시"):
        for key in [
            "early_step",
            "early_answers",
            "employment_type",
            "early_questions",
            "report_date",
            "reemployment_date"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
