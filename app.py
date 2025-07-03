import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="달력 선택", layout="centered")

# 기준 날짜
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 범위
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 날짜 목록
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# 그룹
calendar_groups = {}
for date in cal_dates:
    ym = date.strftime("%Y-%m")
    if ym not in calendar_groups:
        calendar_groups[ym] = []
    calendar_groups[ym].append(date)

# Hidden input 저장용
selected_dates_str = st.text_input("선택한 날짜", value="", key="selected_dates")

# HTML + JS
calendar_html = """
<style>
.calendar {
    display: grid;
    grid-template-columns: repeat(7, 40px);
    grid-gap: 5px;
    margin-bottom: 20px;
}
.day {
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
}
.day:hover {
    background: #eee;
}
.day.selected {
    background: #2196F3;
    color: #fff;
}
</style>

<script>
function toggleDate(el) {
    el.classList.toggle('selected');
    let selected = [];
    let days = document.getElementsByClassName('day');
    for (let d of days) {
        if (d.classList.contains('selected')) {
            selected.push(d.getAttribute('data-date'));
        }
    }
    parent.document.querySelector('input[data-baseweb="input"]').value = selected.join(',');
    const event = new Event('input', { bubbles: true });
    parent.document.querySelector('input[data-baseweb="input"]').dispatchEvent(event);
}
</script>
"""

for ym, dates in calendar_groups.items():
    y, m = ym.split("-")
    calendar_html += f"<h4>{y}년 {m}월</h4><div class='calendar'>"
    for date in dates:
        day_num = date.day
        date_str = date.strftime("%Y-%m-%d")
        calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
    calendar_html += "</div>"

st.components.v1.html(calendar_html, height=600)

# 결과 버튼
if st.button("결과 보기"):
    st.write(f"선택된 날짜: {selected_dates_str}")
    st.write(f"총 선택: {len(selected_dates_str.split(',')) if selected_dates_str else 0}일")

