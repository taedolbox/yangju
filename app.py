import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(layout="centered")

# 기준 날짜 선택
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 직전 달 1일부터 입력 날짜까지 범위 생성
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

# 세션 상태 초기화
if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = []

# 초기 선택 리스트
initial_selected = st.session_state.selected_dates

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
    selected_class = "selected" if date_str in initial_selected else ""
    calendar_html += f'<div class="day {selected_class}" data-date="{date_str}" onclick="toggleDate(this)">{d.day}</div>'

calendar_html += "</div>"

# 숨겨진 textarea + JS
calendar_html += f'''
<textarea id="selectedDatesInput" style="display:none;">{json.dumps(initial_selected)}</textarea>

<script>
const selectedDates = new Set({json.dumps(initial_selected)});

function toggleDate(el) {{
    const date = el.getAttribute("data-date");
    if (selectedDates.has(date)) {{
        selectedDates.delete(date);
        el.classList.remove("selected");
    }} else {{
        selectedDates.add(date);
        el.classList.add("selected");
    }}
    document.getElementById("selectedDatesInput").value = JSON.stringify(Array.from(selectedDates));
}}
</script>
'''

st.components.v1.html(calendar_html, height=450, scrolling=False, key="calendar")

# Streamlit에서 숨겨진 textarea 값 읽기 위한 text_area 연결
selected_dates_json = st.text_area(
    "selected_dates_json",
    value=json.dumps(st.session_state.selected_dates),
    height=1,
    label_visibility="collapsed"
)

try:
    selected_dates = json.loads(selected_dates_json)
except:
    selected_dates = []

# 상태 갱신 (이 부분이 핵심)
st.session_state.selected_dates = selected_dates

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)
    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")

