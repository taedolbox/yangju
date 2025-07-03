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

# JavaScript 메시지 처리 및 결과 계산 함수
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
    else:
        st.session_state.selected_dates_list = []
    
    # 디버깅 로그
    st.write("디버깅: JavaScript 메시지:", st.session_state.js_message)
    st.write("디버깅: 선택된 날짜 리스트:", st.session_state.selected_dates_list)

    # 결과 계산
    selected_dates = st.session_state.selected_dates_list
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

    # 디버깅: 선택된 근무일 수 출력
    st.write("디버깅: 선택된 근무일 수:", worked_days)

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days_str = [
        d.strftime("%Y-%m-%d") for d in cal_dates
        if fourteen_days_prior_start <= d <= fourteen_days_prior_end
    ]
    selected_dates_set = set(selected_dates)
    no_work_14_days = all(d not in selected_dates_set for d in fourteen_days_str)

    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")
    st.write(f"{'✅ 조건 1 충족: 근무일 수가 기준 미만입니다.' if worked_days < threshold else '❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.'}")
    st.write(f"{'✅ 조건 2 충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 근무내역이 없습니다.' if no_work_14_days else '❌ 조건 2 불충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 내 근무기록이 존재합니다.'}")

    st.markdown("### 📌 최종 판단")
    st.write(f"일반일용근로자: {'✅ 신청 가능' if worked_days < threshold else '❌ 신청 불가능'}")
    st.write(f"건설일용근로자: {'✅ 신청 가능' if worked_days < threshold and no_work_14_days else '❌ 신청 불가능'}")

# JavaScript 메시지 수신용 입력 필드 (숨김)
st.text_input(
    label="JavaScript 메시지 (숨김)",
    value="",
    key="js_message",
    on_change=handle_js_message,
    disabled=True,
    help="이 필드는 JavaScript와 Python 간의 통신용입니다."
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

calendar_html += """
</div>
<p id="selectedDatesText"></p>
<style>
.calendar {
    display: grid;
    grid-template-columns: repeat(7, 40px);
    grid-gap: 5px;
    margin-bottom: 20px;
    background-color: #ffffff;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.day-header, .empty-day {
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    font-weight: bold;
    color: #555;
}
.day-header {
    background-color: #e0e0e0;
    border-radius: 5px;
    font-size: 14px;
}
.empty-day {
    background-color: transparent;
    border: none;
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
    transition: background-color 0.1s ease, border 0.1s ease;
    font-size: 16px;
    color: #333;
}
.day:hover {
    background-color: #f0f0f0;
}
.day.selected {
    border: 2px solid #2196F3;
    background-color: #2196F3;
    color: white;
    font-weight: bold;
}
h4 {
    margin: 10px 0 5px 0;
    font-size: 1.2em;
    color: #333;
    text-align: center;
}
#selectedDatesText {
    margin-top: 15px;
    font-size: 0.9em;
    color: #666;
}
</style>
<script>
// 부모 창으로 메시지 전송
function sendMessageToParent(data) {
    console.log("JS: Sending message to parent:", JSON.stringify(data));
    window.parent.postMessage(JSON.stringify(data), '*');
}

// Streamlit 입력 필드 찾기 시도
function tryUpdateInput(selected, attempts = 10, delay = 200) {
    if (attempts <= 0) {
        console.error("JS: Streamlit input not found after multiple attempts! Falling back to postMessage.");
        sendMessageToParent(selected);
        return;
    }
    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
    if (streamlitInput) {
        streamlitInput.value = JSON.stringify(selected);
        const events = ['input', 'change', 'blur'];
        events.forEach(eventType => {
            const event = new Event(eventType, { bubbles: true });
            streamlitInput.dispatchEvent(event);
        });
        console.log("JS: Streamlit input updated to:", JSON.stringify(selected));
    } else {
        console.warn("JS: Streamlit input not found, retrying...");
        setTimeout(() => tryUpdateInput(selected, attempts - 1, delay), delay);
    }
}

function toggleDate(element) {
    element.classList.toggle('selected');
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }
    // 입력 필드 업데이트 시도
    tryUpdateInput(selected);
    // 항상 postMessage로 데이터 전송
    sendMessageToParent(selected);
    // 하단에 선택된 날짜와 카운트 표시
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + (selected.length > 0 ? selected.join(', ') : "없음") + " (총 " + selected.length + "일)";
}

window.onload = function() {
    const currentSelectedTextElement = document.getElementById('selectedDatesText');
    const initialDatesStr = "''' + ','.join(st.session_state.selected_dates_list) + '''";
    if (initialDatesStr && initialDatesStr.length > 0) {
        var initialSelectedArray = initialDatesStr.split(',').filter(date => date);
        var days = document.getElementsByClassName('day');
        for (var i = 0; i < days.length; i++) {
            if (initialSelectedArray.includes(days[i].getAttribute('data-date'))) {
                days[i].classList.add('selected');
            }
        }
        currentSelectedTextElement.innerText = "선택한 날짜: " + initialDatesStr.replace(/,/g, ', ') + " (총 " + initialSelectedArray.length + "일)";
    } else {
        currentSelectedTextElement.innerText = "선택한 날짜: 없음 (총 0일)";
    }
};

// 부모 창으로부터 메시지 수신 (디버깅용)
window.addEventListener('message', function(event) {
    console.log("JS: Received message from parent:", event.data);
});
</script>
"""

# st.components.v1.html 호출
st.components.v1.html(calendar_html, height=600, scrolling=True)

# JavaScript 메시지 수신 처리
st.markdown("""
<script>
window.addEventListener('message', function(event) {
    try {
        const data = JSON.parse(event.data);
        const input = document.querySelector('input[data-testid="stTextInput"]');
        if (input) {
            input.value = JSON.stringify(data);
            const events = ['input', 'change', 'blur'];
            events.forEach(eventType => {
                const event = new Event(eventType, { bubbles: true });
                input.dispatchEvent(event);
            });
            console.log("Python: Streamlit input updated from message:", JSON.stringify(data));
        } else {
            console.error("Python: Streamlit input not found for message!");
        }
    } catch (e) {
        console.error("Python: Failed to parse message:", event.data);
    }
});
</script>
""", unsafe_allow_html=True)
