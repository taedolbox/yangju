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

# 달력 시작 공백
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div class="empty-day"></div>'

# 달력 날짜
for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    calendar_html += f'''
    <div class="day" id="day-{date_str}" onclick="toggleCheckbox('{date_str}')">{d.day}</div>
    '''

calendar_html += "</div>"

calendar_html += """
<script>
function toggleCheckbox(dateStr) {
  const cb = document.getElementById("cb-" + dateStr);
  cb.click();
}
</script>
"""

st.components.v1.html(calendar_html, height=450, scrolling=False)

# 숨겨진 체크박스들 → 파이썬 상태 연결
selected_dates = []
for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    checked = st.checkbox(
        label="",
        value=False,
        key=f"cb-{date_str}",
        label_visibility="collapsed"
    )
    if checked:
        selected_dates.append(date_str)

st.write(f"✅ 선택된 날짜 수: {len(selected_dates)}")
st.write(f"선택된 날짜 리스트: {selected_dates}")

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)
    st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")



