import streamlit as st
import datetime
import calendar
import json
from streamlit_js_eval import streamlit_js_eval # 라이브러리 임포트

# --- CSS 스타일 (이전과 동일) ---
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
/* div.stButton 내부의 button 태그 중 data-selected="true" 속성을 가진 요소에 적용 */
/* Streamlit의 내부 클래스를 더 명시적으로 추가하여 우선순위 높이기 */
.stButton > button[data-selected="true"] { /* div.stButton을 제외하고, 직접 .stButton 클래스 하위의 button을 타겟팅 */
    background-color: #007bff !important; /* 파란색 배경 */
    color: white !important; /* 흰색 글자 */
    border: 2px solid #0056b3 !important; /* 진한 파란색 테두리 */
    box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
}

/* 추가적으로, 마우스 오버 시 선택된 상태의 색상이 바뀌지 않도록 방지 */
.stButton > button[data-selected="true"]:hover {
    background-color: #007bff !important; /* 선택된 상태에서는 호버해도 파란색 유지 */
    border-color: #0056b3 !important;
}

/* (나머지 CSS는 이전과 동일하게 유지) */

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
# 이 함수는 selectedDates_param 매개변수를 받아 버튼 상태를 업데이트합니다.
# MutationObserver는 Streamlit의 DOM 변화를 감지하고 이 함수를 호출합니다.
js_function_definition = """
<script>
    console.log("Streamlit Calendar JS: Script loaded.");

    // 이 함수는 파이썬에서 업데이트된 selectedDates 배열을 받아 호출됩니다.
    window.applyButtonStates = function(selectedDates_param) {
        const selectedDates = new Set(selectedDates_param);
        console.log("JS: applyButtonStates called. Selected dates from Python:", Array.from(selectedDates));

        const buttons = document.querySelectorAll('button[data-testid]');
        // console.log(`JS: Found ${buttons.length} buttons.`); // 너무 많을 수 있어 주석 처리

        buttons.forEach(button => {
            let dateStr = null;
            const dataTestId = button.getAttribute('data-testid');

            if (dataTestId && dataTestId.startsWith('stButton-day_')) {
                dateStr = dataTestId.substring('stButton-day_'.length);

                if (dateStr.match(/^\\d{4}-\\d{2}-\\d{2}$/)) {
                    const isSelected = selectedDates.has(dateStr);
                    button.setAttribute('data-selected', isSelected ? 'true' : 'false');
                    // console.log(`JS: Button for ${dateStr} - isSelected: ${isSelected}, data-selected set to: ${button.getAttribute('data-selected')}`);
                } else {
                    button.removeAttribute('data-selected');
                }
            } else {
                button.removeAttribute('data-selected');
            }
        });
    };

    // MutationObserver는 DOM 변경을 감지하고 applyButtonStates 호출 (초기 로딩 및 리렌더링 시)
    const observer = new MutationObserver((mutationsList, observer) => {
        // 옵저버가 감지한 변경이 실제로 날짜 버튼과 관련이 있는지 확인 (성능 최적화)
        // 여기서는 간단하게 모든 변경에 대해 함수를 호출합니다.
        const currentSelectedDates = window.stSelectedDates || []; // stSelectedDates는 파이썬에서 주입될 전역 변수
        window.applyButtonStates(currentSelectedDates);
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // 초기 로딩 시에도 한 번 실행되도록 (옵저버가 초기 상태를 놓칠 수 있으므로)
    // 그러나 실제 데이터는 Python에서 나중에 주입될 것이므로, 이 첫 호출은 큰 의미 없을 수 있음.
    // setTimeout(() => window.applyButtonStates(window.stSelectedDates || []), 100);
</script>
"""
# JavaScript 함수 정의는 한 번만 삽입합니다. (캐시되어 재실행되지 않도록)
st.markdown(js_function_definition, unsafe_allow_html=True)


# --- 달력 UI 렌더링 ---
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

# 표시해야 할 마지막 날짜
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
if not (st.session_state.input_date.year == first_day_of_previous_month.year and
        st.session_state.input_date.month == first_day_of_previous_month.month):
    months_to_display.append((st.session_state.input_date.year, st.session_state.input_date.month))


for year, month in months_to_display:
    if len(months_to_display) > 1:
        st.markdown(f"<h4 style='text-align: center; margin-top: 15px; margin-bottom: 5px;'>{year}년 {month}월</h4>", unsafe_allow_html=True)

    month_days = cal.monthdatescalendar(year, month)
    for week in month_days:
        cols = st.columns(7)
        for i, day_obj in enumerate(week):
            with cols[i]:
                date_str = day_obj.isoformat()

                is_active_and_in_current_month = (day_obj in active_date_range) and (day_obj.month == month)

                if is_active_and_in_current_month:
                    if st.button(
                        f"{day_obj.day}",
                        key=f"day_{date_str}",
                        help=f"날짜 선택: {date_str}"
                    ):
                        if date_str in st.session_state.selected_dates:
                            st.session_state.selected_dates.remove(date_str)
                        else:
                            st.session_state.selected_dates.add(date_str)
                        st.rerun()
                else:
                    st.button(
                        f"{day_obj.day}",
                        key=f"disabled_day_{date_str}",
                        help=f"선택 불가능한 날짜: {date_str}",
                        disabled=True
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


# --- `streamlit_js_eval`을 사용하여 JavaScript 함수 호출 ---
# 앱이 재렌더링될 때마다 이 부분이 실행되어 최신 selected_dates를 JavaScript로 전달합니다.
streamlit_js_eval(
    js_expressions=[
        f"window.stSelectedDates = {json.dumps(list(st.session_state.selected_dates))};", # 전역 변수에 현재 선택된 날짜들을 저장
        "window.applyButtonStates(window.stSelectedDates);" # 함수 호출
    ],
    key="js_button_update" # 이 컴포넌트의 고유 키
)
