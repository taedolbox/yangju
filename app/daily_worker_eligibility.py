import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<h3>🏗️ 일용직 신청 가능 시점 판단</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='font-size:16px;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    cal_dates = []
    current_date = first_day_prev_month
    while current_date <= last_day:
        cal_dates.append(current_date)
        current_date += timedelta(days=1)

    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")

    html = f"""
    <style>
      .calendar {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        width: 100%;
        max-width: 100%;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
      }}
      .day-header {{
        aspect-ratio: 1/1;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        color: #333;
      }}
      .day-header.sunday {{ color: red; }}
      .day-header.saturday {{ color: blue; }}

      .day {{
        aspect-ratio: 1/1;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
        color: #333;
        cursor: pointer;
      }}
      .day.sunday {{ color: red; }}
      .day.saturday {{ color: blue; }}

      .day.selected {{
        background: #2196F3;
        color: #fff;
        font-weight: bold;
      }}

      .day.empty {{
        border: none;
        background: none;
      }}
    </style>

    <div class="calendar">
      <div class="day-header sunday">일</div>
      <div class="day-header">월</div>
      <div class="day-header">화</div>
      <div class="day-header">수</div>
      <div class="day-header">목</div>
      <div class="day-header">금</div>
      <div class="day-header saturday">토</div>
    """

    # 시작 요일 offset
    start_offset = (cal_dates[0].weekday() + 1) % 7
    for _ in range(start_offset):
        html += '<div class="day empty"></div>'

    for date in cal_dates:
        weekday = (date.weekday() + 1) % 7
        cls = ""
        if weekday == 0:
            cls = "sunday"
        elif weekday == 6:
            cls = "saturday"
        html += f'<div class="day {cls}" onclick="toggleDate(this)" data-date="{date.strftime("%Y-%m-%d")}">{date.day}</div>'

    html += f"""
    </div>

    <div id="resultContainer" style="margin-top:20px; padding:10px; border:1px solid #ddd; border-radius:5px;">
      <h4>📌 조건 기준</h4>
      <div id="resultDetails"></div>
      <h4>📌 최종 판단</h4>
      <div id="finalDecision"></div>
    </div>

    <script>
      const CALENDAR_DATES = {calendar_dates_json};
      const FOURTEEN_DAYS_START = '{fourteen_days_prior_start}';
      const FOURTEEN_DAYS_END = '{fourteen_days_prior_end}';
      const NEXT_POSSIBLE1_DATE = '{next_possible1_str}';

      function toggleDate(el) {{
        el.classList.toggle("selected");
        let selected = [];
        document.querySelectorAll(".day.selected").forEach(e => {{
          selected.push(e.getAttribute("data-date"));
        }});

        let totalDays = CALENDAR_DATES.length;
        let threshold = totalDays / 3;
        let workedDays = selected.length;

        let fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        let noWork14Days = fourteenDays.every(date => !selected.includes(date));

        let nextPossible1 = workedDays >= threshold ? `📅 조건1 충족 위해 ${NEXT_POSSIBLE1_DATE} 이후 신청` : "";
        let nextPossible2 = !noWork14Days ? `📅 조건2 충족 위해 ${FOURTEEN_DAYS_END} 이후 14일 무근무 필요` : "";

        let condition1 = workedDays < threshold ? "✅ 조건1 충족" : "❌ 조건1 불충족";
        let condition2 = noWork14Days ? "✅ 조건2 충족" : "❌ 조건2 불충족";

        let generalOk = workedDays < threshold ? "✅ 일반일용 신청 가능" : "❌ 일반일용 신청 불가";
        let constructionOk = (workedDays < threshold || noWork14Days) ? "✅ 건설일용 신청 가능" : "❌ 건설일용 신청 불가";

        let html = `
          <p>총 기간: ${totalDays}일, 1/3 기준: ${threshold.toFixed(1)}일, 선택: ${workedDays}일</p>
          <p>${condition1}</p>
          <p>${condition2}</p>
          ${nextPossible1 ? `<p>${nextPossible1}</p>` : ""}
          ${nextPossible2 ? `<p>${nextPossible2}</p>` : ""}
        `;
        document.getElementById("resultDetails").innerHTML = html;

        let final = `
          <p>${generalOk}</p>
          <p>${constructionOk}</p>
        `;
        document.getElementById("finalDecision").innerHTML = final;
      }}
    </script>
    """

    st.components.v1.html(html, height=1000, scrolling=False)
