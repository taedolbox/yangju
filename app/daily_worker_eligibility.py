import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<h3>🏗️ 일용직 신청 가능 시점 판단</h3>",
        unsafe_allow_html=True
    )

    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    cal_dates = []
    current_date = first_day_prev_month
    while current_date <= last_day:
        cal_dates.append(current_date)
        current_date += timedelta(days=1)

    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        if ym not in calendar_groups:
            calendar_groups[ym] = []
        calendar_groups[ym].append(date)

    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])

    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")

    calendar_html = """
    <style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 320px;
        margin-bottom: 20px;
    }
    .day-header, .day {
        aspect-ratio: 1 / 1;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
        user-select: none;
    }
    .day-header {
        background: #e0e0e0;
        font-weight: bold;
        color: #555;
    }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }
    .day {
        cursor: pointer;
        color: #333;
        transition: background 0.1s ease, border 0.1s ease;
    }
    .day:hover { background: #f0f0f0; }
    .day.selected {
        border: 2px solid #2196F3;
        background: #2196F3;
        color: #fff;
        font-weight: bold;
    }
    #resultContainer {
        color: #121212;
        background: #fff;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-size: 15px;
        line-height: 1.6;
        max-width: 320px;
    }
    #resultContainer h3 {
        color: #0d47a1;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    #resultContainer p {
        margin: 6px 0;
    }
    </style>
    <div class="calendar">
    """

    # 요일 헤더 추가
    weekdays = [("일", "sunday"), ("월", ""), ("화", ""), ("수", ""), ("목", ""), ("금", ""), ("토", "saturday")]
    for wd, cls in weekdays:
        calendar_html += f'<div class="day-header {cls}">{wd}</div>'

    # 첫 주 빈 칸 채우기
    start_day_offset = (cal_dates[0].weekday() + 1) % 7
    for _ in range(start_day_offset):
        calendar_html += '<div class="day empty-day"></div>'

    # 날짜들 추가
    for date in cal_dates:
        day_num = date.day
        cls = ""
        if date.weekday() == 6:  # 일요일
            cls = "sunday"
        elif date.weekday() == 5:  # 토요일
            cls = "saturday"
        calendar_html += f'<div class="day {cls}" data-date="{date.strftime("%Y-%m-%d")}" onclick="toggleDate(this)">{day_num}</div>'

    calendar_html += "</div>"

    # 결과 영역
    calendar_html += """
    <div id="resultContainer">
        <h3>조건 및 판단 결과</h3>
        <div id="resultDetails">선택된 날짜가 없습니다.</div>
    </div>
    """

    # JS 스크립트
    calendar_html += f"""
    <script>
    const CALENDAR_DATES = {calendar_dates_json};
    const FOURTEEN_DAYS_START = '{fourteen_days_prior_start}';
    const FOURTEEN_DAYS_END = '{fourteen_days_prior_end}';
    const NEXT_POSSIBLE1_DATE = '{next_possible1_str}';

    function saveToLocalStorage(data) {{
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }}

    function loadFromLocalStorage() {{
        const data = localStorage.getItem('selectedDates');
        return data ? JSON.parse(data) : [];
    }}

    function calculateAndDisplayResult(selected) {{
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        const fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        const noWork14Days = fourteenDays.every(date => !selected.includes(date));

        let nextPossible1 = "";
        if (workedDays >= threshold) {{
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }}

        let nextPossible2 = "";
        if (!noWork14Days) {{
            const nextDate = new Date(FOURTEEN_DAYS_END);
            nextDate.setDate(nextDate.getDate() + 14);
            const nextDateStr = nextDate.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2를 충족하려면 오늘 이후에 근로제공이 없는 경우 " + nextDateStr + " 이후에 신청하면 조건 2를 충족할 수 있습니다.";
        }}

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START + " ~ " + FOURTEEN_DAYS_END + ") 무근무"
            : "❌ 조건 2 불충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START + " ~ " + FOURTEEN_DAYS_END + ") 내 근무기록이 존재";

        const generalWorkerText = workedDays < threshold ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = (workedDays < threshold || noWork14Days) ? "✅ 신청 가능" : "❌ 신청 불가능";

        let html = `
            <p>총 기간: ${totalDays}일, 1/3 기준: ${threshold.toFixed(1)}일, 선택: ${workedDays}일</p>
            <p>${condition1Text}</p>
            <p>${condition2Text}</p>
            ${nextPossible1 ? `<p>${nextPossible1}</p>` : ""}
            ${nextPossible2 ? `<p>${nextPossible2}</p>` : ""}
            <h4>최종 판단</h4>
            <p>✅ 일반일용근로자: ${generalWorkerText}</p>
            <p>✅ 건설일용근로자: ${constructionWorkerText}</p>
        `;
        document.getElementById("resultDetails").innerHTML = html;
    }}

    function toggleDate(element) {{
        element.classList.toggle('selected');
        const selected = [];
        const days = document.getElementsByClassName('day');
        for (let i=0; i<days.length; i++) {{
            if(days[i].classList.contains('selected')) {{
                selected.push(days[i].getAttribute('data-date'));
            }}
        }}
        saveToLocalStorage(selected);
        calculateAndDisplayResult(selected);
    }}

    window.onload = function() {{
        // 선택된 날짜 불러와서 표시
        const selected = loadFromLocalStorage();
        const days = document.getElementsByClassName('day');
        for(let i=0; i<days.length; i++) {{
            if(selected.includes(days[i].getAttribute('data-date'))) {{
                days[i].classList.add('selected');
            }}
        }}
        calculateAndDisplayResult(selected);
    }};
    </script>
    """

    st.components.v1.html(calendar_html, height=700, scrolling=False)
