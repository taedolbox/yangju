import sys
import os
import streamlit as st

sys.path.append(os.path.abspath('.'))

try:
    from app.daily_worker_eligibility import daily_worker_eligibility_app
    st.success("임포트 성공!")
except Exception as e:
    st.error("임포트 실패:")
    st.error(str(e))
