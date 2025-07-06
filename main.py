import streamlit as st
import os

st.write("app 폴더 경로:", os.path.abspath("app"))
st.write("app 폴더 파일 리스트:", os.listdir("app"))
