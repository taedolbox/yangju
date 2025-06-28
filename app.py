import streamlit as st
import streamlit.components.v1 as components

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
    .checkbox-container {
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'checkbox_value' not in st.session_state:
    st.session_state.checkbox_value = False

# JavaScript로 .day 클릭 처리
click_handler_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const day = document.querySelector('.day');
    if (day) {
        day.addEventListener('click', function(e) {
            e.preventDefault();
            // Streamlit 상태 토글 요청
            window.parent.postMessage({
                type: 'STREAMLIT_SET_STATE',
                key: 'checkbox_value',
                value: !JSON.parse(window.parent.sessionStorage.getItem('checkbox_value') || 'false')
            }, '*');
            // UI 갱신
            window.parent.location.reload();
        });
    }
});
</script>
"""
components.html(click_handler_js, height=1)

# UI
st.markdown('<div class="day">21</div>', unsafe_allow_html=True)

# 버튼으로 상태 토글 (백업 옵션)
if st.button("21일 선택", key="day_button"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()

# 체크박스 상태 반영
checkbox_value = st.session_state.checkbox_value
st.checkbox("21일 선택", key="test_checkbox", value=checkbox_value, disabled=True)

if checkbox_value:
    st.write("21일이 선택되었습니다!")
else:
    st.write("21일이 선택되지 않았습니다.")
