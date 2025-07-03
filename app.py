import streamlit as st

simple_html = """
<style>
  div { color: blue; font-weight: bold; }
</style>
<div>테스트</div>
"""

st.components.v1.html(simple_html, height=100)

