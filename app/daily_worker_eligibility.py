import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 세션 상태 초기화
# 'selected_dates_list'가 세션 상태에 없으면 빈 리스트로 초기화합니다.
# 이렇게 하면 앱이 처음 로드될 때 또는 세션이 리셋될 때 항상 유효한 리스트를 가집니다.
if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []
    # 초기화 시에도 혹시 모를 타입 불일치를 방지하기 위해,
    # 리스트 안의 요소들이 모두 문자열인지 확인하거나 변환하는 로직을 추가할 수 있습니다.
    # 현재는 빈 리스트이므로 필요 없지만, 다른 초기값을 사용한다면 고려해볼 수 있습니다.

# JavaScript 컴포넌트로부터 데이터를 받을 콜백 함수
# 이 함수는 st.components.v1.html 컴포넌트가 Python으로 값을 보낼 때 호출됩니다.
# Streamlit이 컴포넌트의 '새로운 값'을 첫 번째 인자로 전달합니다.
def receive_selected_dates(new_value):
    # 디버깅: 콜백 함수가 호출되었는지, 어떤 값이 수신되었는지 확인합니다.
    st.write(f"DEBUG: receive_selected_dates 콜백 호출됨. 수신 값: {new_value}")

    # 수신된 값이 None이 아닌지 명시적으로 확인합니다.
    if new_value is not None:
        try:
            # JSON 문자열을 파이썬 리스트로 변환합니다.
            loaded_list = json.loads(new_value)
            
            # 수신된 값이 실제로 리스트인지, 그리고 그 안의 요소들이 모두 문자열인지 확인합니다.
            if isinstance(loaded_list, list) and all(isinstance(item, str) for item in loaded_list):
                st.session_state.selected_dates_list = loaded_list
            else:
                # 예상치 못한 형식의 데이터가 수신되었을 때의 처리
                st.error("수신된 날짜 데이터가 예상된 리스트<문자열> 형식이 아닙니다. 초기화합니다.")
                st.session_state.selected_dates_list = []
        except json.JSONDecodeError as e:
            # JSON 디코딩 중 에러가 발생했을 때의 처리
            st.error(f"날짜 데이터 디코딩 실패: {e}. 리스트를 초기화합니다.")
            st.session_state.selected_dates_list = []
    else:
        # new_value가 None일 경우 (예: 컴포넌트 리셋 시), 리스트를 비웁니다.
        st.session_state.selected_dates_list = []

    # 디버깅: 세션 상태가 어떻게 업데이트되었는지 확인합니다.
    st.write(f"DEBUG: selected_dates_list 업데이트됨: {st.session_state.selected_dates_list}")

# 기준 날짜 선택 (Streamlit의 내장 date_input 위젯 사용)
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 달력 범위 설정: 입력 날짜 기준 직전 달의 1일부터 입력 날짜까지
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

# 달력에 표시할 모든 날짜 리스트 생성
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# 년/월 별로 날짜를 그룹화
calendar_groups = {}
for date in cal_dates:
    year_month = date.strftime("%Y-%m")
    if year_month not in calendar_groups:
        calendar_groups[year_month] = []
    calendar_groups[year_month].append(date)

# HTML + CSS + JavaScript가 포함된 달력 문자열 생성
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

    # 월의 첫 날 요일을 기준으로 빈 칸 추가 (달력 정렬)
    first_day_of_month = dates[0]
    start_day_offset = (first_day_of_month.weekday() + 1) % 7 # 0(월)~6(일) -> 0(일)~6(토)로 변경
    for _ in range(start_day_offset):
        calendar_html += '<div class="empty-day"></div>'

    # 각 날짜에 대한 HTML 생성
    for date in dates:
        day_num = date.day
        date_str = date.strftime("%Y-%m-%d")
        # Python 세션 상태에 저장된 선택된 날짜 목록을 기반으로 'selected' 클래스 추가
        is_selected = " selected" if date_str in st.session_state.selected_dates_list else ""
        calendar_html += f'''
        <div class="day{is_selected}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>
        '''

    calendar_html += "</div>" # .calendar 닫기

