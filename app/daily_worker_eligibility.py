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

    today = datetime.now()
    input_date = st.date_input("📅 기준 날짜 선택", today.date())

    first_day_prev = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    # 날짜 리스트
    dates = []
    cur = first_day_prev
    while cur <= last_day:
        dates.append(cur)
        cur += timedelta(days=1)

    # JSON 데이터
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in dates])
    fourteen_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    fourteen_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next_month_first = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # HTML + CSS + JS
    html = """
    <style>
    .calendar { display: grid; grid-template-columns: repeat(7, 1fr); gap:5px; padding:10px; background:#fff; border-radius:8px; width:100%; max-width:420px; box-sizing:border-box; }
    .day-header, .day { aspect-ratio:1/1; display:flex; justify-content:center; align-items:center; border:1px solid #ddd; border-radius:5px; font-size:16px; }
    .day-header { background:#e0e0e0; font-weight:bold; }
    .day-header.sunday, .day.sunday { color:red; }
    .day-header.saturday, .day.saturday { color:blue; }
    .day { cursor:pointer; transition:background .1s; }
    .day:hover { background:#f0f0f0; }
    .day.selected { background:#2196F3; color:#fff; }
    #resultContainer { margin-top:20px; padding:15px; background:#fff; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.1); max-width:420px; }
    </style>
    <div class='calendar'>
    """

    # 요일 헤더
    weekdays = [("일","sunday"),("월",""),("화",""),("수",""),("목",""),("금",""),("토","saturday")]
    for name, cls in weekdays:
        html += f"<div class='day-header {cls}'>{name}</div>"

    # 빈칸
    offset = (dates[0].weekday() + 1) % 7
    for _ in range(offset): html += "<div class='day empty'></div>"

    # 날짜
    for d in dates:
        cls = ''
        wd = (d.weekday() + 1) % 7
        if wd == 0: cls='sunday'
        if wd == 6: cls='saturday'
        html += f"<div class='day {cls}' data-date='{d.strftime('%Y-%m-%d')}' onclick='toggleDate(this)'>{d.day}</div>"

    html += "</div>"

    # 결과 영역 및 스크립트
    html += f"""
    <div id='resultContainer'><h4>조건 및 최종 판단</h4><div id='resultDetails'>날짜를 선택하세요.</div></div>
    <script>
      const CALENDAR = {calendar_dates_json};
      const START14 = '{fourteen_start}';
      const END14 = '{fourteen_end}';
      const NEXT1 = '{next_month_first}';
      function toggleDate(el) {{
        el.classList.toggle('selected');
        let selected = [...document.querySelectorAll('.day.selected')].map(e=>e.dataset.date);
        let total = CALENDAR.length;
        let thr = total/3;
        let worked = selected.length;
        let last14 = CALENDAR.filter(d=>d>=START14&&d<=END14);
        let no14 = last14.every(d=>!selected.includes(d));
        let c1 = worked<thr ? '✅ 조건1 충족':'❌ 조건1 불충족';
        let c2 = no14?'✅ 조건2 충족':'❌ 조건2 불충족';
        let n1= worked>=thr?`조건1 위해 ${NEXT1} 이후 신청`:'');
        let n2=!no14?`조건2 위해 ${END14} 이후 14일 무근무`:'');
        let g = worked<thr?'✅ 일반일용 신청':'❌ 일반일용 불가';
        let c = (worked<thr||no14)?'✅ 건설일용 신청':'❌ 건설일용 불가';
        document.getElementById('resultDetails').innerHTML =
          `<p>${c1} (${worked}/${thr.toFixed(1)})</p><p>${c2}</p><p>${n1}</p><p>${n2}</p><p>${g}</p><p>${c}</p>`;
      }}
    </script>
    """

    st.components.v1.html(html, height=800, scrolling=False)
