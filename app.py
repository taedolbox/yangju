import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 세션 상태 초기화
if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []
if 'js_message' not in st.session_state:
    st.session_state.js_message = ""

# 기준 날짜 입력
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 달력 날짜 생성
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

calendar_groups = {}
for date in cal_dates:
    year_month = date.strftime("%Y-%m")
    if year_month not in calendar_groups:
        calendar_groups[year_month] = []
    calendar_groups[year_month].append(date)

# JavaScript 메시지 처리 (디버깅용)
def handle_js_message():
    if st.session_state.js_message:
        try:
            data = json.loads(st.session_state.js_message)
            if isinstance(data, list):
                st.session_state.selected_dates_list = list(set(data))
            else:
                st.session_state.selected_dates_list = []
        except json.JSONDecodeError:
            st.session_state.selected_dates_list = []
    
    # 디버깅 로그
    st.write("디버깅: JavaScript 메시지:", st.session_state.js_message)
    st.write("디버깅: 선택된 날짜 리스트:", st.session_state.selected_dates_list)

# JavaScript 메시지 수신용 입력 필드 (디버깅용, 숨김)
st.text_input(
    label="JavaScript 메시지 (숨김)",
    value="",
    key="js_message",
    on_change=handle_js_message,
    disabled=True,
    help="이 필드는 JavaScript와 Python 간의 통신 디버깅용입니다."
)

