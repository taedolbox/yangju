# app.py 파일 내용

import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정 (선택 사항)
st.title("My Custom Calendar App")

# 1. 커스텀 컴포넌트의 경로를 지정합니다.
# 현재 app.py와 my_calendar_component 폴더가 같은 레벨에 있으므로 이렇게 지정합니다.
_COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_calendar_component")

# 2. 커스텀 컴포넌트를 선언합니다.
# declare_component 함수가 frontend 폴더를 알아서 찾아서 로드합니다.
_my_calendar_component = components.declare_component(
    "my_calendar_component",  # 이 컴포넌트의 고유한 이름 (자바스크립트에서도 사용될 수 있음)
    path=_COMPONENT_DIR       # 컴포넌트의 루트 디렉토리 경로
)

# 3. 이제 선언한 컴포넌트를 Streamlit 앱에 표시합니다.
# 여기에 원하는 초기값이나 속성을 전달할 수 있습니다.
# key는 Streamlit이 이 컴포넌트 인스턴스를 식별하는 데 사용됩니다.
# selected_dates는 index.html (JavaScript)로 전달될 초기 날짜 데이터입니다.
selected_dates_from_component = _my_calendar_component(
    selected_dates=["2025-06-15", "2025-06-20"], # 초기 선택된 날짜 (예시)
    key="my_unique_calendar_instance"
)

# 4. 컴포넌트에서 반환된 값을 표시합니다.
# 사용자가 달력에서 날짜를 클릭하면, index.html의 Streamlit.setComponentValue()를 통해
# 파이썬으로 다시 값이 전달되고, 이 변수에 저장됩니다.
st.write("달력 컴포넌트에서 선택된 날짜:", selected_dates_from_component)

st.write("---")
st.write("여기는 app.py의 다른 내용입니다.")
st.button("다른 버튼")
