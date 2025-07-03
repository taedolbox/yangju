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

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

# 선택 상태를 세션에 저장 (처음엔 빈 리스트)
if 'selected_dates' not in st.session_state:
    st.session_state['selected_dates'] = []

# 전체 달력 HTML 만들기
calendar_html = """
<style>
.calendar {
  display: grid;
  grid-template-columns: repeat(7, 40px);
  grid-gap: 5px;
  margin-top: 20px;
}
.day-header {
  font-weight: bold;
  text-align: center;
  background: #eee;
  border-radius: 5px;
  line-height: 40px;
  height: 40px;
  user-select: none;
}
.day {
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 5px;
  line-height: 40px;
  cursor: pointer;
  user-select: none;
  font-weight: normal;
  color: black;
}
.day.selected {
  background-color: #2196F3;
  color: white;
  border: 2px solid #2196F3;
  font-weight: bold;
}
.empty-day {
  border: none;
}
input[type="checkbox"] {
  display: none;
}
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
    checked_attr = "checked" if date_str in st.session_state['selected_dates'] else ""
    selected_class = "selected" if checked_attr else ""
    calendar_html += f'''
    <div class="day {selected_class}" onclick="toggleDate('{date_str}', this)">
        {d.day}
        <input type="checkbox" id="chk_{date_str}" value="{date_str}" {checked_attr}>
    </div>
    '''

calendar_html += "</div>"

calendar_html += f"""
<div style="margin-top:10px; font-weight:bold;">선택된 날짜 수: <span id="selectedCount">{len(st.session_state['selected_dates'])}</span></div>

<script>
function toggleDate(date, el) {{
    const checkbox = el.querySelector('input[type="checkbox"]');
    if (!checkbox) return;
    checkbox.checked = !checkbox.checked;
    el.classList.toggle('selected', checkbox.checked);

    // 선택된 체크박스 수 계산
    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    let selectedDates = [];
    allCheckboxes.forEach(cb => {{
        if(cb.checked) selectedDates.push(cb.value);
    }});
    document.getElementById('selectedCount').innerText = selectedDates.length;

    // Streamlit에 선택 날짜 전달
    window.parent.postMessage({{isStreamlitMessage: true, type: 'selectedDates', value: selectedDates}}, "*");
}}
</script>
"""

# 컴포넌트 출력
st.components.v1.html(calendar_html, height=450, scrolling=False, key="calendar")

# Streamlit에서 JS 메시지 받기
def on_message(msg):
    if msg.get("type") == "selectedDates":
        st.session_state['selected_dates'] = msg.get("value", [])

st.experimental_get_query_params()  # Dummy to keep session active

# 버튼 클릭 시 결과 계산
if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(st.session_state.get('selected_dates', []))
    st.write(f"총 기간 일수: {total_days}일, 기준(1/3): {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")


