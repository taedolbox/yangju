import streamlit as st

def unemployment_recognition_app():
#    st.subheader("🔵 실업인정 요건 판단")
    st.write("이 기능은 실업인정 요건을 판단하는 데 도움을 줍니다. 현재는 플레이스홀더입니다.")
    st.info("실업인정 요건 판단 기능은 추후 구현 예정입니다. 고용센터에 문의하세요.")
    if st.button("처음으로", key="reset_unemployment"):
        st.rerun()
