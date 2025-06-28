import streamlit as st

# 스타일시트
st.markdown("""
    <style>
    .day {
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
    .day:hover {
        background-color: #f0f0f0; /* 호버 시 회색 */
    }
    .day.selected {
        background-color: #007bff; /* 선택 시 파란색 */
        color: white; /* 선택 시 텍스트 흰색 */
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
class_name = "day"
if is_selected:
    class_name += " selected"
if st.button("21", key=key):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()
st.markdown(f'<div class="{class_name}">21</div>', unsafe_allow_html=True)

# 체크박스 상태 반영 (읽기 전용)
checkbox_value = st.session_state.checkbox_value
st.checkbox("21 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21 선택되었습니다.")
else:
    st.write("21 선택되지 않았습니다.")
