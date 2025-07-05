import streamlit as st
from datetime import date
from app.questions import get_employment_questions, get_self_employment_questions

def early_reemployment_app():
    # 👉 제목: 일용직 스타일 동일
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 조기재취업수당 요건 판단</span>",
        unsafe_allow_html=True
    )

    # 👉 상단 고지문
    st.markdown(
        "<p style='font-size:18px; font-weight:700; margin-bottom:10px;'>"
        "ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다."
        "</p>",
        unsafe_allow_html=True
    )

    # ▶️ 초기화
    if "early_step" not in st.session_state:
        st.session_state.early_step = 0
        st.session_state.early_answers = []
        st.session_state.employment_type = None
        st.session_state.early_questions = []
        st.session_state.report_date = None
        st.session_state.reemployment_date = None

    # ▶️ 1단계: 입력 정보
    if st.session_state.early_step == 0:
        st.write("#### 📋 기본 정보 입력")

        col1, col2 = st.columns(2)
        with col1:
            report_date = st.date_input("📅 실업 신고일", value=date.today())
        with col2:
            reemployment_date = st.date_input("📅 재취업 날짜", value=date.today())

        employment_type = st.radio(
            "📌 취업 형태 선택",
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

    # ▶️ 2단계 이후 질문
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

    # ▶️ 결과 출력
    else:
        answers = st.session_state.early_answers[1:]
        if st.session_state.employment_type == "일반 회사 취업":
            required = ["예", "예", "예", "예", "아니요", "아니요", "아니요", "아니요", "아니요", "아니요"]
            questions = get_employment_questions()
        else:
            required = ["예", "예", "예", "아니요", "예", "아니요"]
            questions = get_self_employment_questions()

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
            st.info("조건이 다르면 고용센터에 문의해 추가 확인하세요.")

    # ▶️ 초기화 버튼
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

