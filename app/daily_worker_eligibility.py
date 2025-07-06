import streamlit as st
from datetime import datetime, timedelta

def daily_worker_eligibility_app():
    st.markdown(
        "<h3>🏗️ 일용직 신청 가능 시점 판단</h3>",
        unsafe_allow_html=True
    )

    today = datetime.today()
    input_date = st.date_input("📅 기준 날짜", today)

    first_day = input_date.replace(day=1)
    last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # 달력 날짜 계산
    days = []
    current = first_day
    while current <= last_day:
        days.append(current)
        current += timedelta(days=1)

    # 시작 요일 offset
    start_offset = (first_day.weekday() + 1) % 7  # 일요일 시작
    calendar_html = f"""
    <div class="month-container">
        <h4>{first_day.year}년 {first_day.month}월</h4>
        <div class="calendar">
    """

    # 요일 헤더
    days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
    for idx, day_name in enumerate(days_of_week):
        extra_class = ""
        if idx == 0:
            extra_class = "sunday"
        elif idx == 6:
            extra_class = "saturday"
        calendar_html += f'<div class="day-header {extra_class}">{day_name}</div>'

    # 시작 offset
    for _ in range(start_offset):
        calendar_html += '<div class="empty-day"></div>'

    # 날짜 출력
    for d in days:
        calendar_html += f'<div class="day">{d.day}</div>'

    calendar_html += "</div></div>"

    st.components.v1.html(calendar_html, height=600, scrolling=False)
