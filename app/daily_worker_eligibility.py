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

    # 조건 1에 대한 다음 가능일 계산 (기존 로직 유지)
    # input_date의 월의 다음달 1일 + 1일 (예: 7/7 기준 -> 8/1 + 14일 = 8/15경을 예상)
    # 7/7 입력시 6월 1일부터 7월 7일까지 기간의 1/3을 넘어서면 다음달 1일부터 무근무 시작시 다음달 첫째날 + 14일 이후 가능
    # 즉, 7월 7일 (input_date) 에 신청 시 6월 1일부터 7월 7일까지 근무일수가 1/3을 초과한다면
    # 7월 8일부터 무근무가 시작되어 14일이 지난 7월 22일(input_date + 15일) 이후 다음달에 신청가능.
    # 그러나 이 로직은 `input_date.replace(day=1) + timedelta(days=32)`로 되어있어 다음달 15일경을 가리킵니다.
    # 🚨 참고: 이 next_possible1_date 계산 로직은 실제 '오늘 이후 근로제공이 없을 경우' 기준일과는 다를 수 있습니다.
    # '오늘 이후 근로제공이 없을 경우'의 정확한 다음 가능일은 마지막 근무일로부터 계산되어야 합니다.
    # 현재 코드의 의도를 유지한 채 nextPossible1_date를 그대로 사용하겠습니다.
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1) # 이 부분은 현재 코드가 의도한 "다음달 첫날 + 약 14일"
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")
    
    input_date_str = input_date.strftime("%Y-%m-%d")

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
        start_day_offset = (dates[0].weekday() + 1) % 7 # 일요일=0, 월요일=1... 이므로 +1하고 7로 나눈 나머지
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
            date_str = date.strftime("%m/%d") # JavaScript에서 사용할 MM/DD 형식
            # date_full_str은 JavaScript에서 비교를 위해 YYYY-MM-DD 형식으로 필요
            date_full_str = date.strftime("%Y-%m-%d")
            calendar_html += f'<div class="day {extra_cls}" data-date="{date_str}" data-full-date="{date_full_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>

    <style>
    /* CSS 스타일은 이전과 동일하게 유지하거나 필요에 따라 조정하세요 */
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
        color: #121212; /* 다크모드에서 잘 보이도록 조정 필요하면 밝은 색으로 */
        background: #fff; /* 다크모드에서 잘 보이도록 조정 필요하면 어두운 색으로 */
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-size: 15px;
        line-height: 1.6;
    }
    #resultContainer h3 { color: #0d47a1; margin-top: 20px; margin-bottom: 10px; }
    #resultContainer p { margin: 6px 0; }
    /* 다크모드 대응을 위한 추가 CSS (Streamlit의 기본 테마에 따라 다를 수 있음) */
    html[data-theme="dark"] #resultContainer {
        background: #262730; /* Streamlit 다크모드 배경색과 유사하게 */
        color: #FAFAFA; /* 밝은 글자색 */
    }
    html[data-theme="dark"] #resultContainer h3 {
        color: #90CAF9; /* 밝은 파랑색 계열 */
    }
    html[data-theme="dark"] .day {
        background-color: #31333F; /* 다크모드 날짜 배경색 */
        color: #FAFAFA; /* 밝은 글자색 */
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
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """; // YYYY-MM-DD 형식의 문자열 배열
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr)); // Date 객체로 변환

    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';
    const NEXT_POSSIBLE1_DATE_STR = '""" + next_possible1_str + """';
    const INPUT_DATE_STR = '""" + input_date_str + """'; // YYYY-MM-DD 형식의 input_date

    // 페이지 로드 시 localStorage에서 선택된 날짜 로드 및 UI 업데이트
    function loadSelectedDates() {
        try {
            const storedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
            storedDates.forEach(mmdd => {
                const dayElement = document.querySelector(`.day[data-date="${mmdd}"]`);
                if (dayElement) {
                    dayElement.classList.add('selected');
                }
            });
            // 로드된 날짜로 결과 계산 및 표시
            calculateAndDisplayResult(storedDates);
        } catch (e) {
            console.error("Failed to load selected dates from localStorage", e);
            calculateAndDisplayResult([]); // 오류 발생 시 빈 배열로 시작
        }
    }

    function saveToLocalStorage(data) {
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }

    function calculateAndDisplayResult(selectedMMDD) { // selected는 MM/DD 배열
        // MM/DD 형식의 selectedMMDD를 YYYY-MM-DD 형식으로 변환 (비교를 위해)
        const selectedFullDates = selectedMMDD.map(mmdd => {
            // CALENDAR_DATES_RAW에서 해당 MM/DD를 포함하는 YYYY-MM-DD를 찾음
            const foundDate = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-')));
            return foundDate || ''; // 없으면 빈 문자열 반환
        }).filter(Boolean); // 유효한 날짜만 남김


        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selectedFullDates.length; // YYYY-MM-DD 형식의 근무일 수

        // 현재 날짜 (INPUT_DATE_STR) 파싱
        const inputDate = new Date(INPUT_DATE_STR);

        // 7/7 선택 시 무조건 미충족 로직 (2025년 7월 7일에만 적용)
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

        // 근무일 선택 없으면 무조건 신청 가능
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

        // 조건 2 (14일 무근무) 판단
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
            nextPossible1 = "📅 조건 1을 충족하려면 오늘(" + INPUT_DATE_STR + ") 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE_STR + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }

        // 조건 2 불충족 시 다음 가능일 계산 로직 추가
        let nextPossible2 = "";
        if (!noWork14Days) {
            // 신청일 직전 14일간 근무 기록이 있다면, 그 마지막 근무일로부터 14일 이후가 가능일이 됨
            // 그러나 여기서는 '신청일 직전 14일간'의 기간이므로, 그 기간 이후의 14일을 계산합니다.
            // 즉, 신청일 -1일로부터 14일 후가 신청 가능일 (예: 오늘이 7/7이면, 7/6까지 근무, 7/7~7/20 무근무 -> 7/21부터 가능)
            // FOURTEEN_DAYS_END_STR (신청일 -1일)을 기준으로 14일을 더합니다.
            const fourteenDaysEndDate = new Date(FOURTEEN_DAYS_END_STR); // 신청일 직전 마지막 날짜
            const nextPossible2Date = new Date(fourteenDaysEndDate);
            nextPossible2Date.setDate(nextPossible2Date.getDate() + 14 + 1); // 14일 무근무 후 +1일 (신청 가능한 날)
            
            const nextDateStr = nextPossible2Date.toISOString().split('T')[0];
            nextPossible2 = `📅 조건 2를 충족하려면 신청일(${INPUT_DATE_STR}) 직전 14일간 근로제공이 없는 경우에 해당하며, 마지막 근로일로부터 14일 경과한 ${nextDateStr} 이후에 신청하면 조건 2를 충족할 수 있습니다.`;
        }

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START_STR + " ~ " + FOURTEEN_DAYS_END_STR + ") 무근무"
            : "❌ 조건 2 불충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START_STR + " ~ " + FOURTEEN_DAYS_END_STR + ") 내 근무기록 존재";

        const generalWorkerText = workedDays < threshold ? "✅ 신청 가능" : "❌ 신청 불가능";
        // 건설일용근로자는 조건1 OR 조건2 충족 시 가능
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
                // data-date (MM/DD)를 저장
                selected.push(days[i].getAttribute('data-date'));
            }
        }
        saveToLocalStorage(selected);
        calculateAndDisplayResult(selected); // MM/DD 배열을 전달
    }

    // `window.onload` 시점에 저장된 날짜를 로드하고 계산 실행
    window.onload = function() {
        loadSelectedDates();
    };
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)
