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
        transition: background-color 0.3s, border-color 0.3s; /* border-color 트랜지션 추가 */
        background-color: white;
    }
    .stApp .stButton > button:hover {
        background-color: #f0f0f0;
    }
    .stApp .stButton > button[data-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
        border: 2px solid #007bff !important; /* 파란색 테두리 추가 */
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

# Streamlit 버튼을 생성하고, 클릭 시 상태를 토글
if st.button("21", key=key, help="21을 선택/해제합니다"):
    st.session_state.checkbox_value = not st.session_state.checkbox_value
    st.rerun() # 상태 변경 후 UI를 즉시 업데이트하기 위해 rerun 호출

# Streamlit 재렌더링 시에도 버튼의 data-selected 속성을 동적으로 업데이트
st.markdown(f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const updateButtonState = () => {{
                const button = document.querySelector('button[data-baseweb="button"][title="21을 선택/해제합니다"]');
                if (button) {{
                    const selected = {str(is_selected).lower()};
                    button.setAttribute('data-selected', selected);
                    console.log("Button found, data-selected set to: " + selected);
                }} else {{
                    console.log("Button not found, retrying...");
                }}
            }};

            // DOM 로드 후 초기 상태 설정
            updateButtonState();

            // MutationObserver를 사용하여 Streamlit DOM 변경 감지 및 상태 갱신
            const observer = new MutationObserver((mutations) => {{
                updateButtonState();
            }});
            observer.observe(document.body, {{ childList: true, subtree: true }});
            
            // 버튼 자체의 클릭 이벤트를 감지하여 data-selected 속성을 즉시 업데이트 (Streamlit rerun 전에 시각적 피드백 제공)
            document.addEventListener('click', function(e) {{
                // '21' 텍스트를 가진 Streamlit 버튼인지 확인
                if (e.target && e.target.textContent === '21' && e.target.getAttribute('data-baseweb') === 'button') {{
                    // 현재 data-selected 값을 토글
                    const currentSelected = e.target.getAttribute('data-selected') === 'true';
                    e.target.setAttribute('data-selected', String(!currentSelected));
                    console.log("Button clicked, data-selected toggled to: " + String(!currentSelected));
                }}
            }});
        }});
    </script>
    """, unsafe_allow_html=True)

# 디버깅 메시지
st.write(f"Debug: is_selected = {is_selected}")

# 체크박스 상태 반영 (동기화를 확인하기 위한 보조 UI)
checkbox_value = st.session_state.checkbox_value
st.checkbox("21 선택", key="test_checkbox", value=checkbox_value, disabled=True)

# 상태에 따른 텍스트 출력
if checkbox_value:
    st.write("21 선택되었습니다.")
else:
    st.write("21 선택되지 않았습니다.")
