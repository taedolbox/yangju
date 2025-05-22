import streamlit as st

# -------- 메인 앱 실행 -------- #

def early_reemployment_app():
    st.subheader("🟢 조기재취업수당 요건 판단")

    if "early_step" not in st.session_state:
        st.session_state.early_step = 0
        st.session_state.early_answers = []
        st.session_state.employment_type = None
        st.session_state.early_questions = []
        st.session_state.show_results = False

    # 첫 질문 처리
    if st.session_state.early_step == 0:
        q = "새 일자리가 일반 회사 취업인가요, 자영업/특수고용직(예: 예술인, 노무제공자)인가요?"
        st.write(f"**질문: {q}**")
        ans = st.radio("답변", ["일반 회사 취업", "자영업/특수고용직"], key="early_q0")
        if st.button("다음", key="early_next_0"):
            st.session_state.employment_type = ans
            st.session_state.early_answers.append(ans)
            st.session_state.early_questions = get_employment_questions() if ans == "일반 회사 취업" else get_self_employment_questions()
            st.session_state.early_step += 1
            st.rerun()
    elif st.session_state.early_step <= len(st.session_state.early_questions):
        q_idx = st.session_state.early_step - 1
        q = st.session_state.early_questions[q_idx]
        # 디버깅 출력
        st.write(f"**디버깅**: 경로: {st.session_state.employment_type}, "
                 f"문항 수: {len(st.session_state.early_questions)}, "
                 f"early_step: {st.session_state.early_step}, "
                 f"현재 문항: {q}, "
                 f"답변: {st.session_state.early_answers}")
        st.write(f"**Q{st.session_state.early_step}: {q}**")
        ans = st.radio("답변", ["예", "아니요"], key=f"early_q{st.session_state.early_step}")
        if st.button("다음", key=f"early_next_{st.session_state.early_step}"):
            st.session_state.early_answers.append(ans)
            st.session_state.early_step += 1
            st.rerun()
    elif not st.session_state.show_results:
        st.write("**모든 문항에 답변하였습니다. 결과를 확인하려면 아래 버튼을 클릭하세요.**")
        if st.button("결과 보기", key="early_show_result"):
            st.session_state.show_results = True
            st.rerun()
    else:
        questions = st.session_state.early_questions
        answers = st.session_state.early_answers[1:]  # 첫 항목(취업 유형)은 제외
        if st.session_state.employment_type == "일반 회사 취업":
            required_answers = ["예", "예", "예", "예", "아니요", "아니요", "아니요", "아니요", "아니요", "아니요"]
        else:
            required_answers = ["예", "예", "예", "아니요", "예", "아니요"]

        mismatches = [
            (i + 1, q, a, r) for i, (q, a, r) in enumerate(zip(questions, answers, required_answers)) if a != r
        ]

        if not mismatches:
            st.success("✅ 모든 조건을 충족하였습니다. 고용센터에 확인 및 청구를 진행하세요.")
        else:
            st.warning("❌ 아래 조건을 충족하지 못했습니다:")
            for i, q, a, r in mismatches:
                st.write(f"- Q{i+1}: {q} (답변: {a}, 요구: {r})")
            st.write("고용센터에 문의하여 추가 확인이 필요합니다.")

    if st.button("처음으로", key="early_reset"):
        for key in ["early_step", "early_answers", "employment_type", "early_questions", "show_results"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def remote_assignment_app():
    st.subheader("🟠 원거리 발령에 따른 판단")
    questions = get_remote_assignment_questions()

    if "remote_step" not in st.session_state:
        st.session_state.remote_step = 0
        st.session_state.remote_answers = []

    if st.session_state.remote_step < len(questions):
        q = questions[st.session_state.remote_step]
        st.write(f"**Q{st.session_state.remote_step + 1}. {q}**")
        ans = st.radio("답변", ["예", "아니요"], key=f"remote_{st.session_state.remote_step}")
        if st.button("다음", key=f"next_remote_{st.session_state.remote_step}"):
            st.session_state.remote_answers.append(ans)
            if st.session_state.remote_step == 0 and ans == "아니요":
                st.warning("❌ 통근시간 조건 불충족으로 지급 불가")
                st.session_state.remote_step = len(questions)
            else:
                st.session_state.remote_step += 1
            st.rerun()
    else:
        st.success("✅ 조건 충족 가능. 서류 지참 후 고용센터 방문하여 판단 받으세요.")

    if st.button("처음으로", key="reset_remote"):
        st.session_state.remote_step = 0
        st.session_state.remote_answers = []
        st.rerun()

def wage_delay_app():
    st.subheader("🔴 임금 체불에 의한 판단")
    questions = get_wage_delay_questions()

    if "wage_step" not in st.session_state:
        st.session_state.wage_step = 0
        st.session_state.wage_answers = []

    if st.session_state.wage_step < len(questions):
        q = questions[st.session_state.wage_step]
        st.write(f"**Q{st.session_state.wage_step + 1}. {q}**")
        ans = st.radio("답변", ["예", "아니요"], key=f"wage_{st.session_state.wage_step}")
        if st.button("다음", key=f"next_wage_{st.session_state.wage_step}"):
            st.session_state.wage_answers.append(ans)
            if (st.session_state.wage_step == 0 or st.session_state.wage_step == 2) and ans == "아니요":
                st.warning("❌ 수급 요건이 부족할 수 있습니다.\n임금 체불을 명확히 입증하거나 추가 상담 필요.")
                st.session_state.wage_step = len(questions)
            else:
                st.session_state.wage_step += 1
            st.rerun()
    else:
        st.success("✅ 실업급여 수급 가능성이 있습니다.\n체불 입증 자료와 함께 고용노동청 또는 고용센터에 문의하세요.")

    if st.button("처음으로", key="reset_wage"):
        st.session_state.wage_step = 0
        st.session_state.wage_answers = []
        st.rerun()

def unemployment_recognition_app():
    st.subheader("🔵 실업인정 요건 판단")
    st.write("이 기능은 실업인정 요건을 판단하는 데 도움을 줍니다. 현재는 플레이스홀더입니다.")
    st.info("실업인정 요건 판단 기능은 추후 구현 예정입니다. 고용센터에 문의하세요.")
    if st.button("처음으로", key="reset_unemployment"):
        st.rerun()

def main():
    st.set_page_config(page_title="실업급여 지원 시스템", page_icon="💼", layout="centered")
    
    # 커스텀 스타일링
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stRadio>label {
        font-size: 16px;
        color: #333;
    }
    .stMarkdown, .stSuccess, .stWarning {
        font-family: 'Nanum Gothic', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("💼 실업급여 도우미")

    # 사이드바 검색 기능
    with st.sidebar:
        st.markdown("### 🔍 검색")
        search_query = st.text_input("메뉴 또는 질문을 검색하세요", key="search_query")
        
        # 메뉴와 질문 정의
        menus = {
            "수급자격": ["임금 체불 판단", "원거리 발령 판단"],
            "실업인정": ["실업인정"],
            "취업촉진수당": ["조기재취업수당"]
        }
        all_questions = {
            "임금 체불 판단": get_wage_delay_questions(),
            "원거리 발령 판단": get_remote_assignment_questions(),
            "실업인정": [],  # 실업인정 질문은 플레이스홀더로 비어 있음
            "조기재취업수당": get_employment_questions() + get_self_employment_questions()
        }

        # 검색어로 필터링된 메뉴와 하위 메뉴
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
            # 검색어와 가장 관련 있는 하위 메뉴 자동 선택
            for main_menu, sub_menus in menus.items():
                for sub in sub_menus:
                    if search_query in sub.lower() or any(search_query in q.lower() for q in all_questions.get(sub, [])):
                        selected_sub_menu = sub
                        st.session_state.selected_menu = main_menu
                        break
                if selected_sub_menu:
                    break
        else:
            filtered_menus = menus

        # 대분류 메뉴 선택
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

    # 메뉴에 따른 기능 호출
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

    # 검색어와 관련된 기능 자동 호출
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
    st.markdown("[고용센터 안내](https://www.work.go.kr)에서 자세한 정보를 확인하세요.")

# -------- 공통 질문 함수들 -------- #

def get_employment_questions():
    return [
        "14일 대기기간 이후에 새 일자리에 취업을 했나요?",
        "실업급여를 받을 수 있는 기간(소정급여일수)의 절반 이상이 남아 있나요?",
        "단절없이 12개월 이상 계속해서 일을 했나요?",
        "사업장이 바뀌었다면, 단절 없이 12개월 이상 계속 근무했나요?",
        "이전에 일했던 마지막 회사에 재고용 되거나 관련 사업주(합병, 사업 양도 등)에 다시 채용되었나요?",
        "실업급여 신청 전에 이미 채용이 확정되었나요?",
        "최근 2년 안에 조기재취업수당을 받은 적이 있나요?",
        "실업급여를 부정한 방법으로 받으려 했나요?",
        "현재 월급(세전)이 5,740,000원을 초과하나요?",
        "국가 또는 지방 공무원으로 임용되었나요?"
    ]

def get_self_employment_questions():
    return [
        "14일 대기기간 이후에 사업을 시작했나요?",
        "실업급여를 받을 수 있는 기간(소정급여일수)의 절반 이상이 남아 있나요?",
        "12개월 이상 계속해서 사업을 영위했나요?",
        "최근 2년 안에 조기재취업수당을 받은 적이 있나요?",
        "자영업이나 특수고용직으로 취업했다면, 자영업 준비활동으로 실업인정을 받은 사실이 있나요?",
        "실업급여를 부정한 방법으로 받으려 했나요?"
    ]

def get_remote_assignment_questions():
    return [
        "통근시간이 출퇴근 합산 3시간 이상 소요되었나요?",
        "원거리 발령 확인서, 발령장 등 서류를 제출할 수 있나요?",
        "교통카드 사용 내역을 제출할 수 있나요? (해당 없으면 예)",
        "자차 증빙 자료를 제출할 수 있나요? (해당 없으면 예)",
        "통근 차량 노선표를 제출할 수 있나요? (해당 없으면 예)",
        "기숙사 이용 불가 사유를 제출할 수 있나요? (해당 없으면 예)"
    ]

def get_wage_delay_questions():
    return [
        "임금 체불로 인해 자발적 퇴사를 하였나요?",
        "사업주에게 체불 사실을 명확히 요구했으나 해결되지 않았나요?",
        "근로계약서, 급여명세서, 통장사본 등 체불 입증 자료를 보유하고 있나요?",
        "관할 고용노동청에 진정을 제기했거나, 진정 계획이 있나요?",
        "퇴사 후 실업 신고를 했나요?",
    ]

# -------- 앱 실행 -------- #

if __name__ == "__main__":
    main()