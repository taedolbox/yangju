import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown(
        "<h3>🏗️ 일용직 신청 가능 시점 판단</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:16px;'>ⓘ 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    # 기준 날짜 입력
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 달력에 표시할 날짜 계산
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    cal_dates = []
    current = first_day_prev_month
    while current <= last_day:
        cal_dates.append(current)
        current += timedelta(days=1)

    # JSON 데이터 생성
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    fourteen_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # HTML + CSS + JS 조합
    calendar_html = """
    <style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 420px;
        margin-bottom: 20px;
    }
    .day-header, .day {
        aspect-ratio: 1/1;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
        user-select: none;
    }
    .day-header {
        background: #e0e0e0;
        font-weight: bold;
    }
    .day-header.sunday, .day.sunday { color: red; }
    .day-header.saturday, .day.saturday { color: blue; }
    .day {
        cursor: pointer;
        transition: background 0.1s ease;
    }
    .day:hover { background: #f0f0f0; }
    .day.selected {
        background: #2196F3;
        color: #fff;
    }
    .empty-day {
        background: transparent;
        border: none;
    }
    #resultContainer {
        background: #fff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-width: 420px;
        font-size: 15px;
        line-height: 1.6;
    }
    #resultContainer h4 {
        margin-bottom: 10px;
    }
    </style>
    <div class="calendar">
    """

    # 요일 헤더
    weekdays = [("일", "sunday"), ("월", ""), ("화", ""), ("수", ""), ("목", ""), ("금", ""), ("토", "saturday")]
    for name, cls in weekdays:
        calendar_html += f'<div class="day-header {cls}">{name}</div>'

    # 빈칸 채우기
    offset = (cal_dates[0].weekday() + 1) % 7
    for _ in range(offset):
        calendar_html += '<div class="empty-day"></div>'

    # 날짜 셀
    for d in cal_dates:
        wd = (d.weekday() + 1) % 7
        cls = "sunday" if wd == 0 else "saturday" if wd == 6 else ""
        calendar_html += (
            f'<div class="day {cls}" data-date="{d.strftime("%Y-%m-%d")}" '
            f'onclick="toggleDate(this)">{d.day}</div>'
        )
    calendar_html += "</div>"

    # 결과 표시 영역
    calendar_html += """
    <div id="resultContainer">
      <h4>조건 및 최종 판단</h4>
      <div id="resultDetails">날짜를 선택하세요.</div>
    </div>
    """

    # JavaScript: 선택 토글 & 조건 계산
    calendar_html += (
        "<script>\n"
        f"const CALENDAR = {calendar_dates_json};\n"
        f"const START14 = '{fourteen_start}';\n"
        f"const END14 = '{fourteen_end}';\n"
        f"const NEXT1 = '{next1_date}';\n"

        "function toggleDate(el) {\n"
        "  el.classList.toggle('selected');\n"
        "  const selected = Array.from(document.querySelectorAll('.day.selected'))\n"
        "    .map(e => e.dataset.date);\n"
        "  const total = CALENDAR.length;\n"
        "  const thr = total / 3;\n"
        "  const worked = selected.length;\n"
        "  const last14 = CALENDAR.filter(d => d >= START14 && d <= END14);\n"
        "  const no14 = last14.every(d => !selected.includes(d));\n"

        "  const condition1Text = worked < thr\n"
        "    ? '✅ 조건1 충족: ' + worked + '/' + thr.toFixed(1)\n"
        "    : '❌ 조건1 불충족: ' + worked + '/' + thr.toFixed(1);\n"

        "  const condition2Text = no14\n"
        "    ? '✅ 조건2 충족'\n"
        "    : '❌ 조건2 불충족';\n"

        "  let nextPossible1 = '';\n"
        "  if (worked >= thr) nextPossible1 = '📅 조건1 위해 ' + NEXT1 + ' 이후 신청';\n"

        "  let nextPossible2 = '';\n"
        "  if (!no14) {\n"
        "    const nd = new Date(END14);\n"
        "    nd.setDate(nd.getDate() + 14);\n"
        "    nextPossible2 = '📅 조건2 위해 ' + nd.toISOString().slice(0,10) + ' 이후 신청';\n"
        "  }\n"

        "  const generalOk = worked < thr ? '✅ 일반일용 신청 가능' : '❌ 일반일용 불가';\n"
        "  const constructionOk = (worked < thr || no14)\n"
        "    ? '✅ 건설일용 신청 가능' : '❌ 건설일용 불가';\n"

        "  let html = '';\n"
        "  html += '<p>' + condition1Text + '</p>';\n"
        "  html += '<p>' + condition2Text + '</p>';\n"
        "  if (nextPossible1) html += '<p>' + nextPossible1 + '</p>';\n"
        "  if (nextPossible2) html += '<p>' + nextPossible2 + '</p>';\n"
        "  html += '<h5>최종 판단</h5>';\n"
        "  html += '<p>' + generalOk + '</p>';\n"
        "  html += '<p>' + constructionOk + '</p>';\n"

        "  document.getElementById('resultDetails').innerHTML = html;\n"
        "}\n"

        "window.onload = () => {\n"
        "  const saved = localStorage.getItem('selectedDates');\n"
        "  const sel = saved ? JSON.parse(saved) : [];\n"
        "  sel.forEach(d => {\n"
        "    const el = document.querySelector(`.day[data-date='${d}']`);\n"
        "    if (el) el.classList.add('selected');\n"
        "  });\n"
        "  toggleDate({ classList: { toggle: () => {} } }); // initial calc\n"
        "};\n"
        "</script>"
    )

    st.components.v1.html(calendar_html, height=900, scrolling=False)
