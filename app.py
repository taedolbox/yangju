import streamlit as st
from datetime import datetime, timedelta
import json # JavaScript에서 JSON 문자열을 받을 것이므로 필요합니다.

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 👉 Streamlit 세션 상태 초기화: 선택된 날짜 리스트를 저장합니다.
if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []

# 👉 JavaScript 컴포넌트로부터 데이터를 받을 콜백 함수
# 이 함수는 st.components.v1.html 컴포넌트가 Python으로 값을 보낼 때 호출됩니다.
def receive_selected_dates(selected_dates_json_str):
    if selected_dates_json_str:
        # JSON 문자열을 파이썬 리스트로 변환
        try:
            st.session_state.selected_dates_list = json.loads(selected_dates_json_str)
        except json.JSONDecodeError:
            st.error("날짜 데이터 형식이 올바르지 않습니다.")
            st.session_state.selected_dates_list = []
    else:
        st.session_state.selected_dates_list = []
    
    # 디버깅을 위해 현재 선택된 날짜 목록 출력 (이 부분은 나중에 제거해도 됩니다)
    # st.write(f"Python (receive_selected_dates)에서 수신: {st.session_state.selected_dates_list}")


# 👉 기준 날짜 선택
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 👉 달력 범위: 직전 달 초일부터 입력 날짜까지
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 👉 달력용 날짜 리스트 생성 (년/월 구분)
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
calendar_html = ""

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
        # 현재 선택된 날짜인지 확인하여 'selected' 클래스 추가 (Python 세션 상태 기반)
        is_selected = " selected" if date_str in st.session_state.selected_dates_list else ""
        calendar_html += f'''
        <div class="day{is_selected}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>
        '''

    calendar_html += "</div>"

calendar_html += """
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
// Streamlit 컴포넌트 API 로드 (필수)
const streamlit = window.parent.Streamlit;

function toggleDate(element) {
    element.classList.toggle('selected');

    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }

    // ⭐⭐⭐ 중요: st.text_input을 사용하지 않고 직접 Streamlit에 값을 전달합니다. ⭐⭐⭐
    // Streamlit.setComponentValue(value)를 사용하면 Python의 컴포넌트 호출에 값이 전달됩니다.
    // 여기서는 선택된 날짜 리스트를 JSON 문자열로 변환하여 보냅니다.
    streamlit.setComponentValue(JSON.stringify(selected));

    console.log("JS: Streamlit component value updated to:", selected.join(',')); // 디버깅용

    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}

window.onload = function() {
    // 초기 로드 시 선택된 날짜 텍스트를 업데이트하여 달력에 반영
    const currentSelectedTextElement = document.getElementById('selectedDatesText');
    if (currentSelectedTextElement) {
        const currentSelectedText = currentSelectedTextElement.innerText;
        if (currentSelectedText.includes("선택한 날짜:")) {
            const initialDatesStr = currentSelectedText.split("선택한 날짜: ")[1]?.split(" (총")[0];
            if (initialDatesStr && initialDatesStr.length > 0) {
                var initialSelectedArray = initialDatesStr.split(', ');
                var days = document.getElementsByClassName('day');
                for (var i = 0; i < days.length; i++) {
                    if (initialSelectedArray.includes(days[i].getAttribute('data-date'))) {
                        days[i].classList.add('selected');
                    }
                }
            }
        }
    }
};

</script>
"""

# Streamlit 컴포넌트 렌더링
# st.components.v1.html의 두 번째 인자로 key와 default를 넘겨주면,
# JavaScript의 streamlit.setComponentValue로 전송된 값이 Python의 이 컴포넌트 호출로 돌아옵니다.
# on_change 대신 이 컴포넌트 자체가 변경 감지 역할을 합니다.
# initial_value는 컴포넌트가 처음 로드될 때 JavaScript로 전달될 값입니다.
# Python의 selected_dates_list를 JSON 문자열로 변환하여 전달합니다.
component_value = st.components.v1.html(
    calendar_html,
    height=600,
    scrolling=True,
    key="calendar_component", # 컴포넌트 고유 키
    on_change=lambda: receive_selected_dates(st.session_state["calendar_component"]), # 컴포넌트 값이 변경되면 콜백 호출
    default=json.dumps(st.session_state.selected_dates_list) # 초기값
)

# 이 부분은 실제 컴포넌트가 값을 반환했을 때 (콜백 호출 시) 사용됩니다.
# 하지만 on_change 콜백으로 직접 처리하고 있으므로, 이 변수를 직접 사용할 필요는 없습니다.
# 다만, 컴포넌트의 반환값이 필요한 경우 사용할 수 있습니다.
# st.write(f"컴포넌트 최종 반환 값: {component_value}") # 디버깅용

# 결과 계산 버튼
if st.button("결과 계산"):
    # st.session_state.selected_dates_list는 이미 receive_selected_dates 함수에 의해 최신화되어 있습니다.
    selected_dates = st.session_state.selected_dates_list

    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates) # 이제 이 부분이 올바르게 카운트될 것입니다.

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
    if worked_days < threshold:
        st.write(f"✅ 일반일용근로자: 신청 가능")
    else:
        st.write(f"❌ 일반일용근로자: 신청 불가능")

    if worked_days < threshold and no_work_14_days:
        st.write(f"✅ 건설일용근로자: 신청 가능")
    else:
        st.write(f"❌ 건설일용근로자: 신청 불가능")