# CSS로 입력 필드와 레이블 숨김
st.markdown("""
<style>
input[data-testid="stTextInput"] {
    display: none !important;
}
label[for="js_message"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# 달력 HTML 생성
calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
calendar_html = """
<div id="calendar-container">
"""
for ym, dates in calendar_groups.items():
    year = ym.split("-")[0]
    month = ym.split("-")[1]
    calendar_html += f"""
    <h4>{year}년 {month}월</h4>
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
        calendar_html += f'''
        <div class="day{is_selected}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>
        '''
    calendar_html += "</div>"

calendar_html += f"""
</div>
<p id="selectedDatesText"></p>
<div id="resultContainer"></div>
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
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    font-weight: bold;
    color: #555;
}}
.day-header {{
    background-color: #e0e0e0;
    border-radius: 5px;
    font-size: 14px;
}}
.empty-day {{
    background-color: transparent;
    border: none;
}}
.day {{
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    user-select: none;
    transition: background-color 0.1s ease, border 0.1s ease;
    font-size: 16px;
    color: #333;
}}
.day:hover {{
    background-color: #f0f0f0;
}}
.day.selected {{
    border: 2px solid #2196F3;
    background-color: #2196F3;
    color: white;
    font-weight: bold;
}}
h4 {{
    margin: 10px 0 5px 0;
    font-size: 1.2em;
    color: #333;
    text-align: center;
}}
#selectedDatesText {{
    margin-top: 15px;
    font-size: 0.9em;
    color: #666;
}}
#resultContainer {{
    margin-top: 20px;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 8px;
    font-size: 1em;
    color: #333;
    overflow: hidden; /* 스크롤을 없애는 속성 */
}}
#resultContainer h3 {{
    margin: 0 0 10px 0;
    font-size: 1.2em;
    color: #333;
}}
#calendar-container {{
    overflow: hidden; /* 달력 부분의 스크롤을 없애는 속성 */
}}
</style>
<script>
const CALENDAR_DATES = {calendar_dates_json};
const FOURTEEN_DAYS_START = "{fourteen_days_prior_start}";
const FOURTEEN_DAYS_END = "{fourteen_days_prior_end}";

// localStorage에 데이터 저장
function saveToLocalStorage(data) {{
    console.log("JS: Saving to localStorage:", JSON.stringify(data));
    localStorage.setItem('selectedDates', JSON.stringify(data));
    sendMessageToParent({{type: 'localStorageUpdate', data: data}});
}}

// 부모 창으로 메시지 전송
function sendMessageToParent(data) {{
    console.log("JS: Sending message to parent:", JSON.stringify(data));
    window.parent.postMessage(JSON.stringify(data), '*');
}}

// 결과 계산 및 표시
function calculateAndDisplayResult(selected) {{
    console.log("JS: Calculating result for:", selected);
    const totalDays = CALENDAR_DATES.length;
    const threshold = totalDays / 3;
    const workedDays = selected.length;
    
    const fourteenDays = CALENDAR_DATES.filter(date => 
        date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END
    );
    const noWork14Days = fourteenDays.every(date => !selected.includes(date));

    // 조건 1 - 근무일 수가 기준 미만
    const condition1Text = workedDays < threshold 
        ? `✅ 조건 1 충족: 근무일 수가 기준 미만입니다. (총 ${workedDays}일 / 기간 ${totalDays}일, 기준 ${threshold.toFixed(1)}일)`
        : `❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.`;

    // 조건 2 - 신청일 직전 14일간 근무내역 없음
    const condition2Text = noWork14Days 
        ? `✅ 조건 2 충족: 신청일 직전 14일간 근무 기록이 없습니다.`
        : `❌ 조건 2 불충족: 신청일 직전 14일간 근무 기록이 존재합니다.`;

    // 일반일용근로자 결과: 두 조건이 모두 충족되어야 신청 가능
    const generalWorkerText = (workedDays < threshold && noWork14Days) 
        ? `✅ 신청 가능 수급자격 인정신청일이 속한 달의 직전 달 초일부터 신청일까지(${FOURTEEN_DAYS_START} ~ ${FOURTEEN_DAYS_END}) 근무일 수의 합이 같은 기간 총 일수의 1/3 미만으로 신청 가능합니다.`
        : `❌ 신청 불가능`;

    // 건설일용근로자 결과: 한 가지 조건만 충족해도 신청 가능
    const constructionWorkerText = (workedDays < threshold || noWork14Days) 
        ? `✅ 신청 가능 조건 1과 조건 2 모두 충족하여 신청 가능합니다.`
        : `❌ 신청 불가능`;

    const resultHtml = [
        `<p>총 기간 일수: ${totalDays}일</p>`,
        `<p>기준 (총일수의 1/3): ${threshold.toFixed(1)}일</p>`,
        `<p>선택한 근무일 수: ${workedDays}일</p>`,
        `<p>${condition1Text}</p>`,
        `<p>${condition2Text}</p>`,
        `<h3>📌 최종 판단</h3>`,
        `<p>일반일용근로자: ${generalWorkerText}</p>`,
        `<p>건설일용근로자: ${constructionWorkerText}</p>`
    ].join('');
    
    document.getElementById('resultContainer').innerHTML = resultHtml;
}

function toggleDate(element) {{
    element.classList.toggle('selected');
    const selected = [];
    const days = document.getElementsByClassName('day');
    for (let i = 0; i < days.length; i++) {{
        if (days[i].classList.contains('selected')) {{
            selected.push(days[i].getAttribute('data-date'));
        }}
    }}
    // localStorage에 저장
    saveToLocalStorage(selected);
    // 결과 계산 및 표시
    calculateAndDisplayResult(selected);
    // 하단에 선택된 날짜와 카운트 표시
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + (selected.length > 0 ? selected.join(', ') : "없음") + " (총 " + selected.length + "일)";
}}

window.onload = function() {{
    const currentSelectedTextElement = document.getElementById('selectedDatesText');
    const initialDatesStr = "{','.join(st.session_state.selected_dates_list)}";
    let initialSelectedArray = [];
    if (initialDatesStr && initialDatesStr.length > 0) {{
        initialSelectedArray = initialDatesStr.split(',').filter(date => date);
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {{
            if (initialSelectedArray.includes(days[i].getAttribute('data-date'))) {{
                days[i].classList.add('selected');
            }}
        }}
        currentSelectedTextElement.innerText = "선택한 날짜: " + initialDatesStr.replace(/,/g, ', ') + " (총 " + initialSelectedArray.length + "일)";
    }} else {{
        currentSelectedTextElement.innerText = "선택한 날짜: 없음 (총 0일)";
    }}
    // 초기 localStorage 설정 및 결과 표시
    saveToLocalStorage(initialSelectedArray);
    calculateAndDisplayResult(initialSelectedArray);
}};

// 부모 창으로부터 메시지 수신 (디버깅용)
window.addEventListener('message', function(event) {{
    console.log("JS: Received message from parent:", event.data);
}});
</script>
"""

# st.components.v1.html 호출
st.components.v1.html(calendar_html, height=800, scrolling=False)


