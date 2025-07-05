import streamlit as st
from datetime import datetime, timedelta
from app.questions import get_employment_questions, get_self_employment_questions

def early_reemployment_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 조기재취업수당 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
        unsafe_allow_html=True
    )
    st.markdown("<h4>🏗️ 입력 정보</h4>", unsafe_allow_html=True)
    unemployment_date = st.date_input("📅 실업 신고일", value=datetime(2024, 6, 12))
    employment_date = st.date_input("📅 재취업 날짜", value=datetime(2024, 7, 1))
    daily_benefit = st.number_input("💰 실업급여 일액 (원)", min_value=0, step=1000, value=61000)
    benefit_period_days = 90  # 가정: 수급 기간 90일

    st.markdown("<h4>🏗️ 자격 조건</h4>", unsafe_allow_html=True)
    # 샘플 질문 (questions.py 미제공으로 가정)
    questions = [
        "재취업 후 12개월 이상 근무 가능합니까?",
        "정규직 근로계약을 체결했습니까?",
        "자영업의 경우, 사업자 등록을 완료했습니까?",
        "자영업의 경우, 매출 증빙이 가능합니까?"
    ]
    answers = {}
    for i, q in enumerate(questions, 1):
        answers[q] = st.radio(f"질문 {i}: {q}", ["예", "아니오"], key=f"q{i}")

    if st.button("계산", key="calculate_button"):
        if employment_date < unemployment_date:
            st.error("재취업 날짜는 실업 신고일 이후여야 합니다.")
        else:
            days_since_unemployment = (employment_date - unemployment_date).days
            remaining_days = max(0, benefit_period_days - days_since_unemployment)
            time_eligible = days_since_unemployment < benefit_period_days / 2
            condition_eligible = all(answer == "예" for answer in answers.values())
            eligibility = (
                "신청 가능: 모든 조건 충족"
                if time_eligible and condition_eligible
                else "신청 불가: 조건 미충족"
            )
            estimated_allowance = remaining_days * daily_benefit * 0.5 if condition_eligible else 0

            result = f"""
            **🏗️ 계산 결과**  
            실업 신고일: {unemployment_date}  
            재취업 날짜: {employment_date}  
            남은 수급 일수: {remaining_days}일  
            예상 수당: {estimated_allowance:,.0f}원  
            🏗️ 신청 가능 여부: {eligibility}
            """
            st.markdown(result)

    css = """
    <style>
    body {
        color: #111;
        touch-action: none;
    }
    #resultContainer {
        color: #111;
        font-size: 16px;
        padding: 10px;
        max-width: 600px;
        margin: 0 auto;
    }
    h3, h4 {
        font-size: 22px;
        font-weight: 600;
        margin: 10px 0;
    }
    p {
        font-size: 16px;
        margin: 10px 0;
    }
    @media (prefers-color-scheme: dark) {
        body {
            color: #ddd;
            background: #000;
        }
        #resultContainer {
            color: #eee;
        }
    }
    @media (max-width: 768px) {
        #resultContainer {
            padding: 8px;
            font-size: 12px;
            max-width: 90vw;
        }
        h3, h4 {
            font-size: 18px;
        }
        p {
            font-size: 12px;
        }
    }
    @media (max-width: 480px) {
        #resultContainer {
            padding: 6px;
            font-size: 12px;
            max-width: 95vw;
        }
        h3, h4 {
            font-size: 16px;
        }
        p {
            font-size: 12px;
        }
    }
    @media (orientation: landscape) and (max-width: 768px) {
        #resultContainer {
            padding: 6px;
            font-size: 12px;
            max-width: 95vw;
        }
        h3, h4 {
            font-size: 18px;
        }
        p {
            font-size: 12px;
        }
    }
    </style>
    """
    st.components.v1.html(css, height=100)
