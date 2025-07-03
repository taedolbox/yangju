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
#countDisplay {
  margin-top: 10px;
  font-weight: bold;
  font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# 초기 세션 상태 설정
for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    if date_str not in st.session_state:
        st.session_state[date_str] = False

# 숨긴 체크박스 생성
for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    st.checkbox(label=date_str, key=date_str, value=st.session_state[date_str], label_visibility="collapsed")

# 요일 헤더 출력
days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
st.markdown('<div class="calendar">' + "".join(f'<div class="day-header">{d}</div>' for d in days_of_week) + '</div>', unsafe_allow_html=True)

# 달력 숫자 출력
calendar_html = '<div class="calendar">'
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div class="empty-day"></div>'

for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    selected_class = "selected" if st.session_state.get(date_str, False) else ""
    calendar_html += f'<div class="day {selected_class}" id="{date_str}" onclick="toggleDate(this)">{date.day}</div>'

calendar_html += '</div>'

st.markdown(calendar_html, unsafe_allow_html=True)

# 현재 선택된 개수 계산
selected_count = sum(st.session_state.get(date.strftime("%Y-%m-%d"), False) for date in cal_dates)
st.markdown(f'<div id="countDisplay">선택된 날짜 수: {selected_count}</div>', unsafe_allow_html=True)

# JS 스크립트: 달력 숫자 클릭 시 체크박스 토글 + 카운트 즉시 반영
st.markdown(f"""
<script>
function toggleDate(elem) {{
    const dateStr = elem.id;
    const cb = window.parent.document.querySelector('input[type="checkbox"][data-key="' + dateStr + '"]');
    if(cb) {{
        cb.checked = !cb.checked;
        cb.dispatchEvent(new Event('change'));
    }}

    // 선택된 날짜 수 직접 카운트하여 화면에 즉시 표시
    let selectedCount = 0;
    const days = document.querySelectorAll('.day');
    days.forEach(day => {{
        if(day.classList.contains('selected')) selectedCount++;
    }});

    // 토글 전 클래스는 바뀌지 않으므로 여기서 직접 클래스 토글
    elem.classList.toggle('selected');

    // 클래스 토글 후 다시 계산 (정확한 카운트)
    selectedCount = 0;
    days.forEach(day => {{
        if(day.classList.contains('selected')) selectedCount++;
    }});

    document.getElementById('countDisplay').innerText = '선택된 날짜 수: ' + selectedCount;
}}
</script>
""", unsafe_allow_html=True)

if st.button("결과 계산"):
    worked_days = sum(st.session_state.get(date.strftime("%Y-%m-%d"), False) for date in cal_dates)
    threshold = len(cal_dates) / 3
    st.write(f"선택한 근무일 수: {worked_days}일 (기준: {threshold:.1f}일)")
    if worked_days < threshold:
        st.success("✅ 조건 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 불충족: 근무일 수가 기준 이상입니다.")





