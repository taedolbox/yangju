import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(layout="centered")

# URL 파라미터에서 selectedDates 읽기
params = st.experimental_get_query_params()
selected_dates = []
if "selectedDates" in params:
    try:
        selected_dates = json.loads(params["selectedDates"][0])
    except:
        selected_dates = []

# 기준 날짜 선택
base_date = st.date_input("📅 기준 날짜 선택", datetime.today())

# 달력 범위 계산
first_day_prev_month = (base_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = base_date
cal_dates = []
cur = first_day_prev_month
while cur <= last_day:
    cal_dates.append(cur)
    cur += timedelta(days=1)

# 달력 렌더링
days_of_week = ["일", "월", "화", "수", "목", "금", "토"]
calendar_html = """
<style>
.calendar { display: grid; grid-template-columns: repeat(7, 40px); gap: 5px; margin-top:20px; }
.day-header { font-weight: bold; text-align:center; background:#ddd; border-radius:5px; height:40px; line-height:40px; }
.day { text-align:center; border:1px solid #999; border-radius:5px; height:40px; line-height:40px; cursor:pointer; user-select:none; }
.day.selected { background:#2c91f7; color:white; font-weight:bold; }
.empty { }
#info { margin-top:15px; font-weight:bold; }
</style>
<div class="calendar">
"""
for wd in days_of_week:
    calendar_html += f'<div class="day-header">{wd}</div>'

# 빈칸 채우기
offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(offset):
    calendar_html += '<div class="empty"></div>'

# 날짜칸
for d in cal_dates:
    ds = d.strftime("%Y-%m-%d")
    cls = "selected" if ds in selected_dates else ""
    calendar_html += f'<div class="day {cls}" data-date="{ds}" onclick="onClickDate(this)">{d.day}</div>'

calendar_html += "</div>"

# 결과 정보 표시
# Python에서 바로 렌더링
total = len(cal_dates)
threshold = total / 3
worked = len(selected_dates)
status1 = "✅ 근무일 수가 기준 미만" if worked < threshold else "❌ 근무일 수가 기준 이상"
calendar_html += f"""
<div id="info">
선택된 날짜 수: {worked} &nbsp;&nbsp; (총 {total}일, 기준 1/3={threshold:.1f}일)<br>
{status1}
</div>
"""

# JS: 클릭할 때마다 query string 업데이트 + reload
calendar_html += """
<script>
function onClickDate(el) {
    const date = el.getAttribute("data-date");
    // 현재 URL 파라미터 읽기
    const params = new URLSearchParams(window.location.search);
    let arr = [];
    if (params.has("selectedDates")) {
        try {
            arr = JSON.parse(decodeURIComponent(params.get("selectedDates")));
        } catch {}
    }
    // toggle
    const idx = arr.indexOf(date);
    if (idx >= 0) { arr.splice(idx,1); el.classList.remove("selected"); }
    else           { arr.push(date); el.classList.add("selected"); }
    // 새로운 파라미터 설정 (JSON, URI encoded)
    params.set("selectedDates", encodeURIComponent(JSON.stringify(arr)));
    // 페이지 리로드
    window.location.search = params.toString();
}
</script>
"""

st.components.v1.html(calendar_html, height=600, scrolling=False)


