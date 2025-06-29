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

# 버튼에 선택 상태 동적으로 반영 (Observer 개선 및 상태 동기화)
st.markdown(f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            function updateButtonState() {{
                const button = document.querySelector('button[data-baseweb="button"][title="21을 선택/해제합니다"]');
                if (button) {{
                    const selected = {str(is_selected).lower()}; // 초기 상태
                    button.setAttribute('data-selected', selected);
                    console.log("Button found, data-selected set to: " + selected);
                }} else {{
                    console.log("Button not found, retrying...");
                }}
            }}

            // DOM 로드 후 초기 상태 설정
            updateButtonState();

            // 버튼 클릭 시 상태 갱신 (MutationObserver로 동적 감지)
            const observer = new MutationObserver((mutations) => {{
                updateButtonState();
            }});
            observer.observe(document.body, {{ childList: true, subtree: true }});

            // 버튼 클릭 이벤트 리스너 (Streamlit 재렌더링 후에도 작동)
            document.addEventListener('click', function(e) {{
                if (e.target && e.target.textContent === '21' && e.target.getAttribute('data-baseweb') === 'button') {{
                    const selected = e.target.getAttribute('data-selected') === 'true' ? 'false' : 'true';
                    e.target.setAttribute('data-selected', selected);
                    console.log("Button clicked, data-selected set to: " + selected);
                }}
            }});
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
