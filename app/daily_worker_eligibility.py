import streamlit as st
from datetime import datetime, timedelta
import json
import base64

def daily_worker_eligibility_app():
    # Set today's date in KST
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # Initialize session state for selected dates
    if 'selected_dates' not in st.session_state:
        st.session_state.selected_dates = []

    # Set period for calendar display
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    cal_dates = []
    current_date_for_cal = first_day_prev_month
    while current_date_for_cal <= input_date:
        cal_dates.append(current_date_for_cal)
        current_date_for_cal += timedelta(days=1)

    # Group calendar by month
    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    # Date data for JavaScript
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])

    # 14 days prior date
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    input_date_str = input_date.strftime("%Y-%m-%d")

    # Streamlit HTML/JavaScript component insertion
    calendar_html = "<div id='calendar-container'>"

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
            extra_cls = "saturday" if wd == 5 else "sunday" if wd == 6 else ""
            day_num = date.day
            date_str = date.strftime("%m/%d")
            date_full_str = date.strftime("%Y-%m-%d")
            calendar_html += f'<div class="day {extra_cls}" data-date="{date_str}" data-full-date="{date_full_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>
    <style>
    .calendar { display: grid; grid-template-columns: repeat(7, 44px); grid-gap: 5px; margin-bottom: 20px; background: #fff; padding: 10px 1px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .day-header, .empty-day { width: 44px; height: 44px; line-height: 45px; text-align: center; font-weight: bold; color: #555; }
    .day-header.sunday { color: red; }
    .day-header.saturday { color: blue; }
    .day.sunday { color: red; }
    .day.saturday { color: blue; }
    .day-header { background: #e0e0e0; border-radius: 5px; font-size: 16px; }
    .empty-day { background: transparent; border: none; }
    .day { width: 44px; height: 44px; line-height: 45px; text-align: center; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; user-select: none; transition: background 0.1s ease, border 0.1s ease; font-size: 18px; color: #333; }
    .day:hover { background: #f0f0f0; }
    .day.selected { border: 2px solid #2196F3; background: #2196F3; color: #fff; font-weight: bold; }
    #resultContainer { color: #121212; background: #fff; padding: 15px 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); font-size: 15px; line-height: 1.6; }
    #resultContainer h3 { color: #0d47a1; margin-top: 20px; margin-bottom: 10px; }
    #resultContainer p { margin: 6px 0; }
    #calendar-container h4 { margin-bottom: 5px; }
    html[data-theme="dark"] #resultContainer { background: #262730; color: #FAFAFA; }
    html[data-theme="dark"] #resultContainer h3 { color: #90CAF9; }
    html[data-theme="dark"] h4 { color: #FFFFFF !important; }
    html[data-theme="dark"] .day { background-color: #31333F; color: #FAFAFA; border: 1px solid #4B4B4B; }
    html[data-theme="dark"] .day:hover { background-color: #45475A; }
    html[data-theme="dark"] .day.selected { background: #2196F3; color: #fff; }
    html[data-theme="dark"] .day-header { background: #31333F; color: #BBBBBB; }
    </style>
    <script>
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """;
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr));
    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';
    const INPUT_DATE_STR = '""" + input_date_str + """';

    function getDaysBetween(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (start > end) return 0;
        let count = 0;
        let current = new Date(start);
        current.setHours(0,0,0,0);
        end.setHours(0,0,0,0);
        while (current <= end) { count++; current.setDate(current.getDate() + 1); }
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
        const selectedFullDates = selectedMMDD.map(mmdd => CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/', '-'))) || '').filter(Boolean);
        let latestWorkedDay = selectedFullDates.length > 0 ? selectedFullDates.reduce((max, current) => new Date(current) > max ? new Date(current) : max, null) : null;
        const inputDate = new Date(INPUT_DATE_STR); inputDate.setHours(0,0,0,0);

        if (selectedFullDates.length === 0) {
            document.getElementById('resultContainer').innerHTML = `
                <h3>📌 조건 판단</h3><p>✅ 조건 1 충족: 근무일 0일</p><p>✅ 조건 2 충족: 근무일 0일</p>
                <h3>📌 최종 판단</h3><p>✅ 일반일용근로자: 신청 가능</p><p>✅ 건설일용근로자: 신청 가능</p>
                <h3>📌 종합 신청 가능일</h3><p>현재(${INPUT_DATE_STR}) 바로 신청 가능</p><p>※ 이후 근로제공이 없다는 전제입니다.</p>`;
            return;
        }

        if (selectedFullDates.includes(INPUT_DATE_STR)) {
            const nextDate = new Date(INPUT_DATE_STR); nextDate.setDate(nextDate.getDate() + 15);
            document.getElementById('resultContainer').innerHTML = `
                <h3 style="color: red;">📌 조건 판단</h3><p style="color: red;">❌ 조건 1 불충족: ${INPUT_DATE_STR} 근무</p><p style="color: red;">❌ 조건 2 불충족: ${INPUT_DATE_STR} 근무</p>
                <h3 style="color: red;">📌 최종 판단</h3><p style="color: red;">❌ 일반일용근로자: 신청 불가능</p><p style="color: red;">❌ 건설일용근로자: 신청 불가능</p>
                <h3>📌 종합 신청 가능일</h3><p style="color: red;">${formatDateToYYYYMMDD(nextDate)} 이후 신청 가능</p><p>※ 이후 근로제공이 없다는 전제입니다.</p>`;
            return;
        }

        const currentPeriodStart = getFirstDayOfPrevMonth(inputDate);
        const currentTotalDays = getDaysBetween(currentPeriodStart, inputDate);
        const currentThreshold = currentTotalDays / 3;
        const actualWorkedDays = selectedFullDates.filter(d => new Date(d) <= (latestWorkedDay || inputDate)).length;
        const condition1Met = actualWorkedDays < currentThreshold;
        const condition1Text = condition1Met ? `✅ 조건 1 충족: ${actualWorkedDays} < ${currentThreshold.toFixed(1)}` : `❌ 조건 1 불충족: ${actualWorkedDays} ≥ ${currentThreshold.toFixed(1)}`;

        const fourteenDaysRange = Array.from({length: 14}, (_, i) => formatDateToYYYYMMDD(new Date(inputDate - timedelta(days=14-i)))).reverse();
        const noWork14Days = fourteenDaysRange.every(d => !selectedFullDates.includes(d));
        const condition2Text = noWork14Days ? `✅ 조건 2 충족: ${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR} 무근무` : `❌ 조건 2 불충족: ${FOURTEEN_DAYS_START_STR} ~ ${FOURTEEN_DAYS_END_STR} 내 근무`;

        const generalWorkerEligible = condition1Met;
        const constructionWorkerEligible = condition1Met || noWork14Days;

        document.getElementById('resultContainer').innerHTML = `
            <h3>📌 기준 날짜(${INPUT_DATE_STR}) 기준 조건 판단</h3><p>조건 1: 근무일 수 < ${currentThreshold.toFixed(1)}일</p><p>조건 2: 신청일 직전 14일간 무근무</p>
            <p>근무일 수: ${actualWorkedDays}일</p><p>${condition1Text}</p><p>${condition2Text}</p>
            <h3>📌 최종 판단</h3><p>✅ 일반일용근로자: ${generalWorkerEligible ? '신청 가능' : '신청 불가능'}</p><p>✅ 건설일용근로자: ${constructionWorkerEligible ? '신청 가능' : '신청 불가능'}</p>
            <p>※ 이후 근로제공이 없다는 전제입니다.</p>`;
    }

    function toggleDate(element) {
        element.classList.toggle('selected');
        const selected = Array.from(document.getElementsByClassName('day')).filter(d => d.classList.contains('selected')).map(d => d.getAttribute('data-date'));
        // Send selected dates to Streamlit session state via a hidden input
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_dates';
        input.value = JSON.stringify(selected);
        document.body.appendChild(input);
        calculateAndDisplayResult(selected);
    }

    window.clearCalendar = function() {
        Array.from(document.getElementsByClassName('day')).forEach(d => d.classList.remove('selected'));
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_dates';
        input.value = JSON.stringify([]);
        document.body.appendChild(input);
        calculateAndDisplayResult([]);
    };

    document.addEventListener('DOMContentLoaded', function() {
        calculateAndDisplayResult([]); // Initial load with no selections
    });
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)

    # Handle selected dates from JavaScript
    if st.session_state.get('selected_dates'):
        st.session_state.selected_dates = json.loads(st.session_state.get('selected_dates', '[]'))

    # Generate and download report
    if st.button("보고서 생성 및 HTML 다운로드"):
        report_html = f"""
        <html><body>
        <h2 style="text-align: center;">휴업 사유서</h2>
        <p style="text-align: center;">본인은 {input_date.strftime('%Y년 %m월 %d일')} ○○고용센터에 방문하여 실업급여 수급자 인정신청을 하였습니다.</p>
        <h3>조건 판단</h3>
        <ol>
            <li>수급자 인정신청일이 속한 달의 직전 달 첫날부터 {input_date.strftime('%Y년 %m월 %d일')}까지 근무일 수 {len(st.session_state.selected_dates)}일로, 1/3 미만임을 확인합니다.</li>
            <li>(건설일용근로자로서) 신청일 직전 14일간 무근무 여부: {'' if all(d not in st.session_state.selected_dates for d in fourteenDaysRange) else '불'}충족</li>
        </ol>
        <h3>근무일 확인</h3>
        <table border="1">
            <tr><th>구분</th><th>달력으로 재공인 ○(사)</th><th colspan="6"></th><th>총일수</th></tr>
            <tr><td>월</td>{''.join(f'<td>{d.day}</td>' for d in cal_dates[:7])}</tr>
            <tr><td>일</td>{''.join(f'<td>{d.day}</td>' for d in cal_dates[:7])}</tr>
        </table>
        <p>※ 고용보험법 제40조에 따라 계산된 내용이며, 이후 근로제공이 없다는 전제 하에 작성되었습니다.</p>
        <p style="text-align: right;">작성일자: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')} KST<br>서명: (인)</p>
        </body></html>
        """
        b64 = base64.b64encode(report_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="report_{input_date.strftime("%Y%m%d")}.html">보고서 다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)
