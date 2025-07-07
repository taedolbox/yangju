import streamlit as st

def daily_worker_eligibility_app():
    st.title("📅 실업급여 일용근로자 자격 모의판단")
    st.caption("신청 가능 여부를 달력에서 직접 선택해 모의판단합니다.")

    # ✅ 사용자에게 달력 선택기 안내
    st.markdown("선택된 날짜를 바탕으로 조건을 계산합니다.")

    # ✅ JS 달력 + 조건 판단 출력
    html_code = """
    <style>
      .calendar { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
      .day { border: 1px solid #ddd; padding: 8px; text-align: center; cursor: pointer; }
      .selected { background: #007bff; color: white; }
      .sunday { color: red; }
      .saturday { color: blue; }
      h3 { margin-top: 1em; }
    </style>

    <div id="calendar"></div>
    <div id="resultContainer"></div>

    <script>
    const CALENDAR_DATES = [];
    const today = new Date();
    const start = new Date(today.getFullYear(), today.getMonth() -1, 1);
    const end = new Date(today);

    while (start <= end) {
      const y = start.getFullYear();
      const m = String(start.getMonth() + 1).padStart(2, '0');
      const d = String(start.getDate()).padStart(2, '0');
      CALENDAR_DATES.push(`${y}-${m}-${d}`);
      start.setDate(start.getDate() + 1);
    }

    const FOURTEEN_DAYS_END = CALENDAR_DATES[CALENDAR_DATES.length - 1];
    const fourteenStart = new Date(FOURTEEN_DAYS_END);
    fourteenStart.setDate(fourteenStart.getDate() - 14);
    const FOURTEEN_DAYS_START = fourteenStart.toISOString().split('T')[0];
    const NEXT_POSSIBLE1_DATE = new Date().toISOString().split('T')[0];

    const calendarDiv = document.getElementById('calendar');

    CALENDAR_DATES.forEach(date => {
      const div = document.createElement('div');
      div.className = 'day';
      const day = new Date(date).getDay();
      if (day === 0) div.classList.add('sunday');
      if (day === 6) div.classList.add('saturday');
      div.innerText = date.substring(8, 10);
      div.onclick = () => {
        div.classList.toggle('selected');
        calculateAndDisplayResult(
          Array.from(document.querySelectorAll('.selected')).map(d => d.innerText.padStart(2, '0'))
        );
      };
      calendarDiv.appendChild(div);
    });

    function calculateAndDisplayResult(selected) {
      const totalDays = CALENDAR_DATES.length;
      const threshold = totalDays / 3;
      const workedDays = selected.length;

      const fourteenDays = CALENDAR_DATES.filter(date => date >= FOURTEEN_DAYS_START && date <= FOURTEEN_DAYS_END);
      const noWork14Days = fourteenDays.every(date => !selected.includes(date.substring(8, 10)));

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

      const generalWorkerText = workedDays < threshold ? "✅ 신청 가능" : "❌ 신청 불가능";
      const constructionWorkerText = (workedDays < threshold || noWork14Days) ? "✅ 신청 가능" : "❌ 신청 불가능";

      const finalHtml = `
        <h3>📌 조건 기준</h3>
        <p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>
        <p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실이 없어야 함</p>
        <p>총 기간 일수: ` + totalDays + `일</p>
        <p>1/3 기준: ` + threshold.toFixed(1) + `일</p>
        <p>근무일 수: ` + workedDays + `일</p>
        <h3>📌 조건 판단</h3>
        <p>` + condition1Text + `</p>
        <p>` + condition2Text + `</p>
        ` + (nextPossible1 ? "<p>" + nextPossible1 + "</p>" : "") + `
        ` + (nextPossible2 ? "<p>" + nextPossible2 + "</p>" : "") + `
        <h3>📌 최종 판단</h3>
        <p>✅ 일반일용근로자: ` + generalWorkerText + `</p>
        <p>✅ 건설일용근로자: ` + constructionWorkerText + `</p>
      `;

      document.getElementById('resultContainer').innerHTML = finalHtml;
    }

    calculateAndDisplayResult([]);  // 페이지 로드시 기본 출력
    </script>
    """

    st.components.v1.html(html_code, height=800)
