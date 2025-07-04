import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600; color:#fff;'>🏗️ 일용직 신청 가능 시점 판단</span>",
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
        calendar_html += "<h4 style='color:#fff;'>" + year + "년 " + month + "월</h4>"
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
            full_date_str = date.strftime("%Y-%m-%d")
            calendar_html += f'<div class="day" data-date="{date_str}" data-full-date="{full_date_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <p id="selectedDatesText" style="color:#fff;"></p>
    <div id="resultContainer" style="color:#fff;"></div>

    <style>
    body {
        color: #111;
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        overflow-x: hidden; /* 가로 스크롤 방지 */
    }

    html {
        background-color: transparent;
        /* `viewport` 단위를 사용하여 뷰포트 크기에 유동적으로 반응 */
        width: 100vw;
        height: 100vh;
    }

    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-bottom: 20px;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        width: calc(100% - 20px); /* 패딩 고려 */
        max-width: 700px; /* 너무 넓어지는 것 방지 */
        margin-left: auto; /* 중앙 정렬 */
        margin-right: auto; /* 중앙 정렬 */
        box-sizing: border-box;
    }

    .day-header, .empty-day, .day {
        aspect-ratio: 1/1;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-width: 30px; /* 최소 너비 설정 */
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
        border: none;
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
        color: #111;
        padding: 0 10px 20px; /* 좌우 패딩 추가 */
    }
    #selectedDatesText {
        padding: 0 10px; /* 좌우 패딩 추가 */
    }
    h4 {
        padding: 0 10px; /* 좌우 패딩 추가 */
    }
    h3, p {
        margin-left: 10px; /* 좌측 마진 추가 */
        margin-right: 10px; /* 우측 마진 추가 */
    }


    /* 다크 모드 지원 */
    @media (prefers-color-scheme: dark) {
        body {
            color: #ddd;
        }
        h4 {
            color: #eee !important;
        }
        .calendar {
            background: #333;
            box-shadow: 0 2px 10px rgba(255,255,255,0.1);
        }
        .day {
            background: #444;
            border: 1px solid #555;
            color: #eee;
        }
        .day:hover {
            background: #555;
        }
        .day-header {
            background: #666;
        }
        #resultContainer {
            color: #eee;
        }
        #selectedDatesText {
            color: #eee !important;
        }
    }

    /* 모바일 가로 모드 (landscape)에서 캘린더 너비를 더 유동적으로 조정 */
    @media screen and (orientation: landscape) and (max-width: 900px) {
        .calendar {
            width: calc(100% - 20px); /* 가로모드에서도 전체 너비 사용 */
            max-width: 600px; /* 가로 모드에서 너무 커지지 않도록 최대 너비 조절 */
        }
        .day-header, .empty-day, .day {
            font-size: 12px; /* 가로 모드에서 글자 크기 조정 */
        }
    }
    /* 모바일 세로 모드 (portrait) */
    @media screen and (orientation: portrait) {
        .calendar {
            width: calc(100% - 20px);
            max-width: 700px; /* 세로 모드에서 최대 너비 */
        }
        .day-header, .empty-day, .day {
            font-size: 14px;
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

        const fourteenDaysFullDates = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        const selectedFullDates = Array.from(document.querySelectorAll('.day.selected'))
                                       .map(el => el.getAttribute('data-full-date'));

        const noWork14Days = fourteenDaysFullDates.every(date => !selectedFullDates.includes(date));

        let nextPossible1 = "";
        if (workedDays >= threshold) {
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const nextPossibleDate = new Date(new Date(FOURTEEN_DAYS_END).getTime() + (14 * 24 * 60 * 60 * 1000));
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
        updateSelectedDatesText(selected);
        calculateAndDisplayResult(selected);
        adjustStreamlitHeightDebounced(); // 날짜 선택 후 높이 조정 (디바운싱 적용)
    }

    function updateSelectedDatesText(selected) {
        document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (" + selected.length + "일)";
    }

    // 높이 조정을 위한 디바운스 함수 (성능 최적화)
    let resizeTimer;
    function adjustStreamlitHeightDebounced() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            adjustStreamlitHeight();
        }, 100); // 100ms 지연 후 실행
    }

    function adjustStreamlitHeight() {
        const body = document.body;
        const html = document.documentElement;
        const height = Math.max(body.scrollHeight, body.offsetHeight,
                                 html.clientHeight, html.scrollHeight, html.offsetHeight);

        // 부모 Streamlit 창에 프레임 높이 변경 요청
        if (window.parent) {
            window.parent.postMessage({ type: 'streamlit:setFrameHeight', height: height + 50 }, '*');
        }
    }

    window.onload = function() {
        const storedSelectedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            const dateAttr = days[i].getAttribute('data-date');
            if (storedSelectedDates.includes(dateAttr)) {
                days[i].classList.add('selected');
            }
        }
        updateSelectedDatesText(storedSelectedDates);
        calculateAndDisplayResult(storedSelectedDates);
        adjustStreamlitHeightDebounced(); // 초기 로드 시 높이 조정
    };

    // 화면 방향 변경 및 창 크기 변경 시 높이 조정 (디바운싱 적용)
    window.addEventListener("orientationchange", adjustStreamlitHeightDebounced);
    window.addEventListener("resize", adjustStreamlitHeightDebounced);

    // DOMContentLoaded 이벤트 리스너 추가 (HTML이 완전히 로드된 후 실행)
    document.addEventListener('DOMContentLoaded', () => {
        adjustStreamlitHeightDebounced();
    });

    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=True) # 초기 높이를 충분히 주고, 스크롤링 허용

if __name__ == "__main__":
    daily_worker_eligibility_app()
