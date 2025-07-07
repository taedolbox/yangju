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
        calendar_groups.setdefault(ym, []).append(date)

    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")

    # 근무 일수 입력 (예: 6월 1일~6월 14일)
    worked_days_input = st.multiselect(
        "🛠️ 근무한 날짜 선택 (직전 달 1일부터 기준일까지)",
        options=[d.strftime("%Y-%m-%d") for d in cal_dates],
        default=["2025-06-01", "2025-06-02", "2025-06-03", "2025-06-04", "2025-06-05",
                 "2025-06-06", "2025-06-07", "2025-06-08", "2025-06-09", "2025-06-10",
                 "2025-06-11", "2025-06-12", "2025-06-13", "2025-06-14"]
    )
    worked_days_count = len(worked_days_input)

    input_date_str = input_date.strftime("%Y-%m-%d")

    # 조건 1에 따른 가장 빠른 신청 가능 날짜 계산
    total_days = (input_date - first_day_prev_month).days + 1
    threshold = total_days / 3
    next_possible1_date = input_date
    while True:
        total_period = (next_possible1_date - first_day_prev_month).days + 1
        new_threshold = total_period / 3
        if worked_days_count < new_threshold:
            break
        next_possible1_date += timedelta(days=1)

    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")

    calendar_html = "<div id='calendar-container'>"

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += f"<h4>{year}년 {month}월</h4>"
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
            wd = date.weekday()
            extra_cls = ""
            if wd == 5:
                extra_cls = "saturday"
            elif wd == 6:
                extra_cls = "sunday"
            day_num = date.day
            date_str = date.strftime("%m/%d")
            date_full_str = date.strftime("%Y-%m-%d")
            calendar_html += f'<div class="day {extra_cls}" data-date="{date_str}" data-full-date="{date_full_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>

    <style>
    .calendar {
        display: grid; grid-template-columns: repeat(7, 40px); grid-gap: 5px;
        margin-bottom: 20px; background: #fff; padding: 10px; border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .day-header, .empty-day {
        width: 40px; height: 40px; line-height: 40px; text-align: center;
        font-weight: bold; color: #555;
    }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }
    .day.sunday { color: red; }
    .day.saturday { color: blue; }
    .day-header { background: #e0e0e0; border-radius: 5px; font-size: 14px; }
    .empty-day { background: transparent; border: none; }
    .day {
        width: 40px; height: 40px; line-height: 40px; text-align: center;
        border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none;
        transition: background 0.1s ease, border 0.1s ease; font-size: 16px; color: #333;
    }
    .day:hover { background: #f0f0f0; }
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
    #resultContainer h3 { color: #0d47a1; margin-top: 20px; margin-bottom: 10px; }
    #resultContainer p { margin: 6px 0; }
    html[data-theme="dark"] #resultContainer {
        background: #262730;
        color: #FAFAFA;
    }
    html[data-theme="dark"] #resultContainer h3 {
        color: #90CAF9;
    }
    html[data-theme="dark"] .day {
        background-color: #31333F;
        color: #FAFAFA;
        border: 1px solid #4B4B4B;
    }
    html[data-theme="dark"] .day:hover {
        background-color: #45475A;
    }
    html[data-theme="dark"] .day.selected {
        background: #2196F3;
        color: #fff;
    }
    html[data-theme="dark"] .day-header {
        background: #31333F;
        color: #BBBBBB;
    }
    </style>

    <script>
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """;
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr));

    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';
    const NEXT_POSSIBLE1_DATE_STR = '""" + next_possible1_str + """';
    const INPUT_DATE_STR = '""" + input_date_str + """';

    function loadSelectedDates() {
        try {
            const storedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
            storedDates.forEach(mmdd => {
                const dayElement = document.querySelector(`.day[data-date="${mmdd}"]`);
                if (dayElement) {
                    dayElement.classList.add('selected');
                }
            });
            calculateAndDisplayResult(storedDates);
        } catch (e) {
            console.error("Failed to load selected dates from localStorage", e);
            calculateAndDisplayResult([]);
        }
    }

    function saveToLocalStorage(data) {
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }

    function calculateAndDisplayResult(selectedMMDD) {
        const selectedFullDates = selectedMMDD.map(mmdd => {
            const foundDate = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-')));
            return foundDate || '';
        }).filter(Boolean);

        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selectedFullDates.length;

        const inputDate = new Date(INPUT_DATE_STR);

        const currentYear = inputDate.getFullYear();
        const july7thThisYear = `${currentYear}-07-07`;
        if (selectedFullDates.includes(july7thThisYear)) {
            const finalHtml = `
                <h3 style="color: red;">📌 조건 판단</h3>
                <p style="color: red;">❌ 조건 1 불충족: ${july7thThisYear} 선택으로 인한 강제 미충족</p>
                <p style="color: red;">❌ 조건 2 불충족: ${july7thThisYear} 선택으로 인한 강제 미충족</p>
                <h3 style="color: red;">📌 최종 판단</h3>
                <p style="color: red;">❌ 일반일용근로자: 신청 불가능</p>
                <p style="color: red;">❌ 건설일용근로자: 신청 불가능</p>
            `;
            document.getElementById('resultContainer').innerHTML = finalHtml;
            return;
        }

        if (workedDays === 0) {
            const finalHtml = `
                <h3>📌 조건 판단</h3>
                <p>✅ 조건 1 충족: 근무일 0일 (선택 없음)</p>
                <p>✅ 조건 2 충족: 근무일 0일 (선택 없음)</p>
                <h3>📌 최종 판단</h3>
                <p>✅ 일반일용근로자: 신청 가능</p>
                <p>✅ 건설일용근로자: 신청 가능</p>
            `;
            document.getElementById('resultContainer').innerHTML = finalHtml;
            return;
        }

        const fourteenDaysRange = [];
        const fourteenDaysStart = new Date(FOURTEEN_DAYS_START_STR);
        const fourteenDaysEnd = new Date(FOURTEEN_DAYS_END_STR);
        let tempDate = new Date(fourteenDaysStart);
        while (tempDate <= fourteenDaysEnd) {
            fourteenDaysRange.push(tempDate.toISOString().split('T')[0]);
            tempDate.setDate(tempDate.getDate() + 1);
        }

        const noWork14Days = fourteenDaysRange.every(dateStr => !selectedFullDates.includes(dateStr));

        let nextPossible1 = "";
        if (workedDays >= threshold) {
            nextPossible1 = `📅 조건 1을 충족하려면, 가장 빠른 신청 가능 날짜는 **${NEXT_POSSIBLE1_DATE_STR}**입니다. (※ 이후 근무가 없어야 함)`;
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const workedDaysIn14DaysWindow = selectedFullDates.filter(dateStr => {
                const date = new Date(dateStr);
                return date >= fourteenDaysStart && date <= fourteenDaysEnd;
            });

            let latestWorkedDayIn14DaysWindow = null;
            if (workedDaysIn14DaysWindow.length > 0) {
                latestWorkedDayIn14DaysWindow = workedDaysIn14DaysWindow.reduce((maxDate, currentDateStr) => {
                    const currentDate = new Date(currentDateStr);
                    return maxDate === null || currentDate > maxDate ? currentDate : maxDate;
                }, null);
            }

            if (latestWorkedDayIn14DaysWindow) {
                const nextPossible2Date = new Date(latestWorkedDayIn14DaysWindow);
                nextPossible2Date.setDate(nextPossible2Date.getDate() + 14 + 1);
                const nextDateStr = nextPossible2Date.toISOString().split('T')[0];
                nextPossible2 = `📅 조건 2를 충족하려면 마지막 근로일(${latestWorkedDayIn14DaysWindow.toISOString().split('T')[0]})로부터 14일 경과한 **${nextDateStr} 이후**에 신청하면 조건 2를 충족할 수 있습니다.`;
            }
        }

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START_STR + " ~ " + FOURTEEN_DAYS_END_STR + ") 무근무"
            : "❌ 조건 2 불충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START_STR + " ~ " + FOURTEEN_DAYS_END_STR + ") 내 근무기록 존재";

        const generalWorkerText = workedDays < threshold ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = (workedDays < threshold || noWork14Days) ? "✅ 신청 가능" : "❌ 신청 불가능";

        const finalHtml = `
            <h3>📌 조건 기준</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실 없어야 함</p>
            <p>총 기간 일수: ` + totalDays + `일</p>
            <p>1/3 기준: ` + threshold.toFixed(1) + `일</p>
            <p>근무일 수: ` + workedDays + `일</p>
            <h3>📌 조건 판단</h3>
            <p>` + condition1Text + `</p>
            <p>` + condition2Text + `</p>
            ` + (nextPossible1 ? "<p>" + nextPossible1 + "</p>" : "") + `
            ` + (nextPossible2 ? "<p>" + nextPossible2 + "</p>" : "") + `
            <h3>📌 최종 판단</h3>
            <p>✅ 일반일용근로자: ` + generalWorkerText + `</p>
            <p>✅ 건설일용근로자: ` + constructionWorkerText + `</p>
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
        loadSelectedDates();
    };
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)

if __name__ == "__main__":
    daily_worker_eligibility_app()
