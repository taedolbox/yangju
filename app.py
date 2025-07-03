import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []

def receive_selected_dates(new_value):
    st.write(f"DEBUG: receive_selected_dates 콜백 호출됨. 수신 값: {new_value}")
    if new_value is not None:
        try:
            loaded_list = json.loads(new_value)
            if isinstance(loaded_list, list) and all(isinstance(item, str) for item in loaded_list):
                st.session_state.selected_dates_list = loaded_list
            else:
                st.error("수신된 날짜 데이터가 예상된 리스트<문자열> 형식이 아닙니다.")
                st.session_state.selected_dates_list = []
        except json.JSONDecodeError as e:
            st.error(f"날짜 데이터 디코딩 실패: {e}")
            st.session_state.selected_dates_list = []
    else:
        st.session_state.selected_dates_list = []
    st.write(f"DEBUG: selected_dates_list 업데이트됨: {st.session_state.selected_dates_list}")

# --- (달력 데이터 준비 및 HTML 생성 로직은 이전과 동일) ---
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

calendar_html = ""
for ym, dates in calendar_groups.items():
    year = ym.split("-")[0]
    month = ym.split("-")[1]
    calendar_html += f"""
    <h4>{year}년 {month}월</h4>
    <div class="calendar">
        <div class="day-header">일</div><div class="day-header">월</div><div class="day-header">화</div><div class="day-header">수</div><div class="day-header">목</div><div class="day-header">금</div><div class="day-header">토</div>
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
.calendar { display: grid; grid-template-columns: repeat(7, 40px); grid-gap: 5px; margin-bottom: 20px; background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.day-header, .empty-day { width: 40px; height: 40px; line-height: 40px; text-align: center; font-weight: bold; color: #555; }
.day-header { background-color: #e0e0e0; border-radius: 5px; font-size: 14px; }
.empty-day { background-color: transparent; border: none; }
.day { width: 40px; height: 40px; line-height: 40px; text-align: center; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none; transition: background-color 0.1s ease, border 0.1s ease; font-size: 16px; color: #333; }
.day:hover { background-color: #f0f0f0; }
.day.selected { border: 2px solid #2196F3; background-color: #2196F3; color: white; font-weight: bold; }
h4 { margin: 10px 0 5px 0; font-size: 1.2em; color: #333; text-align: center; }
#selectedDatesText { margin-top: 15px; font-size: 0.9em; color: #666; }
</style>

<script>
const streamlit = window.parent.Streamlit;
function toggleDate(element) {
    element.classList.toggle('selected');
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }
    streamlit.setComponentValue(JSON.stringify(selected)); 
    console.log("JS: Streamlit component value updated to:", JSON.stringify(selected)); 
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

st.write("### 3단계: `on_change` 인자 추가 테스트 (최종)")
st.write("이 단계에서 `TypeError`가 발생한다면, `on_change` 콜백 함수나 JavaScript의 `setComponentValue` 호출 과정에 문제가 있을 수 있습니다.")

component_default_value = json.dumps(st.session_state.selected_dates_list)

try:
    # 모든 인자 포함 (원래 코드)
    component_value = st.components.v1.html(
        calendar_html,
        height=600,
        scrolling=True,
        key="calendar_component", # 원래 키 사용
        default=component_default_value,
        on_change=receive_selected_dates # on_change 콜백 함수 추가
    )
    st.write("✅ 최종 컴포넌트 렌더링 성공! (TypeError 없음)")
    st.write("이제 날짜를 클릭하고 '결과 계산' 버튼을 눌러보세요.")
except TypeError as e:
    st.error(f"❌ 3단계 테스트 실패: TypeError 발생 - {e}")
    st.stop()
except Exception as e:
    st.error(f"❌ 3단계 테스트 실패: 알 수 없는 에러 발생 - {e}")
    st.stop()


# --- 결과 계산 버튼 (모든 단계에서 동일) ---
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
