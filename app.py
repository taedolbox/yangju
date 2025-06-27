import streamlit as st
import streamlit.components.v1 as components

# JavaScript와 HTML 통합
html_code = """
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
}
.day:hover {
    background-color: #f0f0f0;
}
.checkbox-container {
    margin-top: 10px;
}
</style>

<div class="day">21</div>
<div class="checkbox-container">
    <input type="checkbox" id="test_checkbox" style="display:none;">
</div>

<script>
function showPopup(message) {
    alert(message);
}

function setupClickHandlers() {
    const day = document.querySelector('.day');
    if (day) {
        showPopup('Day element found');
        day.addEventListener('click', function(e) {
            e.preventDefault();
            const checkbox = document.getElementById('test_checkbox');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                showPopup('Checkbox toggled: ' + checkbox.checked);
                // Streamlit에 상태 변경 알림
                window.parent.postMessage({
                    type: 'STREAMLIT_CHECKBOX_CHANGE',
                    key: 'test_checkbox',
                    value: checkbox.checked
                }, '*');
                // 상태 변경 후 UI 강제 갱신 요청
                window.parent.location.reload();
            } else {
                showPopup('Checkbox not found');
            }
        });
    } else {
        showPopup('No .day element found after setup');
    }
}

// DOM 로드 후 실행
document.addEventListener('DOMContentLoaded', function() {
    showPopup('DOM loaded, setting up handlers');
    setTimeout(setupClickHandlers, 500);
});

// DOM 변경 감지
new MutationObserver(() => {
    showPopup('DOM mutated, re-checking');
    setTimeout(setupClickHandlers, 500);
}).observe(document.body, { childList: true, subtree: true });
</script>
"""

# HTML 통합 삽입
components.html(html_code, height=200)

# Streamlit 체크박스 상태
if 'checkbox_value' not in st.session_state:
    st.session_state.checkbox_value = False

checkbox_value = st.session_state.checkbox_value
st.checkbox("21일 선택", key="test_checkbox", value=checkbox_value, on_change=lambda: st.session_state.update({'checkbox_value': st.session_state.test_checkbox}))

if checkbox_value:
    st.write("21일이 선택되었습니다!")
else:
    st.write("21일이 선택되지 않았습니다.")
