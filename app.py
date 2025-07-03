import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 👉 Streamlit 세션 상태 초기화: 선택된 날짜 리스트를 저장합니다.
# 'selected_dates_list'가 세션 상태에 없으면 빈 리스트로 초기화합니다.
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
# st.text_input의 값이 변경될 때마다 호출됩니다.
def update_selected_dates_from_input():
    # st.text_input에 설정된 key 'text_input_for_js_communication'을 통해 현재 값을 가져옵니다.
    if st.session_state.text_input_for_js_communication:
        # 콤마로 구분된 문자열을 리스트로 변환 후 중복 제거 및 빈 문자열 필터링
        st.session_state.selected_dates_list = list(
            set(filter(None, st.session_state.text_input_for_js_communication.split(',')))
        )
    else:
        st.session_state.selected_dates_list = []

# 👉 숨겨진 input 박스: JavaScript가 선택한 날짜를 여기에 콤마로 구분된 문자열로 씁니다.
# *** 중요: 이 필드가 달력 클릭 시 실시간으로 업데이트되는지 확인하세요. ***
# *** 이 필드가 업데이트되지 않으면, 아래 JavaScript의 querySelector 부분이 잘못된 것입니다. ***
st.text_input(
    label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)", # 이 라벨이 HTML의 aria-label 속성값으로 사용됩니다.
    value=",".join(st.session_state.selected_dates_list),
    key="text_input_for_js_communication", # JavaScript에서 이 key에 해당하는 input을 찾습니다.
    on_change=update_selected_dates_from_input, # 이 콜백 함수가 호출되어 selected_dates_list를 업데이트합니다.
    help="이 필드는 달력에서 선택된 날짜를 JavaScript에서 Python으로 전달하는 데 사용됩니다. 이 필드의 값을 보면서 JS와 Python 간 통신이 되는지 확인하세요. 정상 작동 확인 후 숨길 수 있습니다."
)

# 👉 CSS를 사용하여 st.text_input 위젯을 숨깁니다.
# 모든 것이 제대로 작동하는 것을 확인한 후에 아래 주석을 해제하여 숨길 수 있습니다.
# 현재는 디버깅을 위해 주석 처리되어 있어 화면에 보입니다.
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

    # 년월 헤더
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

    # 첫 번째 날짜의 요일을 찾아 공백을 채웁니다.
    # Python의 weekday()는 월=0, 화=1, ..., 일=6 입니다.
    # HTML 달력은 보통 일요일부터 시작하므로, 일요일을 0으로 맞춥니다.
    first_day_of_month = dates[0]
    start_day_offset = (first_day_of_month.weekday() + 1) % 7 # 일=0, 월=1 ... 토=6 (HTML 달력 순서)

    for _ in range(start_day_offset):
        calendar_html += '<div class="empty-day"></div>'

    # 날짜 블럭
    for date in dates:
        day_num = date.day
        date_str = date.strftime("%Y-%m-%d")
        # 현재 선택된 날짜인지 확인하여 'selected' 클래스 추가
        # st.session_state.selected_dates_list에 날짜 문자열이 있으면 선택된 것으로 간주합니다.
        is_selected = " selected" if date_str in st.session_state.selected_dates_list else ""
        calendar_html += f'''
        <div class="day{is_selected}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>
        '''

    calendar_html += "</div>"

