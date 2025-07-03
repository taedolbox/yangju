import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="centered")

input_date = st.date_input("기준 날짜 선택", datetime.today())

first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)

cal_dates = []
cur = first_day_prev_month
while cur <= input_date:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 체크박스 숨기기 CSS
st.markdown("""
<style>
input[type="checkbox"] {
  display: none;
}
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
""", unsafe_allow_html=True)

# 체크박스 렌더링
for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    if date_str not in st.session_state:
        st.session_state[date_str] = False
    st.checkbox(label=date_str, key=date_str, value=st.session_state[date_str], label_visibility="collapsed")

# 요일 헤더 출력
days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
st.markdown('<div class="calendar">' + "".join(f'<div class="day-header">{d}</div>' for d in days_of_week) + '</div>', unsafe_allow_html=True)

# 달력 출력
calendar_html = '<div class="calendar">'
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div class="empty-day"></div>'

for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    selected_class = "selected" if st.session_state.get(date_str, False) else ""
    calendar_html += f'<div class="day {selected_class}" onclick="toggleCheckbox(\'{date_str}\')">{date.day}</div>'

calendar_html += '</div>'

st.markdown(calendar_html, unsafe_allow_html=True)

# JS: 달력 숫자 클릭 시 해당 체크박스 토글
st.markdown("""
<script>
function toggleCheckbox(dateStr) {
  const checkbox = window.parent.document.querySelector('input[type="checkbox"][data-key="' + dateStr + '"]');
  if (checkbox) {
    checkbox.checked = !checkbox.checked;
    checkbox.dispatchEvent(new Event('change'));
  }
}
</script>
""", unsafe_allow_html=True)

# 선택된 날짜 목록 생성
selected_dates = [date.strftime("%Y-%m-%d") for date in cal_dates if st.session_state.get(date.strftime("%Y-%m-%d"), False)]

# 선택된 날짜 수 및 기준 출력
st.write(f"선택된 날짜 수: {len(selected_dates)}")
threshold = len(cal_dates) / 3
st.write(f"기준 (총일수의 1/3): {threshold:.1f}")

# 결과 버튼
if st.button("결과 계산"):
    worked_days = len(selected_dates)
    st.write(f"선택한 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 불충족: 근무일 수가 기준 이상입니다.")




