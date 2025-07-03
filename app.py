import streamlit as st
from datetime import datetime, timedelta

st.title("달력과 체크박스 연동 예제")

input_date = st.date_input("기준 날짜 선택", datetime.today())
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 체크박스 상태는 스트림릿 위젯으로 관리
selected_dates = []

# 체크박스를 렌더링할 위치 분리
st.markdown("### 체크박스 (아래를 클릭하세요)")

# 체크박스들을 1열로 나열
for d in cal_dates:
    key = d.strftime("chk_%Y%m%d")
    checked = st.checkbox(f"{d.day}", key=key)
    if checked:
        selected_dates.append(d.strftime("%Y-%m-%d"))

# 달력 UI 생성 (숫자 텍스트에 JS 이벤트 연결)
cal_html = """
<style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 30px);
        grid-gap: 4px;
        margin-bottom: 10px;
    }
    .day {
        background-color: #a0d468; /* 연녹색 */
        text-align: center;
        line-height: 30px;
        border-radius: 4px;
        cursor: pointer;
        user-select: none;
    }
</style>
<div class="calendar">
"""
for d in cal_dates:
    day_str = d.strftime("%Y-%m-%d")
    day_num = d.day
    # 클릭 시 체크박스 아이디 클릭 트리거
    cal_html += f'<div class="day" onclick="document.getElementById(\'{d.strftime("chk_%Y%m%d")}\').click();">{day_num}</div>'
cal_html += "</div>"

# 체크박스 id에 자동 생성되는 streamlit 내부 id 부여 (key와 동일하게 맞춤)
# 이 부분은 체크박스가 실제로 id를 가지고 있어야 작동하므로 하단에 빈 태그로 강제로 id 부여(비표준이나 스트림릿 내부 렌더링 전 JS 작동 테스트 필요)

st.markdown(cal_html, unsafe_allow_html=True)

st.write(f"선택된 날짜 수: {len(selected_dates)}")
st.write("선택된 날짜 목록:", selected_dates)

