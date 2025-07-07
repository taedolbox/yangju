import streamlit as st

html = """
<select style="
    border: 2px solid #007bff;
    border-radius: 6px;
    color: #007bff;
    font-weight: 600;
    padding: 6px;
    font-size: 16px;
    width: 200px;
">
    <option>메뉴 선택</option>
    <option>조기재취업수당</option>
    <option>일용직(건설일용포함)</option>
</select>
"""

st.components.v1.html(html, height=50)
