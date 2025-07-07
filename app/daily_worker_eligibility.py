import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 일용직 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:16px;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    # 👉 기준일 (기본: 오늘)
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 👉 대상 기간: 전월 1일부터 기준일까지
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
        calendar_groups.setdefault(ym, []).append(date)

    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")
    기준일_날짜 = input_date.strftime("%m/%d")

    # 👉 달력 HTML
    calendar_html = "<div id='calendar-container'>"

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += f"<h4>{year}년 {int(month)}월</h4>"
        calendar_html += """
        <div class="calendar">
            <div class="day-header sunday">일</div>
            <div class="day-header">월</div>
            <div class="day-header">화</div>
            <div class="day-header">수</div>
            <div class="day-header">목</div>
            <div class="day-header">금</div>
            <div class="day-header saturday">토</div>
        """
        start_day_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        for date in dates:
            wd = (date.weekday() + 1) % 7
            cls = "sunday" if wd == 0 else "saturday" if wd == 6 else ""
            day_num = date.day
            date_str = date.strftime("%m/%d")
            calendar_html += f'<div class="day {cls}" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>

    <style>
    .calendar {
        display: grid; grid-template-columns: repeat(7, 40px); gap: 5px;
        margin-bottom: 20px; background: #fff; padding: 10px; border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .day-header, .empty-day {
        width: 40px; height: 40px; line-height: 40px; text-align: center;
        font-weight: bold; color: #555;
    }
    .day-header { background: #e0e0e0; border-radius: 5px; font-size: 14px; }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }
    .empty-day { background: transparent; border: none; }
    .day {
        width: 40px; height: 40px; line-height: 40px; text-align: center;
        border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none;
        transition: background 0.1s ease, border 0.1s ease; font-size: 16px; color: #333;
    }
    .day:hover { background: #f0f0f0; }
    .day.sunday { color: red; }
    .day.saturday { color: blue; }
    .day.selected { border: 2px solid #2196F3; background: #2196F3; color: #fff; font-weight: bold; }

    #resultContainer {
        color: #121212;
        background: #fff;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-size: 15px;
        line-height: 1.6;
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

    <script>
    const CALENDAR_DATES = """ + calendar_dates_json + """;
    const FOURTEEN_DAYS_START = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END = '""" + fourteen_days_prior_end + """';
    const NEXT_POSSIBLE1_DATE = '""" + next_possible1_str + """';
    const BASE_DATE = '""" + 기준일_날짜 + """';

    function toggleDate(element) {
        element.classList.toggle('selected');
        const selected = [];
        document.querySelectorAll('.day.selected').forEach(e => selected.push(e.getAttribute('data-date')));
        calculateAndDisplayResult(selected);
    }

    function calculateAndDisplayResult(selected) {
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        const includeBase = selected.includes(BASE_DATE);

        let condition1Text, condition2Text, nextPossible1 = "", nextPossible2 = "";

        if (includeBase) {
            condition1Text = "❌ 기준일 선택 → 조건 1 무조건 불충족";
            condition2Text = "❌ 기준일 선택 → 조건 2 무조건 불충족";
        } else {
            const fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
            const noWork14Days = fourteenDays.every(date => !selected.includes(date.substring(5).replace("-", "/")));

            if (workedDays >= threshold) {
                nextPossible1 = "📅 조건 1을 충족하려면 " + NEXT_POSSIBLE1_DATE + " 이후 신청.";
            }
            if (!noWork14Days) {
                const nextPossibleDate = new Date(FOURTEEN_DAYS_END);
                nextPossibleDate.setDate(nextPossibleDate.getDate() + 14);
                nextPossible2 = "📅 조건 2를 충족하려면 " + nextPossibleDate.toISOString().split('T')[0] + " 이후 신청.";
            }

            condition1Text = workedDays < threshold
                ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
                : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

            condition2Text = noWork14Days
                ? "✅ 조건 2 충족: 14일 무근무"
                : "❌ 조건 2 불충족: 14일 내 근무 있음";
        }

        const generalWorkerText = (includeBase || workedDays >= threshold) ? "❌ 신청 불가능" : "✅ 신청 가능";
        const constructionWorkerText = (includeBase || (workedDays >= threshold && !noWork14Days)) ? "❌ 신청 불가능" : "✅ 신청 가능";

        const finalHtml = `
            <h3>📌 조건 기준</h3>
            <p>총 기간 일수: ${totalDays}일</p>
            <p>1/3 기준: ${threshold.toFixed(1)}일</p>
            <p>근무일 수: ${workedDays}일</p>
            <h3>📌 조건 판단</h3>
            <p>${condition1Text}</p>
            <p>${condition2Text}</p>
            ${nextPossible1 ? "<p>" + nextPossible1 + "</p>" : ""}
            ${nextPossible2 ? "<p>" + nextPossible2 + "</p>" : ""}
            <h3>📌 최종 판단</h3>
            <p>일반일용근로자: ${generalWorkerText}</p>
            <p>건설일용근로자: ${constructionWorkerText}</p>
        `;

        document.getElementById('resultContainer').innerHTML = finalHtml;
    }

    window.onload = () => calculateAndDisplayResult([]);
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)
