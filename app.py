import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

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

# 👉 숨겨진 input 박스로 JS → Python 데이터 전달
# Streamlit의 session_state를 사용해 선택된 날짜를 저장
if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = ""

# 👉 HTML + JS 달력 생성
calendar_html = """
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
"""

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
        calendar_html += f'''
        <div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>
        '''

    calendar_html += "</div>"

calendar_html += """
<p id="selectedDatesText"></p>

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

    // Streamlit 입력 필드 업데이트
    var inputField = document.querySelector('input[id="selected_dates"]');
    if (inputField) {
        inputField.value = selected.join(',');
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
    }

    // 선택된 날짜 표시
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + (selected.length > 0 ? selected.join(', ') : "없음") + " (총 " + selected.length + "일)";
}

// 페이지 로드 시 기존 선택된 날짜 복원
window.onload = function() {
    var selectedDates = " """ + st.session_state.selected_dates + """ ".split(',').filter(date => date);
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (selectedDates.includes(days[i].getAttribute('data-date'))) {
            days[i].classList.add('selected');
        }
    }
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + (selectedDates.length > 0 ? selectedDates.join(', ') : "없음") + " (총 " + selectedDates.length + "일)";
};
</script>
"""

# Streamlit의 숨겨진 input 필드
selected_dates_str = st.text_input("선택한 날짜", value=st.session_state.selected_dates, key="selected_dates", label_visibility="hidden")

# HTML 렌더링
st.components.v1.html(calendar_html, height=600, scrolling=True)

# 👉 결과 버튼
if st.button("결과 계산"):
    # 선택된 날짜 처리
    if selected_dates_str:
        selected_dates = [d.strip() for d in selected_dates_str.split(",") if d.strip()]
    else:
        selected_dates = []

    # 👉 결과 계산 로직
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days = [d for d in cal_dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end]
    selected_dates_set = set(selected_dates)
    no_work_14_days = all(d.strftime("%Y-%m-%d") not in selected_dates_set for d in fourteen_days)

    # 디버깅 정보 출력
    st.write(f"**디버깅 정보**")
    st.write(f"선택된 날짜: {selected_dates}")
    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")
    st.write(f"직전 14일간 ({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}): {'근무 없음' if no_work_14_days else '근무 있음'}")

    # 조건 출력
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

