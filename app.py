import streamlit as st
import streamlit.components.v1 as components
import os
import datetime

# Streamlit 페이지 설정 (선택 사항: 페이지 레이아웃을 넓게 만듭니다)
st.set_page_config(layout="wide", page_title="커스텀 달력 앱")

st.title("나의 커스텀 달력 앱")
st.write("아래 달력에서 날짜를 클릭하여 선택하거나 해제해 보세요.")

# 1. 커스텀 컴포넌트의 경로를 지정합니다.
# app.py와 my_calendar_component 폴더가 같은 레벨에 있다고 가정합니다.
_COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_calendar_component")
# 테스트를 위해 경로를 출력해보세요. (나중에 삭제)
st.write(f"컴포넌트 디렉토리 경로: {_COMPONENT_DIR}")

# 2. 커스텀 컴포넌트를 선언합니다.
# 'my_calendar_component'는 이 컴포넌트의 고유한 이름입니다.
# path는 프론트엔드 코드가 포함된 컴포넌트의 루트 디렉토리를 가리킵니다.
_my_calendar_component = components.declare_component(
    "my_calendar_component",  # 컴포넌트 이름 (JS에서도 사용될 수 있음)
    path=_COMPONENT_DIR       # 컴포넌트의 루트 디렉토리 경로 (이 안에 frontend 폴더가 있음)
)

# 3. 커스텀 컴포넌트를 Streamlit 앱에 렌더링하고 초기값을 전달합니다.
# selected_dates: 달력 컴포넌트로 전달될 초기 선택 날짜 목록입니다.
#                  이 값은 index.html의 JavaScript로 전달되어 달력에 초기 선택 상태를 표시합니다.
# key: Streamlit이 이 컴포넌트 인스턴스를 식별하는 고유한 값입니다. 필수적입니다.
initial_selected_dates = ["2025-06-05", "2025-06-10", "2025-06-15"] # 예시 초기 날짜

selected_dates_from_component = _my_calendar_component(
    selected_dates=initial_selected_dates,
    key="unique_calendar_instance_001"
)

# 4. 커스텀 컴포넌트로부터 반환된 값을 표시합니다.
# 사용자가 달력에서 날짜를 선택/해제할 때마다, Streamlit.setComponentValue()를 통해
# 이 값이 업데이트되고, Streamlit 앱에 실시간으로 반영됩니다.
if selected_dates_from_component:
    st.success(f"현재 선택된 날짜 (컴포넌트에서 전달): {selected_dates_from_component}")
else:
    st.info("선택된 날짜가 없습니다.")

st.write("---")
st.write("이 아래는 Streamlit 앱의 다른 내용입니다.")
st.button("일반 Streamlit 버튼")

# 참고: Streamlit 기본 날짜 선택 위젯 (비교를 위해)
st.subheader("Streamlit 기본 날짜 선택 위젯 (비교)")
st.date_input("기본 날짜 선택", datetime.date.today())
