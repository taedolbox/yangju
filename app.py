import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="달력 선택 일수 카운트", layout="centered")

# 세션 상태 초기화
if "selected_dates_list" not in st.session_state:
    st.session_state.selected_dates_list = []

# 기준 날짜 입력 (오늘 날짜)
input_date = st.date_input("기준 날짜 선택", datetime.today())

# 직전달 1일 계산
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)

# 달력에 표시할 날짜 리스트 생성 (직전달 1일부터 input_date까지)
date_list = []
current = first_day_prev_month
while current <= input_date:
    date_list.append(current)
    current += timedelta(days=1)

# 날짜 클릭 시 선택/해제 로직 함수
def toggle_date(date_str):
    selected = st.session_state.selected_dates_list
    if date_str in selected:
        selected.remove(date_str)
    else:
        selected.append(date_str)

# 달력 UI 그리기
st.write(f"## {first_day_prev_month.strftime('%Y-%m-%d')} ~ {input_date.strftime('%Y-%m-%d')} 달력")

cols = st.columns(7)
weekdays = ["일", "월", "화", "수", "목", "금", "토"]

# 요일 헤더
for i, wd in enumerate(weekdays):
    cols[i].write(f"**{wd}**")

# 빈칸 채우기 (첫날 요일 맞추기)
start_offset = (first_day_prev_month.weekday() + 1) % 7
for _ in range(start_offset):
    cols[_ % 7].write(" ")

# 날짜 버튼 표시
for idx, date in enumerate(date_list):
    col_idx = (start_offset + idx) % 7
    date_str = date.strftime("%Y-%m-%d")

    # 선택 여부에 따라 색상 변경
    is_selected = date_str in st.session_state.selected_dates_list
    btn_label = str(date.day)
    btn_key = f"btn_{date_str}"

    if is_selected:
        if cols[col_idx].button(f"✅{btn_label}", key=btn_key):
            toggle_date(date_str)
            st.experimental_rerun()
    else:
        if cols[col_idx].button(btn_label, key=btn_key):
            toggle_date(date_str)
            st.experimental_rerun()

# 선택한 날짜 표시
st.write(f"선택한 날짜 수: {len(st.session_state.selected_dates_list)}")
st.write("선택된 날짜:", ", ".join(st.session_state.selected_dates_list))

# 결과 계산 버튼 및 조건 표시
if st.button("결과 계산"):
    total_days = len(date_list)
    threshold = total_days / 3
    worked_days = len(st.session_state.selected_dates_list)

    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")

    if worked_days < threshold:
        st.success("✅ 조건 충족: 근무일 수가 기준 미만입니다.")
    else:
        st.error("❌ 조건 불충족: 근무일 수가 기준 이상입니다.")


