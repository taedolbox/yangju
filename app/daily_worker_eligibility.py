import streamlit as st
from datetime import datetime, timedelta

# 페이지 기본 설정
st.set_page_config(page_title="네모형 달력", layout="centered")

# 기준 날짜 입력
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 달력 날짜 범위 계산 (이전달 1일부터 오늘까지)
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# 달력을 연-월별로 그룹화
calendar_groups = {}
for d in cal_dates:
    ym = d.strftime("%Y-%m")
    if ym not in calendar_groups:
        calendar_groups[ym] = []
    calendar_groups[ym].append(d)

# HTML 달력 생성
calendar_html = ""
for ym, dates in calendar_groups.items():
    year, month = ym.split("-")
    calendar_html += f"<h4>{year}년 {month}월</h4><div class='calendar'>"

    # 요일 헤더
    days_header = ['일', '월', '화', '수', '목', '금', '토']
    for day in days_header:
        calendar_html += f"<div class='day-header'>{day}</div>"

    # 시작 요일 공백
    start_day_offset = (dates[0].weekday() + 1) % 7
    for _ in range(start_day_offset):
        calendar_html += "<div class='empty-day'></div>"

    # 날짜 출력
    for d in dates:
        day_num = d.day
        date_str = d.strftime("%Y-%m-%d")
        calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
    calendar_html += "</div>"

calendar_html += """
<style>
.calendar {
    display: grid;
    grid-template-columns: repeat(7, 40px); /* ✅ 네모 칸 크기 고정 */
    grid-gap: 5px;
    margin-bottom: 20px;
}

.day-header, .empty-day, .day {
    width: 40px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 5px; /* 네모(둥근 네모) */
}

.day-header {
    background: #444;
    color: #fff;
    font-weight: bold;
    font-size: 12px;
}

.empty-day {
    background: transparent;
    border: none;
}

.day {
    border: 1px solid #ddd;
    background: #f9f9f9;
    cursor: pointer;
    user-select: none;
    transition: all 0.2s ease;
    font-size: 14px;
    color: #222;
}

.day:hover {
    background: #eee;
}

.day.selected {
    background: #2196F3;
    color: #fff;
    border: 2px solid #2196F3;
    font-weight: bold;
}

h4 {
    margin: 10px 0 5px 0;
    font-size: 18px;
}

/* 모바일 대응 */
@media (max-width: 768px) {
    .calendar {
        grid-template-columns: repeat(7, 30px); /* 모바일에서 작게 */
    }
    .day-header, .empty-day, .day {
        width: 30px;
        height: 30px;
        font-size: 10px;
    }
}
</style>

<script>
const selectedDates = new Set();
function toggleDate(el) {
    const date = el.getAttribute('data-date');
    if(selectedDates.has(date)){
        selectedDates.delete(date);
        el.classList.remove('selected');
    } else {
        selectedDates.add(date);
        el.classList.add('selected');
    }
    document.getElementById('selectedDates').value = Array.from(selectedDates).join(',');
}
</script>
<input type="hidden" id="selectedDates" value="">
"""

st.components.v1.html(calendar_html, height=600, scrolling=True)

# 선택 결과 제출 폼
with st.form("submit_form"):
    selected_dates_raw = st.text_input("선택한 날짜 (달력에서 선택 후 제출)", key="selected_dates_input")
    submitted = st.form_submit_button("제출")

    if submitted and selected_dates_raw:
        selected_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in selected_dates_raw.split(",")]
        total_days = len(cal_dates)
        threshold = total_days / 3
        worked_days = len(selected_dates)

        fourteen_days_prior_end = input_date - timedelta(days=1)
        fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
        fourteen_days = [d for d in cal_dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end]
        no_work_14_days = all(d not in selected_dates for d in fourteen_days)

        st.write(f"총 기간 일수: {total_days}일")
        st.write(f"1/3 기준: {threshold:.1f}일")
        st.write(f"선택한 근무일 수: {worked_days}일")
        st.write(f"{'✅ 조건 1 충족' if worked_days < threshold else '❌ 조건 1 불충족'}")
        st.write(f"{'✅ 조건 2 충족' if no_work_14_days else '❌ 조건 2 불충족'}")

        st.markdown("### 📌 최종 판단")
        if worked_days < threshold:
            st.write(f"✅ 일반일용근로자: 신청 가능")
        else:
            st.write(f"❌ 일반일용근로자: 신청 불가능")

        if worked_days < threshold and no_work_14_days:
            st.write(f"✅ 건설일용근로자: 신청 가능")
        else:
            st.write(f"❌ 건설일용근로자: 신청 불가능")


