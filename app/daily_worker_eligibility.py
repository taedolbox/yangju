import streamlit as st
from datetime import datetime, timedelta

def daily_worker_eligibility_app():
    st.markdown("<h3>🏗️ 일용직 신청 가능 시점 판단</h3>", unsafe_allow_html=True)

    today = datetime.today()
    first_day = today.replace(day=1)
    last_day = today.replace(day=28) + timedelta(days=4)
    last_day = last_day - timedelta(days=last_day.day)

    html = """
    <style>
    .calendar {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 5px;
      width: 100%;
      background: #fff;
      padding: 10px;
      border-radius: 8px;
    }
    .day-header {
      aspect-ratio: 1/1;
      display: flex;
      justify-content: center;
      align-items: center;
      border: 1px solid #ddd;
      border-radius: 5px;
      font-size: 14px;
      font-weight: bold;
      color: #333;
    }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }

    .day {
      aspect-ratio: 1/1;
      display: flex;
      justify-content: center;
      align-items: center;
      border: 1px solid #ddd;
      border-radius: 5px;
      font-size: 16px;
      color: #333;
    }
    .day.sunday { color: red; }
    .day.saturday { color: blue; }

    .day.empty {
      border: none;
      background: none;
    }
    </style>
    <div class="calendar">
      <div class="day-header sunday">일</div>
      <div class="day-header">월</div>
      <div class="day-header">화</div>
      <div class="day-header">수</div>
      <div class="day-header">목</div>
      <div class="day-header">금</div>
      <div class="day-header saturday">토</div>
    """

    start_offset = (first_day.weekday() + 1) % 7
    for _ in range(start_offset):
        html += '<div class="day empty"></div>'

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

