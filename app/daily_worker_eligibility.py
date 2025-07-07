import streamlit as st
from datetime import datetime, timedelta

def daily_worker_eligibility_app():
    st.markdown("<h3>🏗️ 일용직 신청 가능 시점 판단</h3>", unsafe_allow_html=True)

    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=28) + timedelta(days=4)
    last_day = last_day - timedelta(days=last_day.day)

    html = """
    <div class="calendar">
      <div class="day-header sunday">일</div>
      <div class="day-header">월</div>
      <div class="day-header">화</div>
      <div class="day-header">수</div>
      <div class="day-header">목</div>
      <div class="day-header">금</div>
      <div class="day-header saturday">토</div>
    """

    # 시작 요일 맞추기
    start_offset = (first_day.weekday() + 1) % 7
    for _ in range(start_offset):
        html += '<div class="day empty"></div>'

    # 날짜 출력
    current = first_day
    while current <= last_day:
        weekday = current.weekday()
        dow = (weekday + 1) % 7
        cls = ""
        if dow == 0:
            cls = "sunday"
        elif dow == 6:
            cls = "saturday"
        html += f'<div class="day {cls}">{current.day}</div>'
        current += timedelta(days=1)

    html += "</div>"

    st.components.v1.html(html, height=500, scrolling=False)

