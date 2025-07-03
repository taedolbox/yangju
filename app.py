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

def toggle_date(date_str):
    if date_str in st.session_state.selected_dates:
        st.session_state.selected_dates.remove(date_str)
    else:
        st.session_state.selected_dates.add(date_str)

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

# 요일 표시
cols = st.columns(7)
for i, d in enumerate(days_of_week):
    cols[i].write(f"**{d}**")

# 빈 칸 띄우기 (출력은 streamlit 텍스트로 제한적)
for _ in range((first_day_prev_month.weekday() + 1) % 7):
    st.write(" ")

# 날짜 버튼 출력
for idx, d in enumerate(cal_dates):
    col_idx = idx % 7
    if col_idx == 0:
        cols = st.columns(7)
    date_str = d.strftime("%Y-%m-%d")
    selected = date_str in st.session_state.selected_dates
    label = f"**{d.day}**" if selected else str(d.day)
    if cols[col_idx].button(label, key=date_str):
        toggle_date(date_str)
        # st.experimental_rerun() 호출 안 함, Streamlit은 버튼 클릭 후 UI 자동 갱신

st.write(f"✅ 선택된 날짜: {sorted(st.session_state.selected_dates)}")
st.write(f"✅ 선택된 날짜 수: {len(st.session_state.selected_dates)}")

