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


import streamlit as st
import traceback

st.title("🚨 오류 메시지 출력 & 복사 예시")

try:
    # 예시: 일부러 ZeroDivisionError 발생
    a = 1 / 0

except Exception as e:
    # 전체 Traceback 문자열로 받기
    tb_str = "".join(traceback.format_exception(type(e), e, e.__traceback__))

    st.error("❌ 오류가 발생했습니다!")
    st.code(tb_str, language="bash")

    # 복사 팁: 텍스트박스도 같이 제공
    st.text_area("📝 아래 내용 복사:", tb_str, height=200)

    # 필요하면 텍스트파일로 다운로드 버튼 제공
    st.download_button(
        label="📄 에러 로그 파일 다운로드",
        data=tb_str,
        file_name="error_log.txt",
        mime="text/plain"
    )

st.markdown("""
---
- 위 예시는 일부러 `1 / 0`으로 에러를 발생시킨 것임  
- 실제로는 `try: ... except:`로 감싸면 어떤 오류든 그대로 출력됨  
- `st.code` + `st.text_area` + `st.download_button`을 조합하면:
    - 화면에 보기 좋게 출력
    - 복사 가능
    - 파일로 저장도 가능
""")
