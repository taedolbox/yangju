import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="centered")

input_date = st.date_input("기준 날짜 선택", datetime.today())
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 체크박스 키 생성 함수
def checkbox_key(date):
    return f"chk_{date.strftime('%Y%m%d')}"

# CSS로 체크박스 숨기기 (모든 체크박스)
hide_checkbox_style = """
<style>
    div[data-testid="stCheckbox"] > div > input[type="checkbox"] {
        display: none;
    }
</style>
"""
st.markdown(hide_checkbox_style, unsafe_allow_html=True)

# 요일 표시
days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
cols = st.columns(7)
for i, day in enumerate(days_of_week):
    cols[i].markdown(f"**{day}**")

# 빈 칸 처리
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    st.write(" ")

# 달력과 체크박스 그리기
cols = st.columns(7)
selected_dates = []

for idx, d in enumerate(cal_dates):
    col = cols[idx % 7]
    key = checkbox_key(d)
    checked = col.checkbox(str(d.day), key=key)
    if checked:
        selected_dates.append(d.strftime("%Y-%m-%d"))

st.write(f"✅ 선택된 날짜: {selected_dates}")
st.write(f"✅ 선택된 날짜 수: {len(selected_dates)}")

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)
    st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")




