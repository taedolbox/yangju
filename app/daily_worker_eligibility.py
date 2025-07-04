import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app_original_ui(): # 함수명 변경
    st.markdown(
        "<span style='font-size:22px; font-weight:600; color:#fff;'>🏗️ 일용직 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )

    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date # 이 변수 이름을 calculation_end_date로 바꾸는 것을 권장합니다.

    cal_dates = []
    current_date = first_day_prev_month
    while current_date <= last_day: # 여기도 last_day 사용
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

    calendar_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    /* 기본 스타일 */
    body {{
        color: #111;
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        overflow-x: hidden; /* 가로 스크롤 방지 */
        width: 100vw; /* 뷰포트 너비에 맞춤 */
        min-height: 100vh; /* 최소 높이를 뷰포트 높이에 맞춤 */
        box-sizing: border-box; /* 패딩, 보더를 너비/높이에 포함 */
        display: flex; /* flexbox를 사용하여 콘텐츠를 중앙에 배치 */
        flex-direction: column;
        align-items: center; /* 수평 중앙 정렬 */
    }}

    html {{
        background-color: transparent; /* Streamlit의 배경색을 따르도록 투명 설정 */
    }}

    #calendar-container {{
        width: 100%;
        max-width: 700px; /* 전체 컨테이너의 최대 너비 제한 */
        padding: 10px; /* 전체 컨테이너에 패딩 */
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center; /* 자식 요소도 수평 중앙 정렬 */
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
        width: 100%; /* 부모 컨테이너에 꽉 차도록 */
        box-sizing: border-box;
    }}

    .day-header, .empty-day, .day {{
        aspect-ratio: 1/1; /* 너비와 높이를 1:1로 유지 */
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-width: 25px; /* 작은 화면에서 너무 작아지지 않게 */
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

    /* 텍스트 및 결과 영역 스타일 */
    #selectedDatesText, #resultContainer, h3, p {{
        width: 100%; /* 부모에 꽉 차도록 */
        max-width: 680px; /* #calendar-container보다 조금 작게 */
        box-sizing: border-box;
        padding: 0 10px; /* 좌우 패딩 */
        margin-left: auto; /* 중앙 정렬 */
        margin-right: auto; /* 중앙 정렬 */
    }}
    #selectedDatesText, h4 {{
        color:#fff;
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    h4 {{
        text-align: center; /* 월 제목 중앙 정렬 */
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

    /* 미디어 쿼리 - 화면 크기에 따른 폰트 사이즈 및 레이아웃 미세 조정 */
    @media (max-width: 480px) {{ /* 작은 스마트폰 (세로) */
        .day-header, .empty-day, .day {{
            font-size: 11px;
            min-width: 20px;
        }}
        h3, p, #selectedDatesText, #resultContainer {{
            font-size: 14px;
        }}
    }}

    @media (min-width: 481px) and (max-width: 767px) {{ /* 큰 스마트폰 (세로) */
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
            min-width: 15px; /* 더 줄여서 공간 확보 */
        }}
        h3, p, #selectedDatesText, #resultContainer {{
            font-size: 12px; /* 텍스트도 더 작게 */
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

        const fourteenDaysFullDates = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
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
        adjustStreamlitFrameSizeDebounced(); // 날짜 선택 후 프레임 크기 조정
    }}

    function updateSelectedDatesText(selected) {{
        document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (" + selected.length + "일)";
    }}

    // 디바운스 타이머
    let resizeTimer;
    function adjustStreamlitFrameSizeDebounced() {{
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {{
            adjustStreamlitFrameSize();
        }}, 150); // 약간 더 긴 지연 시간 (150ms)
    }}

    // Streamlit 부모 프레임에 크기 정보를 전송하는 함수
    function adjustStreamlitFrameSize() {{
        const body = document.body;
        const html = document.documentElement;
        
        // 스크롤 높이, 오프셋 높이 등 여러 값을 비교하여 실제 콘텐츠 높이를 정확히 측정
        const contentHeight = Math.max(
            body.scrollHeight, body.offsetHeight,
            html.clientHeight, html.scrollHeight, html.offsetHeight
        );
        // iframe 내부의 실제 너비를 측정 (뷰포트 너비)
        const contentWidth = window.innerWidth; 

        if (window.parent) {{
            window.parent.postMessage({{ 
                type: 'streamlit:setFrameHeight', 
                height: contentHeight + 50, // 높이에 버퍼 추가
                width: contentWidth // 너비 정보도 함께 전송
            }}, '*');
            // console.log(`PostMessage: height=${contentHeight + 50}, width=${contentWidth}`); // 디버깅용
        }}
    }}

    // 초기 로드 시 및 화면 방향/크기 변경 시 프레임 크기 조정
    window.onload = function() {{
        const storedSelectedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {{
            const dateAttr = days[i].getAttribute('data-date');
            if (storedSelectedDates.includes(dateAttr)) {{
                days[i].classList.add('selected');
            }
        }}
        updateSelectedDatesText(storedSelectedDates);
        calculateAndDisplayResult(storedSelectedDates);
        adjustStreamlitFrameSizeDebounced(); // 초기 로드 시 디바운스 호출
    }};

    // orientationchange와 resize 이벤트 리스너
    window.addEventListener("orientationchange", adjustStreamlitFrameSizeDebounced);
    window.addEventListener("resize", adjustStreamlitFrameSizeDebounced);
    
    // 추가적으로 DOMContentLoaded도 포함 (일부 환경에서 onload보다 먼저 발생)
    document.addEventListener('DOMContentLoaded', adjustStreamlitFrameSizeDebounced);

    </script>
    </body>
    </html>
    """

    # Streamlit 컴포넌트 설정
    # width는 Streamlit의 컬럼 너비를 따르므로 height만 유동적으로 관리
    st.components.v1.html(calendar_html, height=1000, scrolling=True) 

if __name__ == "__main__":
    # main.py에서 이 함수를 호출하도록 변경하세요.
    daily_worker_eligibility_app_original_ui()
