import streamlit as st
from datetime import datetime

def daily_worker_eligibility_app():
    st.markdown("<h3>달력 7열 테스트</h3>", unsafe_allow_html=True)
    calendar_html = """
    <div class="calendar">
        <div class="day-header sunday">일</div>
        <div class="day-header">월</div>
        <div class="day-header">화</div>
        <div class="day-header">수</div>
        <div class="day-header">목</div>
        <div class="day-header">금</div>
        <div class="day-header saturday">토</div>
        <div class="day">1</div>
        <div class="day">2</div>
        <div class="day">3</div>
        <div class="day">4</div>
        <div class="day">5</div>
        <div class="day">6</div>
        <div class="day">7</div>
        <div class="day">8</div>
        <div class="day">9</div>
    </div>
    """
    st.components.v1.html(calendar_html, height=300)
