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

    # 표시할 기간: 전월1일 ~ 기준일
    first_prev = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    # 날짜 리스트
    dates = []
    d = first_prev
    while d <= last_day:
        dates.append(d)
        d += timedelta(days=1)

    # 월별 그룹핑
    groups = {}
    for dt in dates:
        key = dt.strftime("%Y-%m")
        groups.setdefault(key, []).append(dt)

    # JS 에 쓰일 JSON
    json_dates = json.dumps([dt.strftime("%Y-%m-%d") for dt in dates])
    start14 = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    end14 = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next1 = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # HTML/CSS/JS 조합
    html = """
    <style>
      .month-container { margin-bottom: 2rem; }
      .calendar {
        display: grid; grid-template-columns: repeat(7,1fr);
        gap:5px; padding:10px; background:#fff;
        border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1);
        width:100%; max-width:420px;
      }
      .day-header, .day {
        aspect-ratio:1/1; display:flex; justify-content:center; align-items:center;
        border:1px solid #ddd; border-radius:5px; font-size:16px; user-select:none;
      }
      .day-header { background:#e0e0e0; font-weight:bold; }
      .day-header.sunday, .day.sunday { color:red; }
      .day-header.saturday, .day.saturday { color:blue; }
      .day { cursor:pointer; transition:background .1s; }
      .day:hover { background:#f0f0f0; }
      .day.selected { background:#2196F3; color:#fff; }
      .empty-day { background:transparent; border:none; }
      #resultContainer {
        background:#fff; padding:15px; border-radius:8px;
        box-shadow:0 2px 10px rgba(0,0,0,0.1);
        max-width:420px; font-size:15px; line-height:1.5;
      }
      #resultContainer h4 { margin:12px 0 6px; }
    </style>
    """

    # 달력 월별 출력
    for ym, lst in groups.items():
        y, m = ym.split("-")
        html += f"<div class='month-container'><h4>{y}년 {int(m)}월</h4><div class='calendar'>"
        # 요일 헤더
        for wd, cls in [("일","sunday"),("월",""),("화",""),("수",""),("목",""),("금",""),("토","saturday")]:
            html += f"<div class='day-header {cls}'>{wd}</div>"
        # 빈칸
        offset = (lst[0].weekday()+1)%7
        html += "<div class='empty-day'></div>" * offset
        # 날짜
        for dt in lst:
            wd = (dt.weekday()+1)%7
            cls = "sunday" if wd==0 else "saturday" if wd==6 else ""
            html += (
                f"<div class='day {cls}' data-date='{dt.strftime('%Y-%m-%d')}' "
                "onclick='toggleDate(this)'>" + str(dt.day) + "</div>"
            )
        html += "</div></div>"

    # 결과 영역
    html += """
    <div id='resultContainer'>
      <h4>📌 조건 기준</h4>
      <div id='criteria'></div>
      <h4>📌 조건 판단</h4>
      <div id='judgment'></div>
      <h4>📌 최종 판단</h4>
      <div id='final'></div>
    </div>
    """

    # JavaScript
    html += (
        "<script>\n"
        f"const CALENDAR={json_dates};\n"
        f"const START14='{start14}'; const END14='{end14}'; const NEXT1='{next1}';\n"
        "function toggleDate(el){\n"
        "  el.classList.toggle('selected');\n"
        "  const sel=Array.from(document.querySelectorAll('.day.selected')).map(e=>e.dataset.date);\n"
        "  const total=CALENDAR.length, thr=total/3, worked=sel.length;\n"
        "  // 기준 표시\n"
        "  document.getElementById('criteria').innerHTML=\n"
        "    `<p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>`+\n"
        "    `<p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실이 없어야 함</p>`+\n"
        "    `<p>총 기간 일수: ${total}일</p>`+\n"
        "    `<p>1/3 기준: ${thr.toFixed(1)}일</p>`+\n"
        "    `<p>근무일 수: ${worked}일</p>`;\n"
        "  // 판단\n"
        "  const cond1=worked<thr?`✅ 조건 1 충족: 근무일 수(${worked}) < 기준(${thr.toFixed(1)})`:`❌ 조건 1 불충족: 근무일 수(${worked}) ≥ 기준(${thr.toFixed(1)})`;\n"
        "  const cond2=(()=>{let arr=CALENDAR.filter(d=>d>=START14&&d<=END14);return arr.every(d=>!sel.includes(d))?\n"
        "    `✅ 조건 2 충족: 신청일 직전 14일간(${START14} ~ ${END14}) 무근무`:\n"
        "    `❌ 조건 2 불충족: 신청일 직전 14일간(${START14} ~ ${END14}) 내 근무기록이 존재`;})();\n"
        "  document.getElementById('judgment').innerHTML=`<p>${cond1}</p><p>${cond2}</p>`;\n"
        "  // 최종\n"
        "  const gen=worked<thr?'✅ 일반일용근로자: ✅ 신청 가능':'✅ 일반일용근로자: ❌ 신청 불가능';\n"
        "  const con=(worked<thr||cond2.startsWith('✅'))?'✅ 건설일용근로자: ✅ 신청 가능':'✅ 건설일용근로자: ❌ 신청 불가능';\n"
        "  document.getElementById('final').innerHTML=`<p>${gen}</p><p>${con}</p>`;\n"
        "}\n"
        "window.onload=()=>{document.querySelectorAll('.day').forEach(el=>el.classList.remove('selected'));toggleDate({});};\n"
        "</script>"
    )

    st.components.v1.html(html, height=1000, scrolling=False)
