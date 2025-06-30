import streamlit.components.v1 as components
import os

# 디렉토리 설정
_RELEASE = True # or False

# Streamlit Cloud 배포 환경을 위한 경로
# my_calendar_component 폴더 안에 frontend 폴더가 있고, 그 안에 index.html이 있으므로
# _COMPONENT_DIR은 'my_calendar_component/frontend'를 가리켜야 합니다.
_COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_calendar_component", "frontend")

# 커스텀 컴포넌트 생성
# now path=_COMPONENT_DIR points to 'my_calendar_component/frontend'
# Streamlit will find index.html directly inside this directory.
_my_calendar_component = components.declare_component(
    "my_calendar_component",
    path=_COMPONENT_DIR
)
