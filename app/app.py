import streamlit as st
from app.early_reemployment import early_reemployment_app
from app.remote_assignment import remote_assignment_app
from app.wage_delay import wage_delay_app
from app.unemployment_recognition import unemployment_recognition_app
from app.questions import get_employment_questions, get_self_employment_questions, get_remote_assignment_questions, get_wage_delay_questions

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")
    
    # Apply custom CSS
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.title("💼 실업급여 도우미")

    # Sidebar search functionality
    with st.sidebar:
        st.markdown("### 🔍 검색")
        search_query = st.text_input("메뉴 또는 질문을 검색하세요", key="search_query")
        
        # Menu and question definitions
        menus = {
            "수급자격": ["임금 체불 판단", "원거리 발령 판단"],
            "실업인정": ["실업인정"],
            "취업촉진수당": ["조기재취업수당"]
        }
        all_questions = {
            "임금 체불 판단": get_wage_delay_questions(),
            "원거리 발령 판단": get_remote_assignment_questions(),
            "실업인정": [],  # Unemployment recognition questions are placeholder
            "조기재취업수당": get_employment_questions() + get_self_employment_questions()
        }

        # Filter menus based on search query
        filtered_menus = {}
        selected_sub_menu = None
        if search_query:
            search_query = search_query.lower()
            for main_menu, sub_menus in menus.items():
                filtered_sub_menus = [
                    sub for sub in sub_menus
                    if search_query in sub.lower() or
                    any(search_query in q.lower() for q in all_questions.get(sub, []))
                ]
                if filtered_sub_menus or search_query in main_menu.lower():
                    filtered_menus[main_menu] = filtered_sub_menus
                for sub in sub_menus:
                    if search_query in sub.lower() or any(search_query in q.lower() for q in all_questions.get(sub, [])):
                        selected_sub_menu = sub
                        st.session_state.selected_menu = main_menu
                        break
                if selected_sub_menu:
                    break
        else:
            filtered_menus = menus

        # Main menu selection
        if filtered_menus:
            menu = st.selectbox("📌 메뉴를 선택하세요", list(filtered_menus.keys()), key="main_menu")
            if filtered_menus[menu]:
                sub_menu = st.radio("📋 하위 메뉴", filtered_menus[menu], key="sub_menu")
            else:
                st.warning("검색 결과에 해당하는 하위 메뉴가 없습니다.")
                sub_menu = None
        else:
            st.warning("검색 결과에 해당하는 메뉴가 없습니다.")
            menu = None
            sub_menu = None

    st.markdown("---")

    # Call functions based on menu selection
    if menu == "수급자격" and sub_menu:
        if sub_menu == "임금 체불 판단":
            wage_delay_app()
        elif sub_menu == "원거리 발령 판단":
            remote_assignment_app()
    elif menu == "실업인정" and sub_menu:
        if sub_menu == "실업인정":
            unemployment_recognition_app()
    elif menu == "취업촉진수당" and sub_menu:
        if sub_menu == "조기재취업수당":
            early_reemployment_app()

    # Auto-call function based on search query
    if search_query and selected_sub_menu:
        if selected_sub_menu == "임금 체불 판단":
            wage_delay_app()
        elif selected_sub_menu == "원거리 발령 판단":
            remote_assignment_app()
        elif selected_sub_menu == "실업인정":
            unemployment_recognition_app()
        elif selected_sub_menu == "조기재취업수당":
            early_reemployment_app()

    st.markdown("---")
    st.caption("ⓒ 2025 실업급여 도우미. 실제 수급 가능 여부는 고용센터 판단을 기준으로 합니다.")
    st.markdown("[나의 지역 고용센터 찾기](https://www.work24.go.kr/cm/c/d/0190/retrieveInstSrchLst.do)에서 자세한 정보를 확인하세요.")

if __name__ == "__main__":
    main()