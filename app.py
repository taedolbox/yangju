import streamlit as st
from datetime import datetime, timedelta
import json

st.title("달력 선택 (JS 내 선택 후 복사/붙여넣기 방식)")

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
  background-color: #a0d468;
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
#selectedDatesJson {
  margin-top: 15px;
  width: 100%;
}
button {
  margin-top: 10px;
  padding: 5px 10px;
  font-weight: bold;
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
    calendar_html += f'<div class="day" data-date="{date_str}">{d.day}</div>'

calendar_html += """
</div>
<div id="selectedCount">선택된 날짜 수: 0</div>
<textarea id="selectedDatesJson" rows="3" placeholder="선택된 날짜 JSON이 여기에 표시됩니다. 이 값을 복사해서 아래 입력란에 붙여넣으세요." readonly></textarea>
<button id="copyBtn">선택 날짜 복사</button>

<script>
const calendar = document.querySelector('.calendar');
const selectedDates = new Set();

function updateSelectedCount() {
    document.getElementById("selectedCount").innerText = "선택된 날짜 수: " + selectedDates.size;
    document.getElementById("selectedDatesJson").value = JSON.stringify(Array.from(selectedDates));
}

calendar.addEventListener('click', (e) => {
    const target = e.target;
    if(target.classList.contains('day')) {
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

document.getElementById('copyBtn').onclick = () => {
    const textarea = document.getElementById('selectedDatesJson');
    textarea.select();
    document.execCommand('copy');
    alert('선택된 날짜가 복사되었습니다. 아래 입력란에 붙여넣기 하세요.');
}
</script>
"""

import streamlit.components.v1 as components

components.html(calendar_html, height=480, scrolling=False)

selected_dates_input = st.text_area("선택된 날짜 JSON 붙여넣기", "", help="위에서 복사한 JSON을 여기에 붙여넣으세요.")

try:
    selected_dates = json.loads(selected_dates_input)
except Exception:
    selected_dates = []

st.write(f"선택된 날짜: {selected_dates}")
st.write(f"선택된 날짜 수: {len(selected_dates)}")

# 조건 계산 예
total_days = len(cal_dates)
threshold = total_days / 3
worked_days = len(selected_dates)

st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
if worked_days < threshold:
    st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
else:
    st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")
