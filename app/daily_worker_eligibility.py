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

    # 날짜 생성
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

    # JS 데이터
    json_dates = json.dumps([dt.strftime("%Y-%m-%d") for dt in dates])
    start14 = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    end14   = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    next1   = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # HTML/CSS
    html = """
    <style>
      .month-container { margin-bottom: 2rem; }
      .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        padding: 10px;
        background: #fff;
        border-radius: 8px;
        box-sizing: border-box;
        width: 100%; max-width: 420px;
        margin-bottom: 20px;
        overflow-x: hidden;
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
      @media (max-width: 480px) {
        .calendar { padding-left: 5px; padding-right: 5px; gap: 3px; }
      }
      #resultContainer { background: #fff; padding: 15px; border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 420px;
        font-size: 15px; line-height: 1.5; margin-bottom: 20px;
      }
    </style>
    """

    # 달력 출력
    for ym, lst in groups.items():
        y, m = ym.split("-")
        html += f"<div class='month-container'><h4>{y}년 {int(m)}월</h4><div class='calendar'>"
        for wd, cls in [("일","sunday"),("월",""),("화",""),("수",""),("목",""),("금",""),("토","saturday")]:
            html += f"<div class='day-header {cls}'>{wd}</div>"
        offset = (lst[0].weekday()+1)%7
        html += "".join(["<div class='empty-day'></div>" for _ in range(offset)])
        for dt in lst:
            wd = (dt.weekday()+1)%7
            cls = "sunday" if wd==0 else "saturday" if wd==6 else ""
            html += (
                f"<div class='day {cls}' data-date='{dt.strftime('%Y-%m-%d')}' onclick='toggleDate(this)'>" + str(dt.day) + "</div>"
            )
        html += "</div></div>"

    # 초기 안내
    html += "<div id='resultContainer'>날짜를 선택하세요.</div>"

    # JavaScript 삽입
    html += """
    <script>
    const CALENDAR_DATES = """ + json_dates + """;
    const FOURTEEN_DAYS_START = '""" + start14 + """';
    const FOURTEEN_DAYS_END = '""" + end14 + """';
    const NEXT_POSSIBLE1_DATE = '""" + next1 + """';

    function calculateAndDisplayResult(selected) {
        const totalDays = CALENDAR_DATES.length;
        const threshold = totalDays / 3;
        const workedDays = selected.length;

        const fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
        const noWork14Days = fourteenDays.every(date => !selected.includes(date));

        let nextPossible1 = "";
        if (workedDays >= threshold) {
            nextPossible1 = "📅 조건 1을 충족하려면 오늘 이후에 근로제공이 없는 경우 " + NEXT_POSSIBLE1_DATE + " 이후에 신청하면 조건 1을 충족할 수 있습니다.";
        }

        let nextPossible2 = "";
        if (!noWork14Days) {
            const nextPossibleDate = new Date(FOURTEEN_DAYS_END);
            nextPossibleDate.setDate(nextPossibleDate.getDate() + 14);
            const nextDateStr = nextPossibleDate.toISOString().split('T')[0];
            nextPossible2 = "📅 조건 2를 충족하려면 오늘 이후에 근로제공이 없는 경우 " + nextDateStr + " 이후에 신청하면 조건 2를 충족할 수 있습니다.";
        }

        const condition1Text = workedDays < threshold
            ? "✅ 조건 1 충족: 근무일 수(" + workedDays + ") < 기준(" + threshold.toFixed(1) + ")"
            : "❌ 조건 1 불충족: 근무일 수(" + workedDays + ") ≥ 기준(" + threshold.toFixed(1) + ")";

        const condition2Text = noWork14Days
            ? "✅ 조건 2 충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START + " ~ " + FOURTEEN_DAYS_END + ") 무근무"
            : "❌ 조건 2 불충족: 신청일 직전 14일간(" + FOURTEEN_DAYS_START + " ~ " + FOURTEEN_DAYS_END + ") 내 근무기록이 존재";

        const generalWorkerText = workedDays < threshold ? "✅ 일반일용근로자: ✅ 신청 가능" : "✅ 일반일용근로자: ❌ 신청 불가능";
        const constructionWorkerText = (workedDays < threshold || noWork14Days) ? "✅ 건설일용근로자: ✅ 신청 가능" : "✅ 건설일용근로자: ❌ 신청 불가능";

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
            <p>${generalWorkerText}</p>
            <p>${constructionWorkerText}</p>
        `;

        document.getElementById('resultContainer').innerHTML = finalHtml;
    }

    function toggleDate(el) {
        el.classList.toggle('selected');
        const selected = Array.from(document.querySelectorAll('.day.selected')).map(e => e.dataset.date);
        calculateAndDisplayResult(selected);
    }
    </script>
    """

    st.components.v1.html(html, height=1500, scrolling=False)
