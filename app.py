import streamlit as st

# 스타일시트
st.markdown("""
    <style>
    .stApp .stButton > button {
        width: 40px;
        height: 40px;
        border: 1px solid #ccc;
        text-align: center;
        line-height: 40px;
        cursor: pointer;
        margin: 10px;
        display: inline-block;
        transition: background-color 0.3s;
        background-color: white;
    }
    .stApp .stButton > button:hover {
        background-color: #f0f0f0;
    }
    .stApp .stButton > button[data-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
        border-color: #0056b3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'checkbox_value' not in st.session_state:
    st.session_state.checkbox_value = False

# UI
# 네모 21 버튼
key = "day_21"
is_selected = st.session_state.checkbox_value
if st.button("21", key=key, help="21을 선택/해제합니다"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun()

# 버튼에 선택 상태 동적으로 반영 (선택자 개선 및 MutationObserver 사용)
st.markdown(f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const observer = new MutationObserver((mutations) => {{
                const button = document.querySelector('button[data-baseweb="button"][title="21을 선택/해제합니다"]');
                if (button) {{
                    button.setAttribute('data-selected', {str(is_selected).lower()});
                    console.log("Button found, data-selected set to: " + {str(is_selected).lower()});
                    observer.disconnect(); // 한 번 설정 후 관찰 중지
                }} else {{
                    console.log("Button not found, retrying...");
                }}
            }});
            observer.observe(document.body, {{ childList: true, subtree: true }});
        }});
    </script>
    """, unsafe_allow_html=True)

# 디버깅 메시지
st.write(f"Debug: is_selected = {is_selected}")

# 체크박스 상태 반영
checkbox_value = st.session_state.checkbox_value
st.checkbox("21 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21 선택되었습니다.")
else:
    st.write("21 선택되지 않았습니다.")
