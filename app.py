import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="안전한 다중선택 달력", layout="centered")

input_date = st.date_input("기준 날짜 선택", datetime.today())

first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 날짜 리스트
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# 다중선택
selected_dates = st.multiselect(
    "근무한 날짜 선택",
    options=cal_dates,
    format_func=lambda d: d.strftime("%Y-%m-%d")
)

# 결과
if st.button("결과 보기"):
    st.write(f"선택된 날짜: {[d.strftime('%Y-%m-%d') for d in selected_dates]}")
    st.write(f"총 선택: {len(selected_dates)}일")


