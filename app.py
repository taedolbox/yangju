import streamlit as st

# 스타일시트
st.markdown("""
    <style>
    .day {
        width: 40px;
        height: 40px;
        border: 1px solid #ccc;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        cursor: pointer;
        margin: 10px;
        display: inline-block;
    }
    .day:hover {
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'checkbox_value' not in st.session_state:
    st.session_state.checkbox_value = False

# UI
# 원숫자 21을 버튼으로 대체
if st.button("21", key="day_click"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()

# 추가 버튼 (옵션 유지)
if st.button("21일 선택", key="day_button"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()

# 체크박스 상태 반영 (읽기 전용)
checkbox_value = st.session_state.checkbox_value
st.checkbox("21일 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21일이 선택되었습니다!")
else:
    st.write("21일이 선택되지 않았습니다.")

이것을 유지하면서 21 선택하면 시각적 효과를 줘봐 그리고 21만 아니라 22도 만들줘
