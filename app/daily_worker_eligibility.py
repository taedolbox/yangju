import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 일용직 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:18px; font-weight:700; margin-bottom:10px;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    # 기준 날짜 선택
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 달력 범위 설정: 신청일 속한 달의 직전 달 1일부터 신청일까지
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    # 달력 날짜 리스트 생성
    cal_dates = []
    current_date = first_day_prev_month
    while current_date <= last_day:
        cal_dates.append(current_date)
        current_date += timedelta(days=1)

    # 월별 그룹핑 (년-월 단위)
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    # JS에서 사용할 날짜 JSON
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])

    # 조건 판단에 필요한 날짜들
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")

    # 달력 HTML 생성 시작
    calendar_html = "<div id='calendar-container'>"

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += f"<h4 style='margin-bottom:5px;'>{year}년 {month}월</h4>"
        calendar_html += """
        <div class="calendar">
            <div class="day-header">일</div><div class="day-header">월</div><div class="day-header">화</div>
            <div class="day-header">수</div><div class="day-header">목</div><div class="day-header">금</div><div class="day-header">토</div>
        """

        # 시작 요일 오프셋
        start_day_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        for date in dates:
            day_num = date.day
            date_str = date.strftime("%m/%d")
            calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += "</div>"
    calendar_html += "<div id='resultContainer'></div>"

    # 스타일
    calendar_html += """
    <style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-bottom: 20px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    .day-header, .empty-day {
        width: 100%;
        height: 40px;
        background: #e0e0e0;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        font-size: 14px;
        border-radius: 4px;
    }
    .empty-day {
        background: transparent;
    }
    .day {
        width: 100%;
        height: 40px;
        background: #fff;
        border: 1px solid #ddd;
        text-align: center;
        line-height: 40px;
        cursor: pointer;
        font-size: 16px;
        color: #333;
        border-radius: 4px;
        transition: background 0.2s, border 0.2s;
        user-select: none;
    }
    .day:hover {
        background: #f0f0f0;
    }
    .day.selected {
        border: 2px solid #2196F3;
        background: #2196F3;
        color: #fff;
        font-weight: bold;
    }
    #resultContainer {
        margin-top: 20px;
        padding: 15px;
        border-left: 4px solid #36A2EB;
        background: #f9f9f9;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
        font-size: 15px;
        line-height: 1.5;
        white-space: pre-line;
    }
    @media (max-width: 768px) {
        .calendar {
            max-width: 100%;
        }
        #resultContainer {
            max-width: 100%;
        }
    }
    </style>
    """

    # 자바스크립트 (날짜 선택 및 결과 계산)
    calendar_html += f"""
    <script>
    const CALENDAR_DATES = {calendar_dates_json};
    const FOURTEEN_DAYS_START = '{fourteen_days_prior_start}';
    const FOURTEEN_DAYS_END = '{fourteen_days_prior_end}';
    const NEXT_POSSIBLE1_DATE = '{next_possible1_str}';

    function saveToLocalStorage(data) {{
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }}

    function calculateAndDisplayResult(selected) {{
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        // 14일 무근무 조건 판단 (건설일용근로자용)
        const fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        // 선택된 날짜에 5월/12월 표기 형태 (MM/DD)이 있으므로 맞춰서 확인
        const selectedDatesNormalized = selected.map(d => d.replace('-', '/'));
        const noWork14Days = fourteenDays.every(date => !selectedDatesNormalized.includes(date.substring(5).replace('-', '/')));

        let nextPossible1 = "";
        if (workedDays >= threshold) {{
            nextPossible1 = "📅 조건 1은 근무일 수가 기준 이상입니다. " + NEXT_POSSIBLE1_DATE + " 이후 신청 권장.";
        }}

        let nextPossible2 = "";
        if (!noWork14Days) {{
            const nextPossibleDate = new Date(FOURTEEN_DAYS_END);
            nextPossibleDate.setDate(nextPossibleDate.getDate() + 14);
            const nextDateStr = nextPossibleDate.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2는 직전 14일 근무가 있습니다. " + nextDateStr + " 이후 신청 권장.";
        }}

        const result = `
조건1: 근무일 수 ${workedDays} / 기준 ${threshold.toFixed(1)}
조건1: ${workedDays < threshold ? "✅ 충족" : "❌ 불충족"}
조건2: ${noWork14Days ? "✅ 충족" : "❌ 불충족"}
${nextPossible1 ? nextPossible1 : ""}
${nextPossible2 ? nextPossible2 : ""}
        `;

        document.getElementById('resultContainer').innerText = result;
    }}

    function toggleDate(el) {{
        el.classList.toggle('selected');
        const selected = [];
        document.querySelectorAll('.day.selected').forEach(day => {{
            selected.push(day.getAttribute('data-date'));
        }});
        saveToLocalStorage(selected);
        calculateAndDisplayResult(selected);
    }}

    window.onload = function() {{
        calculateAndDisplayResult([]);
    }};
    </script>
    """

    st.components.v1.html(calendar_html, height=800, scrolling=False)

