import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(layout="centered")

if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = []

input_date = st.date_input("기준 날짜 선택", datetime.today())
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

calendar_groups = {}
for date in cal_dates:
    ym = date.strftime("%Y-%m")
    calendar_groups.setdefault(ym, []).append(date)

calendar_html = """
<style>
.calendar {
  display: grid;
  grid-template-columns: repeat(7, 40px);
  grid-gap: 5px;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  user-select: none;
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
  color: #333;
  font-size: 16px;
  transition: background-color 0.2s, border 0.2s;
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
h4 {
  text-align: center;
  margin: 10px 0 5px 0;
  color: #444;
}
</style>

<script>
const selectedDates = new Set(JSON.parse('""" + json.dumps(st.session_state.selected_dates) + """'));

function toggleDate(el) {
    const date = el.getAttribute('data-date');
    if(selectedDates.has(date)) {
        selectedDates.delete(date);
        el.classList.remove('selected');
    } else {
        selectedDates.add(date);
        el.classList.add('selected');
    }
    document.getElementById('selectedCount').innerText = '선택된 날짜 수: ' + selectedDates.size;

    // Python 쪽으로 선택값 전달
    window.parent.postMessage({isStreamlitMessage: true, type: 'selectedDates', value: Array.from(selectedDates)}, '*');
}

window.onload = () => {
    document.querySelectorAll('.day').forEach(el => {
        if(selectedDates.has(el.getAttribute('data-date'))) {
            el.classList.add('selected');
        }
    });
    document.getElementById('selectedCount').innerText = '선택된 날짜 수: ' + selectedDates.size;
}
</script>
"""

for ym, dates in calendar_groups.items():
    year, month = ym.split("-")
    calendar_html += f"<h4>{year}년 {month}월</h4><div class='calendar'>"
    first_day = dates[0]
    start_offset = (first_day.weekday() + 1) % 7
    for _ in range(start_offset):
        calendar_html += "<div class='empty-day'></div>"
    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        selected_class = "selected" if date_str in st.session_state.selected_dates else ""
        calendar_html += f"<div class='day {selected_class}' data-date='{date_str}' onclick='toggleDate(this)'>{d.day}</div>"
    calendar_html += "</div>"

calendar_html += "<div id='selectedCount' style='text-align:center; margin-top:10px;'>선택된 날짜 수: 0</div>"

def receive_dates(msg):
    if msg is not None and isinstance(msg, dict) and msg.get('type') == 'selectedDates':
        st.session_state.selected_dates = msg.get('value', [])
        st.experimental_rerun()

st.components.v1.html(calendar_html, height=600, scrolling=True, key="cal", on_message=receive_dates)

