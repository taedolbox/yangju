import streamlit as st

st.set_page_config(layout="centered") # 페이지 레이아웃 설정 (선택 사항)

# 세션 상태 초기화
if 'toggle_value' not in st.session_state:
    st.session_state.toggle_value = False

st.markdown("## 21일 선택하기")
st.markdown("---")

# st.toggle을 사용하여 '21' 버튼 구현
# label을 비워두고, 도움말(help)로 설명 제공
col1, col2, col3 = st.columns([0.1, 0.1, 0.8]) # 버튼 크기를 맞추기 위해 컬럼 사용

with col1:
    # st.toggle은 자체적으로 선택 상태를 시각적으로 나타냅니다.
    # 클릭 시 st.session_state.toggle_value를 업데이트합니다.
    st.session_state.toggle_value = st.toggle("21", value=st.session_state.toggle_value, key="day_21_toggle", help="21을 선택/해제합니다.")
    # st.toggle의 기본 스타일을 조작하려면 추가 CSS가 필요할 수 있습니다.

# 디버깅 메시지
st.write(f"Debug: toggle_value = {st.session_state.toggle_value}")

# 상태에 따른 텍스트 출력
if st.session_state.toggle_value:
    st.write("21 선택되었습니다.")
else:
    st.write("21 선택되지 않았습니다.")
