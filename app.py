import streamlit as st
from datetime import datetime, timedelta

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
    year_month = date.strftime("%Y-%m")
    if year_month not in calendar_groups:
        calendar_groups[year_month] = []
    calendar_groups[year_month].append(date)

def update_selected_dates_from_input():
    if st.session_state.text_input_for_js_communication:
        st.session_state.selected_dates_list = list(
            set(filter(None, st.session_state.text_input_for_js_communication.split(',')))
        )
    else:
        st.session_state.selected_dates_list = []

# id="text_input_1"은 Streamlit이 이 위젯에 자동으로 부여한 ID입니다.
# 만약 나중에 다른 st.text_input을 추가한다면 id가 변경될 수 있습니다 (예: text_input_2).
# 이 경우 JavaScript의 getElementById 값도 함께 수정해야 합니다.
st.text_input(
    label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)",
    value=",".join(st.session_state.selected_dates_list),
    key="text_input_for_js_communication",
    on_change=update_selected_dates_from_input,
    help="이 필드는 달력과 Python 간의 통신용입니다. 값이 변경되는지 확인하세요."
)

st.markdown("""
<style>
/* 이 CSS는 모든 것이 작동하는지 확인 후 주석을 해제하여 숨길 수 있습니다. */
/* input[aria-label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)"] {
    display: none !important;
}
div[data-testid="stTextInput"] {
    display: none !important;
} */
</style>
""", unsafe_allow_html=True)


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
function toggleDate(element) {
    element.classList.toggle('selected');

    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }

    // ⭐⭐⭐ 여기를 `getElementById`로 수정했습니다. ⭐⭐⭐
    // 이제 data-testid 대신 <input> 태그에 직접 붙은 id="text_input_1"을 사용합니다.
    const streamlitInput = window.parent.document.getElementById('text_input_1'); 
    // 만약 이 페이지에 다른 st.text_input 위젯이 추가되어 id가 'text_input_2' 등으로 바뀌면,
    // 이 코드도 그에 맞춰 수정해야 합니다.

    if (streamlitInput) {
        streamlitInput.value = selected.join(',');
        streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        console.log("JS: Streamlit input updated to:", selected.join(','));
    } else {
        console.error("JS: Streamlit input element with ID 'text_input_1' not found!");
    }

    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}

window.onload = function() {
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

st.components.v1.html(calendar_html, height=600, scrolling=True)

if st.button("결과 계산"):
    selected_dates = st.session_state.selected_dates_list

    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

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
