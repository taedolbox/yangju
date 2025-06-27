import streamlit as st

# 세션 상태 초기화
# 'selected_days'는 선택된 날짜들을 저장하는 집합 (Set)입니다.
# 집합을 사용하면 날짜 추가/삭제 및 존재 여부 확인이 효율적입니다.
if 'selected_days' not in st.session_state:
    st.session_state.selected_days = set()

st.set_page_config(layout="centered") # 페이지 레이아웃을 중앙으로 설정하여 달력을 보기 좋게 배치

st.title("날짜 선택 달력") # 달력 제목

# 선택된 날짜 수 표시
# len() 함수를 사용하여 집합의 크기(선택된 날짜 수)를 계산합니다.
st.write(f"선택된 날짜 수: {len(st.session_state.selected_days)}개")

# --- CSS 주입: 기본 스타일 및 선택된 날짜 스타일 ---
all_dynamic_styles = []

# 1. 기본 버튼 스타일 (모든 버튼에 적용)
all_dynamic_styles.append("""
div.stButton > button {
    width: 50px;
    height: 50px;
    border: 1px solid #ccc; /* 기본 테두리 색상 */
    border-radius: 50%;
    text-align: center;
    line-height: 50px;
    margin: 5px auto;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    background-color: white; /* 기본 배경색 */
    color: black; /* 기본 텍스트 색상 */
    cursor: pointer;
    transition: all 0.2s ease-in-out; /* 부드러운 전환 효과 */
    padding: 0;
}

div.stButton > button:hover {
    background-color: #f0f0f0; /* 기본 호버 배경색 */
}

div.stButton > button > div { /* Streamlit 내부 텍스트 컨테이너 패딩 제거 */
    padding: 0 !important;
}
""")

# 2. 선택된 날짜에 대한 스타일 (동적 생성)
for day in st.session_state.selected_days:
    all_dynamic_styles.append(f"""
    /* 선택된 버튼의 data-testid를 통해 직접 버튼을 타겟팅 */
    div[data-testid="stButton-primary-day_button_{day}"] > button {{
        background-color: #007bff !important; /* 선택 시 파란색 배경 */
        color: white !important; /* 선택 시 흰색 텍스트 */
        border: 2px solid #007bff !important; /* 선택 시 파란색 테두리 */
    }}
    /* 선택된 버튼의 호버 효과 (선택된 상태에서는 더 진한 파란색으로 변경) */
    div[data-testid="stButton-primary-day_button_{day}"] > button:hover {{
        background-color: #0056b3 !important; /* 호버 시 더 진한 파란색으로 변경 */
    }}
    """)

# 모든 CSS 규칙을 하나의 <style> 블록으로 합쳐서 주입
st.markdown(f"""
<style>
{"\n".join(all_dynamic_styles)}
</style>
""", unsafe_allow_html=True)


# 달력 그리드 생성
# st.columns를 사용하여 7개의 컬럼(요일)을 만듭니다.
columns = st.columns(7)
day_counter = 1 # 날짜 카운터 초기화

# 최대 5주까지 반복하여 달력의 행을 만듭니다.
for _ in range(5):
    # 각 요일 컬럼에 날짜 버튼을 배치합니다.
    for col_idx in range(7):
        with columns[col_idx]:
            # 날짜가 31일 이하일 때만 버튼을 표시합니다.
            if day_counter <= 31:
                # 날짜 버튼을 생성합니다.
                # `key`는 Streamlit이 각 버튼을 고유하게 식별하는 데 사용됩니다.
                # `use_container_width=True`는 버튼이 컬럼의 전체 너비를 사용하도록 하여
                # `margin: auto`가 중앙 정렬에 효과적으로 작동하게 합니다.
                clicked = st.button(
                    str(day_counter), # 버튼에 표시될 날짜 텍스트
                    key=f"day_button_{day_counter}", # 고유 키
                    use_container_width=True # 컨테이너 너비에 맞춤
                )

                # 버튼이 클릭되었을 때의 로직 처리
                if clicked:
                    if day_counter in st.session_state.selected_days:
                        # 이미 선택된 날짜라면 선택 해제
                        st.session_state.selected_days.remove(day_counter)
                    else:
                        # 선택되지 않은 날짜라면 선택
                        st.session_state.selected_days.add(day_counter)
                    # UI를 즉시 업데이트하기 위해 Streamlit 앱을 다시 실행합니다.
                    st.rerun()

                day_counter += 1 # 다음 날짜로 이동
            else:
                st.empty() # 날짜가 없으면 빈 공간을 두어 레이아웃 일관성 유지

# 현재 선택된 날짜들을 정렬하여 표시 (디버깅 또는 확인용)
st.write("선택된 날짜:", sorted(list(st.session_state.selected_days)))



