import streamlit as st
from datetime import datetime
import pytz
import time

# KST
KST = pytz.timezone('Asia/Seoul')

# 캐시 함수 예시
@st.cache_data
def load_data():
    return f"데이터 로드 시각: {datetime.now(KST)}"

# 헤더
st.title("🔄 캐시 삭제 + 진행막대 + 알림 예시")

# 현재 데이터 보여줌 (캐시됨)
st.write(load_data())

# 버튼 누르면 진행
if st.button("🚀 캐시 삭제 & 새로고침"):
    # 진행 막대
    progress_bar = st.progress(0)
    with st.spinner("⏳ 캐시 삭제 및 새로고침 준비 중..."):
        # 진행 막대 단계적으로 채움 (딜레이는 체감용)
        for percent in range(100):
            progress_bar.progress(percent + 1)
            time.sleep(0.01)

        # 캐시 삭제
        st.cache_data.clear()
        # 완료 알림
        st.toast("✅ 캐시 삭제 완료! 새로고침됩니다.")
        # 새로고침
        st.experimental_rerun()

# 설명
st.markdown("""
---
- ⏳ **진행중:** 진행막대 + 스피너 표시  
- ✅ **완료:** 토스트 알림 후 새로고침
- 🔄 **캐시:** `@st.cache_data` 사용
""")
