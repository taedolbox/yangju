# app/daily_worker_eligibility.py

import streamlit as st
from datetime import datetime, timedelta
import json
import os # os 모듈 임포트

def daily_worker_eligibility_app():

    # static/styles.css 파일 로드
    # 이 부분이 모든 CSS를 앱에 적용합니다.
    try:
        # 현재 스크립트 파일 (daily_worker_eligibility.py)의 디렉토리를 기준으로 static/styles.css 경로를 구성
        script_dir = os.path.dirname(__file__)
        css_file_path = os.path.join(script_dir, "static", "styles.css")
        with open(css_file_path, "r", encoding="utf-8") as f: # 인코딩 추가
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("오류: static/styles.css 파일을 찾을 수 없습니다. 파일이 올바른 디렉토리에 있는지 확인하세요.")
    except Exception as e:
        st.error(f"CSS 파일을 로드하는 중 오류 발생: {e}")


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
        # h4 태그는 여전히 이 부분에서 생성됩니다.
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
            date_full_str = date.strftime("%Y-%m-%d") #YYYY-MM-DD 형식 (JS에서 계산용)
            calendar_html += f'<div class="day {extra_cls}" data-date="{date_str}" data-full-date="{date_full_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>
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

    // Date 객체를YYYY-MM-DD 형식 문자열로 포맷
    function formatDateToYYYYMMDD(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // --- Core Logic: 계산 및 결과 표시 ---
    function calculateAndDisplayResult(selectedMMDD) {
        // MM/DD 형식의 선택된 날짜들을YYYY-MM-DD 형식으로 변환하여 사용
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

        // --- 특수 케이스 2: 기준 날짜(INPUT_DATE_STR)가 근무일로 선택된 경우 ---
        // (사용자가 Streamlit 날짜 선택기에서 고른 날짜가 달력에서 근무일로 체크된 경우)
        if (selectedFullDates.includes(INPUT_DATE_STR)) {
            // 기준 날짜가 근무일이므로 조건 1, 2 모두 불충족으로 간주 (사용자 요청)
            const nextPossibleApplicationDate = new Date(INPUT_DATE_STR);
            nextPossibleApplicationDate.setDate(nextPossibleApplicationDate.getDate() + 14 + 1); // 기준 날짜 + 14일 무근무 후 +1일

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

        # 최종 HTML 구성 및 출력 (여기에 스타일 태그 없음)
        final_html_content = f"""
            <h3>📌 기준 날짜({INPUT_DATE_STR}) 기준 조건 판단</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실 없어야 함</p>
            <p>총 기간 일수: {currentTotalDaysForCond1}일</p>
            <p>1/3 기준: {currentThresholdForCond1:.1f}일</p>
            <p>근무일 수: {actualWorkedDaysForCond1}일</p>
            <p>{condition1Text}</p>
            <p>{condition2Text}</p>
            {f"<p>{nextPossible1Message}</p>" if nextPossible1Message else ""}
            {f"<p>{nextPossible2Message}</p>" if nextPossible2Message else ""}
            <h3>📌 기준 날짜({INPUT_DATE_STR}) 기준 최종 판단</h3>
            <p>✅ 일반일용근로자: {'✅ 신청 가능' if condition1Met else '❌ 신청 불가능'}</p>
            <p>✅ 건설일용근로자: {'✅ 신청 가능' if (condition1Met or noWork14Days) else '❌ 신청 불가능'}</p>
            <p>※ 위의 '신청 가능일'은 이후 근로제공이 전혀 없다는 전제 하에 계산된 것이며, 실제 고용센터 판단과는 다를 수 있습니다.</p>
        """

        document.getElementById('resultContainer').innerHTML = final_html_content;
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


    // DOMContentLoaded 이벤트 리스너: HTML 문서가 완전히 로드되고 파싱된 후 스크립트 실행
    document.addEventListener('DOMContentLoaded', function() {
        loadSelectedDates();
    });
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)

# Streamlit 앱 실행
if __name__ == "__main__":
    daily_worker_eligibility_app()
