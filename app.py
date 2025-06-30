import streamlit as st
import datetime
import calendar
import json
from streamlit_js_eval import streamlit_js_eval # 라이브러리 임포트

# --- CSS 스타일 ---
# 이 부분은 변경 없이 그대로 유지됩니다.
st.markdown("""
    <style>
    /* 전체 앱 스타일 */
    .stApp {
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    /* 달력 컨테이너 */
    .calendar-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr); /* 7개의 열 (요일) */
        gap: 5px; /* 버튼 사이 간격 */
        max-width: 500px; /* 달력 최대 너비 */
        margin: auto;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* 요일 헤더 */
    .weekday-header {
        text-align: center;
        font-weight: bold;
        padding: 8px 0;
        color: #555;
        background-color: #e8e8e8;
        border-radius: 4px;
        font-size: 0.9em;
    }
    .weekday-header:nth-child(1) { color: red; } /* 일요일 */
    .weekday-header:nth-child(7) { color: blue; } /* 토요일 */

    /* 개별 날짜 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1;
        border: 1px solid #d0d0d0;
        text-align: center;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s, border-color 0.2s, color 0.2s;
        background-color: white;
        color: #333;
        border-radius: 6px;
        padding: 0;
        line-height: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 마우스 오버 시 */
    div.stButton > button:hover {
        background-color: #e8f5ff;
        border-color: #aaddff;
    }

    /* 선택된 날짜 버튼 스타일 - 가장 중요! */
    .stButton > button[data-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
        border: 2px solid #0056b3 !important;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    /* 추가적으로, 마우스 오버 시 선택된 상태의 색상이 바뀌지 않도록 방지 */
    .stButton > button[data-selected="true"]:hover {
        background-color: #007bff !important;
        border-color: #0056b3 !important;
    }

    /* 비활성화된 날짜 스타일 */
    div.stButton > button[data-testid*="-disabled"] {
        background-color: #f0f0f0 !important;
        color: #aaa !important;
        border-color: #e0e0e0 !important;
        cursor: not-allowed;
        opacity: 0.7;
    }
    div.stButton > button[data-testid*="-disabled"]:hover {
        background-color: #f0f0f0 !important;
    }

    </style>
    """, unsafe_allow_html=True)


# --- 세션 상태 초기화 ---
if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = set()
if 'input_date' not in st.session_state:
    st.session_state.input_date = datetime.date.today()

# --- JavaScript 함수 정의 (단 한 번만 삽입) ---
# 이제 이 JavaScript 함수는 window.stSelectedDates 변수를 직접 사용하지 않고,
# applyButtonStates 함수가 직접 인자를 받도록 합니다.
js_function_definition = """
<script>
    console.log("Streamlit Calendar JS: Script loaded.");

    // 이 함수는 파이썬에서 업데이트된 selectedDates 배열을 받아 호출됩니다.
    // 인자로 받은 selectedDates_param을 직접 사용합니다.
    window.applyButtonStates = function(selectedDates_param) {
        const selectedDates = new Set(selectedDates_param);
        console.log("JS: applyButtonStates called. Selected dates from Python (via arg):", Array.from(selectedDates));

        // 선택자 강화: div.stButton 내부의 button 요소를 찾고, data-testid가 특정 형태로 시작하는 것만 선택
        const buttons = document.querySelectorAll('div.stButton > button[data-testid^="stButton-day_"]'); 
        console.log(`JS: Found ${buttons.length} candidate date buttons.`); // 찾은 버튼 수 로깅

        buttons.forEach(button => {
            const dataTestId = button.getAttribute('data-testid');
            if (dataTestId) { 
                // 정규식을 사용하여 'stButton-day_' 이후의 YYYY-MM-DD 형식의 날짜 문자열 추출
                const dateMatch = dataTestId.match(/stButton-day_(\\d{4}-\\d{2}-\\d{2})/); 
                if (dateMatch && dateMatch[1]) {
                    const dateStr = dateMatch[1]; 
                    const isSelected = selectedDates.has(dateStr);
                    button.setAttribute('data-selected', isSelected ? 'true' : 'false');
                    // 디버깅을 위해 이 로그를 활성화하여 개별 버튼의 상태를 확인해볼 수 있습니다.
                    // console.log(`JS: Button for ${dateStr} - isSelected: ${isSelected}, data-selected set to: ${button.getAttribute('data-selected')}`);
                } else {
                    button.removeAttribute('data-selected');
                }
            } else {
                button.removeAttribute('data-selected');
            }
        });
    };

    // MutationObserver는 DOM 변경을 감지하고 applyButtonStates 호출
    // 이 Observer는 주로 Streamlit이 DOM을 다시 그릴 때 발생할 수 있는 변경을 처리합니다.
    const observer = new MutationObserver((mutationsList, observer) => {
        // console.log("JS: DOM Mutation detected by observer.");
        // 파이썬에서 streamlit_js_eval을 통해 applyButtonStates가 호출될 때까지 기다립니다.
        // 이 observer는 초기 로드 시 applyButtonStates가 호출되지 않을 경우의 백업 역할만 합니다.
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // 초기 로딩 시 applyButtonStates가 즉시 호출될 필요는 없습니다.
    // Python에서 streamlit_js_eval을 통해 정확한 시점에 데이터가 전달될 것이기 때문입니다.
    // setTimeout(() => {
    //     // 이 부분은 이제 Python의 streamlit_js_eval에서 데이터를 직접 전달하므로 제거하거나 비활성화합니다.
    //     // 필요하다면, 초기 로드 시 기본적으로 모든 버튼에 data-selected="false"를 설정하는 로직을 추가할 수 있습니다.
    // }, 200); 

</script>
"""
# JavaScript 함수 정의는 앱이 로드될 때 한 번만 삽입됩니다.
st.markdown(js_function_definition, unsafe_allow_html=True)


