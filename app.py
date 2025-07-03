import streamlit as st
from datetime import datetime, timedelta

# 📌 페이지 설정
st.set_page_config(page_title="일용근로자 수급자격 요건 모의계산기", layout="centered")

# 📌 오늘 날짜 출력
today = datetime.today().date()
st.write(f"오늘 날짜와 시간: {datetime.now().strftime('%Y년 %m월 %d일 %A %p %I:%M KST')}")

# 📋 요건 설명
st.markdown("""
### 📋 요건 조건
- **조건 1:** 수급자격 인정신청일의 직전 달 초일부터 신청일까지의 근무일 수가 총 기간의 1/3 미만이어야 합니다.
- **조건 2 (건설일용근로자만 해당):** 신청일 직전 14일간 근무 사실이 없어야 합니다 (신청일 제외).
""")

# 📌 신청일 입력
input_date = st.date_input("수급자격 신청일을 선택하세요", today)

# 📅 계산 범위 설정
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date

cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

date_options = [d.strftime("%Y-%m-%d") for d in cal_dates]

# ✅ 근무일 선택 (멀티셀렉트)
selected_dates = st.multiselect(
    "근무일 선택",
    options=date_options
)

# 📌 결과 버튼
if st.button("결과 계산"):
    total_days = len(cal_dates)
    worked_days = len(selected_dates)
    threshold = total_days / 3

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days = [
        d for d in cal_dates if fourteen_days_prior_start <= d <= fourteen_days_prior_end
    ]
    fourteen_days_str = [d.strftime("%Y-%m-%d") for d in fourteen_days]

    no_work_14_days = all(d not in selected_dates for d in fourteen_days_str)

    # ✅ 출력
    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    st.write(
        f"{'✅ 조건 1 충족: 근무일 수가 기준 미만입니다.' if worked_days < threshold else '❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.'}"
    )
    st.write(
        f"{'✅ 조건 2 충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 근무내역이 없습니다.' if no_work_14_days else '❌ 조건 2 불충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 내 근무기록이 존재합니다.'}"
    )

    st.markdown("### 📌 최종 판단")
    if worked_days < threshold:
        st.success(f"✅ 일반일용근로자: 신청 가능")
    else:
        st.error(f"❌ 일반일용근로자: 신청 불가능")

    if worked_days < threshold and no_work_14_days:
        st.success(f"✅ 건설일용근로자: 신청 가능")
    else:
        st.error(f"❌ 건설일용근로자: 신청 불가능")

    # 📅 조건 2 충족 날짜 계산 (조건 1은 별도 판단)
    if not no_work_14_days:
        # 선택된 날짜 중 직전 14일에 포함된 것 중 가장 최근 일자 찾기
        conflict_dates = [
            d for d in fourteen_days_str if d in selected_dates
        ]
        if conflict_dates:
            latest_conflict = max(
                datetime.strptime(d, "%Y-%m-%d").date() for d in conflict_dates
            )
            earliest_okay_date = latest_conflict + timedelta(days=15)
            st.warning(
                f"📅 조건 2를 충족하려면 **{earliest_okay_date.strftime('%Y-%m-%d')} 이후**에 신청해야 합니다."
            )

st.markdown("""
---
ⓒ 2025 실업급여 도우미는 도움을 드리기 위한 모의계산기입니다.  
최종 판단은 고용센터의 심사 결과에 따릅니다.
""")


