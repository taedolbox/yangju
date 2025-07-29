import streamlit as st

def job_search_faq_app():
    """
    근로, 취업 및 산재 내역을 Streamlit 위젯으로 렌더링합니다.
    '근로내역 입력' 상세 필드는 숨기고 질문과 라디오 버튼만 표시합니다.
    """
    st.markdown("""
    <style>
        /* CSS는 그대로 유지하되, 일부 선택자 조정 */
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        h2 {
            color: #003087;
            text-align: center;
            margin-bottom: 20px;
        }
        .step {
            margin-bottom: 15px;
            padding: 10px;
            background: #f9f9f9;
            border-left: 4px solid #003087;
        }
        .form-group {
            margin-bottom: 10px;
        }
        label {
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }
        /* Streamlit 기본 라디오 버튼 스타일 */

        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .question-text {
            font-size: 0.9em;
        }
        .sub-text {
            font-size: 0.8em;
        }
        .bold-question {
            font-weight: bold;
        }
        /* Streamlit의 기본 스타일 위에 덮어쓰기 */
        html, body {
            background-color: transparent !important;
            margin: 0 !important;
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True) # CSS는 st.markdown으로 적용

    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h2>근로, 취업 및 산재 내역</h2>', unsafe_allow_html=True)

    # --- 1. 근로 또는 노무제공 내역 ---
    st.markdown('<div class="step">', unsafe_allow_html=True)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label>근로 또는 노무제공 내역</label>', unsafe_allow_html=True)
    st.markdown(
        '<p class="question-text"><span class="bold-question">실업 인정 대상 기간 중 어떠한 형태로든(소득 발생 여부와 관계 없이) 근로 또는 노무를 제공하거나 수당이 발생하는 회의 참석, 자문 등을 한 사실이 있습니까?</span></p>',
        unsafe_allow_html=True
    )

    # '예/아니오' 라디오 버튼
    has_work = st.radio(
        "선택하세요:", # 라디오 버튼 위 텍스트를 숨기려면 빈 문자열을 사용
        options=("예", "아니오"),
        key="workStatus_radio", # 위젯 고유 키
        horizontal=True # 가로로 배치
    )

    # '예'를 선택했을 때만 나타나는 상세 내역 (이번 요청에서는 다시 숨김)
    # 이전 HTML의 workDetails div의 내용이 사라지도록 조건문을 제거하거나, 빈 컨테이너로 대체
    # if has_work == "예":
    #     with st.container(border=True):
    #         st.markdown('<label>근로내역 입력</label>', unsafe_allow_html=True)
    #         st.text_input("근로 내용 입력", placeholder="근로 내용 입력", key="workDescription")
    #         st.number_input("일 소득액", placeholder="일 소득액", key="dailyIncome", min_value=0)
    #         # 아래 3가지 기준은 전체 문맥상 필요하므로, 이 부분에서는 제외

    # 근로내역 설명 (3가지 기준)을 다시 추가
    st.markdown("<p>근로를 제공하거나 소득이 발생한 사실이 있는 경우 근로내역을 입력하십시오.</p>", unsafe_allow_html=True)
    st.markdown("<p>일 소득액이 구직급여 일액 이상인 경우에 해당 근로일에 대한 구직급여 일액이 감액됩니다. (일용근로자의 경우, 일 소득액과 무관하게 해당 근로일에 대한 구직급여 일액 감액).</p>", unsafe_allow_html=True)
    st.markdown("<p>1개월간 60시간(주 15시간) 이상으로 근로 계약을 하고 일한 경우 또는 1개월간 60시간 미만이라 하더라도, 3개월 이상 계속하여 일하기로 한 경우 취업으로 인정됩니다.</p>", unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True) # form-group 닫기
    st.markdown('</div>', unsafe_allow_html=True) # step 닫기

    # --- 2. 취업 내역 ---
    st.markdown('<div class="step">', unsafe_allow_html=True)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label>취업 내역</label>', unsafe_allow_html=True)
    st.markdown(
        '<p class="question-text"><span class="bold-question">실업인정 대상 기간 중 취업(예정)이거나 개인 사업을 개시하셨습니까?</span></p>',
        unsafe_allow_html=True
    )
    st.radio(
        "취업 여부:", # 라디오 버튼 위 텍스트를 숨기려면 빈 문자열 사용
        options=("예", "아니오"),
        key="employmentStatus_radio",
        horizontal=True
    )
    st.markdown('<p class="sub-text">취업 예정으로 신고하고자 하는 경우에는 관할 센터로 문의하시기 바랍니다.</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">임대사업자 중 근로자가 발생하면 취업으로 인정됩니다. 관할센터로 문의하시기 바랍니다.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # form-group 닫기
    st.markdown('</div>', unsafe_allow_html=True) # step 닫기

    # --- 3. 산재 휴업급여 수급권 ---
    st.markdown('<div class="step">', unsafe_allow_html=True)
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    st.markdown('<label>산재 휴업급여 수급권</label>', unsafe_allow_html=True)
    st.markdown(
        '<p class="question-text"><span class="bold-question">산재 휴업급여를 지급받고 있거나 수급권을 가지고 있습니까?</span></p>',
        unsafe_allow_html=True
    )
    st.radio(
        "산재 여부:", # 라디오 버튼 위 텍스트를 숨기려면 빈 문자열 사용
        options=("예", "아니오"),
        key="injuryStatus_radio",
        horizontal=True
    )
    st.markdown('<p class="sub-text">행정심판(심사청구) 또는 행정소송 등을 통해 소급하여 산재 요양이 승인되어 휴업급여 지급 대상이 되거나 지급받은 경우에는 실업급여를 지급받을 수 없고, 지급받은 실업급여는 반환하여야 합니다.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # form-group 닫기
    st.markdown('</div>', unsafe_allow_html=True) # step 닫기

    st.markdown('</div>', unsafe_allow_html=True) # container 닫기
