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

# 세션 상태 초기화
if 'selected_dates_json' not in st.session_state:
    st.session_state.selected_dates_json = "[]"

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

# 초기 선택 날짜 리스트
initial_selected = json.loads(st.session_state.selected_dates_json)

for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    selected_class = "selected" if date_str in initial_selected else ""
    calendar_html += f'<div class="day {selected_class}" data-date="{date_str}" onclick="toggleDate(this)">{d.day}</div>'

calendar_html += "</div>"
calendar_html += f'<div id="selectedCount">선택된 날짜 수: {len(initial_selected)}</div>'

# 숨겨진 textarea (Streamlit 측에서 값 읽을 용도)
calendar_html += f'''
<textarea id="selectedDatesInput" style="display:none;">{json.dumps(initial_selected)}</textarea>
<script>
const selectedDates = new Set({json.dumps(initial_selected)});

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
    document.getElementById("selectedDatesInput").value = JSON.stringify(Array.from(selectedDates));
}}
</script>
'''

st.components.v1.html(calendar_html, height=450, scrolling=False, key="calendar")

# 버튼 클릭 시 JS가 바꾼 hidden textarea 값 읽기
selected_dates_json = st.experimental_get_query_params().get("selectedDates", [st.session_state.selected_dates_json])[0]

selected_dates_json = st.session_state.selected_dates_json  # 기본값

# Streamlit에서 HTML내 textarea값 직접 읽기는 안 되므로 workaround로 폼 제출 혹은 아래 방식 사용 가능
# 따라서 textarea값을 Streamlit에 보내는 작업은 별도 input 위젯이나 폼 전송 필요

# 그래서 아래와 같이 텍스트 입력 박스를 사용자에게 안 보이게 두고 강제로 값 갱신 요청하는 게 필요함

selected_dates_json = st.text_area("selectedDatesJson", st.session_state.selected_dates_json, height=1, key="selectedDatesJson", label_visibility="collapsed")

try:
    selected_dates = json.loads(selected_dates_json)
except Exception:
    selected_dates = []

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)
    st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")
