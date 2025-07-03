import streamlit as st

if st.button("캐시 초기화"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.experimental_rerun()


