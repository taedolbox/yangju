import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(layout="centered")

st.title("직관적인 달력 선택기")

# 1️⃣ 기준 날짜 입력
today = datetime.today()
base_date = st.date_input("📅 기준 날짜 선택", today)

# 2️⃣ 달력 범위 계산
first_day_prev_month = (base_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = base_date

dates = []
cur = first_day_prev_month
while cur <= last_day:
    dates.append(cur)
    cur += timedelta(days=1)

# 3️⃣ 달력 HTML + JS
days_of_week = ["일", "월", "화", "수", "목", "금", "토"]

calendar_html = """
<style>
.calendar { display: grid; grid-template-columns: repeat(7, 40px); gap: 5px; }
.day-header { font-weight: bold; text-align: center; background: #ddd; border-radius: 5px; height: 40px; line-height: 40px; }
.day { text-align: center; border: 1px solid #999; border-radius: 5px; height: 40px; line-height: 40px; cursor: pointer; }
.day.selected { background: #2c91f7; color: white; font-weight: bold; }
</style>

<div class="calendar">
"""

for day in days_of_week:
    calendar_html += f'<div class="day-header">{day}</div>'

# 빈 칸
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    calendar_html += '<div></div>'

for d in dates:
    date_str = d.strftime("%Y-%m-%d")
    calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{d.day}</div>'

calendar_html += "</div>"

calendar_html += """
<br>
<button onclick="copyDates()">📋 선택된 날짜 복사</button>
<pre id="resultArea">[]</pre>

<script>
let selected = [];

function toggleDate(el) {
  const date = el.getAttribute("data-date");
  if (selected.includes(date)) {
    selected = selected.filter(d => d !== date);
    el.classList.remove("selected");
  } else {
    selected.push(date);
    el.classList.add("selected");
  }
  document.getElementById("resultArea").textContent = JSON.stringify(selected, null, 2);
}

function copyDates() {
  const text = document.getElementById("resultArea").textContent;
  navigator.clipboard.writeText(text).then(() => {
    alert("복사되었습니다! 붙여넣기 해주세요!");
  });
}
</script>
"""

st.components.v1.html(calendar_html, height=600, scrolling=False)

# 4️⃣ 선택된 JSON 붙여넣기
st.subheader("✅ 선택된 날짜 JSON 붙여넣기")
selected_json = st.text_area("📋 복사한 JSON을 여기에 붙여넣기", height=100)

if selected_json:
    try:
        selected_list = json.loads(selected_json)
        st.write("🔎 선택된 날짜:", selected_list)
        st.write("✅ 선택된 날짜 수:", len(selected_list))

        # 조건 계산
        total_days = len(dates)
        threshold = total_days / 3
        worked_days = len(selected_list)
        st.write(f"총 기간 일수: {total_days}일, 기준: {threshold:.1f}일, 선택 근무일 수: {worked_days}일")

        if worked_days < threshold:
            st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
        else:
            st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")

    except Exception as e:
        st.error(f"❌ JSON 파싱 오류: {e}")