# CSS 스타일 및 JavaScript 코드 추가
calendar_html += """
<p id="selectedDatesText"></p>
<style>
/* 달력 그리드 컨테이너 스타일 */
.calendar { 
    display: grid; 
    grid-template-columns: repeat(7, 40px); /* 7개 열, 각 열 너비 40px */
    grid-gap: 5px; /* 그리드 셀 간의 간격 */
    margin-bottom: 20px; 
    background-color: #ffffff; 
    padding: 10px; 
    border-radius: 8px; 
    box-shadow: 0 2px 10px rgba(0,0,0,0.1); /* 그림자 효과 */
}

/* 요일 헤더 및 빈 날짜 칸 스타일 */
.day-header, .empty-day { 
    width: 40px; 
    height: 40px; 
    line-height: 40px; /* 텍스트 세로 중앙 정렬 */
    text-align: center; 
    font-weight: bold; 
    color: #555; 
}

/* 요일 헤더별 스타일 */
.day-header { 
    background-color: #e0e0e0; 
    border-radius: 5px; 
    font-size: 14px; 
}

/* 빈 날짜 칸 스타일 (투명) */
.empty-day { 
    background-color: transparent; 
    border: none; 
}

/* 개별 날짜 칸 스타일 */
.day { 
    width: 40px; 
    height: 40px; 
    line-height: 40px; 
    text-align: center; 
    border: 1px solid #ddd; 
    border-radius: 5px; 
    cursor: pointer; /* 클릭 가능한 커서 */
    user-select: none; /* 텍스트 선택 방지 */
    transition: background-color 0.1s ease, border 0.1s ease; /* 부드러운 전환 효과 */
    font-size: 16px; 
    color: #333; 
}

/* 날짜 칸 호버 시 스타일 */
.day:hover { 
    background-color: #f0f0f0; 
}

/* 선택된 날짜 칸 스타일 */
.day.selected { 
    border: 2px solid #2196F3; /* 파란색 테두리 */
    background-color: #2196F3; /* 파란색 배경 */
    color: white; /* 흰색 글자 */
    font-weight: bold; 
}

/* 월 제목 스타일 */
h4 { 
    margin: 10px 0 5px 0; 
    font-size: 1.2em; 
    color: #333; 
    text-align: center; 
}

/* 선택된 날짜 텍스트 표시 영역 스타일 */
#selectedDatesText { 
    margin-top: 15px; 
    font-size: 0.9em; 
    color: #666; 
}
</style>

<script>
// Streamlit 컴포넌트 API에 접근하기 위한 객체
const streamlit = window.parent.Streamlit;

// 날짜 클릭 시 호출되는 함수
function toggleDate(element) {
    // 'selected' 클래스를 토글하여 시각적인 선택/해제 상태 변경
    element.classList.toggle('selected');

    // 현재 선택된 모든 날짜를 수집
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }

    // 선택된 날짜 리스트를 JSON 문자열로 변환하여 Python으로 전달
    // 이 호출은 Python의 receive_selected_dates 함수를 트리거합니다.
    streamlit.setComponentValue(JSON.stringify(selected));

    // 디버깅을 위해 콘솔에 로그 출력 (개발자 도구에서 확인 가능)
    console.log("JS: Streamlit component value updated to:", JSON.stringify(selected)); 

    // 현재 선택된 날짜를 사용자에게 시각적으로 표시 (HTML 내의 <p> 태그 업데이트)
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}

// 웹 페이지 로드 완료 시 실행되는 함수
window.onload = function() {
    // 이 초기 로드 로직은 Python 세션 상태에 선택된 날짜가 있을 경우,
    // 페이지가 처음 로드되거나 새로고침될 때 달력에 해당 날짜를 반영하기 위한 것입니다.
    // Python에서 HTML을 생성할 때 이미 'selected' 클래스를 추가하고 있으므로,
    // 이 부분은 주로 HTML에 초기값이 반영된 후 JS가 다시 한번 시각적으로 일치시키기 위함입니다.
    const currentSelectedTextElement = document.getElementById('selectedDatesText');
    if (currentSelectedTextElement) {
        const currentSelectedText = currentSelectedTextElement.innerText;
        // 텍스트 내용에서 "선택한 날짜:" 문자열을 포함하는지 확인
        if (currentSelectedText.includes("선택한 날짜:")) {
            // 초기 선택된 날짜 문자열을 파싱
            const initialDatesStr = currentSelectedText.split("선택한 날짜: ")[1]?.split(" (총")[0];
            if (initialDatesStr && initialDatesStr.length > 0) {
                var initialSelectedArray = initialDatesStr.split(', ');
                var days = document.getElementsByClassName('day');
                // 모든 날짜 요소들을 순회하며 초기 선택 상태 반영
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

# HTML 컴포넌트의 기본값 생성 (항상 유효한 JSON 문자열)
# Streamlit 컴포넌트에 초기값을 전달하기 위해 현재 세션 상태의 선택된 날짜 리스트를 JSON 문자열로 변환합니다.
# 이렇게 하면 JavaScript 쪽에서 이 값을 파싱하여 초기 UI를 구성할 수 있습니다.
component_default_value = json.dumps(st.session_state.selected_dates_list)

# Streamlit Component 렌더링
# `st.components.v1.html` 함수를 사용하여 정의된 HTML 컨텐츠를 Streamlit 앱에 삽입합니다.
# `height`, `scrolling` 등은 컴포넌트의 시각적 속성을 제어합니다.
# `key`는 Streamlit 세션 상태에서 이 컴포넌트의 값을 고유하게 식별하는 데 사용됩니다.
# `on_change`는 JavaScript 컴포넌트에서 `streamlit.setComponentValue()`를 호출할 때
# Python에서 실행될 콜백 함수를 지정합니다.
# `default`는 컴포넌트의 초기 값으로 JavaScript에 전달될 값입니다.
component_value = st.components.v1.html(
    calendar_html,
    height=600,
    scrolling=True,
    key="calendar_component", # 고유한 키를 지정하여 세션 상태와 연결
    on_change=receive_selected_dates, # 콜백 함수 연결
    default=component_default_value # 초기값 전달
)

# 결과 계산 버튼 (Streamlit의 내장 버튼 위젯 사용)
if st.button("결과 계산"):
    # `st.session_state.selected_dates_list`는 `receive_selected_dates` 콜백 함수에 의해
    # 이미 최신 JavaScript 컴포넌트의 값으로 업데이트되어 있습니다.
    # 따라서 버튼 클릭 시점에는 항상 최신 선택 날짜 목록을 사용할 수 있습니다.
    selected_dates = st.session_state.selected_dates_list

    # 총 기간 일수 계산
    total_days = len(cal_dates)
    # 기준 (총 일수의 1/3) 계산
    threshold = total_days / 3
    # 선택된 근무일 수
    worked_days = len(selected_dates)

    # 신청일 직전 14일간의 날짜 범위 계산
    fourteen_days_prior_end = input_date - timedelta(days=1) # 신청일 하루 전까지
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13) # 14일 전 시작

    # 달력에 표시된 날짜 중 직전 14일 범위에 해당하는 날짜들 필터링
    fourteen_days_str = [
        d.strftime("%Y-%m-%d") for d in cal_dates
        if fourteen_days_prior_start <= d <= fourteen_days_prior_end
    ]
    
    # 빠른 조회를 위해 선택된 날짜를 세트(set)로 변환
    selected_dates_set = set(selected_dates)
    
    # 직전 14일간 근무 내역이 없는지 확인
    no_work_14_days = all(d not in selected_dates_set for d in fourteen_days_str)

    # 계산 결과 및 조건 충족 여부 표시
    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    st.write(f"{'✅ 조건 1 충족: 근무일 수가 기준 미만입니다.' if worked_days < threshold else '❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.'}")
    st.write(f"{'✅ 조건 2 충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 근무내역이 없습니다.' if no_work_14_days else '❌ 조건 2 불충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 내 근무기록이 존재합니다.'}")

    # 최종 판단
    st.markdown("### 📌 최종 판단")
    if worked_days < threshold:
        st.write(f"✅ 일반일용근로자: 신청 가능")
    else:
        st.write(f"❌ 일반일용근로자: 신청 불가능")

    if worked_days < threshold and no_work_14_days:
        st.write(f"✅ 건설일용근로자: 신청 가능")
    else:
        st.write(f"❌ 건설일용근로자: 신청 불가능")
