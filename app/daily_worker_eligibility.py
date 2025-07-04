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

    calendar_html = "<div id='calendar-container'>"

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
            calendar_html += '<div class="day" data-date="' + date_str + '" onclick="toggleDate(this)">' + str(day_num) + '</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <p id="selectedDatesText" style="color: #111;"></p>
    <div id="resultContainer" style="color: #111;"></div>

    <style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-bottom: 20px;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
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
    }
    .empty-day {
        background: transparent;
    }
    .day {
        border: 1px solid #ddd;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        background: #fdfdfd;
    }
    .day:hover { background: #eee; }
    .day.selected {
        border: 2px solid #2196F3;
        background: #2196F3;
        color: #fff !important;
        font-weight: bold;
    }

    @media (prefers-color-scheme: dark) {
        body { background: #000; }
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
            nextPossible1 = "📅 조건 1: 오늘 이후 근로제공 없으면 " + NEXT_POSSIBLE1_DATE + " 이후 신청 가능.";
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const nextPossibleDate = new Date(FOURTEEN_DAYS_END);
            nextPossibleDate.setDate(nextPossibleDate.getDate() + 14);
            const nextDateStr = nextPossibleDate.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2: 오늘 이후 근로제공 없으면 " + nextDateStr + " 이후 신청 가능.";
        }

        const html = `
            <h3>📌 조건 기준</h3>
            <p>조건 1: 직전 달 첫날부터 신청일까지 근무일 수 1/3 미만</p>
            <p>조건 2: 건설일용, 직전 14일간 무근무</p>
            <p>총 기간: ` + totalDays + `일 / 1/3 기준: ` + threshold.toFixed(1) + `일 / 근무일수: ` + workedDays + `일</p>
            <h3>📌 조건 판단</h3>
            <p>` + (workedDays < threshold ? "✅ 조건 1 충족" : "❌ 조건 1 불충족") + `</p>
            <p>` + (noWork14Days ? "✅ 조건 2 충족" : "❌ 조건 2 불충족") + `</p>
            <p>` + nextPossible1 + `</p>
            <p>` + nextPossible2 + `</p>
        `;
        const rc = document.getElementById("resultContainer");
        rc.innerHTML = html;
        rc.style.color = window.matchMedia('(prefers-color-scheme: dark)').matches ? '#fff' : '#111';
        document.getElementById("selectedDatesText").style.color = rc.style.color;
    }

    function toggleDate(e) {
        e.classList.toggle('selected');
        const selected = Array.from(document.querySelectorAll('.day.selected')).map(el => el.getAttribute('data-date'));
        saveToLocalStorage(selected);
        calculateAndDisplayResult(selected);
        document.getElementById("selectedDatesText").innerText = "선택한 날짜: " + selected.join(", ");
    }

    function adjustGrid() {
        const cals = document.querySelectorAll('.calendar');
        cals.forEach(cal => {
            cal.style.gridTemplateColumns = 'repeat(7, 1fr)';
        });
    }

    window.addEventListener("orientationchange", adjustGrid);
    window.addEventListener("resize", adjustGrid);

    window.onload = () => {
        calculateAndDisplayResult([]);
        adjustGrid();
    };
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)

