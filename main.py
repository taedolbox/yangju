import streamlit as st
import os
import sys

st.write("현재 작업 경로:", os.getcwd())
st.write("sys.path:", sys.path)
st.write("app 폴더 경로:", os.path.abspath("app"))
st.write("app 폴더 파일 리스트:", os.listdir("app"))

try:
    from app.daily_worker_eligibility import daily_worker_eligibility_app
    st.write("임포트 성공:", daily_worker_eligibility_app)
except Exception as e:
    st.write("임포트 실패:", e)
