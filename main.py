import sys
import streamlit as st

st.write("sys.path:", sys.path)

import app
st.write("dir(app):", dir(app))
