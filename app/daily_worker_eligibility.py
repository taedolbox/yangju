import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    # ✅ 오늘 날짜 (KST)
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # ✅ 달력 범위 계산
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    cal_dates = []
    current_date_for_cal = first_day_prev_month
    while current_date_for_cal <= input_date:
        cal_dates.append(current_date_for_cal)
        current_date_for_cal += timedelta(days=1)

    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        calendar_groups.setdefault(ym, []).append(date)

    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    input_date_str = input_date.strftime("%Y-%m-%d")

    # ✅ 기존 달력 + 조건 판단 HTML
    calendar_html = "<div id='calendar-container'>"

    calendar_html += """
    <div style="text-align: right; margin-bottom: 15px;">
        <button onclick="clearCalendar()" style="
            background-color: #3F51B5; color: white; padding: 10px 20px;
            border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">
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

    calendar_html += """
    </div>
    <div id="resultContainer"></div>

    <!-- ✅ 확인서 출력 DIV -->
    <div id="reportContainer" style="margin-top:50px; padding:30px; border:1px solid #ccc;">
      <h2 style="text-align:center;">확 인 서</h2>
      <p>본인은 20__. __월 __일 ○○고용센터에 방문하여 실업급여 수급자격 인정신청을 하였는바,</p>
      <p id="reportContent1"></p>
      <p id="reportContent2"></p>
      <div id="workTableContainer"></div>
      <p style="margin-top:30px;">20__. __월 __일</p>
      <p>성명: _____________ (인)</p>
    </div>

    <!-- ✅ PDF/프린트 버튼 -->
    <div style="margin-top:20px;">
      <button onclick="saveReportPDF()" style="margin-right:10px;">📄 확인서 PDF 저장</button>
      <button onclick="printReport()">🖨️ 프린트</button>
    </div>

    <style>
    .calendar {
        display: grid; grid-template-columns: repeat(7, 44px);
        grid-gap: 5px; margin-bottom: 20px; background: #fff;
        padding: 10px 1px; border-radius: 8px;
    }
    .day-header, .empty-day { width:44px; height:44px; line-height:45px; text-align:center; font-weight:bold; }
    .day { width:44px; height:44px; line-height:45px; text-align:center; border:1px solid #ddd; border-radius:5px; cursor:pointer; }
    .day:hover { background: #f0f0f0; }
    .day.selected { border: 2px solid #2196F3; background: #2196F3; color: #fff; font-weight:bold; }
    </style>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

    <script>
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """;
    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """'; 
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';    
    const INPUT_DATE_STR = '""" + input_date_str + """';          

    function getDaysBetween(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        if (start > end) return 0;
        let count = 0, current = new Date(start);
        while (current <= end) {
            count++;
            current.setDate(current.getDate() + 1);
        }
        return count;
    }

    function calculateAndDisplayResult(selectedMMDD) {
        const workedDays = selectedMMDD.length;
        let html = `<p>선택된 근무일 수: ${workedDays}일</p>`;
        document.getElementById('resultContainer').innerHTML = html;

        updateReport(selectedMMDD);
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
        const storedDates = JSON.parse(localStorage.getItem('selectedDates')) || [];
        storedDates.forEach(mmdd => {
            const dayElement = document.querySelector(`.day[data-date="${mmdd}"]`);
            if (dayElement) { dayElement.classList.add('selected'); }
        });
        calculateAndDisplayResult(storedDates);
    }

    function saveToLocalStorage(data) {
        localStorage.setItem('selectedDates', JSON.stringify(data));
    }

    window.clearCalendar = function() {
        const days = document.getElementsByClassName('day');
        for (let i = 0; i < days.length; i++) {
            days[i].classList.remove('selected');
        }
        saveToLocalStorage([]);
        calculateAndDisplayResult([]);
    };

    function updateReport(selectedMMDD) {
        document.getElementById('reportContent1').innerText = `1. 선택된 근무일 수는 총 ${selectedMMDD.length}일입니다.`;
        document.getElementById('reportContent2').innerText = `2. 수급자격 조건에 따라 신청여부를 판단합니다.`;

        let tableHtml = '<table border="1" cellspacing="0" cellpadding="5"><thead><tr><th>일자</th>';
        for (let d = 1; d <= 31; d++) {
            tableHtml += `<th>${d}</th>`;
        }
        tableHtml += '</tr></thead><tbody><tr><td>근무</td>';
        for (let d = 1; d <= 31; d++) {
            const mark = selectedMMDD.some(date => date.endsWith(`/${String(d).padStart(2,'0')}`)) ? '○' : '';
            tableHtml += `<td style="text-align:center;">${mark}</td>`;
        }
        tableHtml += '</tr></tbody></table>';
        document.getElementById('workTableContainer').innerHTML = tableHtml;
    }

    function saveReportPDF() {
        const el = document.getElementById('reportContainer');
        html2pdf().from(el).save('확인서.pdf');
    }

    function printReport() {
        window.print();
    }

    document.addEventListener('DOMContentLoaded', function() { loadSelectedDates(); });
    </script>
    """

    st.components.v1.html(calendar_html, height=1800, scrolling=False)

