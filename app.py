# app.py

import streamlit as st
import streamlit.components.v1 as components
import os
import datetime

st.set_page_config(layout="wide", page_title="커스텀 달력 앱")

st.title("나의 커스텀 달력 앱")
st.write("아래 달력에서 날짜를 클릭하여 선택하거나 해제해 보세요.")

_COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_calendar_component")
st.write(f"컴포넌트 디렉토리 경로 (디버깅용): {_COMPONENT_DIR}") # 디버깅용

_my_calendar_component = components.declare_component(
    "my_calendar_component",
    path=_COMPONENT_DIR
)

initial_selected_dates = ["2025-06-05", "2025-06-10", "2025-06-15"]

selected_dates_from_component = _my_calendar_component(
    selected_dates=initial_selected_dates,
    key="unique_calendar_instance_001"
)

if selected_dates_from_component:
    st.success(f"현재 선택된 날짜 (컴포넌트에서 전달): {selected_dates_from_component}")
else:
    st.info("선택된 날짜가 없습니다.")

st.write("---")
st.write("이 아래는 Streamlit 앱의 다른 내용입니다.")
st.button("일반 Streamlit 버튼")

st.subheader("Streamlit 기본 날짜 선택 위젯 (비교)")
st.date_input("기본 날짜 선택", datetime.date.today())