# JavaScript 코드와 스타일 시트
calendar_html += """
<p id="selectedDatesText"></p>

<style>
/* 달력 전체 컨테이너 */
.calendar {
    display: grid;
    grid-template-columns: repeat(7, 40px); /* 7개의 열 (요일별) */
    grid-gap: 5px; /* 셀 간 간격 */
    margin-bottom: 20px;
    background-color: #ffffff; /* 배경색 */
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* 요일 헤더 스타일 */
.day-header, .empty-day {
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    font-weight: bold;
    color: #555;
}

.day-header {
    background-color: #e0e0e0; /* 요일 헤더 배경색 */
    border-radius: 5px;
    font-size: 14px;
}

/* 빈 날짜 셀 (달의 첫 날 이전 공백) */
.empty-day {
    background-color: transparent;
    border: none;
}

/* 각 날짜 셀 (가장 중요한 부분) */
.day {
    width: 40px;
    height: 40px;
    line-height: 40px; /* 텍스트 수직 중앙 정렬 */
    text-align: center; /* 텍스트 수평 중앙 정렬 */
    border: 1px solid #ddd; /* 테두리 */
    border-radius: 5px; /* 둥근 모서리 */
    cursor: pointer; /* 마우스 오버 시 포인터 변경 */
    user-select: none; /* 텍스트 선택 방지 */
    transition: background-color 0.1s ease, border 0.1s ease; /* 부드러운 애니메이션 */
    font-size: 16px;
    color: #333;
}

/* 날짜 셀 호버 시 */
.day:hover {
    background-color: #f0f0f0;
}

/* 선택된 날짜 셀 */
.day.selected {
    border: 2px solid #2196F3; /* 파란색 테두리 */
    background-color: #2196F3; /* 파란색 배경 */
    color: white; /* 흰색 텍스트 */
    font-weight: bold;
}

/* 월/년 헤더 */
h4 {
    margin: 10px 0 5px 0;
    font-size: 1.2em; /* 더 큰 글씨 */
    color: #333;
    text-align: center;
}

/* 선택된 날짜 표시 텍스트 */
#selectedDatesText {
    margin-top: 15px;
    font-size: 0.9em;
    color: #666;
}
</style>

<script>
function toggleDate(element) {
    // 선택/해제 토글
    element.classList.toggle('selected');

    // 현재 선택된 모든 날짜 수집
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }

    // --- 중요: Streamlit의 st.text_input 필드를 찾아 값 업데이트 ---
    // VM662 오류 발생 시, 이 아래 줄의 'querySelector' 선택자를 수정해야 합니다!
    // 1. Streamlit 앱을 실행하고, '선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)'라는 입력 필드를 찾습니다.
    // 2. 해당 입력 필드 위에서 마우스 오른쪽 클릭 -> '검사' (Inspect)를 선택합니다.
    // 3. 개발자 도구에서 해당 <input> 태그의 'data-testid'와 'aria-label' 속성 값을 정확히 확인합니다.
    // 4. 확인된 값을 아래 querySelector의 'XXX'와 'YYY' 자리에 넣어주세요.
    //    일반적인 data-testid는 "stTextInputInput" 또는 "stTextInput-0" 등입니다.
    //    aria-label은 Python 코드의 st.text_input에 설정한 'label' 값과 동일해야 합니다.
    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInputInput"][aria-label="선택한 날짜 (이 필드가 제대로 동작하는지 확인하세요)"]');
    
    if (streamlitInput) {
        streamlitInput.value = selected.join(','); // 선택된 날짜들을 콤마로 구분된 문자열로 설정
        // 'input' 이벤트를 발생시켜 Streamlit에게 값이 변경되었음을 알립니다.
        // 이 이벤트를 통해 Python의 on_change 콜백(update_selected_dates_from_input)이 트리거됩니다.
        streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        console.log("JS: Streamlit input updated to:", selected.join(',')); // 디버깅을 위해 콘솔에 로그 출력
    } else {
        // 입력 필드를 찾지 못했을 때 오류 메시지를 콘솔에 출력합니다.
        console.error("JS: Streamlit hidden input element not found! Please check data-testid and aria-label in querySelector.");
    }

    // 사용자를 위해 현재 선택된 날짜들을 텍스트로 표시
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}

// Streamlit 앱이 로드될 때 (또는 페이지 새로고침 시) 달력의 초기 선택 상태를 반영합니다.
// (Python의 st.session_state.selected_dates_list에 저장된 값에 따라 'selected' 클래스를 추가합니다.)
window.onload = function() {
    const currentSelectedTextElement = document.getElementById('selectedDatesText');
    if (currentSelectedTextElement) {
        const currentSelectedText = currentSelectedTextElement.innerText;
        // '선택한 날짜:' 문구가 포함되어 있고, 그 뒤에 날짜 문자열이 있다면 파싱합니다.
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
st.components.v1.html(calendar_html, height=600, scrolling=True)

# 👉 결과 버튼
if st.button("결과 계산"):
    # selected_dates는 이제 st.session_state.selected_dates_list에서 직접 가져옵니다.
    # 이 리스트는 JavaScript가 st.text_input을 업데이트하고 on_change 콜백이 실행될 때마다 최신화되므로,
    # '결과 계산' 버튼을 누를 시점에는 항상 최신 값을 가지고 있습니다.
    selected_dates = st.session_state.selected_dates_list

    # 👉 결과 계산 로직
    total_days = len(cal_dates) # 달력에 표시된 전체 일수
    threshold = total_days / 3 # 총 일수의 1/3 기준
    worked_days = len(selected_dates) # 사용자가 선택한 근무일 수

    # 신청일 직전 14일 기간 계산
    fourteen_days_prior_end = input_date - timedelta(days=1) # 신청일 하루 전까지
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13) # 13일을 더 빼서 총 14일 기간

    # 14일 기간 내의 날짜들을 'YYYY-MM-DD' 문자열 형식으로 가져옵니다.
    fourteen_days_str = [
        d.strftime("%Y-%m-%d") for d in cal_dates
        if fourteen_days_prior_start <= d <= fourteen_days_prior_end
    ]
    
    # 선택된 날짜 목록을 set으로 변환하여 빠른 검색이 가능하게 합니다.
    selected_dates_set = set(selected_dates)
    
    # 신청일 직전 14일 기간 내에 근무 내역이 없는지 확인합니다.
    # 이 기간 내의 모든 날짜가 selected_dates_set에 없어야 '근무 내역 없음'으로 판단합니다.
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
