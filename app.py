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
# 'label'은 Streamlit이 이 input에 자동으로 'aria-label' 속성을 부여하게 합니다.
# 'value'는 세션 상태의 현재 선택된 날짜 리스트를 기반으로 초기화됩니다.
# 'key'는 이 위젯을 세션 상태와 연결하며, 'on_change'는 콜백 함수를 지정합니다.
st.text_input(
    label="선택한 날짜", # 이 라벨이 HTML의 aria-label 속성값으로 사용됩니다.
    value=",".join(st.session_state.selected_dates_list),
    key="text_input_for_js_communication", # JavaScript에서 이 key에 해당하는 input을 찾습니다.
    on_change=update_selected_dates_from_input, # 이 콜백 함수가 호출되어 selected_dates_list를 업데이트합니다.
    help="이 필드는 달력에서 선택된 날짜를 JavaScript에서 Python으로 전달하는 데 사용됩니다. 실제 앱에서는 숨겨집니다."
)

# 👉 CSS를 사용하여 st.text_input 위젯을 숨깁니다.
# 개발자 도구에서 실제 data-testid와 aria-label을 확인한 후 이 주석을 해제하세요.
st.markdown("""
<style>
/* Streamlit의 st.text_input 위젯을 숨깁니다 (실제 배포 시 사용) */
/* input[data-testid="stTextInputInput"][aria-label="선택한 날짜"] {
    display: none !important;
} */
/* 아래 div.stTextInput는 st.text_input의 부모 컨테이너이므로 함께 숨기거나, 
   aria-label을 통해 input 자체를 정확히 타겟팅하는 것이 좋습니다. */
/* div[data-testid="stTextInput"] {
    display: none !important;
} */
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
    """

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

<script>
function toggleDate(element) {
    // 선택/해제
    element.classList.toggle('selected');

    // 선택된 날짜 수집
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }

    // Streamlit hidden input으로 전달 (input box 업데이트)
    // '선택한 날짜'라는 label을 가진 input을 찾습니다.
    // VM662 오류 발생 시, F12 개발자 도구에서 input의 실제 data-testid와 aria-label 값을 확인하여
    // 아래 querySelector의 선택자를 정확히 수정해야 합니다. (가장 중요한 부분)
    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInputInput"][aria-label="선택한 날짜"]');
    
    if (streamlitInput) {
        streamlitInput.value = selected.join(',');
        // input 이벤트 디스패치 (Streamlit에 변경 사항 알림)
        // 이 이벤트를 통해 Python의 on_change 콜백이 트리거됩니다.
        streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        console.log("JS: Streamlit input updated to:", selected.join(',')); // 디버깅용
    } else {
        console.error("JS: Streamlit hidden input element with label '선택한 날짜' not found!"); // 디버깅용
    }

    // 선택된 날짜 텍스트 업데이트 (사용자에게 시각적으로 보여주기 위함)
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}

// Streamlit 앱이 로드될 때 초기 선택 상태를 반영
// (Python의 st.session_state.selected_dates_list에 기반하여 달력에 'selected' 클래스를 추가합니다)
window.onload = function() {
    // selectedDatesText 요소의 텍스트에서 초기 선택된 날짜 문자열을 파싱합니다.
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
st.components.v1.html(calendar_html, height=600, scrolling=True)

# 👉 결과 버튼
if st.button("결과 계산"):
    # 이제 selected_dates는 st.session_state.selected_dates_list에서 직접 가져옵니다.
    # 이 리스트는 JavaScript가 st.text_input을 업데이트하고 on_change 콜백이 실행될 때마다 최신화됩니다.
    selected_dates = st.session_state.selected_dates_list

    # 👉 결과 계산 로직
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates) # 이제 이 부분이 정확히 카운트됩니다.

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    
    # 14일 기간 내의 날짜들을 'YYYY-MM-DD' 문자열 형식으로 가져옵니다.
    fourteen_days_str = [d.strftime("%Y-%m-%d") for d in cal_dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end]
    
    # 선택된 날짜 목록을 set으로 변환하여 검색 효율성을 높입니다.
    selected_dates_set = set(selected_dates)
    
    # 14일 기간 내에 선택된 근무일이 하나라도 있는지 확인합니다.
    # 모든 14일 기간의 날짜가 selected_dates_set에 없으면 True (근무 내역 없음)
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
