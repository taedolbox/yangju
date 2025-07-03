import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 👉 session_state 초기화
def initialize_session_state():
    if "selected_dates" not in st.session_state:
        st.session_state.selected_dates = ""

initialize_session_state()

# 👉 기준 날짜 선택
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 👉 달력 범위: 직전 달 초일부터 입력 날짜까지
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 👉 달력용 날짜 리스트 생성
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# 👉 년/월 별로 그룹화
calendar_groups = {}
for date in cal_dates:
    year_month = date.strftime("%Y-%m")
    if year_month not in calendar_groups:
        calendar_groups[year_month] = []
    calendar_groups[year_month].append(date)

# 👉 HTML + JS 달력 생성
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
    user-select: none;
}

.day:hover {
    background-color: #eee;
}

.day.selected {
    border: 2px solid #2196F3;
    background-color: #2196F3;
    color: white;
}

h4 {
    margin: 10px 0 5px 0;
    font-size: 18px;
}
</style>
"""

for ym, dates in calendar_groups.items():
    year = ym.split("-")[0]
    month = ym.split("-")[1]
    calendar_html += f"""
    <h4>{year}년 {month}월</h4>
    <div class="calendar">
    """
    for date in dates:
        day_num = date.day
        date_str = date.strftime("%Y-%m-%d")
        calendar_html += f'''
        <div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>
        '''
    calendar_html += "</div>"

calendar_html += """
<p id="selectedDatesText"></p>

<script>
function toggleDate(element) {
    element.classList.toggle('selected');
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }
    var inputField = window.parent.document.querySelector('input[data-testid="stTextInput"]');
    if (inputField) {
        console.log('Input field found:', inputField.id, inputField.getAttribute('data-testid'));
        console.log('Setting input value to:', selected.join(','));
        inputField.value = selected.join(',');
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
        inputField.dispatchEvent(new Event('change', { bubbles: true }));
        console.log('Input field value after setting:', inputField.value);
    } else {
        console.error('Streamlit input field not found. Available inputs:', Array.from(window.parent.document.querySelectorAll('input')).map(input => ({
            id: input.id,
            dataTestid: input.getAttribute('data-testid'),
            value: input.value
        })));
    }
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + (selected.length > 0 ? selected.join(', ') : "없음") + " (총 " + selected.length + "일)";
}

window.onload = function() {
    var selectedDates = " """ + st.session_state.selected_dates + """ ".split(',').filter(date => date.trim());
    console.log('Restoring selected dates:', selectedDates);
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (selectedDates.includes(days[i].getAttribute('data-date'))) {
            days[i].classList.add('selected');
        }
    }
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + (selectedDates.length > 0 ? selectedDates.join(', ') : "없음") + " (총 " + selectedDates.length + "일)";
};
</script>
"""

# HTML 렌더링
st.components.v1.html(calendar_html, height=600, scrolling=True)

# Streamlit의 숨겨진 input 필드
selected_dates_str = st.text_input("선택한 날짜", value=st.session_state.selected_dates, key="selected_dates", label_visibility="hidden")

# 👉 디버깅: 선택된 날짜 출력
st.write(f"**디버깅: 현재 선택된 날짜 (session_state)**: {st.session_state.selected_dates}")
st.write(f"**디버깅: 현재 선택된 날짜 (text_input)**: {selected_dates_str}")

# 👉 선택된 날짜 카운트 확인
if st.button("선택된 날짜 확인"):
    selected_dates = [d.strip() for d in selected_dates_str.split(",") if d.strip()] if selected_dates_str else []
    st.session_state.selected_dates = selected_dates_str
    st.write(f"**선택된 날짜**: {selected_dates}")
    st.write(f"**선택한 일수**: {len(selected_dates)}일")
