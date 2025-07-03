import streamlit as st
from datetime import datetime, timedelta

today = datetime.today().date()
input_date = st.date_input("신청일 선택", today)

# 달력 기간
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 선택 후보일 리스트
dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    dates.append(current_date)
    current_date += timedelta(days=1)

# 선택 위젯
selected_dates = st.multiselect(
    "근무일을 선택하세요", 
    [d.strftime("%Y-%m-%d") for d in dates]
)

# 결과 버튼
if st.button("계산"):
    total_days = len(dates)
    worked_days = len(selected_dates)
    threshold = total_days / 3

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days = [d for d in dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end]
    fourteen_days_str = [d.strftime("%Y-%m-%d") for d in fourteen_days]

    no_work_14_days = all(d not in selected_dates for d in fourteen_days_str)

    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준: {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    if worked_days < threshold:
        st.success("✅ 조건 1 충족")
    else:
        st.error("❌ 조건 1 불충족")

    if no_work_14_days:
        st.success("✅ 조건 2 충족")
    else:
        st.error("❌ 조건 2 불충족")

