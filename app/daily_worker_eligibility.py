import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_app():
    st.markdown("<h3>🏗️ 일용직 신청 가능 시점 판단</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:16px;'>ⓘ 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    # 기준 날짜 입력
    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 전월 1일 ~ 기준일의 날짜 리스트
    first_prev = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date
    dates = []
    d = first_prev
    while d <= last_day:
        dates.append(d)
        d += timedelta(days=1)

    # 월별로 그룹핑
    groups = {}
    for dt in dates:
        ym = dt.strftime("%Y-%m")
        groups.setdefault(ym, []).append(dt)

    # JS 에 전달할 JSON
    cal_json = json.dumps([dt.strftime("%Y-%m-%d") for dt in dates])
    start14 = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    end14 = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next1 = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # CSS + 달력 HTML
    calendar_html = f"""
    <style>
      .month {{ margin-bottom:1.5rem; }}
      .calendar {{
        display:grid; grid-template-columns:repeat(7,1fr);
        gap:5px; padding:10px; background:#fff;
        border-radius:8px; box-sizing:border-box;
        width:100%; max-width:420px; overflow-x:hidden;
      }}
      .day-header, .day {{
        aspect-ratio:1/1; display:flex;
        justify-content:center; align-items:center;
        border:1px solid #ddd; border-radius:5px;
        user-select:none; font-size:16px;
      }}
      .day-header {{ background:#e0e0e0; font-weight:bold; }}
      .day-header.sunday, .day.sunday {{ color:red; }}
      .day-header.saturday, .day.saturday {{ color:blue; }}
      .day {{ cursor:pointer; transition:background .1s; }}
      .day:hover {{ background:#f0f0f0; }}
      .day.selected {{ background:#2196F3; color:#fff; }}
      .empty {{ border:none; background:transparent; }}
      @media (max-width:480px) {{
        .calendar {{ padding:5px; gap:3px; }}
      }}
      #result {{ background:#fff; padding:15px;
        border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1);
        max-width:420px; font-size:15px; line-height:1.5;
        margin-top:1rem;
      }}
    </style>
    """

    # 월별 달력 추가
    for ym, lst in groups.items():
        year, mon = ym.split("-")
        calendar_html += f"<div class='month'><h4>{year}년 {int(mon)}월</h4><div class='calendar'>"
        # 요일 헤더
        for wd, cls in [("일","sunday"),("월",""),("화",""),("수",""),("목",""),("금",""),("토","saturday")]:
            calendar_html += f"<div class='day-header {cls}'>{wd}</div>"
        # 빈칸
        offset = (lst[0].weekday()+1) % 7
        calendar_html += "".join(["<div class='empty'></div>" for _ in range(offset)])
        # 날짜
        for dt in lst:
            wd = (dt.weekday()+1) % 7
            cls = "sunday" if wd==0 else "saturday" if wd==6 else ""
            calendar_html += (
                f"<div class='day {cls}' data-date='{dt.strftime('%Y-%m-%d')}' onclick='toggleDate(this)'>"
                f"{dt.day}</div>"
            )
        calendar_html += "</div></div>"

    # 결과 컨테이너
    calendar_html += "<div id='result'>날짜를 선택하세요.</div>"

    # JS: calculateAndDisplayResult 함수 그대로 사용
    calendar_html += f"""
    <script>
      const CALENDAR_DATES = {cal_json};
      const FOURTEEN_DAYS_START = '{start14}';
      const FOURTEEN_DAYS_END = '{end14}';
      const NEXT_POSSIBLE1_DATE = '{next1}';

      function calculateAndDisplayResult(selected) {{
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        const fourteenDays = CALENDAR_DATES.filter(d=> d>= FOURTEEN_DAYS_START && d<= FOURTEEN_DAYS_END);
        const noWork14Days = fourteenDays.every(d=> !selected.includes(d));

        let nextPossible1 = "";
        if (workedDays >= threshold) {{
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " 
                           + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }}

        let nextPossible2 = "";
        if (!noWork14Days) {{
            const nd = new Date(FOURTEEN_DAYS_END);
            nd.setDate(nd.getDate()+14);
            const nxt = nd.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2를 충족하려면 오늘 이후에 근로제공이 없는 경우 "
                           + nxt + " 이후에 신청하면 조건 2를 충족할 수 있습니다.";
        }}

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START 
              + " ~ " + FOURTEEN_DAYS_END + ") 무근무"
            : "❌ 조건 2 불충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START 
              + " ~ " + FOURTEEN_DAYS_END + ") 내 근무기록이 존재";

        const generalWorkerText = workedDays < threshold ? "✅ 신청 가능" : "❌ 신청 불가능";
        const constructionWorkerText = (workedDays < threshold || noWork14Days) 
            ? "✅ 신청 가능" : "❌ 신청 불가능";

        const finalHtml = `
            <h3>📌 조건 기준</h3>
            <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
            <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실이 없어야 함</p>
            <p>총 기간 일수: ${totalDays}일</p>
            <p>1/3 기준: ${threshold.toFixed(1)}일</p>
            <p>근무일 수: ${workedDays}일</p>
            <h3>📌 조건 판단</h3>
            <p>${condition1Text}</p>
            <p>${condition2Text}</p>
            ${nextPossible1 ? `<p>${nextPossible1}</p>` : ""}
            ${nextPossible2 ? `<p>${nextPossible2}</p>` : ""}
            <h3>📌 최종 판단</h3>
            <p>✅ 일반일용근로자: ${generalWorkerText}</p>
            <p>✅ 건설일용근로자: ${constructionWorkerText}</p>
        `;
        document.getElementById('result').innerHTML = finalHtml;
      }}

      function toggleDate(el) {{
        el.classList.toggle('selected');
        const sel = Array.from(document.querySelectorAll('.day.selected'))
                          .map(e=> e.dataset.date);
        calculateAndDisplayResult(sel);
      }}

      // 초기 호출: 근무 기록 0 으로 표시
      window.onload = () => calculateAndDisplayResult([]);
    </script>
    """

    # 렌더링
    st.components.v1.html(calendar_html, height=900, scrolling=False)

