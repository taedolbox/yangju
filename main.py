import streamlit as st
import streamlit.components.v1 as components

st.title("커스텀 스타일 콤보박스 with 링크")

html_code = """
<select id="menuSelect" style="
    border: 2px solid #007bff;
    border-radius: 6px;
    color: #007bff;
    font-weight: 600;
    padding: 6px;
    font-size: 16px;
    width: 250px;
">
    <option value="">메뉴 선택</option>
    <option value="early_reemployment">조기재취업수당</option>
    <option value="daily_worker">일용직(건설일용포함)</option>
</select>

<div id="linkArea" style="margin-top: 20px; font-weight: 600;"></div>

<script>
const menuSelect = document.getElementById('menuSelect');
const linkArea = document.getElementById('linkArea');

function sendMessage() {
    const selected = menuSelect.value;
    if (selected === "early_reemployment") {
        linkArea.innerHTML = '<a href="https://example.com/early_reemployment" target="_blank" style="color:#007bff;">조기재취업수당 바로가기</a>';
    } else if (selected === "daily_worker") {
        linkArea.innerHTML = '<a href="https://example.com/daily_worker" target="_blank" style="color:#007bff;">일용직(건설일용 포함) 바로가기</a>';
    } else {
        linkArea.innerHTML = "";
    }
}

menuSelect.addEventListener('change', sendMessage);
</script>
"""

components.html(html_code, height=150)
