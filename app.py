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
if 'selected_days' not in st.session_state:
    st.session_state.selected_days = set()

# UI
# 원숫자 21과 22를 버튼으로 대체
for day in [21, 22]:
    key = f"day_{day}"
    is_selected = day in st.session_state.selected_days
    class_name = "day"
    if is_selected:
        class_name += " selected"
    if st.button(str(day), key=key):
        if day in st.session_state.selected_days:
            st.session_state.selected_days.remove(day)
        else:
            st.session_state.selected_days.add(day)
        st.rerun()
    st.markdown(f'<div class="{class_name}">{day}</div>', unsafe_allow_html=True)

# 추가 버튼 (옵션 유지)
if st.button("21일 선택", key="day_button"):
    st.session_state.selected_days.add(21)  # 21만 선택
    st.rerun()

# 체크박스 상태 반영 (읽기 전용)
checkbox_value = 21 in st.session_state.selected_days  # 21에 기반
st.checkbox("21일 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21일이 선택되었습니다!")
else:
    st.write("21일이 선택되지 않았습니다.")
