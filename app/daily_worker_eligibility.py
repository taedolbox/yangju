import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    # Set today's date in KST
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # Set period for calendar display (from the first day of the previous month to the selected date)
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    
    cal_dates = []
    current_date_for_cal = first_day_prev_month
    while current_date_for_cal <= input_date: # Include up to the selected date
        cal_dates.append(current_date_for_cal)
        current_date_for_cal += timedelta(days=1)

    # Group calendar by month
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    # Date data for JavaScript (JSON array string)
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    
    # 14 days prior date needed for Condition 2 calculation (depends on the base date)
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    
    input_date_str = input_date.strftime("%Y-%m-%d")

    # Streamlit HTML/JavaScript component insertion
    calendar_html = "<div id='calendar-container'>"

    # Add the Clear Calendar button here, above the month headers
    calendar_html += """
    <div style="text-align: right; margin-bottom: 15px;">
        <button onclick="clearCalendar()" style="
            background-color: #3F51B5; /* Changed from red to indigo blue */
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
        # Fill empty days for the first week of the month
        start_day_offset = (dates[0].weekday() + 1) % 7 # weekday(): Mon0~Sun6 -> Sun0~Sat6
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        
        # Create day buttons
        for date in dates:
            wd = date.weekday()
            extra_cls = ""
            if wd == 5:
                extra_cls = "saturday"
            elif wd == 6:
                extra_cls = "sunday"
            day_num = date.day
            date_str = date.strftime("%m/%d") # MM/DD format (for local storage key and JS)
            date_full_str = date.strftime("%Y-%m-%d") #YYYY-MM-DD format (for JS calculation)
            calendar_html += f'<div class="day {extra_cls}" data-date="{date_str}" data-full-date="{date_full_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>
    <style>
    /* CSS styles */
    .calendar {
        display: grid; 
        grid-template-columns: repeat(7, 44px); /* 40px -> 45px: increased column width */
        grid-gap: 5px;
        margin-bottom: 20px; background: #fff; 
        padding: 10px 1px; /* Maintain 10px top/bottom, 1px left/right */
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .day-header, .empty-day {
        width: 44px; height: 44px; /* 40px -> 45px: increased header size */
        line-height: 45px; /* 40px -> 45px: maintain vertical text alignment */
        text-align: center;
        font-weight: bold; color: #555;
    }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }
    .day.sunday { color: red; }
    .day.saturday { color: blue; }
    .day-header { background: #e0e0e0; border-radius: 5px; font-size: 16px; /* 14px -> 16px */ }
    .empty-day { background: transparent; border: none; }
    .day {
        width: 44px; height: 44px; /* 40px -> 45px: increased day cell size */
        line-height: 45px; /* 40px -> 45px: maintain vertical text alignment */
        text-align: center;
        border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none;
        transition: background 0.1s ease, border 0.1s ease; font-size: 18px; /* 16px -> 18px */ color: #333;
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

    /* Adjust spacing between year/month text and calendar container */
    #calendar-container h4 {
        margin-bottom: 5px; /* Reduce bottom margin of year/month text to be closer to the calendar. */
    }

    /* Dark mode styles */
    html[data-theme="dark"] #resultContainer {
        background: #262730;
        color: #FAFAFA;
    }
    html[data-theme="dark"] #resultContainer h3 {
        color: #90CAF9;
    }
    /* ★★★ This part has been changed: Force color for year/month text in dark mode ★★★ */
    html[data-theme="dark"] h4 {
        color: #FFFFFF !important; /* Set bright color for all h4 and force with !important */
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
    // Python-passed date data (injected as JSON array string)
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """;
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr)); 

    // Python-passed base date related strings
    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """'; 
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';    
    const INPUT_DATE_STR = '""" + input_date_str + """';          

    // --- Helper Functions ---
    // Calculate days between two dates (inclusive of start and end dates)
    function getDaysBetween(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (start > end) return 0;
        let count = 0;
        let current = new Date(start); 
        // Set time to 00:00:00 for accurate date comparison
        current.setHours(0,0,0,0); 
        end.setHours(0,0,0,0);
        while (current <= end) {
            count++;
            current.setDate(current.getDate() + 1);
        }
        return count;
    }

    // Get the first day of the month prior to the given date
    function getFirstDayOfPrevMonth(date) {
        const d = new Date(date);
        d.setDate(1); 
        d.setMonth(d.getMonth() - 1); 
        return d;
    }

    // Format Date object toYYYY-MM-DD string
    function formatDateToYYYYMMDD(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // --- Core Logic: Calculation and Result Display ---
    function calculateAndDisplayResult(selectedMMDD) {
        // Convert selected MM/DD dates toYYYY-MM-DD format
        const selectedFullDates = selectedMMDD.map(mmdd => {
            const foundDate = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-')));
            return foundDate || '';
        }).filter(Boolean); // Remove empty strings (if storedDates contained dates not in the current calendar)

        // Find the latest worked day among selected working days (assuming no further work)
        let latestWorkedDay = null;
        if (selectedFullDates.length > 0) {
            latestWorkedDay = selectedFullDates.reduce((maxDate, currentDateStr) => {
                const currentDate = new Date(currentDateStr);
                return maxDate === null || currentDate > maxDate ? currentDate : maxDate;
            }, null);
        }

        const inputDate = new Date(INPUT_DATE_STR); // User selected base date (today's date)
        inputDate.setHours(0,0,0,0); // Initialize time

        // --- Special Case 1: No working days selected ---
        if (selectedFullDates.length === 0) {
            const finalHtml = `
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
            document.getElementById('resultContainer').innerHTML = finalHtml;
            return;
        }

        // --- Special Case 2: Base date (INPUT_DATE_STR) is selected as a working day ---
        // (If the date selected by the user in the Streamlit date picker is checked as a working day in the calendar)
        if (selectedFullDates.includes(INPUT_DATE_STR)) {
            // If base date is a working day, both Condition 1 and 2 are considered unfulfilled (user request)
            const nextPossibleApplicationDate = new Date(INPUT_DATE_STR);
            nextPossibleApplicationDate.setDate(nextPossibleApplicationDate.getDate() + 14 + 1); // Base date + 14 days no work + 1 day

            const finalHtml = `
                <h3 style="color: red;">📌 조건 판단</h3>
                <p style="color: red;">❌ 조건 1 불충족: 기준 날짜(${INPUT_DATE_STR}) 근무로 인한 미충족</p>
                <p style="color: red;">❌ 조건 2 불충족: 기준 날짜(${INPUT_DATE_STR}) 근무로 인한 미충족</p>
                <h3 style="color: red;">📌 최종 판단</h3>
                <p style="color: red;">❌ 일반일용근로자: 신청 불가능</p>
                <p style="color: red;">❌ 건설일용근로자: 신청 불가능</p>
                <h3>📌 종합 신청 가능일</h3>
                <p style="color: red;">기준 날짜(${INPUT_DATE_STR})에 근무 기록이 있으므로 현재 신청 불가능합니다.</p>
                <p style="color: red;">(이 경우, ${INPUT_DATE_STR}이 마지막 근무일이라면 **${formatDateToYYYYMMDD(nextPossibleApplicationDate)}** 이후 신청 가능) (이후 근로제공이 없다는 전제)</p>
                <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
            `;
            document.getElementById('resultContainer').innerHTML = finalHtml;
            return;
        }


        // --- Condition 1 Current Judgment (based on base date) ---
        const currentPeriodStartForCond1 = getFirstDayOfPrevMonth(inputDate);
        currentPeriodStartForCond1.setHours(0,0,0,0); // Initialize time

        const currentTotalDaysForCond1 = getDaysBetween(currentPeriodStartForCond1, inputDate);
        const currentThresholdForCond1 = currentTotalDaysForCond1 / 3;
        
        // Calculate actual working days within Condition 1 period for the current base date
        const actualWorkedDaysForCond1 = selectedFullDates.filter(dateStr => {
            const date = new Date(dateStr);
            date.setHours(0,0,0,0); // Initialize time
            return date >= currentPeriodStartForCond1 && date <= latestWorkedDay; // Count only up to latestWorkedDay (assuming no further work)
        }).length;

        const condition1Met = actualWorkedDaysForCond1 < currentThresholdForCond1;
        let condition1Text = condition1Met
            ? `✅ 조건 1 충족: 근무일 수(${actualWorkedDaysForCond1}) < 기준(${currentThresholdForCond1.toFixed(1)})`
            : `❌ 조건 1 불충족: 근무일 수(${actualWorkedDaysForCond1}) ≥ 기준(${currentThresholdForCond1.toFixed(1)})`;

        let nextPossible1Message = "";
        let nextPossible1Date = null; // Store as Date object

        if (!condition1Met) { // If Condition 1 is not met for the current base date, calculate the earliest possible date
            let testApplicationDate = new Date(inputDate);
            testApplicationDate.setDate(testApplicationDate.getDate() + 1); // Start checking from tomorrow
            testApplicationDate.setHours(0,0,0,0); // Initialize time

            let loopCount = 0;
            const maxLoopDays = 365; // Max search days to prevent infinite loop (generously 1 year)

            while (loopCount < maxLoopDays) {
                const testPeriodStart = getFirstDayOfPrevMonth(testApplicationDate);
                testPeriodStart.setHours(0,0,0,0); // Initialize time

                const testTotalDays = getDaysBetween(testPeriodStart, testApplicationDate);
                
                // Actual working days within the test period (only reflecting records up to the latest worked day)
                let effectiveWorkedDaysForCond1Test = 0;
                if (latestWorkedDay && latestWorkedDay >= testPeriodStart) { // If latestWorkedDay is after the test period start
                    effectiveWorkedDaysForCond1Test = selectedFullDates.filter(dateStr => {
                        const date = new Date(dateStr);
                        date.setHours(0,0,0,0); // Initialize time
                        return date >= testPeriodStart && date <= latestWorkedDay; // Count only work between test period start and latestWorkedDay
                    }).length;
                }
                // If latestWorkedDay is before testPeriodStart, effectiveWorkedDaysForCond1Test will be 0 (correct behavior)

                if (effectiveWorkedDaysForCond1Test < testTotalDays / 3) {
                    nextPossible1Date = testApplicationDate; // Found the earliest date that satisfies the condition
                    break;
                }

                testApplicationDate.setDate(testApplicationDate.getDate() + 1); // Move to the next day
                loopCount++;
            }

            if (nextPossible1Date) {
                nextPossible1Message = `📅 조건 1 충족을 위한 가장 빠른 신청 가능일: **${formatDateToYYYYMMDD(nextPossible1Date)}** (이후 근로제공이 없다는 전제)`;
            } else {
                nextPossible1Message = `🤔 조건 1 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (선택된 근무일이 매우 많거나 계산 범위(${maxLoopDays}일) 초과)`;
            }
        }


        // --- Condition 2 Current Judgment (based on base date) ---
        const fourteenDaysRangeForCurrentInput = [];
        const fourteenDaysStartForCurrentInput = new Date(FOURTEEN_DAYS_START_STR);
        fourteenDaysStartForCurrentInput.setHours(0,0,0,0); // Initialize time
        const fourteenDaysEndForCurrentInput = new Date(FOURTEEN_DAYS_END_STR);
        fourteenDaysEndForCurrentInput.setHours(0,0,0,0); // Initialize time

        let tempDateForRange = new Date(fourteenDaysStartForCurrentInput);
        while (tempDateForRange <= fourteenDaysEndForCurrentInput) {
            fourteenDaysRangeForCurrentInput.push(formatDateToYYYYMMDD(tempDateForRange));
            tempDateForRange.setDate(tempDateForRange.getDate() + 1);
        }

        const noWork14Days = fourteenDaysRangeForCurrentInput.every(dateStr => !selectedFullDates.includes(dateStr)); // Check for 14 days of no work
        
        let condition2Text = noWork14Days
            ? `✅ 조건 2 충족: 신청일 직전 14일간(${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR}) 무근무`
            : `❌ 조건 2 불충족: 신청일 직전 14일간(${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR}) 내 근무기록 존재`;

        let nextPossible2Message = "";
        let nextPossible2Date = null; // Store as Date object

        if (!noWork14Days) { // If Condition 2 is not met for the current base date, calculate the earliest possible date
            if (latestWorkedDay) { // If there is a latest worked day
                nextPossible2Date = new Date(latestWorkedDay);
                nextPossible2Date.setDate(nextPossible2Date.getDate() + 14 + 1); // Last worked day + 14 days no work + 1 day (possible application date)
                nextPossible2Date.setHours(0,0,0,0); // Initialize time
                nextPossible2Message = `📅 조건 2 충족을 위한 가장 빠른 신청 가능일: **${formatDateToYYYYMMDD(nextPossible2Date)}** (마지막 근로일(${formatDateToYYYYMMDD(latestWorkedDay)}) 기준) (이후 근로제공이 없다는 전제)`;
            } else {
                nextPossible2Message = `🤔 조건 2 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (근무 기록 확인 필요)`;
            }
        }

        // --- Final Application Eligibility Judgment (based on current base date) ---
        const generalWorkerEligible = condition1Met;
        const constructionWorkerEligible = condition1Met || noWork14Days; // Construction daily workers only need to meet one of the two conditions
        
        const generalWorkerText = generalWorkerEligible ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = constructionWorkerEligible ? "✅ 신청 가능" : "❌ 신청 불가능";
        
        // Construct and display final HTML
        const finalHtml = `
            <h3>📌 기준 날짜(${INPUT_DATE_STR}) 기준 조건 판단</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실 없어야 함</p>
            <p>총 기간 일수: ` + currentTotalDaysForCond1 + `일</p>
            <p>1/3 기준: ` + currentThresholdForCond1.toFixed(1) + `일</p>
            <p>근무일 수: ` + actualWorkedDaysForCond1 + `일</p>
            <p>` + condition1Text + `</p>
            <p>` + condition2Text + `</p>
            ` + (nextPossible1Message ? "<p>" + nextPossible1Message + "</p>" : "") + `
            ` + (nextPossible2Message ? "<p>" + nextPossible2Message + "</p>" : "") + `
            <h3>📌 기준 날짜(${INPUT_DATE_STR}) 기준 최종 판단</h3>
            <p>✅ 일반일용근로자: ` + generalWorkerText + `</p>
            <p>✅ 건설일용근로자: ` + constructionWorkerText + `</p>
            <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
        `;

        document.getElementById('resultContainer').innerHTML = finalHtml;
    }

    // Toggle date selection/deselection function
    function toggleDate(element) {
        element.classList.toggle('selected');
        const selected = [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            if (days[i].classList.contains('selected')) {
                selected.push(days[i].getAttribute('data-date'));
            }
        }
        saveToLocalStorage(selected); // Save to local storage
        calculateAndDisplayResult(selected); // Recalculate result
    }

    // Load selected dates from local storage
    function loadSelectedDates() {
        try {
            const storedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
            storedDates.forEach(mmdd => {
                // Add 'selected' class only to dates present in the current calendar
                const dayElement = document.querySelector(`.day[data-date="${mmdd}"]`);
                if (dayElement) {
                    dayElement.classList.add('selected');
                }
            });
            calculateAndDisplayResult(storedDates); // Calculate initial result with loaded dates
        } catch (e) {
            console.error("Failed to load selected dates from localStorage or calculate result:", e);
            calculateAndDisplayResult([]); // Initialize with empty state on error
        }
    }

    // Save selected dates to local storage
    function saveToLocalStorage(data) {
        try {
            localStorage.setItem('selectedDates', JSON.stringify(data));
        } catch (e) {
            console.error("Failed to save selected dates to localStorage:", e);
        }
    }

    // Function to clear all selected dates
    window.clearCalendar = function() { // Make it global by assigning to window
        // Remove 'selected' class from all days
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            days[i].classList.remove('selected');
        }
        // Clear local storage
        saveToLocalStorage([]);
        // Recalculate and display result
        calculateAndDisplayResult([]);
    };


    // DOMContentLoaded event listener: Execute script after HTML document is fully loaded and parsed
    document.addEventListener('DOMContentLoaded', function() {
        loadSelectedDates();
    });
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)
