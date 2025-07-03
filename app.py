import streamlit as st
from datetime import datetime, timedelta
import json
import html

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 세션 상태 초기화
if "selected_dates_list" not in st.session_state:
    st.session_state.selected_dates_list = []

# 기준 날짜 입력
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 직전 달 1일 계산
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)

# 달력에 표시할 날짜 리스트 (직전 달 1일부터 input_date까지)
cal_dates = []
cur = first_day_prev_month
while cur <= input_date:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 년월별 그룹화
calendar_groups = {}
for d in cal_dates:
    ym = d.strftime("%Y-%m")
    calendar_groups.setdefault(ym, []).append(d)

# 현재 선택된 날짜 JSON 문자열 (HTML 내 삽입용으로 escape)
selected_dates_json = json.dumps(st.session_state.selected_dates_list)
escaped_selected_dates_json = html.escape(selected_dates_json)

# 달력 HTML + CSS + JS 생성 (중괄호 이스케이프 {{}} 중요)
calendar_html = ""

for ym, dates in calendar_groups.items():
    year, month = ym.split("-")
    calendar_html += f"""
    <h4>{year}년 {int(month)}월</h4>
    <div class="calendar">
        <div class="day-header">일</div><div class="day-header">월</div><div class="day-header">화</div>
        <div class="day-header">수</div><div class="day-header">목</div><div class="day-header">금</div><div class="day-header">토</div>
    """

    first_day_of_month = dates[0]
    start_day_offset = (first_day_of_month.weekday() + 1) % 7
    for _ in range(start_day_offset):
        calendar_html += '<div class="empty-day"></div>'

    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        day_num = date.day
        is_selected = " selected" if date_str in st.session_state.selected_dates_list else ""
        calendar_html += f'<div class="day{is_selected}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'

    calendar_html += "</div>"

calendar_html += f"""
<p id="selectedDatesText">선택한 날짜: {', '.join(st.session_state.selected_dates_list)} (총 {len(st.session_state.selected_dates_list)}일)</p>

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
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i=0; i < days.length; i++) {{{{
        if (days[i].classList.contains('selected')) {{{{
            selected.push(days[i].getAttribute('data-date'));
        }}}}
    }}}}
    // Streamlit text_area에 선택 날짜 JSON 넣기
    const textarea = window.parent.document.getElementById('selected_dates_textarea');
    if (textarea) {{{{
        textarea.value = JSON.stringify(selected);
        textarea.dispatchEvent(new Event('input'));
    }}}}
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}}}}
window.onload = function() {{{{
    // 초기 선택 날짜 텍스트 반영
    const textarea = window.parent.document.getElementById('selected_dates_textarea');
    if(textarea) {{{{
        try {{{{
            const val = JSON.parse(textarea.value || '[]');
            document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + val.join(', ') + " (총 " + val.length + "일)";
            // 선택된 날짜 달력에 반영
            var days = document.getElementsByClassName('day');
            for (var i=0; i < days.length; i++) {{{{
                if (val.includes(days[i].getAttribute('data-date'))) {{{{
                    days[i].classList.add('selected');
                }}}}
            }}}}
        }}}} catch(e) {{{{
            console.error("JSON parse error:", e);
        }}}}
    }}}}
}}};
</script>
"""

# 달력 HTML 렌더링
st.components.v1.html(calendar_html, height=650, scrolling=True, key="calendar_component")

# 선택된 날짜를 저장하는 숨겨진 텍스트 영역 (JS와 Python 간 데이터 전달 통로)
selected_dates_json_input = st.text_area(
    label="선택된 날짜 JSON",
    value=json.dumps(st.session_state.selected_dates_list),
    key="selected_dates_textarea",
    label_visibility="collapsed",
    height=100,
)

# text_area의 값 파싱하여 세션 상태에 반영
try:
    selected_dates = json.loads(selected_dates_json_input)
    if isinstance(selected_dates, list):
        st.session_state.selected_dates_list = selected_dates
except Exception:
    st.session_state.selected_dates_list = []

# 결과 계산 버튼과 출력
if st.button("결과 계산"):
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(st.session_state.selected_dates_list)

    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    if worked_days < threshold:
        st.success("✅ 조건 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 불충족: 근무일 수가 기준 이상입니다.")



