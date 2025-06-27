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

# 모든 버튼에 적용될 기본 CSS 스타일을 정의합니다.
# 이 스타일은 버튼을 원형으로 만들고, 기본적인 테두리와 텍스트 정렬을 설정합니다.
st.markdown("""
<style>
/* Streamlit 버튼의 주 요소인 div.stButton 내부의 button 태그를 타겟팅합니다. */
div.stButton > button {
    width: 50px; /* 버튼의 너비 */
    height: 50px; /* 버튼의 높이 */
    border: 1px solid #ccc; /* 기본 테두리 색상과 두께 */
    border-radius: 50%; /* 원형으로 만들기 위해 50% 설정 */
    text-align: center; /* 텍스트 가운데 정렬 */
    line-height: 50px; /* 텍스트 수직 가운데 정렬 (높이와 동일하게 설정) */
    margin: 5px auto; /* 상하 5px 마진, 좌우 auto 마진으로 컬럼 내에서 중앙 정렬 */
    display: flex; /* flexbox를 사용하여 버튼 내용(날짜 텍스트)을 완벽히 가운데 정렬 */
    justify-content: center; /* 수평 가운데 정렬 */
    align-items: center; /* 수직 가운데 정렬 */
    font-weight: bold; /* 글꼴 굵게 */
    background-color: white; /* 기본 배경색 */
    color: black; /* 기본 텍스트 색상 */
    cursor: pointer; /* 마우스 오버 시 포인터 변경 */
    transition: all 0.2s ease-in-out; /* 모든 속성 변경 시 부드러운 전환 효과 */
    padding: 0; /* 버튼의 기본 패딩 제거 */
}

/* 마우스 오버 시 배경색 변경 효과 */
div.stButton > button:hover {
    background-color: #f0f0f0;
}

/* Streamlit 버튼 내부에 자동으로 생성되는 텍스트 컨테이너의 패딩을 제거하여 텍스트 정렬 보장 */
div.stButton > button > div {
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True) # HTML 스타일 주입 허용

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
                # 현재 날짜가 선택된 날짜 집합에 있는지 확인합니다.
                is_selected = day_counter in st.session_state.selected_days

                # 선택 여부에 따라 버튼에 적용될 동적 CSS 스타일을 생성합니다.
                # 이 스타일은 해당 버튼의 `data-testid` 속성을 타겟팅하여
                # 선택 시 파란색 테두리, 배경색, 텍스트 색상을 적용합니다.
                dynamic_style = ""
                if is_selected:
                    dynamic_style = f"""
                    <style>
                    /* 특정 버튼을 data-testid 속성으로 타겟팅합니다. */
                    /* Streamlit은 `stButton-primary-{key}` 형태로 data-testid를 할당합니다. */
                    div[data-testid="stButton-primary-day_button_{day_counter}"] > button {{
                        border: 2px solid #007bff !important; /* 선택 시 파란색 테두리 */
                        background-color: #e0f0ff !important; /* 선택 시 연한 파란색 배경 */
                        color: #007bff !important; /* 선택 시 파란색 텍스트 */
                    }}
                    </style>
                    """
                # 동적 스타일을 페이지에 주입합니다.
                st.markdown(dynamic_style, unsafe_allow_html=True)

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
