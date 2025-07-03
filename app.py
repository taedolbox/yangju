import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="centered")

input_date = st.date_input("기준 날짜 선택", datetime.today())

# 달력 범위: 이전 달 1일부터 입력일 까지
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = set()

days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

st.write("## 달력")
cols = st.columns(7)
for i, day_name in enumerate(days_of_week):
    cols[i].write(f"**{day_name}**")

# 달력 첫날 요일 오프셋 (일요일=0)
start_offset = (first_day_prev_month.weekday() + 1) % 7

# 빈 칸 출력
for _ in range(start_offset):
    st.write("")

# 체크박스 숨기는 CSS
hide_checkbox_css = """
    <style>
    .hidden-checkbox {
        display: none;
    }
    </style>
"""
st.markdown(hide_checkbox_css, unsafe_allow_html=True)

# 체크박스 숨기고 달력 숫자 버튼으로 동기화
for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    checked = date_str in st.session_state.selected_dates

    # 체크박스 (숨김)
    checkbox_id = f"cb_{date_str}"
    checked_new = st.checkbox(label="", key=checkbox_id, value=checked, help=date_str)

    # 체크박스 상태 변화 감지
    if checked_new and date_str not in st.session_state.selected_dates:
        st.session_state.selected_dates.add(date_str)
    elif not checked_new and date_str in st.session_state.selected_dates:
        st.session_state.selected_dates.remove(date_str)

# 달력 숫자 출력 및 클릭 JS (Streamlit HTML 내 버튼으로 대체)
calendar_html = """
<style>
.calendar {
  display: grid;
  grid-template-columns: repeat(7, 40px);
  grid-gap: 5px;
  margin-top: 10px;
}
.day {
  width: 40px;
  height: 40px;
  text-align: center;
  line-height: 40px;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  user-select: none;
}
.selected {
  background-color: #2196F3;
  color: white;
  font-weight: bold;
  border: 2px solid #2196F3;
}
.empty {
  background-color: transparent;
  border: none;
  cursor: default;
}
</style>
<div class="calendar">
"""

# 빈칸 채우기
for _ in range(start_offset):
    calendar_html += '<div class="day empty"></div>'

for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    is_selected = "selected" if date_str in st.session_state.selected_dates else ""
    calendar_html += f'<div class="day {is_selected}" onclick="toggleCheckbox(\'cb_{date_str}\')" id="day_{date_str}">{d.day}</div>'

calendar_html += "</div>"

# JS 함수: 달력 숫자 클릭 시 해당 체크박스 클릭 유도
calendar_html += """
<script>
function toggleCheckbox(cb_id) {
    const cb = window.parent.document.querySelector('input[id="'+cb_id+'"]');
    if(cb) {
        cb.click();
    }
}
</script>
"""

st.components.v1.html(calendar_html, height=300, scrolling=False)

st.write(f"### 선택된 날짜 수: {len(st.session_state.selected_dates)}")
st.write(f"### 선택된 날짜: {sorted(st.session_state.selected_dates)}")

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(st.session_state.selected_dates)
    st.write(f"총 기간 일수: {total_days}일, 기준(1/3): {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")





