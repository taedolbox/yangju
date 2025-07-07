import os
import streamlit as st

st.write("현재 작업 경로:", os.getcwd())
st.write("app 폴더 존재 여부:", os.path.isdir("app"))
st.write("app/__init__.py 존재 여부:", os.path.isfile("app/__init__.py"))
st.write("app/daily_worker_eligibility.py 존재 여부:", os.path.isfile("app/daily_worker_eligibility.py"))
