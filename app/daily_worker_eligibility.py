import streamlit as st
from datetime import datetime, timedelta
import json
import os 

def daily_worker_eligibility_app():
    # KST (한국 표준시)로 오늘 날짜 설정
    now_utc = datetime.utcnow()
    today_kst = now_utc + timedelta(hours=9)
    input_date = st.date_input("기준 날짜 선택", today_kst.date(), help="실업급여를 신청하고자 하는 기준 날짜를 선택해주세요.")

    st.warning("달력에서 근무한 날짜를 **클릭하여 선택**해주세요. 선택된 날짜는 파란색으로 표시됩니다. 한번 더 클릭하면 선택이 해제됩니다.")

    # 달력 표시 기간 설정 (선택된 날짜의 직전 달 첫날부터 선택된 날짜까지)
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    
    cal_dates = []
    current_date_for_cal = first_day_prev_month
    while current_date_for_cal <= input_date:
        cal_dates.append(current_date_for_cal)
        current_date_for_cal += timedelta(days=1)

    # 월별로 달력 그룹화
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    # JavaScript에서 사용하기 위한 날짜 데이터 (JSON 배열 문자열)
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    
    # 조건 2 계산을 위한 14일 이전 날짜 범위 (기준 날짜에 따라 달라짐)
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    
    input_date_str = input_date.strftime("%Y-%m-%d")

    # --- 보고서 템플릿 파일 읽어오기 ---
    # 현재 스크립트 파일 (daily_worker_eligibility.py)의 디렉토리를 기준으로 템플릿 파일 경로 설정
    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, "report_template.html") 
    
    report_template_content = ""
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            report_template_content = f.read()
    except FileNotFoundError:
        st.error(f"오류: 보고서 템플릿 파일 '{template_path}'을(를) 찾을 수 없습니다. 경로를 확인해주세요.")
        return 
    
    # JavaScript로 보고서 템플릿 내용을 전달하기 위해 JSON 문자열로 인코딩
    report_template_json = json.dumps(report_template_content)

    # Streamlit HTML/JavaScript 컴포넌트 삽입
    calendar_html = "<div id='calendar-container'>"

    # 달력 초기화 버튼
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

    # 월별 달력 생성
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
        # 해당 월의 첫 날이 시작되는 요일까지 빈 칸 채우기
        start_day_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        
        # 날짜 버튼 생성
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
    /* CSS styles */
    .calendar {
        display: grid; 
        grid-template-columns: repeat(7, 44px); 
        grid-gap: 5px;
        margin-bottom: 20px; background: #fff; 
        padding: 10px 1px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .day-header, .empty-day {
        width: 44px; height: 44px;
        line-height: 45px;
        text-align: center;
        font-weight: bold; color: #555;
    }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }
    .day.sunday { color: red; }
    .day.saturday { color: blue; }
    .day-header { background: #e0e0e0; border-radius: 5px; font-size: 16px; }
    .empty-day { background: transparent; border: none; }
    .day {
        width: 44px; height: 44px;
        line-height: 45px;
        text-align: center;
        border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none;
        transition: background 0.1s ease, border 0.1s ease; font-size: 18px; color: #333;
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

    #calendar-container h4 {
        margin-bottom: 5px;
    }

    html[data-theme="dark"] #resultContainer {
        background: #262730;
        color: #FAFAFA;
    }
    html[data-theme="dark"] #resultContainer h3 {
        color: #90CAF9;
    }
    html[data-theme="dark"] h4 {
        color: #FFFFFF !important;
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
    const INPUT_DATE_STR = '""" + input_date_str + """';          
    
    const REPORT_TEMPLATE = JSON.parse(`""" + report_template_json + """`);

    function getDaysBetween(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (start > end) return 0;
        let count = 0;
        let current = new Date(start); 
        current.setHours(0,0,0,0); 
        end.setHours(0,0,0,0);
        while (current <= end) {
            count++;
            current.setDate(current.getDate() + 1);
        }
        return count;
    }

    function getFirstDayOfPrevMonth(date) {
        const d = new Date(date);
        d.setDate(1); 
        d.setMonth(d.getMonth() - 1); 
        return d;
    }

    function formatDateToYYYYMMDD(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function calculateAndDisplayResult(selectedMMDD) {
        const selectedFullDates = selectedMMDD.map(mmdd => {
            const foundDate = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-')));
            return foundDate || '';
        }).filter(Boolean);

        let latestWorkedDay = null;
        if (selectedFullDates.length > 0) {
            latestWorkedDay = selectedFullDates.reduce((maxDate, currentDateStr) => {
                const currentDate = new Date(currentDateStr);
                return maxDate === null || currentDate > maxDate ? currentDate : maxDate;
            }, null);
        }

        const inputDate = new Date(INPUT_DATE_STR);
        inputDate.setHours(0,0,0,0);

        if (selectedFullDates.length === 0) {
            const finalHtml = `
                <h3>조건 판단</h3>
                <p>조건 1 충족: 근무일 0일 (선택 없음)</p>
                <p>조건 2 충족: 근무일 0일 (선택 없음)</p>
                <h3>최종 판단</h3>
                <p>일반일용근로자: 신청 가능</p>
                <p>건설일용근로자: 신청 가능</p>
                <h3>종합 신청 가능일</h3>
                <p>근무일이 없으므로, 현재(${INPUT_DATE_STR}) 바로 신청 가능합니다.</p>
                <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
            `;
            document.getElementById('resultContainer').innerHTML = finalHtml;
            window.eligibilityResults = {
                cond1Met: true,
                cond2Met: true,
                generalEligible: true,
                constructionEligible: true,
                cond1WorkedDays: 0,
                cond1Threshold: 0,
                lastWorkedDay: null,
                selectedDates: selectedFullDates
            };
            return;
        }

        if (selectedFullDates.includes(INPUT_DATE_STR)) {
            const nextPossibleApplicationDate = new Date(INPUT_DATE_STR);
            nextPossibleApplicationDate.setDate(nextPossibleApplicationDate.getDate() + 14 + 1);

            const finalHtml = `
                <h3 style="color: red;">조건 판단</h3>
                <p style="color: red;">조건 1 불충족: 기준 날짜(${INPUT_DATE_STR}) 근무로 인한 미충족</p>
                <p style="color: red;">조건 2 불충족: 기준 날짜(${INPUT_DATE_STR}) 근무로 인한 미충족</p>
                <h3 style="color: red;">최종 판단</h3>
                <p style="color: red;">일반일용근로자: 신청 불가능</p>
                <p style="color: red;">건설일용근로자: 신청 불가능</p>
                <h3>종합 신청 가능일</h3>
                <p style="color: red;">기준 날짜(${INPUT_DATE_STR})에 근무 기록이 있으므로 현재 신청 불가능합니다.</p>
                <p style="color: red;">(이 경우, ${INPUT_DATE_STR}이 마지막 근무일이라면 **${formatDateToYYYYMMDD(nextPossibleApplicationDate)}** 이후 신청 가능) (이후 근로제공이 없다는 전제)</p>
                <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
            `;
            document.getElementById('resultContainer').innerHTML = finalHtml;
            window.eligibilityResults = {
                cond1Met: false,
                cond2Met: false,
                generalEligible: false,
                constructionEligible: false,
                cond1WorkedDays: null,
                cond1Threshold: null,
                lastWorkedDay: new Date(INPUT_DATE_STR),
                selectedDates: selectedFullDates
            };
            return;
        }


        const currentPeriodStartForCond1 = getFirstDayOfPrevMonth(inputDate);
        currentPeriodStartForCond1.setHours(0,0,0,0);

        const currentTotalDaysForCond1 = getDaysBetween(currentPeriodStartForCond1, inputDate);
        const currentThresholdForCond1 = currentTotalDaysForCond1 / 3;
        
        const actualWorkedDaysForCond1 = selectedFullDates.filter(dateStr => {
            const date = new Date(dateStr);
            date.setHours(0,0,0,0);
            return date >= currentPeriodStartForCond1 && date <= inputDate; 
        }).length;

        const condition1Met = actualWorkedDaysForCond1 < currentThresholdForCond1;
        let condition1Text = condition1Met
            ? `조건 1 충족: 근무일 수(${actualWorkedDaysForCond1}) < 기준(${currentThresholdForCond1.toFixed(1)})`
            : `조건 1 불충족: 근무일 수(${actualWorkedDaysForCond1}) ≥ 기준(${currentThresholdForCond1.toFixed(1)})`;

        let nextPossible1Message = "";
        let nextPossible1Date = null;

        if (!condition1Met) {
            let testApplicationDate = new Date(inputDate);
            testApplicationDate.setDate(testApplicationDate.getDate() + 1);
            testApplicationDate.setHours(0,0,0,0);

            let loopCount = 0;
            const maxLoopDays = 365;

            while (loopCount < maxLoopDays) {
                const testPeriodStart = getFirstDayOfPrevMonth(testApplicationDate);
                testPeriodStart.setHours(0,0,0,0);

                const testTotalDays = getDaysBetween(testPeriodStart, testApplicationDate);
                
                let effectiveWorkedDaysForCond1Test = 0;
                if (latestWorkedDay && latestWorkedDay >= testPeriodStart) {
                    effectiveWorkedDaysForCond1Test = selectedFullDates.filter(dateStr => {
                        const date = new Date(dateStr);
                        date.setHours(0,0,0,0);
                        return date >= testPeriodStart && date <= latestWorkedDay; 
                    }).length;
                }

                if (effectiveWorkedDaysForCond1Test < testTotalDays / 3) {
                    nextPossible1Date = testApplicationDate;
                    break;
                }

                testApplicationDate.setDate(testApplicationDate.getDate() + 1);
                loopCount++;
            }

            if (nextPossible1Date) {
                nextPossible1Message = `조건 1 충족을 위한 가장 빠른 신청 가능일: **${formatDateToYYYYMMDD(nextPossible1Date)}** (이후 근로제공이 없다는 전제)`;
            } else {
                nextPossible1Message = `조건 1 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (선택된 근무일이 매우 많거나 계산 범위(${maxLoopDays}일) 초과)`;
            }
        }


        const fourteenDaysRangeForCurrentInput = [];
        const fourteenDaysStartForCurrentInput = new Date(FOURTEEN_DAYS_START_STR);
        fourteenDaysStartForCurrentInput.setHours(0,0,0,0);
        const fourteenDaysEndForCurrentInput = new Date(FOURTEEN_DAYS_END_STR);
        fourteenDaysEndForCurrentInput.setHours(0,0,0,0);

        let tempDateForRange = new Date(fourteenDaysStartForCurrentInput);
        while (tempDateForRange <= fourteenDaysEndForCurrentInput) {
            fourteenDaysRangeForCurrentInput.push(formatDateToYYYYMMDD(tempDateForRange));
            tempDateForRange.setDate(tempDateForRange.getDate() + 1);
        }

        const noWork14Days = fourteenDaysRangeForCurrentInput.every(dateStr => !selectedFullDates.includes(dateStr));
        
        let condition2Text = noWork14Days
            ? `조건 2 충족: 신청일 직전 14일간(${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR}) 무근무`
            : `조건 2 불충족: 신청일 직전 14일간(${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR}) 내 근무기록 존재`;

        let nextPossible2Message = "";
        let nextPossible2Date = null;

        if (!noWork14Days) {
            if (latestWorkedDay) {
                nextPossible2Date = new Date(latestWorkedDay);
                nextPossible2Date.setDate(nextPossible2Date.getDate() + 14 + 1);
                nextPossible2Date.setHours(0,0,0,0);
                nextPossible2Message = `조건 2 충족을 위한 가장 빠른 신청 가능일: **${formatDateToYYYYMMDD(nextPossible2Date)}** (마지막 근로일(${formatDateToYYYYMMDD(latestWorkedDay)}) 기준) (이후 근로제공이 없다는 전제)`;
            } else {
                nextPossible2Message = `조건 2 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (근무 기록 확인 필요)`;
            }
        }

        const generalWorkerEligible = condition1Met;
        const constructionWorkerEligible = condition1Met || noWork14Days;
        
        const generalWorkerText = generalWorkerEligible ? "신청 가능" : "신청 불가능";
        const constructionWorkerText = constructionWorkerEligible ? "신청 가능" : "신청 불가능";
        
        const finalHtml = `
            <h3>기준 날짜(${INPUT_DATE_STR}) 기준 조건 판단</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실 없어야 함</p>
            <p>총 기간 일수: ` + currentTotalDaysForCond1 + `일</p>
            <p>1/3 기준: ` + currentThresholdForCond1.toFixed(1) + `일</p>
            <p>근무일 수: ` + actualWorkedDaysForCond1 + `일</p>
            <p>` + condition1Text + `</p>
            <p>` + condition2Text + `</p>
            ` + (nextPossible1Message ? "<p>" + nextPossible1Message + "</p>" : "") + `
            ` + (nextPossible2Message ? "<p>" + nextPossible2Message + "</p>" : "") + `
            <h3>기준 날짜(${INPUT_DATE_STR}) 기준 최종 판단</h3>
            <p>일반일용근로자: ` + generalWorkerText + `</p>
            <p>건설일용근로자: ` + constructionWorkerText + `</p>
            <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
        `;

        document.getElementById('resultContainer').innerHTML = finalHtml;

        window.eligibilityResults = {
            cond1Met: condition1Met,
            cond2Met: noWork14Days,
            generalEligible: generalWorkerEligible,
            constructionEligible: constructionWorkerEligible,
            cond1WorkedDays: actualWorkedDaysForCond1,
            cond1Threshold: currentThresholdForCond1,
            cond1TotalDays: currentTotalDaysForCond1,
            cond1PeriodStart: formatDateToYYYYMMDD(currentPeriodStartForCond1),
            cond1PeriodEnd: INPUT_DATE_STR,
            cond2PeriodStart: FOURTEEN_DAYS_START_STR,
            cond2PeriodEnd: FOURTEEN_DAYS_END_STR,
            lastWorkedDay: latestWorkedDay ? formatDateToYYYYMMDD(latestWorkedDay) : null,
            selectedDates: selectedFullDates.sort()
        };
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
            console.error("Failed to load selected dates from localStorage or calculate result:", e);
            calculateAndDisplayResult([]);
        }
    }

    function saveToLocalStorage(data) {
        try {
            localStorage.setItem('selectedDates', JSON.stringify(data));
        } catch (e) {
            console.error("Failed to save selected dates to localStorage:", e);
        }
    }

    window.clearCalendar = function() {
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            days[i].classList.remove('selected');
        }
        saveToLocalStorage([]);
        calculateAndDisplayResult([]);
    };

    window.generateReport = function() {
        const results = window.eligibilityResults;
        if (!results) {
            alert("먼저 근무일을 선택하여 조건을 확인해주세요.");
            return;
        }

        let reportHtml = REPORT_TEMPLATE;

        const inputDateObj = new Date(INPUT_DATE_STR);
        const inputYear = inputDateObj.getFullYear();
        const inputMonth = String(inputDateObj.getMonth() + 1).padStart(2, '0');
        const inputDay = String(inputDateObj.getDate()).padStart(2, '0');

        reportHtml = reportHtml.replace(/{{INPUT_DATE_YEAR}}/g, inputYear);
        reportHtml = reportHtml.replace(/{{INPUT_DATE_MONTH}}/g, inputMonth);
        reportHtml = reportHtml.replace(/{{INPUT_DATE_DAY}}/g, inputDay);
        reportHtml = reportHtml.replace(/{{COND1_PERIOD_START}}/g, results.cond1PeriodStart);
        reportHtml = reportHtml.replace(/{{COND1_PERIOD_END}}/g, results.cond1PeriodEnd);
        reportHtml = reportHtml.replace(/{{COND1_WORKED_DAYS}}/g, results.cond1WorkedDays);
        reportHtml = reportHtml.replace(/{{COND1_TOTAL_DAYS}}/g, results.cond1TotalDays);
        reportHtml = reportHtml.replace(/{{COND1_THRESHOLD}}/g, results.cond1Threshold.toFixed(1));
        reportHtml = reportHtml.replace(/{{COND2_PERIOD_START}}/g, results.cond2PeriodStart);
        reportHtml = reportHtml.replace(/{{COND2_PERIOD_END}}/g, results.cond2PeriodEnd);
        
        let calendarTableHTML = "";
        let currentMonthNum = null;
        let currentRowFor15Days = [];
        const datesToDisplay = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr));

        for (let i = 0; i < datesToDisplay.length; i++) {
            const tempDate = datesToDisplay[i];
            const month = tempDate.getMonth() + 1;
            const dayNum = tempDate.getDate();
            const isSelected = results.selectedDates.includes(formatDateToYYYYMMDD(tempDate));
            const displayChar = isSelected ? "○" : " ";

            if (currentMonthNum === null || month !== currentMonthNum) {
                if (currentMonthNum !== null) {
                    while (currentRowFor15Days.length < 15) {
                        currentRowFor15Days.push('<td></td>');
                    }
                    // 마지막 달의 전체 일수 계산을 더 정확하게
                    const lastDayOfPrevMonth = new Date(tempDate.getFullYear(), currentMonthNum, 0);
                    calendarTableHTML += `<tr>${currentRowFor15Days.join('')}<td></td><td class="total-days">${lastDayOfPrevMonth.getDate()}일</td></tr>`;
                    currentRowFor15Days = [];
                }
                currentMonthNum = month;
                calendarTableHTML += `<tr><td rowspan="2" style="font-weight: bold; text-align: center; vertical-align: middle;">${String(month).padStart(2, '0')}월</td>`;
                currentRowFor15Days = [];
            }
            
            currentRowFor15Days.push(`<td style="width: 30px; text-align: center;">${dayNum}<br>${displayChar}</td>`);

            if (currentRowFor15Days.length === 15) {
                calendarTableHTML += `<tr>${currentRowFor15Days.join('')}<td></td><td class="total-days"></td></tr>`;
                currentRowFor15Days = [];
                if (dayNum < new Date(tempDate.getFullYear(), tempDate.getMonth() + 1, 0).getDate()) {
                    calendarTableHTML += `<tr>`;
                }
            }
        }
        if (currentRowFor15Days.length > 0) {
            while (currentRowFor15Days.length < 15) {
                currentRowFor15Days.push('<td></td>');
            }
            # 마지막 달의 전체 일수 계산
            const lastDateInCalendar = datesToDisplay[datesToDisplay.length - 1];
            const lastDayOfLastMonth = new Date(lastDateInCalendar.getFullYear(), lastDateInCalendar.getMonth() + 1, 0);
            calendarTableHTML += `<tr>${currentRowFor15Days.join('')}<td></td><td class="total-days">${lastDayOfLastMonth.getDate()}일</td></tr>`;
        }
        reportHtml = reportHtml.replace(/{{CALENDAR_TABLE}}/g, calendarTableHTML);

        reportHtml = reportHtml.replace(/{{SELECTED_DATES_LIST}}/g, results.selectedDates.join(', '));

        const printWindow = window.open('', '_blank');
        printWindow.document.write(reportHtml);
        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
    };

    document.addEventListener('DOMContentLoaded', function() {
        loadSelectedDates();
    });
    </script>
    """

    st.components.v1.html(calendar_html, height=1000, scrolling=True, key="my_calendar_component") 

    st.warning("버튼 클릭 후 새 창(팝업)이 뜨지 않는다면, 브라우저에서 팝업이 차단되었을 수 있습니다. 브라우저 주소창 근처의 팝업 차단 아이콘을 확인하고 **팝업을 허용**해주세요.")

    st.components.v1.html(
        """
        <button id="printReportBtn" style="
            background-color: #28A745;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 17px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: background-color 0.2s;
            margin-top: 10px;
        " onmouseover="this.style.backgroundColor='#218838'" onmouseout="this.style.backgroundColor='#28A745'">
            📄 확인서 출력 (PDF 저장)
        </button>
        <script>
            document.getElementById('printReportBtn').onclick = function() {
                window.generateReport();
            };
        </script>
        """,
        height=70,
        key="print_button_component"
    )

if __name__ == "__main__":
    def main():
        daily_worker_eligibility_app()

    main()
