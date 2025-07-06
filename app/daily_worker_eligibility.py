import streamlit as st

def daily_worker_eligibility_app():
    st.markdown("<h3>달력 7열 테스트</h3>", unsafe_allow_html=True)
    html = """
    <style>
      .calendar {
        display: grid !important;
        grid-template-columns: repeat(7, 1fr) !important;
        gap: 5px !important;
        width: 100% !important;
        background: #fff !important;
        padding: 10px !important;
        border-radius: 8px !important;
      }
      .day-header, .day {
        aspect-ratio: 1 / 1 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border: 1px solid #ddd !important;
        border-radius: 5px !important;
        font-size: 16px !important;
      }
      .day-header.sunday { color: red !important; }
      .day-header.saturday { color: blue !important; }
    </style>
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
    </div>
    """
    st.components.v1.html(html, height=300)
