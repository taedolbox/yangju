import streamlit as st
from datetime import datetime, timedelta

# --- 앱 기본 설정 ---
st.set_page_config(page_title="일용근로자 수급자격 요건 모의계산", layout="centered")

# --- 현재 날짜와 시간 표시 ---
now = datetime.now()
st.markdown(f"## 일용근로자 수급자격 요건 모의계산")
st.markdown(f"오늘 날짜와 시간: {now.strftime('%Y년 %m월 %d일 %A 오후 %I:%M')} KST")

# --- 조건 설명 ---
st.markdown("""
---
📋 **요건 조건**
- 조건 1: 수급자격 인정신청일의 직전 달 초일부터 신청일까지의 근무일 수가 총 일수의 1/3 미만이어야 합니다.
- 조건 2 (건설일용근로자만 해당): 신청일 직전 14일간 근무 사실이 없어야 합니다 (신청일 제외).
""")

# --- 기준일 선택 ---
input_date = st.date_input("수급자격 신청일을 선택하세요", now.date())

# --- 달력용 날짜 리스트 생성 (직전달 1일부터 신청일까지) ---
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

# --- 년월별 그룹화 ---
calendar_groups = {}
for date in cal_dates:
    ym = date.strftime("%Y-%m")
    if ym not in calendar_groups:
        calendar_groups[ym] = []
    calendar_groups[ym].append(date)

# --- 선택한 날짜를 저장하는 숨겨진 input ---
selected_dates_str = st.text_input("선택한 날짜", value="", key="selected_dates")

# --- 달력 HTML 생성 ---
calendar_html = ""

for ym, dates in calendar_groups.items():
    year, month = ym.split("-")
    calendar_html += f"""
    <h4>{int(year)}년 {int(month)}월</h4>
    <div class="calendar">
    """
    for date in dates:
        day_num = date.day
        date_str = date.strftime("%Y-%m-%d")
        calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
    calendar_html += "</div>"

calendar_html += """
<p id="selectedDatesText"></p>

<style>
.calendar {
    display: grid;
    grid-template-columns: repeat(7, 40px);
    grid-gap: 5px;
    margin-bottom: 20px;
}

.day {
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    user-select: none;
}

.day:hover {
    background-color: #eee;
}

.day.selected {
    border: 2px solid #2196F3;
    background-color: #2196F3;
    color: white;
}

h4 {
    margin: 10px 0 5px 0;
    font-size: 18px;
}
</style>

<script>
function toggleDate(element) {
    element.classList.toggle('selected');

    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }

    const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInputInput"]');
    if (streamlitInput) {
        streamlitInput.value = selected.join(',');
        streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

    // 선택 날짜 MM/DD 형식으로 표시
    var mmdd = selected.map(d => {
        var parts = d.split("-");
        return parts[1] + "/" + parts[2];
    });
    document.getElementById('selectedDatesText').innerText = "✅ 선택된 근무일자: " + mmdd.join(", ");
}
</script>
"""

st.components.v1.html(calendar_html, height=600, scrolling=True)

# --- 결과 버튼 및 로직 ---
if st.button("결과 계산"):
    # 선택 날짜 처리
    if selected_dates_str.strip():
        selected_dates = selected_dates_str.split(",")
    else:
        selected_dates = []

    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days = [d for d in cal_dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end]
    selected_dates_set = set(selected_dates)

    no_work_14_days = all(d.strftime("%Y-%m-%d") not in selected_dates_set for d in fourteen_days)

    # 출력
    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    if worked_days < threshold:
        st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")

    if no_work_14_days:
        st.success(f"✅ 조건 2 충족: 신청일 직전 14일간({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}) 근무내역이 없습니다.")
    else:
        st.error(f"❌ 조건 2 불충족: 신청일 직전 14일간({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}) 내 근무기록이 존재합니다.")

    # 조건 2 불충족 시 언제 신청해야 하는지 계산 (조건 2 충족 시점)
    next_eligible_date = fourteen_days_prior_end + timedelta(days=14)
    if not no_work_14_days:
        st.markdown(f"📅 조건 2를 충족하려면 언제 신청해야 할까요?\n✅ {next_eligible_date.strftime('%Y-%m-%d')} 이후에 신청하면 조건 2를 충족할 수 있습니다.")

    # 최종 판단
    st.markdown("### 📌 최종 판단")
    if worked_days < threshold:
        st.success("✅ 일반일용근로자: 신청 가능\n수급자격 인정신청일이 속한 달의 직전 달 초부터 수급자격 인정신청일까지"
                   f"({first_day_prev_month.strftime('%Y-%m-%d')} ~ {last_day.strftime('%Y-%m-%d')}) 근로일 수의 합이 같은 기간 동안의 총 일수의 3분의 1 미만")
    else:
        st.error("❌ 일반일용근로자: 신청 불가능\n수급자격 인정신청일이 속한 달의 직전 달 초부터 수급자격 인정신청일까지"
                 f"({first_day_prev_month.strftime('%Y-%m-%d')} ~ {last_day.strftime('%Y-%m-%d')}) 근로일 수가 총 일수의 1/3 이상입니다.")

    if worked_days < threshold and no_work_14_days:
        st.success("✅ 건설일용근로자: 신청 가능\n수급자격 인정신청일이 속한 달의 직전 달 초부터 수급자격 인정신청일까지"
                   f"({first_day_prev_month.strftime('%Y-%m-%d')} ~ {last_day.strftime('%Y-%m-%d')}) 근로일 수의 합이 총 일수의 3분의 1 미만이고, 신청일 직전 14일간"
                   f"({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}) 근무 사실이 없음을 확인합니다.")
    else:
        st.error("❌ 건설일용근로자: 신청 불가능")
        if worked_days >= threshold:
            st.write(f"수급자격 인정신청일이 속한 달의 직전 달 초부터 수급자격 인정신청일까지"
                     f"({first_day_prev_month.strftime('%Y-%m-%d')} ~ {last_day.strftime('%Y-%m-%d')}) 근무일 수가 총 일수의 1/3 이상입니다.")
        if not no_work_14_days:
            st.write(f"신청일 직전 14일간({fourteen_days_prior_start.strftime('%Y-%m-%d')} ~ {fourteen_days_prior_end.strftime('%Y-%m-%d')}) 내 근무내역이 존재합니다.")

# --- 하단 안내 ---
st.markdown("""
---
ⓒ 2025 실업급여 도우미는 도움을 드리기 위한 목적입니다. 실제 가능 여부는 고용센터의 판단을 기준으로 합니다.

거주지역 고용센터 찾기에서 자세한 정보를 확인하세요.
""")
