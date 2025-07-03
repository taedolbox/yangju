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

# CSS 스타일
st.markdown("""
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
""", unsafe_allow_html=True)

# 달력 그리기 시작
st.markdown('<div class="calendar">', unsafe_allow_html=True)

# 요일 헤더
for d in days_of_week:
    st.markdown(f'<div class="day-header">{d}</div>', unsafe_allow_html=True)

# 빈 칸
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    st.markdown('<div class="empty-day"></div>', unsafe_allow_html=True)

# 날짜별 체크박스와 달력 숫자 출력
for d in cal_dates:
    date_str = d.strftime("%Y-%m-%d")
    key = f"chk_{date_str}"

    # 체크박스 위젯 생성 (숨김 처리됨)
    checked = st.checkbox(label=date_str, key=key, value=False)

    # 체크박스 상태에 따라 CSS class 지정
    selected_class = "selected" if st.session_state[key] else ""

    # 체크박스 id = key로 지정하여 JS에서 제어할 수 있게 함
    st.markdown(
        f'''
        <label for="{key}" class="day {selected_class}" onclick="toggleCheckbox('{key}', this)">{d.day}</label>
        ''',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# JS 스크립트로 클릭 시 체크박스 토글, 선택 상태에 따라 스타일 바꾸기
st.markdown("""
<script>
function toggleCheckbox(id, el) {
    const checkbox = document.getElementById(id);
    if (!checkbox) return;

    checkbox.checked = !checkbox.checked;
    if(checkbox.checked) {
        el.classList.add("selected");
    } else {
        el.classList.remove("selected");
    }
}
</script>
""", unsafe_allow_html=True)

# 선택된 날짜 개수 계산
selected_dates = [d.strftime("%Y-%m-%d") for d in cal_dates if st.session_state.get(f"chk_{d.strftime('%Y-%m-%d')}", False)]
st.write(f"선택된 날짜 수: {len(selected_dates)}")

if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

    st.write(f"총 기간 일수: {total_days}일, 기준(1/3): {threshold:.1f}일, 선택된 근무일 수: {worked_days}일")

    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")

