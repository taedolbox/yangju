import streamlit as st
from datetime import datetime, timedelta
import json
import html

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []

input_date = st.date_input("기준 날짜 선택", datetime.today())

first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

calendar_groups = {}
for date in cal_dates:
    ym = date.strftime("%Y-%m")
    calendar_groups.setdefault(ym, []).append(date)

# JSON 데이터를 HTML에 안전하게 넣기 위해 escape 처리
selected_dates_json = json.dumps(st.session_state.selected_dates_list)
escaped_selected_dates_json = html.escape(selected_dates_json)

selected_dates_text = ", ".join(st.session_state.selected_dates_list)
selected_dates_count = len(st.session_state.selected_dates_list)

calendar_html = ""

for ym, dates in calendar_groups.items():
    year, month = ym.split("-")
    calendar_html += f"""
    <h4>{year}년 {int(month)}월</h4>
    <div class="calendar">
        <div class="day-header">일</div>
        <div class="day-header">월</div>
        <div class="day-header">화</div>
        <div class="day-header">수</div>
        <div class="day-header">목</div>
        <div class="day-header">금</div>
        <div class="day-header">토</div>
    """

    first_day_of_month = dates[0]
    start_day_offset = (first_day_of_month.weekday() + 1) % 7

    for _ in range(start_day_offset):
        calendar_html += '<div class="empty-day"></div>'

    for date in dates:
        day_num = date.day
        date_str = date.strftime("%Y-%m-%d")
        is_selected = " selected" if date_str in st.session_state.selected_dates_list else ""
        calendar_html += f'<div class="day{is_selected}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'

    calendar_html += "</div>"

# 최종 HTML에 JSON 데이터를 JS 변수로 전달하는 방식 적용
calendar_html += f"""
<p id="selectedDatesText">선택한 날짜: {selected_dates_text} (총 {selected_dates_count}일)</p>

<style>
.calendar {{ 
    display: grid; 
    grid-template-columns: repeat(7, 40px); 
    grid-gap: 5px; 
    margin-bottom: 20px; 
    background-color: #ffffff; 
    padding: 10px; 
    border-radius: 8px; 
    box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
}}
.day-header, .empty-day {{ 
    width: 40px; height: 40px; line-height: 40px; text-align: center; font-weight: bold; color: #555;
}}
.day-header {{ background-color: #e0e0e0; border-radius: 5px; font-size: 14px;}}
.empty-day {{ background-color: transparent; border: none; }}
.day {{ 
    width: 40px; height: 40px; line-height: 40px; text-align: center; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none; transition: background-color 0.1s ease, border 0.1s ease; font-size: 16px; color: #333;
}}
.day:hover {{ background-color: #f0f0f0; }}
.day.selected {{ border: 2px solid #2196F3; background-color: #2196F3; color: white; font-weight: bold; }}
h4 {{ margin: 10px 0 5px 0; font-size: 1.2em; color: #333; text-align: center; }}
#selectedDatesText {{ margin-top: 15px; font-size: 0.9em; color: #666; }}
</style>

<script>
const selectedDatesInput = {escaped_selected_dates_json};

function toggleDate(element) {{
    element.classList.toggle('selected');
    let selected = [];
    let days = document.getElementsByClassName('day');
    for (let i=0; i < days.length; i++) {{
        if (days[i].classList.contains('selected')) {{
            selected.push(days[i].getAttribute('data-date'));
        }}
    }}
    // Streamlit에 직접 값 전달이 안되니 아래처럼 숨겨진 input 업데이트 필요하면 추가 구현
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}}
</script>
"""

st.components.v1.html(calendar_html, height=700, scrolling=True, key="calendar_component")

# 아래 부분은 필요하면 세션 상태와 연동하도록 추가 구현하세요

