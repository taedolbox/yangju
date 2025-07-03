import streamlit as st
from datetime import datetime, timedelta
import json

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
    st.session_state.selected_dates = []

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

calendar_html = f"""
<style>
.calendar {{
  display: grid;
  grid-template-columns: repeat(7, 40px);
  grid-gap: 5px;
  margin-top: 20px;
}}
.day-header {{
  font-weight: bold;
  text-align: center;
  background: #eee;
  border-radius: 5px;
  line-height: 40px;
  height: 40px;
}}
.day {{
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 5px;
  line-height: 40px;
  cursor: pointer;
  user-select: none;
  font-size: 16px;
  color: #333;
  transition: background-color 0.2s, border 0.2s;
}}
.day:hover {{
  background-color: #f0f0f0;
}}
.day.selected {{
  background-color: #2196F3;
  color: white;
  border: 2px solid #2196F3;
  font-weight: bold;
}}
.empty-day {{
  border: none;
}}
#selectedCount {{
  margin-top: 10px;
  font-weight: bold;
}}
</style>

<div class="calendar">
"""
for d in days_of_week:
    calendar_html += f'<div class="day-header">{d}</div>'

start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div class="empty-day"></div>'

for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    selected_class = "selected" if date_str in st.session_state.selected_dates else ""
    calendar_html += f'<div class="day {selected_class}" data-date="{date_str}" onclick="toggleDate(this)">{d.day}</div>'

calendar_html += "</div>"
calendar_html += f'<div id="selectedCount">선택된 날짜 수: {len(st.session_state.selected_dates)}</div>'

calendar_html += f"""
<script>
const selectedDates = new Set({json.dumps(st.session_state.selected_dates)});

function toggleDate(el) {{
    const date = el.getAttribute("data-date");
    if(selectedDates.has(date)) {{
        selectedDates.delete(date);
        el.classList.remove("selected");
    }} else {{
        selectedDates.add(date);
        el.classList.add("selected");
    }}
    document.getElementById("selectedCount").innerText = "선택된 날짜 수: " + selectedDates.size;

    // 여기서 Streamlit에 선택 날짜 전달 필요
    // 하지만 기본 st.components.v1.html 에선 콜백 직접 연결 안 됨
    // 임시로 console.log()만 출력
    console.log("선택된 날짜 목록:", Array.from(selectedDates));
}}
</script>
"""

st.components.v1.html(calendar_html, height=450, scrolling=False)




