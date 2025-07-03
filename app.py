import streamlit as st
from datetime import datetime, timedelta

st.title("달력 날짜 선택 테스트")

input_date = st.date_input("기준 날짜 선택", datetime.today())
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 선택 상태를 체크박스로 관리
selected_days = []
cols = st.columns(7)

for idx, d in enumerate(cal_dates):
    key = f"chk_{d.strftime('%Y%m%d')}"
    # 숨김 체크박스 (실제로는 보이지만 CSS로 감출 수도 있음)
    checked = st.checkbox(str(d.day), key=key, value=False, label_visibility="hidden")
    if checked:
        selected_days.append(d.strftime('%Y-%m-%d'))
    # 달력 숫자는 그냥 표시
    cols[idx % 7].write(d.day)

st.write(f"선택된 날짜 수: {len(selected_days)}")
st.write("선택된 날짜:", selected_days)

