import streamlit as st

# 스타일시트
st.markdown("""
    <style>
    .stApp .stButton > button[data-baseweb="button"][title="21을 선택/해제합니다"] {
        width: 40px;
        height: 40px;
        border: 1px solid #ccc;
        text-align: center;
        line-height: 40px;
        cursor: pointer;
        margin: 10px;
        display: inline-block;
        transition: background-color 0.3s; /* 부드러운 전환 효과 */
        background-color: white; /* 기본 배경색 */
    }
    .stApp .stButton > button[data-baseweb="button"][title="21을 선택/해제합니다"]:hover {
        background-color: #f0f0f0; /* 호버 시 회색 */
    }
    .stApp .stButton > button[data-baseweb="button"][title="21을 선택/해제합니다"].selected {
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
# 네모 21 버튼
key = "day_21"
is_selected = st.session_state.checkbox_value
if st.button("21", key=key, help="21을 선택/해제합니다"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()

# 버튼에 선택 상태 동적으로 반영
if is_selected:
    st.markdown("""
        <style>
        .stApp .stButton > button[data-baseweb="button"][title="21을 선택/해제합니다"] {
            background-color: #007bff !important;
            color: white !important;
            border-color: #0056b3 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# 디버깅 메시지
st.write(f"Debug: is_selected = {is_selected}")  # 상태 확인

# 체크박스 상태 반영 (읽기 전용)
checkbox_value = st.session_state.checkbox_value
st.checkbox("21 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21 선택되었습니다.")
else:
    st.write("21 선택되지 않았습니다.")
