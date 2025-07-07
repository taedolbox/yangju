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

    # 기간: 전월 1일 ~ 기준일
    first_prev = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    # 날짜 리스트 생성
    dates = []
    d = first_prev
    while d <= last_day:
        dates.append(d)
        d += timedelta(days=1)

    # 월별 그룹핑
    groups = {}
    for dt in dates:
        ym = dt.strftime("%Y-%m")
        groups.setdefault(ym, []).append(dt)

    # 전달용 JSON
    cal_json = json.dumps([dt.strftime("%Y-%m-%d") for dt in dates])
    start14 = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    end14   = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next1   = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # CSS
    css = """
    <style>
      .calendar { display:grid; grid-template-columns:repeat(7,1fr); gap:5px;
                  padding:10px; background:#fff; border-radius:8px;
                  max-width:420px; overflow-x:hidden; }
      .day, .day-header { aspect-ratio:1/1; display:flex;
        justify-content:center; align-items:center; border:1px solid #ddd; }
      .day-header { background:#e0e0e0; font-weight:bold; }
      .day.sunday, .day-header.sunday { color:red; }
      .day.saturday, .day-header.saturday { color:blue; }
      .day { cursor:pointer; transition:background .1s; }
      .day:hover { background:#f0f0f0; }
      .day.selected { background:#2196F3; color:#fff; }
      .empty { background:transparent; border:none; }
      @media (max-width:480px) { .calendar { padding:5px; gap:3px; } }
      #result { margin-top:1rem; padding:15px; background:#fff;
                 border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1);
                 max-width:420px; font-size:15px; }
    </style>
    """

    # HTML 초기화
    html = css

    # 달력 렌더링
    for ym, lst in groups.items():
        year, mon = ym.split("-")
        html += f"<h4>{year}년 {int(mon)}월</h4><div class='calendar'>"
        # 요일 헤더
        for wd, cls in [("일","sunday"),("월",""),("화",""),("수",""),("목",""),("금",""),("토","saturday")]:
            html += f"<div class='day-header {cls}'>{wd}</div>"
        # 빈칸
        offset = (lst[0].weekday()+1) % 7
        html += "".join(["<div class='empty'></div>" for _ in range(offset)])
        # 날짜
        for dt in lst:
            wd = (dt.weekday()+1) % 7
            cls = "sunday" if wd == 0 else "saturday" if wd == 6 else ""
            html += (
                f"<div class='day {cls}' data-date='{dt.strftime('%Y-%m-%d')}' onclick='onClick(this)'>"
                + str(dt.day) + "</div>"
            )
        html += "</div>"

    # 결과 컨테이너
    html += "<div id='result'>날짜를 선택하세요.</div>"

    # JS 로직
    js = f"""
    <script>
      const CAL = {cal_json};
      const S14 = '{start14}'; const E14 = '{end14}'; const N1 = '{next1}';
      function onClick(el) {{
        el.classList.toggle('selected');
        const sel = Array.from(document.querySelectorAll('.day.selected')).map(e=>e.dataset.date);
        calc(sel);
      }}
      function calc(sel) {{
        const total = CAL.length;
        const thr = total/3;
        const wd = sel.length;
        const last14 = CAL.filter(d=>d>=S14 && d<=E14);
        const nw14 = last14.every(d=>!sel.includes(d));
        let np1 = "";
        if (wd >= thr) np1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + N1 + " 이후 신청";
        let np2 = "";
        if (!nw14) {{ const dt=new Date(E14); dt.setDate(dt.getDate()+14); const dstr=dt.toISOString().split('T')[0]; np2 = "📅 조건 2를 충족하려면 오늘 이후에 근로제공이 없는 경우 " + dstr + " 이후 신청"; }}
        const c1 = wd < thr ? "✅ 조건 1 충족: " + wd + "/" + thr.toFixed(1) : "❌ 조건 1 불충족: " + wd + "/" + thr.toFixed(1);
        const c2 = nw14 ? "✅ 조건 2 충족" : "❌ 조건 2 불충족";
        const g = wd < thr ? "✅ 일반 신청" : "❌ 일반 불가";
        const c = (wd < thr || nw14) ? "✅ 건설 신청" : "❌ 건설 불가";
        const html =
          '<h3>📌 조건 기준</h3>' +
          '<p>' + c1 + '</p>' + '<p>' + c2 + '</p>' +
          '<p>' + np1 + '</p>' + '<p>' + np2 + '</p>' +
          '<h3>📌 최종 판단</h3>' + '<p>' + g + '</p>' + '<p>' + c + '</p>';
        document.getElementById('result').innerHTML = html;
      }}
      window.onload = function() {{ calc([]); }};
    </script>
    """

    html += js

    st.components.v1.html(html, height=900, scrolling=False)

