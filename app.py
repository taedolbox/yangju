import streamlit as st

# 스타일시트
st.markdown("""
    <style>
    .stButton > button {
        width: 40px;
        height: 40px;
        border: 1px solid #ccc;
        text-align: center;
        line-height: 40px;
        cursor: pointer;
        margin: 10px;
        display: inline-block;
        transition: background-color 0.3s; /* 부드러운 전환 효과 */
    }
    .stButton > button:hover {
        background-color: #f0f0f0; /* 호버 시 회색 */
    }
    .stButton > button[data-selected="true"] {
        background-color: #007bff !important; /* 선택 시 파란색 */
        color: white !important; /* 선택 시 텍스트 흰색 */
        border-color: #0056b3 !important; /* 선택 시 테두리 색상 */
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'checkbox_value' not in st.session_state:
    st.session_state.checkbox_value = False

# UI
# 네모 21 버튼 (파란색 배경 통합)
key = "day_21"
is_selected = st.session_state.checkbox_value
if st.button("21", key=key, help="21을 선택/해제합니다"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()

# 버튼에 선택 상태 동적으로 반영 (JavaScript 없이 CSS로 처리)
st.markdown(f"""
    <script>
        const button = document.querySelector('button[data-baseweb="button"][title="21을 선택/해제합니다"]');
        if (button) {{
            button.setAttribute('data-selected', {is_selected});
        }}
    </script>
    """, unsafe_allow_html=True)

# 체크박스 상태 반영 (읽기 전용)
checkbox_value = st.session_state.checkbox_value
st.checkbox("21 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21 선택되었습니다.")
else:
    st.write("21 선택되지 않았습니다.")
