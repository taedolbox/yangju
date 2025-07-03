import streamlit as st
from datetime import datetime, timedelta
from streamlit_js_eval import streamlit_js_eval  # 꼭 필요!

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
}
.day {
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 5px;
  line-height: 40px;
  cursor: pointer;
  user-select: none;
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
</style>

<div class="calendar">
"""

# 요일 헤더
for d in days_of_week:
    calendar_html += f'<div class="day-header">{d}</div>'

# 시작 공백
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div class="empty-day"></div>'

# 달력 날짜
for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    calendar_html += f'''
    <div class="day" id="day-{date_str}" onclick="toggleDay('{date_str}')">{d.day}</div>
    '''

calendar_html += """
</div>

<script>
const selectedDates = new Set();

function toggleDay(dateStr) {
  const dayDiv = document.getElementById("day-" + dateStr);
  if (selectedDates.has(dateStr)) {
    selectedDates.delete(dateStr);
    dayDiv.classList.remove("selected");
  } else {
    selectedDates.add(dateStr);
    dayDiv.classList.add("selected");
  }
  // 선택 목록을 hidden input에 넣어 둔다.
  document.getElementById("selectedDatesHidden").value = JSON.stringify(Array.from(selectedDates));
}
</script>

<input type="hidden" id="selectedDatesHidden" value="[]">
"""

st.components.v1.html(calendar_html, height=500, scrolling=False)

# 👉 핵심! JS로 hidden input에 넣고 Py로 eval로 가져오기
selected_dates = streamlit_js_eval(
    js_expressions=["document.getElementById('selectedDatesHidden').value"],
    key="js_getter"
)[0]

try:
    selected_dates = eval(selected_dates) if selected_dates else []
except:
    selected_dates = []

st.write(f"✅ 선택된 날짜: {selected_dates}")
st.write(f"✅ 선택된 날짜 수: {len(selected_dates)}")

if st.button("결과 계산"):
    st.write(f"선택된 날짜: {selected_dates}")
    st.write(f"선택된 날짜 수: {len(selected_dates)}")
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)
    st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")





