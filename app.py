import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="다중선택 달력", layout="centered")

input_date = st.date_input("기준 날짜 선택", datetime.today())

first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

calendar_groups = {}
for d in cal_dates:
    ym = d.strftime("%Y-%m")
    if ym not in calendar_groups:
        calendar_groups[ym] = []
    calendar_groups[ym].append(d)

# 👉 Streamlit에서 부모 input field
selected_dates_str = st.text_input("선택한 날짜", value="", key="selected_dates")

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
    let input = parent.document.querySelector('input[data-testid="stTextInput"]');
    if (input) {
        input.value = selected.join(',');
        const event = new Event('input', { bubbles: true });
        input.dispatchEvent(event);
    }
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

if st.button("결과 보기"):
    st.write(f"선택된 날짜: {selected_dates_str}")
    st.write(f"총 선택: {len(selected_dates_str.split(',')) if selected_dates_str else 0}일")

