import sys
import os
sys.path.append(os.path.abspath('.'))

import streamlit as st
from app.daily_worker_eligibility import daily_worker_eligibility_app

st.write("임포트 확인")

daily_worker_eligibility_app()
