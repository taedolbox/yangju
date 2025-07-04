import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 일용직 신청 가능 시점 판단</span>",
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

    calendar_html = "<div id='calendar-wrapper'><div id='calendar-container'>"

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += "<h4>" + year + "년 " + month + "월</h4>"
        calendar_html += """
        <div class="calendar">
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
    </div></div>
    <p id="selectedDatesText"></p>
    <div id="resultContainer"></div>

    <style>
    #calendar-wrapper {
        width: 50%;
        margin: 0 auto;
    }
    #calendar-container {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }

    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-bottom: 20px;
    }

    .day-header, .empty-day, .day {
        aspect-ratio: 1/1;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .day-header {
        background: #444;
        color: #fff;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
    }

    .empty-day {
        background: transparent;
    }

    .day {
        border: 1px solid #ddd;
        border-radius: 5px;
        cursor: pointer;
        user-select: none;
        transition: background 0.1s ease, border 0.1s ease;
        font-size: 16px;
        color: #222;
        background: #fdfdfd;
    }

    .day:hover {
        background: #eee;
    }

    .day.selected {
        border: 2px solid #2196F3;
        background: #2196F3;
        color: #fff !important;
        font-weight: bold;
    }

    #resultContainer {
        margin-top: 20px;
        color: #111;
    }

    @media (prefers-color-scheme: dark) {
        body {
            background: #000;
            color: #ddd;
        }
        #calendar-container {
            background: #1a1a1a;
        }
        .calendar {
            background: transparent;
        }
        .day {
            background: #2a2a2a;
            color: #ddd;
        }
        .day:hover {
            background: #3a3a3a;
        }
        #resultContainer {
            color: #eee;
        }
    }

    @media (max-width: 768px) {
        #calendar-wrapper {
            width: 100%;
        }
        #calendar-container {
            border-radius: 0;
        }
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
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후 근로가 없으면 " + NEXT_POSSIBLE1_DATE + " 이후 신청 가능.";
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const nextPossibleDate = new Date(FOURTEEN_DAYS_END);
            nextPossibleDate.setDate(nextPossibleDate.getDate() + 14);
            const nextDateStr = nextPossibleDate.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2 충족은 " + nextDateStr + " 이후 신청 가능.";
        }

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 직전 14일 무근무"
            : "❌ 조건 2 불충족";

        const finalHtml = `
            <h3>📌 판단 결과</h3>
            <p>${condition1Text}</p>
            <p>${condition2Text}</p>
            ${nextPossible1 ? `<p>${nextPossible1}</p>` : ""}
            ${nextPossible2 ? `<p>${nextPossible2}</p>` : ""}
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
        document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (" + selected.length + "일)";
    }

    window.onload = function() {
        calculateAndDisplayResult([]);
    };
    </script>
    """

    st.components.v1.html(calendar_html, height=1800, scrolling=False)

