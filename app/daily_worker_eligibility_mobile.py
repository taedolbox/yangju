import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_mobile_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 일용직 신청 가능 시점 판단 (모바일용)</span>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        "<p style='font-size:16px; font-weight:700; margin-bottom:10px;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
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

    calendar_html = "<div id='calendar-container'>"

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += f"<h4>{year}년 {month}월</h4>"
        calendar_html += """
        <div class="calendar-mobile">
            <div class="day-header">일</div>
            <div class="day-header">월</div>
            <div class="day-header">화</div>
            <div class="day-header">수</div>
            <div class="day-header">목</div>
            <div class="day-header">금</div>
            <div class="day-header">토</div>
        """
        start_day_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        for date in dates:
            day_num = date.day
            date_str = date.strftime("%m/%d")
            calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>

    <style>
    .calendar-mobile {
        display: grid; 
        grid-template-columns: repeat(7, 1fr);
        gap: 3px;
        margin-bottom: 20px; 
        background: #fff; 
        padding: 5px; 
        border-radius: 6px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        justify-content: flex-start;
    }
    .day-header, .empty-day {
        width: 100%;
        aspect-ratio: 1/1;
        line-height: normal;
        text-align: center;
        font-weight: 600;
        color: #555;
        font-size: 12px;
    }
    .day-header { 
        background: #e0e0e0; 
        border-radius: 4px; 
    }
    .empty-day { 
        background: transparent; 
        border: none; 
    }
    .day {
        width: 100%; 
        aspect-ratio: 1/1;
        line-height: normal;
        text-align: center;
        border: 1px solid #ddd; 
        border-radius: 4px; 
        cursor: pointer; 
        user-select: none;
        transition: background 0.1s ease, border 0.1s ease; 
        font-size: 14px; 
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2px;
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
        padding: 10px 15px;
        border-radius: 6px;
        box-shadow: 0 0 8px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.4;
    }
    #resultContainer h3 {
        color: #0d47a1;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    #resultContainer p {
        margin: 5px 0;
    }
    </style>

    <script>
    const CALENDAR_DATES = """ + calendar_dates_json + """;
    const FOURTEEN_DAYS_START = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END = '""" + fourteen_days_prior_end + """';
    const NEXT_POSSIBLE1_DATE = '""" + next_possible1_str + """';

    function saveToLocalStorage(data) {
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }

    function calculateAndDisplayResult(selected) {
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        const fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        const noWork14Days = fourteenDays.every(date => !selected.includes(date.substring(5).replace("-", "/")));

        let nextPossible1 = "";
        if (workedDays >= threshold) {
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const nextPossibleDate = new Date(FOURTEEN_DAYS_END);
            nextPossibleDate.setDate(nextPossibleDate.getDate() + 14);
            const nextDateStr = nextPossibleDate.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2를 충족하려면 오늘 이후에 근로제공이 없는 경우 " + nextDateStr + " 이후에 신청하면 조건 2를 충족할 수 있습니다.";
        }

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START + " ~ " + FOURTEEN_DAYS_END + ") 무근무"
            : "❌ 조건 2 불충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START + " ~ " + FOURTEEN_DAYS_END + ") 내 근무기록이 존재";

        const generalWorkerText = workedDays < threshold ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = (workedDays < threshold || noWork14Days) ? "✅ 신청 가능" : "❌ 신청 불가능";

        const finalHtml = `
            <h3>📌 조건 기준</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실이 없어야 함</p>
            <p>총 기간 일수: ${totalDays}일</p>
            <p>1/3 기준: ${threshold.toFixed(1)}일</p>
            <p>근무일 수: ${workedDays}일</p>
            <h3>📌 조건 판단</h3>
            <p>${condition1Text}</p>
            <p>${condition2Text}</p>
            ${nextPossible1 ? `<p>${nextPossible1}</p>` : ""}
            ${nextPossible2 ? `<p>${nextPossible2}</p>` : ""}
            <h3>📌 최종 판단</h3>
            <p>✅ 일반일용근로자: ${generalWorkerText}</p>
            <p>✅ 건설일용근로자: ${constructionWorkerText}</p>
        `;

        document.getElementById('resultContainer').innerHTML = finalHtml;
    }

    function toggleDate(element) {
        element.classList.toggle('selected');
        const selected = [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            if (days[i].classList.contains('selected')) {
                selected.push(days[i].getAttribute('data-date'));
            }
        }
        saveToLocalStorage(selected);
        calculateAndDisplayResult(selected);
    }

    window.onload = function() {
        calculateAndDisplayResult([]);
    };
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)

