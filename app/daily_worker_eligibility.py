import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown("<h3>🏗️ 일용직 신청 가능 시점 판단</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:16px;'>ⓘ 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    # 기준 날짜
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 표시할 기간: 전월 1일 ~ 기준일
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    # 날짜 리스트 만들기
    cal_dates = []
    d = first_day_prev_month
    while d <= last_day:
        cal_dates.append(d)
        d += timedelta(days=1)

    # 월별 그룹핑
    calendar_groups = {}
    for date in cal_dates:
        key = date.strftime("%Y-%m")
        calendar_groups.setdefault(key, []).append(date)

    # JS로 사용할 JSON 데이터
    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    fourteen_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next1 = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # HTML/CSS/JS 코드 조립
    html = """
    <style>
    .month-container { margin-bottom: 2rem; }
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        width: 100%; max-width: 420px;
    }
    .day-header, .day {
        aspect-ratio: 1/1;
        display: flex; justify-content: center; align-items: center;
        border: 1px solid #ddd; border-radius: 5px; font-size: 16px;
        user-select: none;
    }
    .day-header { background: #e0e0e0; font-weight: bold; }
    .day-header.sunday, .day.sunday { color: red; }
    .day-header.saturday, .day.saturday { color: blue; }
    .day { cursor: pointer; transition: background .1s; }
    .day:hover { background: #f0f0f0; }
    .day.selected { background: #2196F3; color: #fff; }
    .empty-day { background: transparent; border: none; }
    #resultContainer {
        background: #fff; padding: 15px; border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 420px;
        font-size: 15px; line-height: 1.5;
    }
    #resultContainer h4 { margin-top: 0; }
    </style>
    """

    # 월별 달력 생성
    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        html += f"<div class='month-container'><h4>{year}년 {int(month)}월</h4><div class='calendar'>"

        # 요일 헤더
        days_of_week = [("일","sunday"),("월",""),("화",""),("수",""),("목",""),("금",""),("토","saturday")]
        for wd, cls in days_of_week:
            html += f"<div class='day-header {cls}'>{wd}</div>"

        # 빈칸
        start_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_offset):
            html += "<div class='empty-day'></div>"

        # 날짜 셀
        for d in dates:
            wd = (d.weekday() + 1) % 7
            cls = "sunday" if wd==0 else "saturday" if wd==6 else ""
            html += (
                f"<div class='day {cls}' data-date='{d.strftime('%Y-%m-%d')}' "
                "onclick='toggleDate(this)'>" + str(d.day) + "</div>"
            )

        html += "</div></div>"

    # 결과 컨테이너
    html += """
    <div id='resultContainer'>
      <h4>조건 및 최종 판단</h4>
      <div id='resultDetails'>날짜를 선택하세요.</div>
    </div>
    """

    # JavaScript
    html += (
        "<script>\n"
        f"const CALENDAR = {calendar_dates_json};\n"
        f"const START14 = '{fourteen_start}';\n"
        f"const END14 = '{fourteen_end}';\n"
        f"const NEXT1 = '{next1}';\n"
        "function toggleDate(el) {\n"
        "  el.classList.toggle('selected');\n"
        "  const sel = Array.from(document.querySelectorAll('.day.selected')).map(e=>e.dataset.date);\n"
        "  const total = CALENDAR.length;\n"
        "  const thr = total/3;\n"
        "  const worked = sel.length;\n"
        "  const last14 = CALENDAR.filter(d=>d>=START14&&d<=END14);\n"
        "  const no14 = last14.every(d=>!sel.includes(d));\n"
        "  const c1 = worked<thr?'✅ 조건1 충족':'❌ 조건1 불충족';\n"
        "  const c2 = no14?'✅ 조건2 충족':'❌ 조건2 불충족';\n"
        "  let n1=''; if(worked>=thr) n1='📅 조건1 위해 '+NEXT1+' 이후 신청';\n"
        "  let n2=''; if(!no14){let d=new Date(END14);d.setDate(d.getDate()+14);n2='📅 조건2 위해 '+d.toISOString().slice(0,10)+' 이후 신청';}\n"
        "  const g = worked<thr?'✅ 일반일용 신청 가능':'❌ 일반일용 불가';\n"
        "  const c = (worked<thr||no14)?'✅ 건설일용 신청 가능':'❌ 건설일용 불가';\n"
        "  let html='';\n"
        "  html+='<p>'+c1+' ('+worked+'/'+thr.toFixed(1)+')</p>';\n"
        "  html+='<p>'+c2+'</p>';\n"
        "  if(n1) html+='<p>'+n1+'</p>';\n"
        "  if(n2) html+='<p>'+n2+'</p>';\n"
        "  html+='<h5>최종 판단</h5>';\n"
        "  html+='<p>'+g+'</p>';\n"
        "  html+='<p>'+c+'</p>';\n"
        "  document.getElementById('resultDetails').innerHTML=html;\n"
        "}\n"
        "window.onload=function(){\n"
        "  const saved=localStorage.getItem('selectedDates');\n"
        "  const sel=saved?JSON.parse(saved):[];\n"
        "  sel.forEach(d=>{const e=document.querySelector(`.day[data-date='${d}']`);if(e) e.classList.add('selected');});\n"
        "  toggleDate({})\n"
        "};\n"
        "</script>"
    )

    st.components.v1.html(html, height=1000, scrolling=False)

