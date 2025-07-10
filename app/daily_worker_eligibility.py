import streamlit as st
from datetime import datetime, timedelta
import json

# ✅ core daily_worker_eligibility_app()
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
    <div style="text-align: right; margin-bottom: 15px;">
        <button onclick="clearCalendar()">🔄 달력 초기화</button>
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

    <!-- 숨겨진 확인서 템플릿 -->
    <div id="hiddenReport" style="display:none;">
      <h2 style="text-align:center;">확 인 서</h2>
      <div id="reportBody"></div>
    </div>

    <div style="margin-top:20px; text-align:right;">
      <button onclick="savePDF()">📄 PDF 저장</button>
      <button onclick="window.print()">🖨️ 프린트</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    """

    calendar_html += """
    <script>
    const CALENDAR_DATES_RAW = """ + calendar_dates_json + """;
    const CALENDAR_DATES = CALENDAR_DATES_RAW.map(dateStr => new Date(dateStr));
    const FOURTEEN_DAYS_START_STR = '""" + fourteen_days_prior_start + """';
    const FOURTEEN_DAYS_END_STR = '""" + fourteen_days_prior_end + """';
    const INPUT_DATE_STR = '""" + input_date_str + """';

    function savePDF() {
      html2pdf().from(document.getElementById('hiddenReport')).save(`확인서_${INPUT_DATE_STR}.pdf`);
    }

    function toggleDate(el) {
      el.classList.toggle('selected');
      const selected = [];
      document.querySelectorAll('.day.selected').forEach(d => selected.push(d.getAttribute('data-date')));
      calculateAndDisplayResult(selected);
    }

    function calculateAndDisplayResult(selected) {
      document.getElementById('reportBody').innerHTML = `<p>기준일: ${INPUT_DATE_STR}</p><p>선택된 날짜: ${selected.join(', ')}</p>`;
      document.getElementById('resultContainer').innerHTML = `<p>계산 결과 표시</p>`;
    }

    function clearCalendar() {
      document.querySelectorAll('.day').forEach(d => d.classList.remove('selected'));
      calculateAndDisplayResult([]);
    }

    </script>
    """

    st.components.v1.html(calendar_html, height=1500, scrolling=False)


