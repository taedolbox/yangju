import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    # 외부 CSS 파일 링크 삽입
    st.markdown('<link rel="stylesheet" href="/static/styles.css">', unsafe_allow_html=True)

    # 오늘 날짜(KST) 기준 날짜 선택
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 기준 날짜로 달력 표시 범위 계산 (이전 달 1일부터 입력 날짜까지)
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    
    cal_dates = []
    current_date_for_cal = first_day_prev_month
    while current_date_for_cal <= input_date:
        cal_dates.append(current_date_for_cal)
        current_date_for_cal += timedelta(days=1)

    # 월별로 그룹핑
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    # JS에서 쓸 날짜 JSON 문자열 생성
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])

    # 조건2 계산용 14일 전 기간
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    input_date_str = input_date.strftime("%Y-%m-%d")

    # 달력 + 결과 + 스크립트 HTML 생성 (기존 코드를 거의 그대로 유지)
    calendar_html = "<div id='calendar-container'>"

    # 초기화 버튼 추가
    calendar_html += """
    <div style="text-align: right; margin-bottom: 15px;">
        <button onclick="clearCalendar()" style="
            background-color: #3F51B5;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: background-color 0.2s;
        " onmouseover="this.style.backgroundColor='#303F9F'" onmouseout="this.style.backgroundColor='#3F51B5'">
            🔄 달력 초기화
        </button>
    </div>
    """

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

    calendar_html += "</div><div id='resultContainer'></div>"

    # 자바스크립트 코드 (조건 계산, 날짜 선택 등 기존 로직 전부 삽입)
    calendar_html += f"""
    <script>
    const CALENDAR_DATES_RAW = {calendar_dates_json};
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr));
    const FOURTEEN_DAYS_START_STR = '{fourteen_days_prior_start}';
    const FOURTEEN_DAYS_END_STR = '{fourteen_days_prior_end}';
    const INPUT_DATE_STR = '{input_date_str}';

    function getDaysBetween(startDate, endDate) {{
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (start > end) return 0;
        let count = 0;
        let current = new Date(start);
        current.setHours(0,0,0,0);
        end.setHours(0,0,0,0);
        while (current <= end) {{
            count++;
            current.setDate(current.getDate() + 1);
        }}
        return count;
    }}

    function getFirstDayOfPrevMonth(date) {{
        const d = new Date(date);
        d.setDate(1);
        d.setMonth(d.getMonth() - 1);
        return d;
    }}

    function formatDateToYYYYMMDD(date) {{
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${{year}}-${{month}}-${{day}}`;
    }}

    function calculateAndDisplayResult(selectedMMDD) {{
        const selectedFullDates = selectedMMDD.map(mmdd => {{
            const foundDate = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-')));
            return foundDate || '';
        }}).filter(Boolean);

        let latestWorkedDay = null;
        if (selectedFullDates.length > 0) {{
            latestWorkedDay = selectedFullDates.reduce((maxDate, currentDateStr) => {{
                const currentDate = new Date(currentDateStr);
                return maxDate === null || currentDate > maxDate ? currentDate : maxDate;
            }}, null);
        }}

        const inputDate = new Date(INPUT_DATE_STR);
        inputDate.setHours(0,0,0,0);

        if (selectedFullDates.length === 0) {{
            document.getElementById('resultContainer').innerHTML = `
                <h3>📌 조건 판단</h3>
                <p>✅ 조건 1 충족: 근무일 0일 (선택 없음)</p>
                <p>✅ 조건 2 충족: 근무일 0일 (선택 없음)</p>
                <h3>📌 최종 판단</h3>
                <p>✅ 일반일용근로자: 신청 가능</p>
                <p>✅ 건설일용근로자: 신청 가능</p>
                <h3>📌 종합 신청 가능일</h3>
                <p>근무일이 없으므로, 현재(${INPUT_DATE_STR}) 바로 신청 가능합니다.</p>
                <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
            `;
            return;
        }}

        if (selectedFullDates.includes(INPUT_DATE_STR)) {{
            const nextPossibleApplicationDate = new Date(INPUT_DATE_STR);
            nextPossibleApplicationDate.setDate(nextPossibleApplicationDate.getDate() + 15);

            document.getElementById('resultContainer').innerHTML = `
                <h3 style="color: red;">📌 조건 판단</h3>
                <p style="color: red;">❌ 조건 1 불충족: 기준 날짜(${INPUT_DATE_STR}) 근무로 인한 미충족</p>
                <p style="color: red;">❌ 조건 2 불충족: 기준 날짜(${INPUT_DATE_STR}) 근무로 인한 미충족</p>
                <h3 style="color: red;">📌 최종 판단</h3>
                <p style="color: red;">❌ 일반일용근로자: 신청 불가능</p>
                <p style="color: red;">❌ 건설일용근로자: 신청 불가능</p>
                <h3>📌 종합 신청 가능일</h3>
                <p style="color: red;">기준 날짜(${INPUT_DATE_STR})에 근무 기록이 있으므로 현재 신청 불가능합니다.</p>
                <p style="color: red;">(이 경우, ${INPUT_DATE_STR}이 마지막 근무일이라면 <b>${formatDateToYYYYMMDD(nextPossibleApplicationDate)}</b> 이후 신청 가능) (이후 근로제공이 없다는 전제)</p>
                <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
            `;
            return;
        }}

        const currentPeriodStartForCond1 = getFirstDayOfPrevMonth(inputDate);
        currentPeriodStartForCond1.setHours(0,0,0,0);

        const currentTotalDaysForCond1 = getDaysBetween(currentPeriodStartForCond1, inputDate);
        const currentThresholdForCond1 = currentTotalDaysForCond1 / 3;

        const actualWorkedDaysForCond1 = selectedFullDates.filter(dateStr => {{
            const date = new Date(dateStr);
            date.setHours(0,0,0,0);
            return date >= currentPeriodStartForCond1 && date <= latestWorkedDay;
        }}).length;

        const condition1Met = actualWorkedDaysForCond1 < currentThresholdForCond1;
        let condition1Text = condition1Met
            ? `✅ 조건 1 충족: 근무일 수(${actualWorkedDaysForCond1}) < 기준(${currentThresholdForCond1.toFixed(1)})`
            : `❌ 조건 1 불충족: 근무일 수(${actualWorkedDaysForCond1}) ≥ 기준(${currentThresholdForCond1.toFixed(1)})`;

        let nextPossible1Message = "";
        let nextPossible1Date = null;

        if (!condition1Met) {{
            let testApplicationDate = new Date(inputDate);
            testApplicationDate.setDate(testApplicationDate.getDate() + 1);
            testApplicationDate.setHours(0,0,0,0);

            let loopCount = 0;
            const maxLoopDays = 365;

            while (loopCount < maxLoopDays) {{
                const testPeriodStart = getFirstDayOfPrevMonth(testApplicationDate);
                testPeriodStart.setHours(0,0,0,0);

                const testTotalDays = getDaysBetween(testPeriodStart, testApplicationDate);

                let effectiveWorkedDaysForCond1Test = 0;
                if (latestWorkedDay && latestWorkedDay >= testPeriodStart) {{
                    effectiveWorkedDaysForCond1Test = selectedFullDates.filter(dateStr => {{
                        const date = new Date(dateStr);
                        date.setHours(0,0,0,0);
                        return date >= testPeriodStart && date <= latestWorkedDay;
                    }}).length;
                }}

                if (effectiveWorkedDaysForCond1Test < testTotalDays / 3) {{
                    nextPossible1Date = testApplicationDate;
                    break;
                }}

                testApplicationDate.setDate(testApplicationDate.getDate() + 1);
                loopCount++;
            }}

            if (nextPossible1Date) {{
                nextPossible1Message = `📅 조건 1 충족을 위한 가장 빠른 신청 가능일: <b>${formatDateToYYYYMMDD(nextPossible1Date)}</b> (이후 근로제공이 없다는 전제)`;
            }} else {{
                nextPossible1Message = `🤔 조건 1 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (선택된 근무일이 많거나 계산 범위 초과)`;
            }}
        }}

        const fourteenDaysRangeForCurrentInput = [];
        const fourteenDaysStartForCurrentInput = new Date(FOURTEEN_DAYS_START_STR);
        fourteenDaysStartForCurrentInput.setHours(0,0,0,0);
        const fourteenDaysEndForCurrentInput = new Date(FOURTEEN_DAYS_END_STR);
        fourteenDaysEndForCurrentInput.setHours(0,0,0,0);

        let tempDateForRange = new Date(fourteenDaysStartForCurrentInput);
        while (tempDateForRange <= fourteenDaysEndForCurrentInput) {{
            fourteenDaysRangeForCurrentInput.push(formatDateToYYYYMMDD(tempDateForRange));
            tempDateForRange.setDate(tempDateForRange.getDate() + 1);
        }}

        const noWork14Days = fourteenDaysRangeForCurrentInput.every(dateStr => !selectedFullDates.includes(dateStr));

        let condition2Text = noWork14Days
            ? `✅ 조건 2 충족: 신청일 직전 14일간 무근무`
            : `❌ 조건 2 불충족: 신청일 직전 14일간 근무 기록 존재`;

        let nextPossible2Message = "";
        let nextPossible2Date = null;

        if (!noWork14Days) {{
            if (latestWorkedDay) {{
                nextPossible2Date = new Date(latestWorkedDay);
                nextPossible2Date.setDate(nextPossible2Date.getDate() + 15);
                nextPossible2Date.setHours(0,0,0,0);
                nextPossible2Message = `📅 조건 2 충족을 위한 가장 빠른 신청 가능일: <b>${formatDateToYYYYMMDD(nextPossible2Date)}</b> (마지막 근로일 기준) (이후 근로제공 없다는 전제)`;
            }} else {{
                nextPossible2Message = `🤔 조건 2 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (근무 기록 필요)`;
            }}
        }}

        const generalWorkerEligible = condition1Met;
        const constructionWorkerEligible = noWork14Days;

        const generalWorkerText = generalWorkerEligible ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = constructionWorkerEligible ? "✅ 신청 가능" : "❌ 신청 불가능";

        document.getElementById('resultContainer').innerHTML = `
            <h3>📌 기준 날짜(${INPUT_DATE_STR}) 기준 조건 판단</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 무근무</p>
            <p>총 기간 일수: ${{currentTotalDaysForCond1}}일</p>
            <p>1/3 기준: ${{currentThresholdForCond1.toFixed(1)}}일</p>
            <p>근무일 수: ${{actualWorkedDaysForCond1}}일</p>
            <p>${condition1Text}</p>
            <p>${condition2Text}</p>
            ${nextPossible1Message ? `<p>${nextPossible1Message}</p>` : ""}
            ${nextPossible2Message ? `<p>${nextPossible2Message}</p>` : ""}
            <h3>📌 기준 날짜(${INPUT_DATE_STR}) 기준 최종 판단</h3>
            <p>✅ 일반일용근로자: ${{generalWorkerText}}</p>
            <p>✅ 건설일용근로자: ${{constructionWorkerText}}</p>
            <p>※ 위 '신청 가능일'은 이후 근로제공이 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과 다를 수 있음.</p>
        `;
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
        calculateAndDisplayResult(selected);
    }}

    function loadSelectedDates() {{
        try {{
            const storedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
            storedDates.forEach(mmdd => {{
                const dayElement = document.querySelector(`.day[data-date="${{mmdd}}"]`);
                if (dayElement) {{
                    dayElement.classList.add('selected');
                }}
            }});
            calculateAndDisplayResult(storedDates);
        }} catch (e) {{
            console.error("Failed to load selected dates from localStorage or calculate result:", e);
            calculateAndDisplayResult([]);
        }}
    }}

    function saveToLocalStorage(data) {{
        try {{
            localStorage.setItem('selectedDates', JSON.stringify(data));
        }} catch (e) {{
            console.error("Failed to save selected dates to localStorage:", e);
        }}
    }}

    window.clearCalendar = function() {{
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {{
            days[i].classList.remove('selected');
        }}
        saveToLocalStorage([]);
        calculateAndDisplayResult([]);
    }};

    document.addEventListener('DOMContentLoaded', function() {{
        loadSelectedDates();
    }});
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)


if __name__ == "__main__":
    daily_worker_eligibility_app()
