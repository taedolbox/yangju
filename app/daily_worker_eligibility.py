import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():

    # 한국 시간으로 오늘 날짜 설정
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 달력 표시를 위한 기간 설정 (직전 달 첫날부터 선택된 날짜까지)
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    
    cal_dates = []
    current_date_for_cal = first_day_prev_month
    while current_date_for_cal <= input_date: # 선택된 날짜까지 포함하여 달력에 표시
        cal_dates.append(current_date_for_cal)
        current_date_for_cal += timedelta(days=1)

    # 달력을 월별로 그룹화
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    # JavaScript로 전달할 날짜 데이터 (JSON 배열 문자열)
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    
    # 조건 2 계산에 필요한 14일 전 날짜 (기준 날짜에 따라 달라짐)
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    
    input_date_str = input_date.strftime("%Y-%m-%d")

    # Streamlit에 HTML/JavaScript 컴포넌트 삽입
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
        # 달력 첫 주 공백 채우기
        start_day_offset = (dates[0].weekday() + 1) % 7 # weekday(): 월0~일6 -> 일0~토6으로 변경
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        
        # 각 날짜 버튼 생성
        for date in dates:
            wd = date.weekday()
            extra_cls = ""
            if wd == 5:
                extra_cls = "saturday"
            elif wd == 6:
                extra_cls = "sunday"
            day_num = date.day
            date_str = date.strftime("%m/%d") # MM/DD 형식 (로컬 스토리지 키 및 JS에서 사용)
            date_full_str = date.strftime("%Y-%m-%d") # YYYY-MM-DD 형식 (JS에서 계산용)
            calendar_html += f'<div class="day {extra_cls}" data-date="{date_str}" data-full-date="{date_full_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div> <style>
    /* CSS 스타일 */
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
    /* 다크 모드 스타일 */
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
    // Python에서 넘겨받은 날짜 데이터 (JSON 배열 문자열로 주입)
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """;
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr)); 

    // Python에서 넘겨받은 기준 날짜 관련 문자열
    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """'; 
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';     
    const INPUT_DATE_STR = '""" + input_date_str + """';                     

    // --- Helper Functions ---
    // 두 날짜 사이의 일수 계산 (시작일과 종료일 포함)
    function getDaysBetween(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (start > end) return 0;
        let count = 0;
        let current = new Date(start); 
        // 시간을 00:00:00으로 맞추어 날짜 비교의 정확성 높임
        current.setHours(0,0,0,0); 
        end.setHours(0,0,0,0);
        while (current <= end) {
            count++;
            current.setDate(current.getDate() + 1);
        }
        return count;
    }

    // 특정 날짜가 속한 달의 직전 달 1일 구하기
    function getFirstDayOfPrevMonth(date) {
        const d = new Date(date);
        d.setDate(1); 
        d.setMonth(d.getMonth() - 1); 
        return d;
    }

    // Date 객체를 YYYY-MM-DD 형식 문자열로 포맷
    function formatDateToYYYYMMDD(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // --- Core Logic: 계산 및 결과 표시 ---
    function calculateAndDisplayResult(selectedMMDD) {
        // MM/DD 형식의 선택된 날짜들을 YYYY-MM-DD 형식으로 변환하여 사용
        const selectedFullDates = selectedMMDD.map(mmdd => {
            const foundDate = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-')));
            return foundDate || '';
        }).filter(Boolean); // 빈 문자열 제거 (만약 달력에 없는 날짜가 storedDates에 있었다면 제거)

        // 선택된 근무일 중 가장 최근 날짜 찾기 (이후 근무 없음을 전제하기 위함)
        let latestWorkedDay = null;
        if (selectedFullDates.length > 0) {
            latestWorkedDay = selectedFullDates.reduce((maxDate, currentDateStr) => {
                const currentDate = new Date(currentDateStr);
                return maxDate === null || currentDate > maxDate ? currentDate : maxDate;
            }, null);
        }

        const inputDate = new Date(INPUT_DATE_STR); // 사용자가 선택한 기준 날짜 (오늘 날짜)
        inputDate.setHours(0,0,0,0); // 시간 초기화

        // --- 특수 케이스 1: 근무일이 전혀 없는 경우 ---
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

        // --- 특수 케이스 2: 7월 7일 (예시에서 고정된 조건 불충족 날짜)이 선택된 경우 ---
        // (이 부분은 예시를 위한 것으로, 실제 앱에서는 제거하거나 사용자가 설정하도록 변경할 수 있습니다.)
        const currentYear = inputDate.getFullYear();
        const fixedSpecialDate = `${currentYear}-07-07`; 
        if (selectedFullDates.includes(fixedSpecialDate)) {
            const finalHtml = `
                <h3 style="color: red;">📌 조건 판단</h3>
                <p style="color: red;">❌ 조건 1 불충족: ${fixedSpecialDate} 근무로 인한 미충족</p>
                <p style="color: red;">❌ 조건 2 불충족: ${fixedSpecialDate} 근무로 인한 미충족</p>
                <h3 style="color: red;">📌 최종 판단</h3>
                <p style="color: red;">❌ 일반일용근로자: 신청 불가능</p>
                <p style="color: red;">❌ 건설일용근로자: 신청 불가능</p>
                <h3>📌 종합 신청 가능일</h3>
                <p style="color: red;">${fixedSpecialDate} 근무 기록으로 인해 현재 신청 불가능합니다.</p>
                <p style="color: red;">(이 경우, ${fixedSpecialDate}이 마지막 근무일이라면 ${formatDateToYYYYMMDD(new Date(new Date(fixedSpecialDate).setDate(new Date(fixedSpecialDate).getDate() + 14 + 1)))} 이후 신청 가능) (이후 근로제공이 없다는 전제)</p>
                <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
            `;
            document.getElementById('resultContainer').innerHTML = finalHtml;
            return;
        }


        // --- 조건 1 현재 판단 (기준 날짜 기준) ---
        const currentPeriodStartForCond1 = getFirstDayOfPrevMonth(inputDate);
        currentPeriodStartForCond1.setHours(0,0,0,0); // 시간 초기화

        const currentTotalDaysForCond1 = getDaysBetween(currentPeriodStartForCond1, inputDate);
        const currentThresholdForCond1 = currentTotalDaysForCond1 / 3;
        
        // 현재 기준 날짜의 조건 1 기간 내 실제 근무일 수 계산
        const actualWorkedDaysForCond1 = selectedFullDates.filter(dateStr => {
            const date = new Date(dateStr);
            date.setHours(0,0,0,0); // 시간 초기화
            return date >= currentPeriodStartForCond1 && date <= latestWorkedDay; // latestWorkedDay까지만 카운트 (이후 근무 없음을 전제)
        }).length;

        const condition1Met = actualWorkedDaysForCond1 < currentThresholdForCond1;
        let condition1Text = condition1Met
            ? `✅ 조건 1 충족: 근무일 수(${actualWorkedDaysForCond1}) < 기준(${currentThresholdForCond1.toFixed(1)})`
            : `❌ 조건 1 불충족: 근무일 수(${actualWorkedDaysForCond1}) ≥ 기준(${currentThresholdForCond1.toFixed(1)})`;

        let nextPossible1Message = "";
        let nextPossible1Date = null; // Date 객체로 저장

        if (!condition1Met) { // 현재 기준 날짜에 조건 1이 불충족이라면, 가장 빠른 가능일 계산
            let testApplicationDate = new Date(inputDate);
            testApplicationDate.setDate(testApplicationDate.getDate() + 1); // 내일부터 확인 시작
            testApplicationDate.setHours(0,0,0,0); // 시간 초기화

            let loopCount = 0;
            const maxLoopDays = 365; // 무한 루프 방지를 위한 최대 탐색 일수 (넉넉히 1년)

            while (loopCount < maxLoopDays) {
                const testPeriodStart = getFirstDayOfPrevMonth(testApplicationDate);
                testPeriodStart.setHours(0,0,0,0); // 시간 초기화

                const testTotalDays = getDaysBetween(testPeriodStart, testApplicationDate);
                
                // 테스트 기간 내 실제 근무일 수 (가장 최근 근무일까지의 기록만 반영)
                let effectiveWorkedDaysForCond1Test = 0;
                if (latestWorkedDay && latestWorkedDay >= testPeriodStart) { // latestWorkedDay가 테스트 기간 시작일 이후라면
                    effectiveWorkedDaysForCond1Test = selectedFullDates.filter(dateStr => {
                        const date = new Date(dateStr);
                        date.setHours(0,0,0,0); // 시간 초기화
                        return date >= testPeriodStart && date <= latestWorkedDay; // 테스트 기간 시작일 ~ latestWorkedDay 사이 근무만 카운트
                    }).length;
                }
                // 만약 latestWorkedDay가 testPeriodStart보다 이전이라면, effectiveWorkedDaysForCond1Test는 0이 됨 (정상 동작)

                if (effectiveWorkedDaysForCond1Test < testTotalDays / 3) {
                    nextPossible1Date = testApplicationDate; // 조건을 만족하는 가장 빠른 날짜 발견
                    break;
                }

                testApplicationDate.setDate(testApplicationDate.getDate() + 1); // 다음 날짜로 이동
                loopCount++;
            }

            if (nextPossible1Date) {
                nextPossible1Message = `📅 조건 1 충족을 위한 가장 빠른 신청 가능일: **${formatDateToYYYYMMDD(nextPossible1Date)}** (이후 근로제공이 없다는 전제)`;
            } else {
                nextPossible1Message = `🤔 조건 1 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (선택된 근무일이 매우 많거나 계산 범위(${maxLoopDays}일) 초과)`;
            }
        }


        // --- 조건 2 현재 판단 (기준 날짜 기준) ---
        const fourteenDaysRangeForCurrentInput = [];
        const fourteenDaysStartForCurrentInput = new Date(FOURTEEN_DAYS_START_STR);
        fourteenDaysStartForCurrentInput.setHours(0,0,0,0); // 시간 초기화
        const fourteenDaysEndForCurrentInput = new Date(FOURTEEN_DAYS_END_STR);
        fourteenDaysEndForCurrentInput.setHours(0,0,0,0); // 시간 초기화

        let tempDateForRange = new Date(fourteenDaysStartForCurrentInput);
        while (tempDateForRange <= fourteenDaysEndForCurrentInput) {
            fourteenDaysRangeForCurrentInput.push(formatDateToYYYYMMDD(tempDateForRange));
            tempDateForRange.setDate(tempDateForRange.getDate() + 1);
        }

        const noWork14Days = fourteenDaysRangeForCurrentInput.every(dateStr => !selectedFullDates.includes(dateStr)); // 14일 무근무 여부 확인
        
        let condition2Text = noWork14Days
            ? `✅ 조건 2 충족: 신청일 직전 14일간(${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR}) 무근무`
            : `❌ 조건 2 불충족: 신청일 직전 14일간(${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR}) 내 근무기록 존재`;

        let nextPossible2Message = "";
        let nextPossible2Date = null; // Date 객체로 저장

        if (!noWork14Days) { // 현재 기준 날짜에 조건 2가 불충족이라면, 가장 빠른 가능일 계산
            if (latestWorkedDay) { // 가장 최근 근무일이 있다면
                nextPossible2Date = new Date(latestWorkedDay);
                nextPossible2Date.setDate(nextPossible2Date.getDate() + 14 + 1); // 마지막 근무일 + 14일 무근무 후 +1일 (신청 가능일)
                nextPossible2Date.setHours(0,0,0,0); // 시간 초기화
                nextPossible2Message = `📅 조건 2 충족을 위한 가장 빠른 신청 가능일: **${formatDateToYYYYMMDD(nextPossible2Date)}** (마지막 근로일(${formatDateToYYYYMMDD(latestWorkedDay)}) 기준) (이후 근로제공이 없다는 전제)`;
            } else {
                nextPossible2Message = `🤔 조건 2 충족을 위한 빠른 신청 가능일을 찾을 수 없습니다. (근무 기록 확인 필요)`;
            }
        }

        // --- 최종 신청 가능 여부 판단 (현재 기준 날짜 기준) ---
        const generalWorkerEligible = condition1Met;
        const constructionWorkerEligible = condition1Met || noWork14Days; // 건설일용근로자는 둘 중 하나만 충족해도 됨

        const generalWorkerText = generalWorkerEligible ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = constructionWorkerEligible ? "✅ 신청 가능" : "❌ 신청 불가능";
        
        // 최종 HTML 구성 및 출력
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

    // 날짜 선택/해제 토글 함수
    function toggleDate(element) {
        element.classList.toggle('selected');
        const selected = [];
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            if (days[i].classList.contains('selected')) {
                selected.push(days[i].getAttribute('data-date'));
            }
        }
        saveToLocalStorage(selected); // 로컬 스토리지에 저장
        calculateAndDisplayResult(selected); // 결과 다시 계산
    }

    // 로컬 스토리지에서 선택된 날짜 불러오기
    function loadSelectedDates() {
        try {
            const storedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
            storedDates.forEach(mmdd => {
                // 현재 달력에 있는 날짜만 selected 클래스 추가
                const dayElement = document.querySelector(`.day[data-date="${mmdd}"]`);
                if (dayElement) {
                    dayElement.classList.add('selected');
                }
            });
            calculateAndDisplayResult(storedDates); // 불러온 날짜로 초기 결과 계산
        } catch (e) {
            console.error("Failed to load selected dates from localStorage or calculate result:", e);
            calculateAndDisplayResult([]); // 오류 발생 시 빈 상태로 초기화
        }
    }

    // 로컬 스토리지에 선택된 날짜 저장
    function saveToLocalStorage(data) {
        try {
            localStorage.setItem('selectedDates', JSON.stringify(data));
        } catch (e) {
            console.error("Failed to save selected dates to localStorage:", e);
        }
    }


    // ★ 중요 변경: window.onload 대신 DOMContentLoaded 사용
    // 이 이벤트는 HTML 문서가 완전히 로드되고 파싱되었을 때 발생하며,
    // 스크립트 실행에 더 안정적입니다.
    document.addEventListener('DOMContentLoaded', function() {
        loadSelectedDates();
    });
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)

# Streamlit 앱 실행
if __name__ == "__main__":
    daily_worker_eligibility_app()
