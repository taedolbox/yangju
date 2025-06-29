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
    /* Streamlit 내부의 button 태그를 직접 선택합니다. */
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
        padding: 0; /* 내부 패딩 제거 */
        line-height: 1; /* 텍스트 중앙 정렬 */
        display: flex;
        justify-content: center;
        align-items: center;
        /* 기본적으로 data-selected가 없는 상태 */
        border-color: #d0d0d0; /* 기본 테두리 색상 */
    }

    /* 마우스 오버 시 */
    .stApp .stButton > button:hover {
        background-color: #e8f5ff; /* 연한 파랑 */
        border-color: #aaddff;
    }

    /* 선택된 날짜 버튼 스타일 - 가장 중요! */
    /* data-selected="true" 속성이 있는 Streamlit 버튼에 적용 */
    .stApp .stButton > button[data-selected="true"] {
        background-color: #007bff !important; /* 파란색 배경 */
        color: white !important; /* 흰색 글자 */
        border: 2px solid #0056b3 !important; /* 진한 파란색 테두리 */
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    /* 현재 달이 아닌 날짜에 대한 시각적 구분 */
    .stApp .stButton > button[data-other-month="true"] {
        background-color: #f0f0f0 !important;
        color: #aaa !important;
        border-color: #e0e0e0 !important;
        cursor: default;
        opacity: 0.7;
    }
    .stApp .stButton > button[data-other-month="true"]:hover {
        background-color: #f0f0f0 !important; /* 호버 시에도 동일 */
    }

    /* Streamlit 내부 버튼 컨테이너의 마진/패딩 제거 */
    /* 버튼 정렬을 위해 필요할 수 있습니다 */
    .stApp .stButton {
        margin: 0 !important;
        padding: 0 !important;
        width: 100%; /* 버튼 컨테이너도 100% 너비를 차지하게 */
    }
    </style>
    """, unsafe_allow_html=True)


# --- 세션 상태 초기화 ---
if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = set() # 선택된 날짜들을 저장할 set (중복 방지)
if 'current_year' not in st.session_state:
    st.session_state.current_year = datetime.date.today().year
if 'current_month' not in st.session_state:
    st.session_state.current_month = datetime.date.today().month

# --- 날짜 유틸리티 함수 ---
def get_month_name(month_num):
    return datetime.date(1, month_num, 1).strftime('%B')

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
            // Streamlit은 각 st.button에 고유한 data-testid를 부여합니다 (예: stButton-day_YYYY-MM-DD)
            const buttons = document.querySelectorAll('.stButton > button');
            console.log(`JS: Found ${buttons.length} buttons.`);

            buttons.forEach(button => {{
                let dateStr = null;
                const buttonKey = button.getAttribute('data-testid');
                const helpTitle = button.getAttribute('title'); // help='...' 속성이 title로 매핑됨

                // 옵션 1: data-testid에서 날짜 추출 (Streamlit 버전에 따라 다를 수 있음)
                if (buttonKey && buttonKey.startsWith('stButton-day_')) {{
                    dateStr = buttonKey.substring('stButton-day_'.length);
                    // console.log(`JS: Extracted date from data-testid: ${dateStr}`);
                }}
                // 옵션 2: help (title) 속성에서 날짜 추출 (더 견고할 수 있음)
                else if (helpTitle && helpTitle.startsWith('날짜 선택: ')) {{
                    dateStr = helpTitle.substring('날짜 선택: '.length);
                    // console.log(`JS: Extracted date from title: ${dateStr}`);
                }}

                if (dateStr && dateStr.match(/^\d{{4}}-\d{{2}}-\d{{2}}$/)) {{ // YYYY-MM-DD 형식 유효성 검사
                    const isSelected = selectedDates.has(dateStr);
                    button.setAttribute('data-selected', isSelected ? 'true' : 'false');
                    // console.log(`JS: Button for ${dateStr} - isSelected: ${isSelected}, data-selected set to: ${button.getAttribute('data-selected')}`);

                    // 현재 달이 아닌 날짜에 대한 data-other-month 속성 설정
                    // 이 로직은 파이썬에서 해당 날짜를 버튼으로 생성할 때 이미 '다른 달'로 구분했으므로,
                    // 이곳에서는 실제로 필요 없을 수 있습니다. (빈 div로 대체했기 때문)
                    // 하지만 혹시 나중에 다른 달 날짜도 버튼으로 만들 경우를 대비해 예시로 둡니다.
                    // const buttonDate = new Date(dateStr);
                    // if (buttonDate.getMonth() + 1 !== {st.session_state.current_month} || buttonDate.getFullYear() !== {st.session_state.current_year}) {
                    //     button.setAttribute('data-other-month', 'true');
                    // } else {
                    //     button.removeAttribute('data-other-month');
                    // }

                } else {
                    // 날짜 버튼이 아니거나 날짜를 추출할 수 없는 경우, data-selected 초기화
                    button.removeAttribute('data-selected');
                    // console.log(`JS: Non-date button or invalid date extracted: ${button.textContent}, removing data-selected.`);
                }
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
st.title("🗓️ 날짜 선택 달력")

# 월/년 네비게이션
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("◀️ 이전 달", key="prev_month"):
        st.session_state.current_month -= 1
        if st.session_state.current_month < 1:
            st.session_state.current_month = 12
            st.session_state.current_year -= 1
        st.rerun()
with col2:
    st.header(f"{st.session_state.current_year}년 {get_month_name(st.session_state.current_month)}월", divider='rainbow')
with col3:
    if st.button("다음 달 ▶️", key="next_month"):
        st.session_state.current_month += 1
        if st.session_state.current_month > 12:
            st.session_state.current_month = 1
            st.session_state.current_year += 1
        st.rerun()

st.markdown('<div class="calendar-container">', unsafe_allow_html=True)

# 요일 헤더
weekdays = ["일", "월", "화", "수", "목", "금", "토"]
for day in weekdays:
    st.markdown(f'<div class="weekday-header">{day}</div>', unsafe_allow_html=True)

# 달력 날짜 채우기
cal = calendar.Calendar(firstweekday=6) # 일요일부터 시작 (0=월, 6=일)
month_days = cal.monthdatescalendar(st.session_state.current_year, st.session_state.current_month)

for week in month_days:
    cols = st.columns(7) # 한 주에 7개의 컬럼 생성
    for i, day_obj in enumerate(week):
        with cols[i]: # 각 날짜를 해당 컬럼에 배치
            # 현재 달의 날짜만 버튼으로 표시
            if day_obj.month == st.session_state.current_month:
                date_str = day_obj.isoformat() # 'YYYY-MM-DD' 형식

                # Streamlit 버튼 생성
                # key는 JavaScript에서 버튼을 식별하는 데 사용될 수 있도록 f"day_{date_str}" 형식으로 생성
                # help 속성(title로 변환됨)도 JavaScript에서 날짜 추출에 사용
                if st.button(
                    f"{day_obj.day}",
                    key=f"day_{date_str}", # 고유한 키
                    help=f"날짜 선택: {date_str}" # JavaScript가 파싱할 수 있도록 명확한 형식
                ):
                    if date_str in st.session_state.selected_dates:
                        st.session_state.selected_dates.remove(date_str)
                    else:
                        st.session_state.selected_dates.add(date_str)
                    st.rerun() # 날짜 선택 시 페이지 재렌더링

            else:
                # 현재 달이 아닌 날짜는 빈 공간으로 유지
                # CSS Grid 덕분에 자동으로 간격이 맞춰집니다.
                st.markdown(
                    f'<div style="width: 100%; aspect-ratio: 1 / 1; display: flex; justify-content: center; align-items: center; color: #ccc; background-color: #f8f8f8; border: 1px dashed #eee; border-radius: 6px;"></div>',
                    unsafe_allow_html=True
                )


st.markdown('</div>', unsafe_allow_html=True) # calendar-container 닫기

# --- JavaScript 실행 (선택 상태 반영) ---
# 이 함수는 현재 선택된 날짜들을 JavaScript로 전달하고, DOM 조작을 트리거합니다.
# selected_dates는 set이므로, JavaScript로 전달하기 위해 list로 변환해야 합니다.
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
    # 날짜를 정렬하여 보여주기
    sorted_dates = sorted(list(st.session_state.selected_dates))
    st.write(", ".join(sorted_dates))
else:
    st.write("선택된 날짜가 없습니다.")
