import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# KST
KST = pytz.timezone('Asia/Seoul')

# 캐시 예시 함수
@st.cache_data
def load_data():
    # 캐시 확인용으로 시간 리턴
    return f"데이터 로드 시각: {datetime.now(KST)}"

# 앱 시작
st.title("📦 캐시 삭제 & 재배포 테스트")

st.write(load_data())

# 캐시 삭제 버튼
if st.button("🔄 캐시 지우고 새로고침"):
    st.cache_data.clear()
    st.experimental_rerun()

st.markdown("""
---
- 🔹 **깃허브에 `push` 하면 자동으로 재배포**
- 🔹 위 버튼 클릭 시 캐시만 삭제하고 앱 새로고침
""")

