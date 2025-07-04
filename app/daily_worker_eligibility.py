import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 👉 Streamlit 세션 상태 초기화: 선택된 날짜 리스트를 저장합니다.
if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []

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

# 👉 JavaScript에서 전달된 문자열을 파이썬 리스트로 변환하여 세션 상태에 저장하는 콜백 함수
def update_selected_dates_from_input():
    if st.session_state.text_input_for_js_communication:
        st.session_state.selected_dates_list = list(
            set(filter(None, st.session_state.text_input_for_js_communication.split(',')))
        )
    else:
        st.session_state.selected_dates_list = []

# 👉 이 필드가 달력 클릭 시 실시간으로 업데이트되는지 확인해야 합니다!
# 확인 후에는 아래 CSS 주석을 해제하여 숨길 수 있습니다.
st.text_input(
    label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)",
    value=",".join(st.session_state.selected_dates_list),
    key="text_input_for_js_communication",
    on_change=update_selected_dates_from_input,
    help="이 필드는 달력과 Python 간의 통신용입니다. 값이 변경되는지 확인하세요."
)

# 👉 이 CSS 주석은 모든 것이 작동하는지 확인 후 해제하세요.
st.markdown("""
<style>
/* input[data-testid="stTextInputInput"][aria-label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)"] {
    display: none !important;
}
div[data-testid="stTextInput"] {
    display: none !important;
}
*/
</style>
""", unsafe_allow_html=True)


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
    transition: background-color 0.1s ease;
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

    // ⭐⭐⭐ 이 부분을 수정해야 합니다! ⭐⭐⭐
    // 1. Streamlit 앱 실행 후 브라우저에서 F12 (개발자 도구)를 엽니다.
    // 2. 앱 화면의 '선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)'라는 입력 필드를 찾습니다.
    // 3. 해당 입력 필드 위에서 마우스 오른쪽 클릭 -> '검사' (Inspect)를 선택합니다.
    // 4. 개발자 도구의 'Elements' 탭에서 파란색으로 강조된 <input> 태그를 확인합니다.
    // 5. 그 <input> 태그에 'data-testid="값"' 과 'aria-label="값"' 속성이 있을 것입니다.
    // 6. 확인된 정확한 'data-testid'와 'aria-label' 값을 아래 querySelector 안의 따옴표 안에 넣어주세요.
    //    예시: data-testid가 "stTextInputInput"이고 aria-label이 "선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)"라면,
    //    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInputInput"][aria-label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)"]');
    //    만약 aria-label이 없는 경우, data-testid만으로도 시도해볼 수 있습니다:
    //    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInputInput"]');
    
    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInputInput"][aria-label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)"]');
    // ⭐⭐⭐ 여기까지 수정해야 합니다! ⭐⭐⭐

    if (streamlitInput) {
        streamlitInput.value = selected.join(',');
        streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        console.log("JS: Streamlit input updated to:", selected.join(','));
    } else {
        console.error("JS: Streamlit hidden input element not found! Please check data-testid and aria-label in querySelector.");
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

# 👉 결과 버튼
if st.button("결과 계산"):
    # Python 코드에서는 이미 selected_dates_list를 사용하여 카운트합니다.
    # JavaScript에서 이 리스트가 정확히 업데이트되면 카운트는 자동으로 올바르게 됩니다.
    selected_dates = st.session_state.selected_dates_list

    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates) # 이 부분이 정확히 카운트됩니다.

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
