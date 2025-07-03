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

# 클릭 시 날짜 선택/해제 처리 함수
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

# 빈칸 표시
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    st.write(" ")

# 날짜 출력 및 선택 상태 표시
cols = st.columns(7)
for idx, d in enumerate(cal_dates):
    col = cols[idx % 7]
    date_str = d.strftime("%Y-%m-%d")
    selected = date_str in st.session_state.selected_dates
    style = (
        "background-color: #2196F3; color: white; font-weight: bold; border-radius: 5px; "
        if selected else
        "border: 1px solid #ddd; border-radius: 5px; cursor: pointer;"
    )

    # 버튼 대신 streamlit 버튼으로 처리 (버튼 누르면 선택 토글)
    if col.button(str(d.day), key=date_str):
        toggle_date(date_str)
        st.experimental_rerun()  # 즉시 UI 갱신

    # 하지만 버튼 스타일 제어가 제한되어 있어
    # 스타일을 바로 적용하려면 st.markdown + HTML + JS가 필요함

# 선택된 날짜 출력
st.write(f"✅ 선택된 날짜: {sorted(st.session_state.selected_dates)}")
st.write(f"✅ 선택된 날짜 수: {len(st.session_state.selected_dates)}")

