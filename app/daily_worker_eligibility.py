import streamlit as st
from datetime import datetime, timedelta
import json
import os

def daily_worker_eligibility_app():
    # KST 오늘 날짜
    now_utc = datetime.utcnow()
    today_kst = now_utc + timedelta(hours=9)
    input_date = st.date_input("기준 날짜 선택", today_kst.date())

    st.warning("달력에서 근무한 날짜를 클릭하여 선택하세요. 파란색으로 표시됩니다. 다시 클릭하면 해제됩니다.")

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

    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, "report_template.html")

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            report_template_content = f.read()
    except FileNotFoundError:
        st.error(f"보고서 템플릿 파일이 없습니다: {template_path}")
        return

    # 안전 JSON 인코딩
    report_template_json = json.dumps(report_template_content).replace("</", "<\\/")

    calendar_html = """
    <div id="calendar-container">
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

    calendar_html += "</div>"

    calendar_html += f"""
    <style>
    .calendar {{
        display: grid; grid-template-columns: repeat(7, 44px); grid-gap: 5px;
    }}
    .day-header, .empty-day {{
        width: 44px; height: 44px; line-height: 45px; text-align: center;
    }}
    .day {{
        width: 44px; height: 44px; line-height: 45px; text-align: center;
        border: 1px solid #ddd; border-radius: 5px; cursor: pointer;
    }}
    .day.selected {{
        background: #2196F3; color: #fff; font-weight: bold;
    }}
    </style>

    <script>
    const CALENDAR_DATES = {calendar_dates_json};
    const FOURTEEN_DAYS_START = '{fourteen_days_prior_start}';
    const FOURTEEN_DAYS_END = '{fourteen_days_prior_end}';
    const INPUT_DATE = '{input_date_str}';
    const REPORT_TEMPLATE = JSON.parse(`{report_template_json}`);

    function toggleDate(el) {{
        el.classList.toggle('selected');
    }}

    function clearCalendar() {{
        const days = document.getElementsByClassName('day');
        for (let d of days) d.classList.remove('selected');
    }}

    function generateReport() {{
        // 예시: 보고서 생성
        const printWindow = window.open('', '_blank');
        printWindow.document.write(REPORT_TEMPLATE);
        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
    }}

    // 모든 주석은 // 사용
    </script>
    """

    st.components.v1.html(calendar_html, height=700, scrolling=True)

    st.button("초기화", on_click=None)  # 실제 초기화는 JS에서 실행
    st.button("📄 확인서 출력", on_click=None)

    st.markdown("""
    <script>
    document.querySelector("button:nth-of-type(1)").onclick = clearCalendar;
    document.querySelector("button:nth-of-type(2)").onclick = generateReport;
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    daily_worker_eligibility_app()

