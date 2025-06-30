import streamlit.components.v1 as components

# 'my_calendar_component' 폴더 안에 'frontend' 폴더 경로를 지정
_COMPONENT_DIR = "my_calendar_component"

# 컴포넌트를 선언합니다.
_component_func = components.declare_component(
    "my_calendar_component", # 컴포넌트 이름
    path=_COMPONENT_DIR      # 프론트엔드 코드가 있는 폴더의 상위 경로
)

# 이제 _component_func를 사용하여 Streamlit 앱에서 커스텀 컴포넌트를 렌더링할 수 있습니다.
# 예를 들어:
# result = _component_func(name="World", key="my_custom_calendar")
