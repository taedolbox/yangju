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
        calendar_html += "<h4 style='color:#fff;'>" + year + "년 " + month + "월</h4>" # h4 색상 추가
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
            # data-full-date 속성 추가 (YYYY-MM-DD 형식)
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
        margin: 0; /* 기본 마진 제거 */
        padding: 0; /* 기본 패딩 제거 */
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Streamlit 앱의 배경색을 따르도록 설정 */
    html {
        background-color: transparent;
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
        width: 100%;
        box-sizing: border-box;
    }

    .day-header, .empty-day, .day {
        aspect-ratio: 1/1; /* 너비와 높이를 1:1로 유지 */
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
        padding-bottom: 20px;
    }

    /* 다크 모드 지원 */
    @media (prefers-color-scheme: dark) {
        body {
            color: #ddd;
            /* background: #000; Streamlit의 배경색을 따르므로 주석 처리 */
        }
        h4 {
            color: #eee !important; /* 다크 모드에서 월 제목 색상 조정 */
        }
        .calendar {
            background: #333; /* 다크 모드 캘린더 배경 */
            box-shadow: 0 2px 10px rgba(255,255,255,0.1);
        }
        .day {
            background: #444; /* 다크 모드 일자 배경 */
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

    /* 화면 너비가 768px 이하일 때 캘린더 그리드 조정 (기존 유지) */
    @media (max-width: 768px) {
        .calendar {
            grid-template-columns: repeat(7, 1fr);
        }
    }
    </style>

    <script>
    const CALENDAR_DATES = """ + calendar_dates_json + """;
    const FOURTEEN_DAYS_START = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END = '""" + fourteen_days_prior_end + """';
    const NEXT_POSSIBLE1_DATE = '""" + next_possible1_str + """';

    // 로컬 스토리지에 선택된 날짜 저장
    function saveToLocalStorage(data) {
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }

    // 결과 계산 및 표시
    function calculateAndDisplayResult(selected) {
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        // YYYY-MM-DD 형식의 전체 캘린더 날짜 중 14일 기간 필터링
        const fourteenDaysFullDates = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);

        // 선택된 날짜를 YYYY-MM-DD 형식으로 변환 (data-full-date 사용)
        const selectedFullDates = Array.from(document.querySelectorAll('.day.selected'))
                                       .map(el => el.getAttribute('data-full-date'));

        const noWork14Days = fourteenDaysFullDates.every(date => !selectedFullDates.includes(date));

        let nextPossible1 = "";
        if (workedDays >= threshold) {
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const nextPossibleDate = new Date(new Date(FOURTEEN_DAYS_END).getTime() + (14 * 24 * 60 * 60 * 1000)); // 14일 추가
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

    // 날짜 선택/해제 토글
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
        adjustStreamlitHeight(); // 날짜 선택 후 높이 조정
    }

    // 선택된 날짜 텍스트 업데이트
    function updateSelectedDatesText(selected) {
        document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (" + selected.length + "일)";
    }

    // Streamlit 프레임 높이 조정 (부모 창에 메시지 전송)
    function adjustStreamlitHeight() {
        const body = document.body;
        const html = document.documentElement;
        // 스크롤 높이, 오프셋 높이 등 여러 값을 비교하여 실제 콘텐츠 높이를 정확히 측정
        const height = Math.max( body.scrollHeight, body.offsetHeight, 
                                 html.clientHeight, html.scrollHeight, html.offsetHeight );
        
        // 부모 Streamlit 창에 프레임 높이 변경 요청
        if (window.parent) {
            window.parent.postMessage({ type: 'streamlit:setFrameHeight', height: height + 50 }, '*'); // 약간의 버퍼 추가
        }
    }

    window.onload = function() {
        const storedSelectedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
        // 로컬 스토리지에 저장된 선택 상태 복원
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            const dateAttr = days[i].getAttribute('data-date');
            if (storedSelectedDates.includes(dateAttr)) {
                days[i].classList.add('selected');
            }
        }
        updateSelectedDatesText(storedSelectedDates);
        calculateAndDisplayResult(storedSelectedDates);
        adjustStreamlitHeight(); // 초기 로드 시 높이 조정
    };

    // 화면 방향 변경 및 창 크기 변경 시 높이 조정
    window.addEventListener("orientationchange", adjustStreamlitHeight);
    window.addEventListener("resize", adjustStreamlitHeight);

    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=True) # 초기 높이를 충분히 주고, 스크롤링 허용

if __name__ == "__main__":
    daily_worker_eligibility_app()
