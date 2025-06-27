import streamlit as st
import streamlit.components.v1 as components

# 스타일시트 (간소화)
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
    }
    .day:hover {
        background-color: #f0f0f0;
    }
    .checkbox-container {
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# JavaScript로 .day 클릭 시 체크박스 토글
click_handler_js = """
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
            const checkbox = document.querySelector('input[type="checkbox"]');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                showPopup('Checkbox toggled: ' + checkbox.checked);
            } else {
                showPopup('Checkbox not found');
            }
        });
    } else {
        showPopup('No .day element found');
    }
}

// DOM이 완전히 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    showPopup('DOM loaded, setting up handlers');
    setTimeout(setupClickHandlers, 100); // 100ms 대기 후 실행
});

// DOM 변경 감지
new MutationObserver(() => {
    showPopup('DOM mutated, re-applying handlers');
    setTimeout(setupClickHandlers, 100);
}).observe(document.body, { childList: true, subtree: true });
</script>
"""
components.html(click_handler_js, height=1)

# 간단한 UI
st.markdown('<div class="day">21</div>', unsafe_allow_html=True)
st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
checkbox_value = st.checkbox("21일 선택", key="test_checkbox")
st.markdown('</div>', unsafe_allow_html=True)

if checkbox_value:
    st.write("21일이 선택되었습니다!")
else:
    st.write("21일이 선택되지 않았습니다.")
