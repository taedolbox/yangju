import streamlit as st
from datetime import datetime, timedelta
import json

st.title("달력 선택 + JS에서 날짜 관리 후 Python으로 전달")

input_date = st.date_input("기준 날짜 선택", datetime.today())

first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

# 초기 선택 날짜 상태는 빈 배열로 시작
if "selected_dates" not in st.session_state:
    st.session_state.selected_dates = []

# 달력 HTML + JS (선택 토글 및 파란색 하이라이트)
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
  background-color: #a0d468; /* 연두색 */
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
#selectedCount {
  margin-top: 10px;
  font-weight: bold;
}
button {
  margin-top: 15px;
  padding: 6px 12px;
  font-weight: bold;
}
</style>

<div class="calendar">
"""

# 요일 헤더
for d in days_of_week:
    calendar_html += f'<div class="day-header">{d}</div>'

start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div class="empty-day"></div>'

for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    calendar_html += f'<div class="day" data-date="{date_str}">{d.day}</div>'

calendar_html += """
</div>
<div id="selectedCount">선택된 날짜 수: 0</div>
<button id="sendSelectionBtn">선택완료</button>

<script>
const calendar = document.querySelector('.calendar');
const selectedDates = new Set();

function updateSelectedCount() {
    document.getElementById("selectedCount").innerText = "선택된 날짜 수: " + selectedDates.size;
}

calendar.addEventListener('click', (e) => {
    const target = e.target;
    if (target.classList.contains('day') && !target.classList.contains('day-header') && !target.classList.contains('empty-day')) {
        const date = target.getAttribute('data-date');
        if(selectedDates.has(date)) {
            selectedDates.delete(date);
            target.classList.remove('selected');
        } else {
            selectedDates.add(date);
            target.classList.add('selected');
        }
        updateSelectedCount();
    }
});

document.getElementById("sendSelectionBtn").onclick = () => {
    const selectedArray = Array.from(selectedDates);
    // Streamlit 으로 선택된 날짜 리스트 전달
    window.parent.postMessage({isStreamlitMessage:true, type:"selectedDates", value:selectedArray}, "*");
}
</script>
"""

import streamlit.components.v1 as components

# 달력 컴포넌트 렌더링, on_message 콜백으로 JS에서 보낸 메시지 받음
def receive_selected_dates(msg):
    if msg["type"] == "selectedDates":
        st.session_state.selected_dates = msg["value"]

components.html(calendar_html, height=450, scrolling=False, key="calendar_component", on_message=receive_selected_dates)

# 선택완료 버튼 클릭 후 선택된 날짜 출력
st.write(f"선택된 날짜 (세션 상태): {st.session_state.selected_dates}")
st.write(f"선택된 날짜 수: {len(st.session_state.selected_dates)}")

# 기준일수, 조건 계산 예시
total_days = len(cal_dates)
threshold = total_days / 3
worked_days = len(st.session_state.selected_dates)

st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")

if worked_days < threshold:
    st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
else:
    st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")
