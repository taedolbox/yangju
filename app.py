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
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

calendar_groups = {}
for d in cal_dates:
    ym = d.strftime("%Y-%m")
    calendar_groups.setdefault(ym, []).append(d)

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
        <div class="day-header">일</div><div class="day-header">월</div><div class="day-header">화</div><div class="day-header">수</div><div class="day-header">목</div><div class="day-header">금</div><div class="day-header">토</div>
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

# 이 부분에서 CSS, JS 내 중괄호 {} 는 모두 {{}} 로 치환 (f-string 중괄호 이스케이프)
calendar_html += f"""
<p id="selectedDatesText">선택한 날짜: {selected_dates_text} (총 {selected_dates_count}일)</p>

<style>
.calendar {{{{
    display: grid;
    grid-template-columns: repeat(7, 40px);
    grid-gap: 5px;
    margin-bottom: 20px;
    background-color: #fff;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}}}
.day-header, .empty-day {{{{
    width: 40px; height: 40px; line-height: 40px; text-align: center; font-weight: bold; color: #555;
}}}}
.day-header {{{{
    background-color: #e0e0e0; border-radius: 5px; font-size: 14px;
}}}}
.empty-day {{{{
    background-color: transparent; border: none;
}}}}
.day {{{{
    width: 40px; height: 40px; line-height: 40px; text-align: center; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none; transition: background-color 0.1s ease, border 0.1s ease; font-size: 16px; color: #333;
}}}}
.day:hover {{{{
    background-color: #f0f0f0;
}}}}
.day.selected {{{{
    border: 2px solid #2196F3; background-color: #2196F3; color: white; font-weight: bold;
}}}}
h4 {{{{
    margin: 10px 0 5px 0; font-size: 1.2em; color: #333; text-align: center;
}}}}
#selectedDatesText {{{{
    margin-top: 15px; font-size: 0.9em; color: #666;
}}}}
</style>

<script>
function toggleDate(element) {{{{
    element.classList.toggle('selected');
    let selected = [];
    let days = document.getElementsByClassName('day');
    for (let i=0; i<days.length; i++) {{{{
        if (days[i].classList.contains('selected')) {{{{
            selected.push(days[i].getAttribute('data-date'));
        }}}}
    }}}}
    // Streamlit text_area에 선택 날짜 JSON 업데이트
    const textArea = window.parent.document.getElementById('selected_dates_textarea');
    if (textArea) {{{{
        textArea.value = JSON.stringify(selected);
        textArea.dispatchEvent(new Event('input'));
    }}}}
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}}}}

// 초기 로드시 선택 날짜 텍스트 동기화
window.onload = function() {{{{
    const textArea = window.parent.document.getElementById('selected_dates_textarea');
    if(textArea) {{{{
        const val = JSON.parse(textArea.value || '[]');
        document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + val.join(', ') + " (총 " + val.length + "일)";
    }}}}
}}}};
</script>
"""

st.components.v1.html(calendar_html, height=700, scrolling=True, key="calendar_component")

selected_dates_json_input = st.text_area(
    "선택된 날짜 JSON",
    value=json.dumps(st.session_state.selected_dates_list),
    key="selected_dates_textarea",
    label_visibility="collapsed",
    height=100,
)

try:
    selected_dates = json.loads(selected_dates_json_input)
    if isinstance(selected_dates, list):
        st.session_state.selected_dates_list = selected_dates
except Exception:
    st.session_state.selected_dates_list = []

# 이하 결과 계산 로직 생략


