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

if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = set()

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

st.write("## 달력")
cols = st.columns(7)
for i, day_name in enumerate(days_of_week):
    cols[i].write(f"**{day_name}**")

start_offset = (first_day_prev_month.weekday() + 1) % 7

# 빈 칸 출력
for _ in range(start_offset):
    st.write("")

# 날짜 버튼 생성 (누르면 선택 토글)
for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    selected = date_str in st.session_state.selected_dates
    label = f"**{d.day}**" if selected else str(d.day)
    if st.button(label, key=date_str):
        if selected:
            st.session_state.selected_dates.remove(date_str)
        else:
            st.session_state.selected_dates.add(date_str)
        st.experimental_rerun()  # 클릭시 화면 갱신

st.write(f"### 선택된 날짜 수: {len(st.session_state.selected_dates)}")
st.write(f"### 선택된 날짜: {sorted(st.session_state.selected_dates)}")

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(st.session_state.selected_dates)
    st.write(f"총 기간 일수: {total_days}일, 기준(1/3): {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")





