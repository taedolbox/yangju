import streamlit as st
from datetime import datetime, timedelta
import json

if 'selected_dates_list' not in st.session_state:
    st.session_state.selected_dates_list = []

input_date = st.date_input("기준 날짜 선택", datetime.today())
# 달력 범위, 달력 생성 코드 동일 (생략)

# -- 중략: calendar_html 생성 (기존 CSS+HTML+JS 포함하되 JS 수정 필요) --

# JS에서 선택된 날짜를 아래 hidden input에 저장하도록 변경 필요
calendar_html += """
<input type="hidden" id="selectedDatesInput" name="selectedDatesInput" value='[]' />
<script>
function toggleDate(element) {
    element.classList.toggle('selected');
    var selected = [];
    var days = document.getElementsByClassName('day');
    for (var i = 0; i < days.length; i++) {
        if (days[i].classList.contains('selected')) {
            selected.push(days[i].getAttribute('data-date'));
        }
    }
    document.getElementById('selectedDatesInput').value = JSON.stringify(selected);
    document.getElementById('selectedDatesText').innerText = "선택한 날짜: " + selected.join(', ') + " (총 " + selected.length + "일)";
}
</script>
"""

st.components.v1.html(calendar_html, height=600, scrolling=True, key="calendar_component")

# 숨겨진 input 값을 Streamlit에서 읽기
selected_dates_json = st.text_input("hidden_selected_dates", value=json.dumps(st.session_state.selected_dates_list), key="hidden_selected_dates", label_visibility="collapsed")
try:
    selected_dates = json.loads(selected_dates_json)
    if isinstance(selected_dates, list):
        st.session_state.selected_dates_list = selected_dates
except:
    st.session_state.selected_dates_list = []

if st.button("결과 계산"):
    selected_dates = st.session_state.selected_dates_list
    # 이후 기존 계산 로직 그대로 진행
