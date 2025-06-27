import streamlit as st

# 세션 상태 초기화: 'selected_days'는 선택된 날짜들을 저장하는 집합 (Set)입니다.
# 집합을 사용하면 날짜 추가/삭제 및 존재 여부 확인이 효율적입니다.
if 'selected_days' not in st.session_state:
    st.session_state.selected_days = set()

# 페이지 레이아웃을 중앙으로 설정하여 달력을 보기 좋게 배치합니다.
st.set_page_config(layout="centered")

# 달력 제목을 표시합니다.
st.title("날짜 선택 달력")

# 현재 선택된 날짜의 총 개수를 표시합니다.
# 이 값은 'selected_days' 집합의 크기(length)에 따라 실시간으로 업데이트됩니다.
st.write(f"선택된 날짜 수: {len(st.session_state.selected_days)}개")

# --- CSS 스타일 주입: 기본 스타일 및 선택된 날짜 스타일 ---
# 이 섹션은 Streamlit이 생성하는 HTML 요소에 사용자 정의 스타일을 적용합니다.
# `!important`를 사용하여 Streamlit의 기본 스타일보다 높은 우선순위를 가집니다.
all_dynamic_styles = []

# 1. 모든 날짜 버튼에 적용될 공통 기본 스타일 정의
# 이 스타일은 버튼의 크기, 모양(원형), 텍스트 정렬, 기본 색상 등을 설정합니다.
all_dynamic_styles.append("""
div.stButton > button {
    width: 50px !important; /* 버튼 너비, Streamlit 기본값보다 우선 */
    height: 50px !important; /* 버튼 높이, Streamlit 기본값보다 우선 */
    border: 1px solid #ccc !important; /* 기본 테두리 색상 */
    border-radius: 50% !important; /* 원형 모양 */
    text-align: center !important; /* 텍스트 가운데 정렬 */
    line-height: 50px !important; /* 텍스트 수직 가운데 정렬 */
    margin: 5px auto !important; /* 상하 5px, 좌우 자동 마진으로 중앙 정렬 */
    display: flex !important; /* Flexbox를 사용하여 내용 정렬 */
    justify-content: center !important; /* 수평 가운데 정렬 */
    align-items: center !important; /* 수직 가운데 정렬 */
    font-weight: bold !important; /* 글꼴 굵게 */
    background-color: white !important; /* 기본 배경색 (선택되지 않았을 때) */
    color: black !important; /* 기본 텍스트 색상 (선택되지 않았을 때) */
    cursor: pointer !important; /* 마우스 오버 시 포인터 변경 */
    transition: all 0.2s ease-in-out !important; /* 부드러운 전환 효과 */
    padding: 0 !important; /* 버튼 내부 패딩 제거 */
}

/* 마우스 오버 시의 기본 배경색 변화 (선택되지 않은 버튼에 적용) */
div.stButton > button:hover {
    background-color: #f0f0f0 !important;
}

/* Streamlit이 버튼 텍스트를 감싸는 div에 자동으로 추가하는 패딩 제거 */
/* 이 div가 텍스트 정렬에 영향을 줄 수 있으므로 패딩을 0으로 설정합니다. */
div.stButton > button > div {
    padding: 0 !important;
}
""")

# 2. 선택된 날짜에 대한 동적 스타일 (selected_days 집합에 있는 날짜에만 적용)
# 각 선택된 날짜에 대해 고유한 CSS 규칙을 생성하고, !important를 통해 강력하게 적용합니다.
for day in st.session_state.selected_days:
    all_dynamic_styles.append(f"""
    /* 선택된 버튼의 data-testid를 통해 해당 버튼을 직접 타겟팅합니다. */
    div[data-testid="stButton-primary-day_button_{day}"] > button {{
        background-color: #007bff !important; /* 선택 시 진한 파란색 배경 */
        color: white !important; /* 선택 시 흰색 텍스트 */
        border: 2px solid #007bff !important; /* 선택 시 파란색 테두리 */
    }}
    /* 선택된 버튼 위에 마우스를 올렸을 때의 호버 효과 */
    /* 선택된 상태에서도 파란색 계열의 호버 효과를 유지합니다. */
    div[data-testid="stButton-primary-day_button_{day}"] > button:hover {{
        background-color: #0056b3 !important; /* 호버 시 더 진한 파란색으로 변경 */
    }}
    """)

# 위에서 정의된 모든 CSS 규칙들을 하나의 `<style>` 태그로 묶어 Streamlit 앱에 주입합니다.
st.markdown(f"""
<style>
{"\n".join(all_dynamic_styles)}
</style>
""", unsafe_allow_html=True)


# 달력 그리드 생성
# `st.columns`를 사용하여 7개의 컬럼(요일)을 만듭니다.
columns = st.columns(7)
day_counter = 1 # 1일부터 시작하는 날짜 카운터

# 일반적으로 달력은 최대 5주를 표시하므로 5번 반복합니다.
for _ in range(5):
    # 각 요일 컬럼에 순서대로 날짜 버튼을 배치합니다.
    for col_idx in range(7):
        with columns[col_idx]: # 현재 컬럼 내부에 위젯을 배치합니다.
            # 날짜가 31일 이하일 때만 버튼을 표시합니다 (일반적인 월의 최대 일수).
            if day_counter <= 31:
                # 날짜 버튼을 생성합니다.
                # `key`는 Streamlit이 각 버튼을 고유하게 식별하는 데 필수적입니다.
                # `use_container_width=True`는 버튼이 컬럼의 전체 너비를 사용하도록 하여 정렬에 도움을 줍니다.
                clicked = st.button(
                    str(day_counter), # 버튼에 표시될 날짜 (예: "1", "2" 등)
                    key=f"day_button_{day_counter}", # 각 버튼의 고유 키 (예: "day_button_1", "day_button_2")
                    use_container_width=True # 컨테이너(컬럼)의 너비에 맞춤
                )

                # 버튼이 클릭되었을 때의 로직 처리
                if clicked:
                    if day_counter in st.session_state.selected_days:
                        # 이미 선택된 날짜라면 selected_days 집합에서 제거 (선택 해제)
                        st.session_state.selected_days.remove(day_counter)
                    else:
                        # 선택되지 않은 날짜라면 selected_days 집합에 추가 (선택)
                        st.session_state.selected_days.add(day_counter)
                    # UI를 즉시 업데이트하고 변경된 상태를 반영하기 위해 Streamlit 앱을 다시 실행 (리런)합니다.
                    st.rerun()

                day_counter += 1 # 다음 날짜로 이동
            else:
                st.empty() # 날짜가 31일을 초과하면 해당 위치에 빈 공간을 두어 레이아웃을 유지합니다.

# 현재 선택된 날짜들을 오름차순으로 정렬하여 웹 페이지 하단에 표시 (확인용)
st.write("선택된 날짜:", sorted(list(st.session_state.selected_days)))

