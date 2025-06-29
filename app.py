import streamlit as st
import datetime
import calendar
import json # JavaScript로 데이터 전달을 위해 필요

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
    .stApp .stButton > button {
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
    .stApp .stButton > button:hover {
        background-color: #e8f5ff; /* 연한 파랑 */
        border-color: #aaddff;
    }

    /* 선택된 날짜 버튼 스타일 - 가장 중요! */
    .stApp .stButton > button[data-selected="true"] {
        background-color: #007bff !important; /* 파란색 배경 */
        color: white !important; /* 흰색 글자 */
        border: 2px solid #0056b3 !important; /* 진한 파란색 테두리 */
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    /* 비활성화된 날짜 스타일 (달력 범위 밖) */
    .stApp .stButton > button[data-disabled="true"] {
        background-color: #f0f0f0 !important;
        color: #aaa !important;
        border-color: #e0e0e0 !important;
        cursor: not-allowed; /* 클릭 불가능 커서 */
        opacity: 0.7;
    }
    .stApp .stButton > button[data-disabled="true"]:hover {
        background-color: #f0f0f0 !important; /* 호버 시에도 동일 */
    }

    /* Streamlit 내부 버튼 컨테이너의 마진/패딩 제거 */
    .stApp .stButton {
        margin: 0 !important;
        padding: 0 !important;
        width: 100%;
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
        // console.log("Streamlit Calendar JS: Script loaded.");

        // 이 함수는 모든 Streamlit 렌더링 후에 호출되어 버튼 상태를 업데이트합니다.
        function applyButtonStates() {{
            const selectedDates = new Set({selected_dates_js_array});
            // console.log("JS: applyButtonStates called. Selected dates from Python:", Array.from(selectedDates));

            const buttons = document.querySelectorAll('.stButton > button');
            // console.log(`JS: Found ${{buttons.length}} buttons.`);

            buttons.forEach(button => {{
                let dateStr = null;
                const helpTitle = button.getAttribute('title'); // help='...' 속성이 title로 매핑됨

                if (helpTitle && helpTitle.startsWith('날짜 선택: ')) {{
                    dateStr = helpTitle.substring('날짜 선택: '.length);
                    // console.log(`JS: Extracted date from title: ${{dateStr}}`);
                }}

                if (dateStr && dateStr.match(/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/)) {{ // YYYY-MM-DD 형식 유효성 검사
                    const isSelected = selectedDates.has(dateStr);
                    button.setAttribute('data-selected', isSelected ? 'true' : 'false');
                    // console.log(`JS: Button for ${{dateStr}} - isSelected: ${{isSelected}}, data-selected set to: ${{button.getAttribute('data-selected')}}`);

                    // 비활성화된 날짜는 data-disabled="true" 속성을 설정 (Python에서 처리하지만 혹시 모를 경우를 대비)
                    // 이 부분은 Python에서 이미 'disabled' 버튼으로 만들었으므로 JS에서는 조작할 필요가 없습니다.
                    // 그러나 JS에서 시각적으로만 비활성화를 표현하고 싶다면 활용 가능.
                }} else {{
                    // 날짜 버튼이 아니거나 날짜를 추출할 수 없는 경우, data-selected 초기화
                    button.removeAttribute('data-selected');
                    // console.log(`JS: Non-date button or invalid date extracted: ${{button.textContent}}, removing data-selected.`);
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
first_day_of_previous_month = (st.session_state.input_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
# 입력된 날짜 기준 달까지 표시 (단, 입력된 날짜까지만 클릭 가능)
display_year = first_day_of_previous_month.year
display_month = first_day_of_previous_month.month

st.header(f"{first_day_of_previous_month.year}년 {first_day_of_previous_month.month}월 ~ {st.session_state.input_date.year}년 {st.session_state.input_date.month}월", divider='rainbow')

st.markdown('<div class="calendar-container">', unsafe_allow_html=True)

# 요일 헤더
weekdays = ["일", "월", "화", "수", "목", "금", "토"]
for day in weekdays:
    st.markdown(f'<div class="weekday-header">{day}</div>', unsafe_allow_html=True)

# 달력 날짜 채우기
cal = calendar.Calendar(firstweekday=6) # 일요일부터 시작 (0=월, 6=일)

# 직전 달의 날짜들을 가져옴
month_days_prev = cal.monthdatescalendar(first_day_of_previous_month.year, first_day_of_previous_month.month)
# 현재 달의 날짜들을 가져옴
month_days_current = cal.monthdatescalendar(st.session_state.input_date.year, st.session_state.input_date.month)

# 두 달의 날짜를 합치되, 중복되는 주(직전 달 마지막 주와 현재 달 첫 주가 겹칠 수 있음)는 처리 필요
# 여기서는 간단하게 두 달 전체를 그리는 방식으로 하겠습니다.
# 실제로는 겹치는 부분을 제거하고, 입력된 날짜까지만 표시해야 합니다.

# 입력된 날짜의 직전 달부터 시작 (이 부분의 렌더링 로직을 좀 더 정교하게 만듦)
current_date_to_render = first_day_of_previous_month

# 표시해야 할 마지막 날짜
end_date_inclusive = st.session_state.input_date

# 직전 달 1일부터 입력 날짜까지의 모든 날짜를 포함하는 Set을 만듭니다.
# 이는 날짜 버튼을 활성화/비활성화 하는 기준으로 사용됩니다.
active_date_range = set()
delta = datetime.timedelta(days=1)
while current_date_to_render <= end_date_inclusive:
    active_date_range.add(current_date_to_render)
    current_date_to_render += delta

# 이제 두 달 (직전 달, 현재 달)을 모두 표시합니다.
# 첫 번째 달 (직전 달) 렌더링
for week in month_days_prev:
    cols = st.columns(7)
    for i, day_obj in enumerate(week):
        with cols[i]:
            # 달력 표시 범위 내에 있는 날짜 (직전 달 1일부터 입력 날짜까지)
            is_in_active_range = day_obj in active_date_range

            if is_in_active_range:
                date_str = day_obj.isoformat()
                is_selected = date_str in st.session_state.selected_dates

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
                # 활성 범위 밖의 날짜는 비활성화된 것처럼 표시
                # date_str을 만들어서 data-disabled="true"를 JavaScript에서 부여하도록 하거나,
                # 아예 버튼을 만들지 않고 비활성 div로 대체.
                # 여기서는 버튼을 만들되 data-disabled로 처리하여 JS에서 스타일링하도록 합니다.
                date_str = day_obj.isoformat()
                st.button(
                    f"{day_obj.day}",
                    key=f"disabled_day_{date_str}", # 고유 키
                    help=f"선택 불가능한 날짜: {date_str}",
                    disabled=True # Streamlit의 기본 disabled 기능 활용
                )
                # Note: Streamlit의 disabled=True는 버튼을 클릭할 수 없게 만들지만,
                # 커스텀 CSS를 위한 data-disabled="true" 속성은 JS에서 부여해야 합니다.
                # 현재는 기본 disabled 스타일 + JS에서 data-disabled를 부여하는 형태로 동작.


# 두 번째 달 (현재 달) 렌더링 (단, 현재 달은 입력 날짜까지만 활성화)
# 이미 active_date_range에 입력 날짜까지 모든 날짜가 포함되어 있습니다.
for week in month_days_current:
    cols = st.columns(7)
    for i, day_obj in enumerate(week):
        with cols[i]:
            is_in_active_range = day_obj in active_date_range

            if is_in_active_range:
                date_str = day_obj.isoformat()
                is_selected = date_str in st.session_state.selected_dates

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
                # 활성 범위 밖의 날짜는 비활성화
                date_str = day_obj.isoformat()
                st.button(
                    f"{day_obj.day}",
                    key=f"disabled_day_{date_str}",
                    help=f"선택 불가능한 날짜: {date_str}",
                    disabled=True
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
