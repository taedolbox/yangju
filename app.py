import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="조건 판단 달력", layout="centered")

# 👉 기준 날짜 선택
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 👉 기준 기간 계산 (직전달 1일부터 기준일까지)
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 👉 전체 기간 날짜 리스트
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# 👉 다중 선택 (근무일 선택)
selected_dates = st.multiselect(
    "근무한 날짜 선택",
    options=cal_dates,
    format_func=lambda d: d.strftime("%Y-%m-%d")
)

# 👉 결과 버튼
if st.button("✅ 결과 보기"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days = [d for d in cal_dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end]

    no_work_14_days = all(d not in selected_dates for d in fourteen_days)

    st.write(f"### 📊 결과")
    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    # 조건1
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")

    # 조건2
    if no_work_14_days:
        st.success(f"✅ 조건 2 충족: 신청일 직전 14일간({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}) 근무내역이 없습니다.")
    else:
        st.error(f"❌ 조건 2 불충족: 신청일 직전 14일간({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}) 내 근무기록이 존재합니다.")

    st.write("### 📌 최종 판단")
    if worked_days < threshold:
        st.success(f"✅ 일반일용근로자: 신청 가능")
    else:
        st.error(f"❌ 일반일용근로자: 신청 불가능")

    if worked_days < threshold and no_work_14_days:
        st.success(f"✅ 건설일용근로자: 신청 가능")
    else:
        st.error(f"❌ 건설일용근로자: 신청 불가능")