# --- 달력 UI 렌더링 (이전과 동일) ---
st.title("🗓️ 기간 선택 달력")

# 1. 날짜 입력 받기
selected_input_date = st.date_input(
    "기준 날짜를 선택해주세요:",
    value=st.session_state.input_date,
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date(2100, 12, 31),
    key="date_input_picker"
)

# 입력 날짜가 변경되었을 때 세션 상태 업데이트 및 선택된 날짜 초기화
if selected_input_date != st.session_state.input_date:
    st.session_state.input_date = selected_input_date
    st.session_state.selected_dates = set()
    st.rerun()

# 입력된 날짜 기준 직전 달 초일 계산
first_day_of_previous_month = (st.session_state.input_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

st.header(
    f"{first_day_of_previous_month.year}년 {first_day_of_previous_month.month}월 ~ {st.session_state.input_date.year}년 {st.session_state.input_date.month}월",
    divider='rainbow'
)

st.markdown('<div class="calendar-container">', unsafe_allow_html=True)

# 요일 헤더
weekdays = ["일", "월", "화", "수", "목", "금", "토"]
for day in weekdays:
    st.markdown(f'<div class="weekday-header">{day}</div>', unsafe_allow_html=True)

# 달력 날짜 채우기
cal = calendar.Calendar(firstweekday=6)

# 표시해야 할 마지막 날짜 (현재 날짜 기준)
end_date_inclusive = st.session_state.input_date

# 직전 달 1일부터 입력 날짜까지의 모든 날짜를 포함하는 Set을 만듭니다.
active_date_range = set()
current_date_to_populate = first_day_of_previous_month
while current_date_to_populate <= end_date_inclusive:
    active_date_range.add(current_date_to_populate)
    current_date_to_populate += datetime.timedelta(days=1)


# 달력에 표시할 월 리스트 (직전 달과 현재 달)
months_to_display = []
months_to_display.append((first_day_of_previous_month.year, first_day_of_previous_month.month))
# 현재 달이 직전 달과 다르면 현재 달도 추가합니다.
if not (st.session_state.input_date.year == first_day_of_previous_month.year and
        st.session_state.input_date.month == first_day_of_previous_month.month):
    months_to_display.append((st.session_state.input_date.year, st.session_state.input_date.month))


for year, month in months_to_display:
    if len(months_to_display) > 1: # 두 달을 표시할 때만 월 헤더를 보여줍니다.
        st.markdown(f"<h4 style='text-align: center; margin-top: 15px; margin-bottom: 5px;'>{year}년 {month}월</h4>", unsafe_allow_html=True)

    month_days = cal.monthdatescalendar(year, month)
    for week in month_days:
        cols = st.columns(7)
        for i, day_obj in enumerate(week):
            with cols[i]:
                date_str = day_obj.isoformat() # YYYY-MM-DD 형식의 날짜 문자열

                # 날짜가 활성 범위에 있고 해당 월에 속하는지 확인
                is_active_and_in_current_month = (day_obj in active_date_range) and (day_obj.month == month)

                if is_active_and_in_current_month:
                    if st.button(
                        f"{day_obj.day}",
                        key=f"day_{date_str}", # 고유 키: day_YYYY-MM-DD
                        help=f"날짜 선택: {date_str}"
                    ):
                        # 버튼 클릭 시 선택 상태 토글 및 rerender
                        if date_str in st.session_state.selected_dates:
                            st.session_state.selected_dates.remove(date_str)
                        else:
                            st.session_state.selected_dates.add(date_str)
                        st.rerun() # 선택 상태 변경 시 앱을 다시 렌더링
                else:
                    # 비활성화된 날짜 버튼
                    st.button(
                        f"{day_obj.day}",
                        key=f"disabled_day_{date_str}", # 고유 키: disabled_day_YYYY-MM-DD
                        help=f"선택 불가능한 날짜: {date_str}",
                        disabled=True # 비활성화 상태
                    )


st.markdown('</div>', unsafe_allow_html=True) # calendar-container 닫기


st.markdown(
f"""
---

### 📆 선택 결과

선택된 날짜 수: **{len(st.session_state.selected_dates)}일**
"""
)

# 선택된 날짜 목록 (디버깅/확인용)
if st.session_state.selected_dates:
    st.write("선택된 날짜:")
    sorted_dates = sorted(list(st.session_state.selected_dates))
    st.write(", ".join(sorted_dates))
else:
    st.write("선택된 날짜가 없습니다.")


# --- `streamlit_js_eval`을 사용하여 JavaScript 함수 호출 (핵심 변경!) ---
# 앱이 재렌더링될 때마다 이 부분이 실행되어 최신 selected_dates를 JavaScript로 전달합니다.
streamlit_js_eval(
    js_expressions=[
        # applyButtonStates 함수를 직접 호출하고, 파이썬 데이터를 args로 전달합니다.
        # 이렇게 하면 JavaScript 코드 내에서 window.stSelectedDates 변수를 사용할 필요가 없어집니다.
        "if (typeof window.applyButtonStates === 'function') { window.applyButtonStates(args.selected_dates); }"
    ],
    args={
        # 파이썬의 selected_dates를 'selected_dates'라는 이름의 인자로 JavaScript에 전달합니다.
        "selected_dates": list(st.session_state.selected_dates)
    },
    key="js_button_update" # 이 컴포넌트의 고유 키
)
