import streamlit as st
from datetime import datetime, timedelta
import json

# --- 일용직 신청 가능 시점 판단 UI 함수 ---
def daily_worker_eligibility_app(): # 함수 이름이 daily_worker_eligibility_app 입니다.
    """
    일용직 근로자를 위한 실업급여 신청 가능 시점 판단 UI를 렌더링합니다.
    기존 달력 디자인을 유지하며 모바일 반응형을 지원합니다.
    """
    st.markdown(
        "<span style='font-size:22px; font-weight:600; color:#fff;'>🏗️ 일용직 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )

    # --- 날짜 계산 및 초기화 ---
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 지난달 첫날부터 오늘까지의 기간 계산
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    calculation_end_date = input_date # 사용자님의 코드에서는 last_day 였으나, 의미상 calculation_end_date로 변경

    cal_dates = []
    current_date = first_day_prev_month
    while current_date <= calculation_end_date:
        cal_dates.append(current_date)
        current_date += timedelta(days=1)

    # 월별로 날짜 그룹화
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        if ym not in calendar_groups:
            calendar_groups[ym] = []
        calendar_groups[ym].append(date)

    # JavaScript에서 사용할 JSON 데이터 준비
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")

    # 조건 1 충족을 위한 다음 가능일 (예상)
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")

    # --- HTML 및 JavaScript 코드 (캘린더 UI) ---
    # 중요: <head> 태그와 <meta name="viewport"> 를 추가하고, 스타일/스크립트 위치를 적절히 조정했습니다.
    calendar_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    /* 기존 달력 스타일 (사용자님이 선호하는 디자인 유지) */
    body {{
        color: #111;
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        overflow-x: hidden;
        width: 100vw;
        min-height: 100vh;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: transparent; /* Streamlit 배경이 비치도록 */
    }}

    #calendar-container {{
        width: 100%;
        max-width: 700px;
        padding: 10px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .calendar {{
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
    }}

    .day-header, .empty-day, .day {{
        aspect-ratio: 1/1;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-width: 25px;
    }}
    .day-header {{
        background: #444;
        color: #fff;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
    }}
    .empty-day {{
        background: transparent;
        border: none;
    }}
    .day {{
        border: 1px solid #ddd;
        border-radius: 5px;
        cursor: pointer;
        user-select: none;
        transition: background 0.1s ease, border 0.1s ease;
        font-size: 16px;
        color: #222;
        background: #fdfdfd;
    }}
    .day:hover {{
        background: #eee;
    }}
    .day.selected {{
        border: 2px solid #2196F3;
        background: #2196F3;
        color: #fff !important;
        font-weight: bold;
    }}

    #selectedDatesText, #resultContainer, h3, p, h4 {{
        width: 100%;
        max-width: 680px;
        box-sizing: border-box;
        padding: 0 10px;
        margin-left: auto;
        margin-right: auto;
    }}
    #selectedDatesText, h4 {{
        color:#fff; /* Streamlit 배경색에 맞춤 */
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    h4 {{
        text-align: center;
    }}
    #resultContainer {{
        padding-bottom: 20px;
        color: #111;
    }}

    /* 다크 모드 지원 */
    @media (prefers-color-scheme: dark) {{
        body {{
            color: #ddd;
        }}
        h4 {{
            color: #eee !important;
        }}
        .calendar {{
            background: #333;
            box-shadow: 0 2px 10px rgba(255,255,255,0.1);
        }}
        .day {{
            background: #444;
            border: 1px solid #555;
            color: #eee;
        }}
        .day:hover {{
            background: #555;
        }}
        .day-header {{
            background: #666;
        }}
        #resultContainer {{
            color: #eee;
        }}
        #selectedDatesText {{
            color: #eee !important;
        }}
    }}

    /* --- 모바일 반응형 미디어 쿼리 (추가된 부분) --- */
    /* 작은 스마트폰 (세로) */
    @media (max-width: 480px) {{
        .day-header, .empty-day, .day {{
            font-size: 11px;
            min-width: 20px;
        }}
        h3, p, #selectedDatesText, #resultContainer {{
            font-size: 14px;
        }}
    }}

    /* 큰 스마트폰 (세로) */
    @media (min-width: 481px) and (max-width: 767px) {{
        .day-header, .empty-day, .day {{
            font-size: 13px;
        }}
        h3, p, #selectedDatesText, #resultContainer {{
            font-size: 15px;
        }}
    }}

    /* 모바일 가로 모드 (landscape) - 높이가 제한적일 때 폰트 크기 줄임 */
    @media screen and (orientation: landscape) and (max-height: 400px) {{
        .day-header, .empty-day, .day {{
            font-size: 10px;
            min-width: 15px;
        }}
        h3, p, #selectedDatesText, #resultContainer {{
            font-size: 12px;
        }}
    }}
    </style>
    </head>
    <body>
    <div id='calendar-container'>
    """

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += f"<h4 style='color:#fff;'>{year}년 {month}월</h4>"
        calendar_html += """
        <div class="calendar">
            <div class="day-header">일</div>
            <div class="day-header">월</div>
            <div class="day-header">화</div>
            <div class="day-header">수</div>
            <div class="day-header">목</div>
            <div class="day-header">금</div>
            <div class="day-header">토</div>
        </div>
        """
        start_day_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        for date in dates:
            day_num = date.day
            date_str = date.strftime("%m/%d")
            full_date_str = date.strftime("%Y-%m-%d") # JS에서 비교하기 위해 전체 날짜 문자열 추가
            calendar_html += f'<div class="day" data-date="{date_str}" data-full-date="{full_date_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += f"""
    </div>
    <p id="selectedDatesText"></p>
    <div id="resultContainer"></div>

    <script>
    // JavaScript
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

        // full_date_str을 사용하여 정확한 날짜 비교
        const allFullDates = Array.from(document.querySelectorAll('.day'))
                                   .map(el => el.getAttribute('data-full-date'));

        const fourteenDaysFullDates = allFullDates.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        const selectedFullDates = Array.from(document.querySelectorAll('.day.selected'))
                                       .map(el => el.getAttribute('data-full-date'));

        const noWork14Days = fourteenDaysFullDates.every(date => !selectedFullDates.includes(date));

        let nextPossible1 = "";
        if (workedDays >= threshold) {{
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }}

        let nextPossible2 = "";
        if (!noWork14Days) {{
            const nextPossibleDate = new Date(new Date(FOURTEEN_DAYS_END).getTime() + (14 * 24 * 60 * 60 * 1000));
            const nextDateStr = nextPossibleDate.toISOString().split('T')[0];
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
    }}

    function toggleDate(element) {{
        element.classList.toggle('selected');
        const selected = [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {{
            if (days[i].classList.contains('selected')) {{
                selected.push(days[i].getAttribute('data-date'));
            }}
        }}
        saveToLocalStorage(selected);
        updateSelectedDatesText(selected);
        calculateAndDisplayResult(selected);
        adjustStreamlitFrameSizeDebounced(); // 높이 조절 함수 호출
    }}

    function updateSelectedDatesText(selected) {{
        document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (" + selected.length + "일)";
    }}

    let resizeTimer;
    function adjustStreamlitFrameSizeDebounced() {{
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {{
            adjustStreamlitFrameSize();
        }}, 150);
    }}

    function adjustStreamlitFrameSize() {{
        const body = document.body;
        const html = document.documentElement;
        const contentHeight = Math.max(
            body.scrollHeight, body.offsetHeight,
            html.clientHeight, html.scrollHeight, html.offsetHeight
        );
        const contentWidth = window.innerWidth;

        if (window.parent) {{
            window.parent.postMessage({{
                type: 'streamlit:setFrameHeight',
                height: contentHeight + 50, // 여유 공간 추가
                width: contentWidth
            }}, '*');
        }}
    }}

    window.onload = function() {{
        const storedSelectedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {{
            const dateAttr = days[i].getAttribute('data-date');
            if (storedSelectedDates.includes(dateAttr)) {{
                days[i].classList.add('selected');
            }}
        }}
        updateSelectedDatesText(storedSelectedDates);
        calculateAndDisplayResult(storedSelectedDates);
        adjustStreamlitFrameSizeDebounced(); // 페이지 로드 시 높이 조절
    }};

    window.addEventListener("orientationchange", adjustStreamlitFrameSizeDebounced);
    window.addEventListener("resize", adjustStreamlitFrameSizeDebounced);
    document.addEventListener('DOMContentLoaded', adjustStreamlitFrameSizeDebounced);

    </script>
    </body>
    </html>
    """

    # height는 처음 로드될 때의 대략적인 높이로, 이후 JS가 동적으로 조절
    st.components.v1.html(calendar_html, height=1000, scrolling=True) # scrolling=True로 변경하여 혹시 모를 상황 대비

