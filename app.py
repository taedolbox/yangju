import streamlit as st
import datetime

st.title("Streamlit 기본 달력 테스트")

# Streamlit 기본 날짜 선택 위젯 (Date Input)
# 이 위젯은 선택하면 자동으로 선택된 날짜가 강조됩니다.
selected_date = st.date_input("날짜를 선택해 보세요:", datetime.date.today())

st.write(f"선택된 날짜: {selected_date}")

# Streamlit이 기본으로 제공하는 위젯도 선택 시 시각적 피드백이 없다면,
# 브라우저나 Streamlit 설치 자체의 문제일 수 있습니다.
# 하지만 보통은 잘 작동합니다.
