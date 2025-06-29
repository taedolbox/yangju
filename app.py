import streamlit as st
import datetime
import calendar
import json

# --- CSS 스타일 ---
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
    /* Streamlit이 생성하는 버튼의 실제 HTML 구조를 고려한 선택자 */
    /* stButton 클래스 내부의 button 태그 */
    div.stButton > button {
        width: 100%; /* 컬럼 너비에 맞춤 */
        aspect-ratio: 1 / 1; /* 가로 세로 비율 1:1 (정사각형) */
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
        background-color: #e8f5ff; /* 연한 파랑 */
        border-color: #aaddff;
    }

    /* 선택된 날짜 버튼 스타일 - 가장 중요! */
    /* data-selected="true" 속성이 있는 Streamlit 버튼에 적용 */
    /* div.stButton을 추가하여 선택자의 우선순위를 높임 */
    div.stButton > button[data-selected="true"] {
        background-color: #007bff !important; /* 파란색 배경 */
        color: white !important; /* 흰색 글자 */
        border: 2px solid #0056b3 !important; /* 진한 파란색 테두리 */
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    /* 비활성화된 날짜 스타일 (달력 범위 밖) */
    /* Streamlit의 disabled 속성으로 인해 자동으로 data-testid에 "-disabled"가 붙습니다. */
    /* 또는 직접 data-disabled="true"를 부여할 수도 있습니다. */
    div.stButton > button[data-testid*="-disabled"] { /* disabled 버튼을 더 일반적인 방식으로 선택 */
        background-color: #f0f0f0 !important;
        color: #aaa !important;
        border-color: #e0e0e0 !important;
        cursor: not-allowed; /* 클릭 불가능 커서 */
        opacity: 0.7;
    }
    div.stButton > button[data-testid*="-disabled"]:hover {
        background-color: #f0f0f0 !important; /* 호버 시에도 동일 */
    }

    </style>
    """, unsafe_allow_html=True)


# --- 세션 상태 초기화 ---
if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = set() # 선택된 날짜들을 저장할 set (중복 방지)
if 'input_date' not in st.session_state:
    st.session_state.input_date = datetime.date.today() # 기본값은 오늘 날짜

# --- JavaScript 삽입 함수 ---
def inject_js_for_button_styling(selected_dates_list):
    # Python set을 JavaScript에서 사용할 수 있는 JSON 배열 문자열로 변환
    selected_dates_js_array = json.dumps(selected_dates_list)

    js_code = f"""
    <script>
        console.log("Streamlit Calendar JS: Script loaded.");

        // 이 함수는 모든 Streamlit 렌더링 후에 호출되어 버튼 상태를 업데이트합니다.
        function applyButtonStates() {{
            const selectedDates = new Set({selected_dates_js_array});
            console.log("JS: applyButtonStates called. Selected dates from Python:", Array.from(selectedDates));

            // 모든 Streamlit 버튼 요소를 찾습니다.
            // data-testid 속성을 가진 모든 버튼을 선택합니다.
            const buttons = document.querySelectorAll('button[data-testid]');
            console.log(`JS: Found ${{buttons.length}} buttons.`);

            buttons.forEach(button => {{
                let dateStr = null;
                const dataTestId = button.getAttribute('data-testid'); // data-testid 속성 가져오기

                // data-testid가 'stButton-day_YYYY-MM-DD' 형식인지 확인
                if (dataTestId && dataTestId.startsWith('stButton-day_')) {{
                    // 'stButton-day_' 접두사를 제거하여 날짜 문자열 추출
                    dateStr = dataTestId.substring('stButton-day_'.length);
                    // console.log(`JS: Extracted date from data-testid: ${{dateStr}}`);

                    // 날짜 문자열이 유효한 YYYY-MM-DD 형식인지 확인
                    if (dateStr.match(/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/)) {{
                        const isSelected = selectedDates.has(dateStr);
                        button.setAttribute('data-selected', isSelected ? 'true' : 'false');
                        // console.log(`JS: Button for ${{dateStr}} - isSelected: ${{isSelected}}, data-selected set to: ${{button.getAttribute('data-selected')}}`);
                    }} else {{
                        // 유효하지 않은 날짜 형식인 경우 data-selected 제거
                        button.removeAttribute('data-selected');
                        // console.log(`JS: Invalid date format for ${{dateStr}}, removing data-selected.`);
                    }}
                }} else {{
                    // 날짜 버튼이 아니거나 data-testid 형식이 일치하지 않는 경우 data-selected 제거
                    button.removeAttribute('data-selected');
                    // console.log(`JS: Non-date button or data-testid mismatch: ${{dataTestId}}, removing data-selected.`);
                }}
            }});
        }}

        // Streamlit 렌더링 완료 후 함수 실행 보장:
        // MutationObserver는 DOM 변경을 감지하여 applyButtonStates를 호출합니다.
        const observer = new MutationObserver((mutationsList, observer) => {{
            // console.log("JS: DOM Mutation detected.");
            applyButtonStates();
        }});

        // document.body의 자식 변경 및 하위 트리의 모든 변경을 감시합니다.
        observer.observe(document.body, {{ childList: true, subtree: true }});

        // 스크립트 로드 시 즉시 한 번 실행 (초기 렌더링 시)
        applyButtonStates();

        // 0.1초 후에도 다시 실행하여 모든 컴포넌트가 로드되었는지 확인 (안정성 강화)
        setTimeout(applyButtonStates, 100);
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

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
    st.session_state.selected_dates = set() # 날짜 범위가 변경되면 선택된 날짜 초기화
    st.rerun() # 재실행하여 달력 업데이트

# 입력된 날짜 기준 직전 달 초일 계산
# 예를 들어 2023-03-15를 입력하면, 2023-02-01이 시작 날짜가 됩니다.
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
cal = calendar.Calendar(firstweekday=6) # 일요일부터 시작 (0=월, 6=일)

# 표시해야 할 마지막 날짜
end_date_inclusive = st.session_state.input_date

# 직전 달 1일부터 입력 날짜까지의 모든 날짜를 포함하는 Set을 만듭니다.
# 이는 날짜 버튼을 활성화/비활성화 하는 기준으로 사용됩니다.
active_date_range = set()
current_date_to_populate = first_day_of_previous_month
while current_date_to_populate <= end_date_inclusive:
    active_date_range.add(current_date_to_populate)
    current_date_to_populate += datetime.timedelta(days=1)


# 달력에 표시할 월 리스트 (직전 달과 현재 달)
months_to_display = []
months_to_display.append((first_day_of_previous_month.year, first_day_of_previous_month.month))
# 현재 달이 직전 달과 다르면 추가
if not (st.session_state.input_date.year == first_day_of_previous_month.year and
        st.session_state.input_date.month == first_day_of_previous_month.month):
    months_to_display.append((st.session_state.input_date.year, st.session_state.input_date.month))


for year, month in months_to_display:
    # 각 월의 이름 표시 (선택 사항)
    if len(months_to_display) > 1: # 두 달 이상 표시될 때만 월 이름 표시
        st.markdown(f"<h4 style='text-align: center; margin-top: 15px; margin-bottom: 5px;'>{year}년 {month}월</h4>", unsafe_allow_html=True)

    month_days = cal.monthdatescalendar(year, month)
    for week in month_days:
        cols = st.columns(7) # 한 주에 7개의 컬럼 생성
        for i, day_obj in enumerate(week):
            with cols[i]: # 각 날짜를 해당 컬럼에 배치
                date_str = day_obj.isoformat() # 'YYYY-MM-DD' 형식

                # 해당 날짜가 활성 범위 내에 있고, 현재 표시하는 달에 속하는지 확인
                is_active_and_in_current_month = (day_obj in active_date_range) and (day_obj.month == month)

                if is_active_and_in_current_month:
                    # 클릭 가능한 버튼
                    if st.button(
                        f"{day_obj.day}",
                        key=f"day_{date_str}", # 고유한 키 (data-testid로 자동 변환)
                        help=f"날짜 선택: {date_str}" # JavaScript가 파싱할 수 있도록 명확한 형식
                    ):
                        if date_str in st.session_state.selected_dates:
                            st.session_state.selected_dates.remove(date_str)
                        else:
                            st.session_state.selected_dates.add(date_str)
                        st.rerun() # 날짜 선택 시 페이지 재렌더링
                else:
                    # 비활성 날짜 (클릭 불가능)
                    # Streamlit의 disabled=True를 사용하면 자동으로 data-testid에 '-disabled'가 붙습니다.
                    # CSS에서 이 속성을 활용하여 스타일링합니다.
                    st.button(
                        f"{day_obj.day}",
                        key=f"disabled_day_{date_str}", # 고유 키
                        help=f"선택 불가능한 날짜: {date_str}",
                        disabled=True # Streamlit의 기본 disabled 기능 활용
                    )


st.markdown('</div>', unsafe_allow_html=True) # calendar-container 닫기

# --- JavaScript 실행 (선택 상태 반영) ---
# 이 함수는 현재 선택된 날짜들을 JavaScript로 전달하고, DOM 조작을 트리거합니다.
inject_js_for_button_styling(list(st.session_state.selected_dates))


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
