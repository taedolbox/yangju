import streamlit as st
from datetime import datetime, timedelta
import calendar

def get_korean_day_name(weekday):
    """요일 숫자를 한국어 요일 이름으로 변환"""
    days = ["월", "화", "수", "목", "금", "토", "일"]
    # calendar.weekday는 월요일=0, 일요일=6
    # 우리의 달력은 일요일부터 시작하므로 인덱스 조정 (일=0, 월=1, ..., 토=6)
    return days[(weekday + 6) % 7]

def daily_worker_eligibility_app_native():
    st.markdown(
        "<span style='font-size:22px; font-weight:600; color:#fff;'>🏗️ 일용직 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )

    today_kst = datetime.utcnow() + timedelta(hours=9)
    
    # 세션 상태에서 선택된 날짜를 관리합니다.
    if 'selected_dates' not in st.session_state:
        st.session_state.selected_dates = []

    # 기준 날짜 선택
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    # 계산 기간 설정
    # 신청일이 속한 달의 직전 달 첫날부터 신청일까지
    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    calculation_end_date = input_date
    
    # 달력 표시를 위한 기간 (직전 달 첫날부터 현재 선택된 날짜까지)
    current_display_date = first_day_prev_month
    
    st.markdown("---")
    st.markdown("### 📆 근무일 선택")

    # 월별로 달력 표시
    while current_display_date <= calculation_end_date:
        year = current_display_date.year
        month = current_display_date.month

        st.subheader(f"{year}년 {month}월")

        # 달력 헤더 (요일)
        col_headers = st.columns(7)
        day_names = ["일", "월", "화", "수", "목", "금", "토"]
        for i, day_name in enumerate(day_names):
            # 일요일은 빨간색, 토요일은 파란색
            color = "red" if i == 0 else ("blue" if i == 6 else "white")
            col_headers[i].markdown(f"<p style='text-align:center; color:{color}; font-weight:bold;'>{day_name}</p>", unsafe_allow_html=True)

        # 달력 일자 표시
        cal = calendar.Calendar(firstweekday=6) # 일요일을 주의 시작으로 설정 (0=월, 6=일)
        month_days = cal.monthdayscalendar(year, month)

        for week in month_days:
            cols = st.columns(7)
            for i, day_num in enumerate(week):
                if day_num == 0: # 해당 월이 아닌 날짜
                    cols[i].empty()
                else:
                    current_day_date = datetime(year, month, day_num).date()
                    
                    # 계산 범위 내에 있는 날짜만 활성화
                    is_active_day = first_day_prev_month <= current_day_date <= calculation_end_date

                    date_str = current_day_date.strftime("%Y-%m-%d")
                    is_selected = date_str in st.session_state.selected_dates

                    # 날짜 버튼 스타일 (CSS 직접 삽입)
                    button_style = f"""
                        width: 100%;
                        height: 100%;
                        aspect-ratio: 1 / 1; /* 정사각형 유지 */
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        border: 1px solid {'#2196F3' if is_selected else '#ddd'};
                        border-radius: 5px;
                        background-color: {'#2196F3' if is_selected else ('#fdfdfd' if is_active_day else '#eee')};
                        color: {'#fff' if is_selected else ('#222' if is_active_day else '#aaa')} !important;
                        cursor: {'pointer' if is_active_day else 'default'};
                        font-weight: {'bold' if is_selected else 'normal'};
                        font-size: 16px;
                        user-select: none;
                        transition: background-color 0.1s ease, border 0.1s ease;
                    """
                    # 비활성 날짜는 클릭 불가
                    button_key = f"day_button_{date_str}"
                    if is_active_day:
                        if cols[i].button(str(day_num), key=button_key, help=f"{date_str} 선택/해제"):
                            if is_selected:
                                st.session_state.selected_dates.remove(date_str)
                            else:
                                st.session_state.selected_dates.append(date_str)
                            st.rerun() # 선택 상태 변경 시 앱 다시 실행하여 UI 업데이트
                    else:
                        # 비활성 날짜는 단순히 텍스트로 표시
                        cols[i].markdown(f"<div style='{button_style}'>{day_num}</div>", unsafe_allow_html=True)
                    
                    # 다크 모드 스타일
                    st.markdown("""
                    <style>
                    @media (prefers-color-scheme: dark) {
                        div[data-testid*="stButton"] > button {
                            background-color: #444 !important;
                            border-color: #555 !important;
                            color: #eee !important;
                        }
                        div[data-testid*="stButton"] > button:hover {
                            background-color: #555 !important;
                        }
                        div[data-testid*="stButton"] > button[data-selected="true"] { /* Streamlit 내부적으로 selected 상태가 없으므로 CSS 셀렉터가 작동 안 할 수 있음 */
                            background-color: #2196F3 !important;
                            border-color: #2196F3 !important;
                            color: #fff !important;
                        }
                        /* 직접 삽입된 div 스타일은 prefers-color-scheme에서 직접 수정해야 함 */
                        div[style*="background-color: rgb(253, 253, 253);"] { /* #fdfdfd */
                            background-color: #444 !important;
                            border-color: #555 !important;
                            color: #eee !important;
                        }
                        div[style*="background-color: rgb(238, 238, 238);"] { /* #eee */
                            background-color: #333 !important;
                            border-color: #444 !important;
                            color: #aaa !important;
                        }
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # 각 버튼에 인라인 스타일 적용 (Streamlit 버튼 위젯의 스타일을 직접 조작)
                    st.markdown(f"""
                        <style>
                            div[data-testid="stColumn"] > div > div[data-testid*="stButton"] > button[key="{button_key}"] {{
                                {button_style}
                            }}
                        </style>
                    """, unsafe_allow_html=True)

        current_display_date = current_display_date.replace(day=1) + timedelta(days=32)
        current_display_date = current_display_date.replace(day=1) # 다음 달의 첫째 날

    # 선택된 날짜 출력 (UI 업데이트용)
    selected_count = len(st.session_state.selected_dates)
    st.markdown(f"<p style='color:#fff;'>선택한 날짜: {', '.join(sorted(st.session_state.selected_dates))} ({selected_count}일)</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 조건 판단")

    # 계산 로직 (이전과 동일)
    total_days = (calculation_end_date - first_day_prev_month).days + 1
    threshold = total_days / 3
    worked_days = len(st.session_state.selected_dates)

    fourteen_days_prior_end_dt = calculation_end_date - timedelta(days=1)
    fourteen_days_prior_start_dt = calculation_end_date - timedelta(days=14)

    # 선택된 날짜 중 14일 기간 내 근무 여부 확인
    no_work_14_days = True
    for selected_date_str in st.session_state.selected_dates:
        selected_date_dt = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        if fourteen_days_prior_start_dt <= selected_date_dt <= fourteen_days_prior_end_dt:
            no_work_14_days = False
            break

    condition1_text = f"근무일 수({worked_days}) < 기준({threshold:.1f})"
    condition2_text = f"신청일 직전 14일간({fourteen_days_prior_start_dt} ~ {fourteen_days_prior_end_dt}) 무근무"

    st.markdown("### 📌 조건 기준")
    st.markdown(f"<p>조건 1: 신청일이 속한 달의 직전 달 첫날부터 신청일까지 근무일 수가 전체 기간의 1/3 미만</p>", unsafe_allow_html=True)
    st.markdown(f"<p>조건 2: 건설일용근로자만 해당, 신청일 직전 14일간(신청일 제외) 근무 사실이 없어야 함</p>", unsafe_allow_html=True)
    st.markdown(f"<p>총 기간 일수: {total_days}일</p>", unsafe_allow_html=True)
    st.markdown(f"<p>1/3 기준: {threshold:.1f}일</p>", unsafe_allow_html=True)
    st.markdown(f"<p>근무일 수: {worked_days}일</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📌 조건 판단")
    if worked_days < threshold:
        st.success(f"✅ 조건 1 충족: {condition1_text}")
    else:
        st.error(f"❌ 조건 1 불충족: {condition1_text}")
        # 다음 신청 가능일 계산
        next_possible1_date = (calculation_end_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        st.info(f"📅 조건 1을 충족하려면 오늘({calculation_end_date}) 이후 근로제공이 없는 경우 **{next_possible1_date.strftime('%Y-%m-%d')}** 이후에 신청하면 조건 1을 충족할 수 있습니다.")


    if no_work_14_days:
        st.success(f"✅ 조건 2 충족: {condition2_text}")
    else:
        st.error(f"❌ 조건 2 불충족: {condition2_text}")
        # 다음 신청 가능일 계산
        next_possible2_date = fourteen_days_prior_end_dt + timedelta(days=14)
        st.info(f"📅 조건 2를 충족하려면 오늘({calculation_end_date}) 이후 근로제공이 없는 경우 **{next_possible2_date.strftime('%Y-%m-%d')}** 이후에 신청하면 조건 2를 충족할 수 있습니다.")


    st.markdown("---")
    st.markdown("### 📌 최종 판단")
    general_worker_eligible = worked_days < threshold
    construction_worker_eligible = (worked_days < threshold) or no_work_14_days

    if general_worker_eligible:
        st.success("✅ 일반일용근로자: 신청 가능")
    else:
        st.error("❌ 일반일용근로자: 신청 불가능")

    if construction_worker_eligible:
        st.success("✅ 건설일용근로자: 신청 가능")
    else:
        st.error("❌ 건설일용근로자: 신청 불가능")

if __name__ == "__main__":
    daily_worker_eligibility_app_native()
