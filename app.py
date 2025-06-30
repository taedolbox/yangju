import streamlit as st
import streamlit.components.v1 as components
import os

# _RELEASE 변수는 개발 환경과 배포 환경을 구분합니다.
# 개발 중에는 False로 설정하여 로컬에서 frontend/index.html을 직접 로드하고,
# 배포 시에는 True로 설정하여 빌드된 컴포넌트를 사용합니다.
_RELEASE = True  # 배포 시에는 True로 설정합니다.

if not _RELEASE:
    # 개발 환경 (로컬)
    # 현재 스크립트(app.py)의 디렉토리에서 'my_calendar_component/frontend'를 찾습니다.
    _COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_calendar_component", "frontend")
    _my_calendar_component = components.declare_component(
        "my_calendar_component",
        path=_COMPONENT_DIR
    )
else:
    # 배포 환경 (Streamlit Cloud)
    # 이 부분은 Streamlit 컴포넌트가 패키지화되었을 때 사용됩니다.
    # 일반적으로 setup.py 등을 통해 패키징된 후 설치될 때의 경로를 가리킵니다.
    # 하지만 Streamlit Cloud에서는 GitHub 리포지토리를 직접 클론하므로,
    # 로컬 개발 환경과 동일하게 상대 경로를 사용하는 것이 일반적입니다.
    # 따라서 _RELEASE가 True일 때도 _COMPONENT_DIR을 동일하게 설정합니다.
    _COMPONENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_calendar_component", "frontend")
    _my_calendar_component = components.declare_component(
        "my_calendar_component",
        path=_COMPONENT_DIR
    )


# Streamlit 앱의 메인 함수
def main():
    st.set_page_config(layout="wide")
    st.title("나의 커스텀 달력 앱")

    st.write("---")
    st.header("Streamlit 기본 날짜 선택 위젯 (비교)")
    st.date_input("날짜를 선택하세요")
    st.write("---")

    st.header("커스텀 달력 컴포넌트")

    # 커스텀 컴포넌트를 호출하고 값을 받습니다.
    # 이 컴포넌트는 selected_date라는 키로 날짜 값을 반환할 것입니다.
    # default는 컴포넌트가 로드되기 전이나 값이 없을 때의 기본값입니다.
    # 컴포넌트의 props (예: 'initial_date')는 여기에 키워드 인수로 전달합니다.
    # 예를 들어, 오늘 날짜를 초기값으로 전달하고 싶다면:
    # my_date_value = _my_calendar_component(initial_date="2025-07-01", key="my_calendar")
    my_date_value = _my_calendar_component(key="my_calendar")

    if my_date_value:
        st.success(f"선택된 날짜: {my_date_value}")
    else:
        st.info("달력에서 날짜를 선택해주세요.")

if __name__ == "__main__":
    main()
