import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="centered")

# 기준 날짜
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 직전 달 1일 구하기
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)

# 달력 날짜 리스트
cal_dates = []
cur = first_day_prev_month
while cur <= input_date:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 숨긴 체크박스들을 생성 (이때 키는 날짜 문자열)
for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    # 체크박스 숨기기 스타일 추가할 예정
    if date_str not in st.session_state:
        st.session_state[date_str] = False
    st.checkbox(f"{date_str}", key=date_str, value=st.session_state[date_str], label_visibility="collapsed")

# 달력 UI: 간단히 요일 + 날짜들 (기존처럼 예쁘게 바꾸셔도 됨)
days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

st.markdown("""
<style>
.calendar { display: grid; grid-template-columns: repeat(7, 40px); grid-gap: 5px; }
.day-header, .day { width: 40px; height: 40px; line-height: 40px; text-align: center; border-radius: 5px; user-select: none; cursor: pointer; }
.day-header { font-weight: bold; background: #eee; }
.day { border: 1px solid #ddd; }
.day.selected { background-color: #2196F3; color: white; font-weight: bold; border: 2px solid #2196F3; }
.hidden-checkbox { display:none; }
</style>
""", unsafe_allow_html=True)

# 요일 출력
cols = st.columns(7)
for i, day in enumerate(days_of_week):
    cols[i].markdown(f'<div class="day-header">{day}</div>', unsafe_allow_html=True)

# 날짜 출력
calendar_html = '<div class="calendar">'
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div></div>'

for date in cal_dates:
    date_str = date.strftime("%Y-%m-%d")
    selected = "selected" if st.session_state.get(date_str, False) else ""
    calendar_html += f'<div class="day {selected}" onclick="toggleCheckbox(\'{date_str}\')">{date.day}</div>'
calendar_html += '</div>'

st.markdown(calendar_html, unsafe_allow_html=True)

# JS 스크립트: 클릭 시 해당 날짜 체크박스 토글
st.markdown("""
<script>
function toggleCheckbox(date_str) {
    const cb = window.parent.document.querySelector('input[type=checkbox][data-key="' + date_str + '"]');
    if (cb) {
        cb.checked = !cb.checked;
        cb.dispatchEvent(new Event('change'));
        // 화면에서 선택 표시 반영을 위해 간단히 새로고침
        window.location.reload();
    }
}
</script>
""", unsafe_allow_html=True)

# 선택된 날짜 카운트 및 결과 계산
selected_dates = [date.strftime("%Y-%m-%d") for date in cal_dates if st.session_state.get(date.strftime("%Y-%m-%d"), False)]

st.write(f"선택된 날짜 수: {len(selected_dates)}")
threshold = len(cal_dates) / 3
st.write(f"기준 (총일수의 1/3): {threshold:.1f}")

if st.button("결과 계산"):
    worked_days = len(selected_dates)
    st.write(f"선택한 근무일 수: {worked_days}일")
    if worked_days < threshold:
        st.success("✅ 조건 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 불충족: 근무일 수가 기준 이상입니다.")





