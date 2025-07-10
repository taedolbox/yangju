import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

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

    calendar_html = "<div id='calendar-container'>"

    calendar_html += """
    <div style="text-align:right; margin-bottom:10px;">
        <button onclick="clearCalendar()" style="
            background:#3F51B5; color:white; padding:8px 16px; border:none;
            border-radius:5px; cursor:pointer;">🔄 달력 초기화</button>
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

    <!-- ✅ 숨겨진 확인서 -->
    <div id="hiddenReport" style="display:none;">
      <h2 style="text-align:center;">확 인 서</h2>
      <div id="reportBody"></div>
    </div>

    <!-- ✅ PDF/프린트 버튼 -->
    <div style="margin-top:20px;">
      <button onclick="savePDF()">📄 확인서 PDF 저장</button>
      <button onclick="window.print()">🖨️ 프린트</button>
    </div>

    <style>
    .calendar {
        display:grid; grid-template-columns:repeat(7,44px); grid-gap:5px; margin-bottom:20px;
    }
    .day-header, .empty-day, .day {
        width:44px; height:44px; line-height:44px; text-align:center; font-weight:bold; border-radius:5px;
    }
    .day { border:1px solid #ddd; cursor:pointer; user-select:none; font-size:18px; }
    .day:hover { background:#eee; }
    .day.selected { background:#2196F3; color:#fff; }
    .day-header { background:#e0e0e0; }
    .sunday { color:red; } .saturday { color:blue; }
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
        let count = 0, current = new Date(start);
        while (current <= end) { count++; current.setDate(current.getDate()+1); }
        return count;
    }
    function getFirstDayOfPrevMonth(date) {
        const d = new Date(date); d.setDate(1); d.setMonth(d.getMonth()-1); return d;
    }
    function formatDateToYYYYMMDD(date) {
        const y = date.getFullYear(), m = ('0'+(date.getMonth()+1)).slice(-2), d = ('0'+date.getDate()).slice(-2);
        return `${y}-${m}-${d}`;
    }
    function toggleDate(el) {
        el.classList.toggle('selected');
        const days = document.getElementsByClassName('day');
        const selected = [];
        for (let i=0;i<days.length;i++) if (days[i].classList.contains('selected')) selected.push(days[i].getAttribute('data-date'));
        localStorage.setItem('selectedDates', JSON.stringify(selected));
        calculateAndDisplayResult(selected);
    }
    function loadSelectedDates() {
        const stored = JSON.parse(localStorage.getItem('selectedDates'))||[];
        stored.forEach(mmdd => {
            const el = document.querySelector(`.day[data-date="${mmdd}"]`);
            if(el) el.classList.add('selected');
        });
        calculateAndDisplayResult(stored);
    }
    window.clearCalendar = function() {
        const days = document.getElementsByClassName('day');
        for (let i=0;i<days.length;i++) days[i].classList.remove('selected');
        localStorage.removeItem('selectedDates');
        calculateAndDisplayResult([]);
    };

    function makeWorkTable(selectedFullDates) {
        let html = '<table border="1" cellspacing="0" cellpadding="5"><tr>';
        for (let i=1; i<=31; i++) html += `<th>${i}</th>`;
        html += '</tr><tr>';
        for (let i=1; i<=31; i++) {
            const found = selectedFullDates.some(d => parseInt(d.split('-')[2])===i);
            html += `<td style="text-align:center;">${found?'○':''}</td>`;
        }
        html += '</tr></table>';
        return html;
    }

    function calculateAndDisplayResult(selectedMMDD) {
        const selectedFullDates = selectedMMDD.map(mmdd => {
            const f = CALENDAR_DATES_RAW.find(d => d.endsWith(mmdd.replace('/','-')));
            return f||'';
        }).filter(Boolean);

        let latestWorkedDay = null;
        if(selectedFullDates.length>0) {
            latestWorkedDay = selectedFullDates.reduce((maxDate, c) => new Date(c)>maxDate?new Date(c):maxDate, new Date(selectedFullDates[0]));
        }

        const inputDate = new Date(INPUT_DATE_STR);
        const currentPeriodStart = getFirstDayOfPrevMonth(inputDate);
        const totalDays = getDaysBetween(currentPeriodStart, inputDate);
        const threshold = totalDays/3;
        const workedDays = selectedFullDates.filter(dateStr => {
            const d = new Date(dateStr);
            return d>=currentPeriodStart && d<=inputDate;
        }).length;

        const cond1 = workedDays<threshold;
        const cond1Text = cond1 ? `✅ 조건1 충족 (${workedDays}일 < ${threshold.toFixed(1)})` : `❌ 조건1 불충족 (${workedDays}일 ≥ ${threshold.toFixed(1)})`;

        const range14 = [];
        let temp = new Date(FOURTEEN_DAYS_START_STR);
        while(temp<=new Date(FOURTEEN_DAYS_END_STR)) {
            range14.push(formatDateToYYYYMMDD(temp));
            temp.setDate(temp.getDate()+1);
        }
        const cond2 = range14.every(d => !selectedFullDates.includes(d));
        const cond2Text = cond2 ? `✅ 조건2 충족 (14일 무근무)` : `❌ 조건2 불충족 (14일 내 근무)`;

        const html = `<h3>판단</h3><p>${cond1Text}</p><p>${cond2Text}</p>`;
        document.getElementById('resultContainer').innerHTML = html;

        document.getElementById('reportBody').innerHTML = `
          <p>본인은 ${INPUT_DATE_STR} 기준 수급자격 확인을 위해 방문하였으며,</p>
          <p>${cond1Text}</p>
          <p>${cond2Text}</p>
          <h4>근무일 달력</h4>
          ${makeWorkTable(selectedFullDates)}
          <p style="margin-top:30px;">20__. __월 __일</p>
          <p>성명: _____________ (인)</p>
        `;
    }

    function savePDF() {
        html2pdf().from(document.getElementById('hiddenReport')).save(`확인서_${INPUT_DATE_STR}.pdf`);
    }

    document.addEventListener('DOMContentLoaded', loadSelectedDates);
    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)


