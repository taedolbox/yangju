import streamlit as st
from datetime import datetime, timedelta

# 1. 기준 날짜
base_date = st.date_input("📅 기준 날짜 선택", datetime.today())

# 2. 달력 범위: 직전달 1일부터 기준일까지
start = (base_date.replace(day=1) - timedelta(days=1)).replace(day=1)
end = base_date

dates = []
cur = start
while cur <= end:
    dates.append(cur.strftime("%Y-%m-%d"))
    cur += timedelta(days=1)

# 3. 연·월별 그룹화
from collections import defaultdict
groups = defaultdict(list)
for d in dates:
    ym = d[:7]  # 'YYYY-MM'
    groups[ym].append(d)

# 4. UI: multiselect로 각 그룹 선택
st.header("📅 날짜 선택")
selected = []
for ym, ds in sorted(groups.items()):
    st.subheader(f"▶ {ym}")
    sel = st.multiselect(
        label=f"{ym} 날짜 선택",
        options=ds,
        default=[],
        key=ym  # 그룹별 고유 key
    )
    selected.extend(sel)

# 5. 결과 표시 및 계산
st.markdown("***")
st.write(f"✅ 선택된 날짜 수: {len(selected)}")
st.write(selected)

total_days = len(dates)
threshold = total_days / 3
worked_days = len(selected)

st.write(f"총 기간 일수: {total_days}일, 기준(1/3): {threshold:.1f}일, 선택 근무일 수: {worked_days}일")
if worked_days < threshold:
    st.success("✅ 조건 1 충족: 근무일 수가 기준 미만입니다.")
else:
    st.error("❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.")


