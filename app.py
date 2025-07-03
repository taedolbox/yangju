import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="년월 구분 다중선택 달력", layout="centered")

# 세션 상태 초기화
if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []

input_date = st.date_input("기준 날짜 선택", datetime.today())

# 달력 날짜 생성
first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
last_day = input_date
cal_dates = []
current_date = first_day_prev_month
while current_date <= last_day:
    cal_dates.append(current_date)
    current_date += timedelta(days=1)

calendar_groups = {}
for date in cal_dates:
    year_month = date.strftime("%Y-%m")
    if year_month not in calendar_groups:
        calendar_groups[year_month] = []
    calendar_groups[year_month].append(date)

# 세션 상태 업데이트 및 결과 계산 함수
def update_selected_dates_from_input():
    if st.session_state.text_input_for_js_communication:
        st.session_state.selected_dates_list = list(
            set(filter(None, st.session_state.text_input_for_js_communication.split(',')))
        )
    else:
        st.session_state.selected_dates_list = []
    
    # 디버깅 로그
    st.write("디버깅: text_input_for_js_communication 값:", st.session_state.text_input_for_js_communication)
    st.write("디버깅: 선택된 날짜 리스트:", st.session_state.selected_dates_list)

    # 결과 계산
    selected_dates = st.session_state.selected_dates_list
    total_days = len(cal_dates)
    threshold = total_days / 3
    worked_days = len(selected_dates)

    # 디버깅: 선택된 근무일 수 출력
    st.write("디버깅: 선택된 근무일 수:", worked_days)

    fourteen_days_prior_end = input_date - timedelta(days=1)
    fourteen_days_prior_start = fourteen_days_prior_end - timedelta(days=13)
    fourteen_days_str = [
        d.strftime("%Y-%m-%d") for d in cal_dates
        if fourteen_days_prior_start <= d <= fourteen_days_prior_end
    ]
    selected_dates_set = set(selected_dates)
    no_work_14_days = all(d not in selected_dates_set for d in fourteen_days_str)

    st.write(f"총 기간 일수: {total_days}일")
    st.write(f"기준 (총일수의 1/3): {threshold:.1f}일")
    st.write(f"선택한 근무일 수: {worked_days}일")
    st.write(f"{'✅ 조건 1 충족: 근무일 수가 기준 미만입니다.' if worked_days < threshold else '❌ 조건 1 불충족: 근무일 수가 기준 이상입니다.'}")
    st.write(f"{'✅ 조건 2 충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 근무내역이 없습니다.' if no_work_14_days else '❌ 조건 2 불충족: 신청일 직전 14일간(' + fourteen_days_prior_start.strftime('%Y-%m-%d') + ' ~ ' + fourteen_days_prior_end.strftime('%Y-%m-%d') + ') 내 근무기록이 존재합니다.'}")

    st.markdown("### 📌 최종 판단")
    if worked_days < threshold:
        st.write(f"✅ 일반일용근로자: 신청 가능")
    else:
        st.write(f"❌ 일반일용근로자: 신청 불가능")
    if worked_days < threshold and no_work_14_days:
        st.write(f"✅ 건설일용근로자: 신청 가능")
