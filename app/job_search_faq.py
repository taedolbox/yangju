# app/job_search_faq.py

import streamlit as st

def job_search_faq_app():
    """
    근로, 취업 및 산재 내역 HTML 페이지를 Streamlit으로 렌더링합니다.
    """
    # HTML과 CSS를 Streamlit의 st.markdown을 사용하여 직접 렌더링합니다.
    # Javascript는 <script> 태그 안에 그대로 유지합니다.
    st.markdown("""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>근로, 취업 및 산재 내역</title>
        <style>
            body {
                font-family: "맑은 고딕", Malgun Gothic, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5; /* 이 배경색은 Streamlit 앱 전체에 적용되지 않을 수 있습니다 */
            }
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
            .radio-group {
                display: flex;
                align-items: center;
            }
            input[type="radio"] {
                margin-right: 10px;
            }
            .work-details {
                display: none;
                margin-top: 10px;
            }
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
            /* Streamlit 환경에서 body와 html 스타일이 직접 적용되지 않을 수 있으므로,
               container 또는 Streamlit의 기본 요소에 대한 스타일링을 고려해야 합니다. */
            html, body {
                /* Streamlit의 기본 스타일 위에 덮어쓰기 위해 */
                background-color: transparent !important;
                margin: 0 !important;
                padding: 0 !important;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>근로, 취업 및 산재 내역</h2>
            <div class="step">
                <div class="form-group">
                    <label>근로 또는 노무제공 내역</label>
                    <p class="question-text"><span class="bold-question">실업 인정 대상 기간 중 어떠한 형태로든(소득 발생 여부와 관계 없이) 근로 또는 노무를 제공하거나 수당이 발생하는 회의 참석, 자문 등을 한 사실이 있습니까?</span>
                        <div class="radio-group">
                            <input type="radio" id="yesWork" name="workStatus" value="yes" onchange="toggleWorkDetails()">
                            <label for="yesWork">예</label>
                            <input type="radio" id="noWork" name="workStatus" value="no" onchange="toggleWorkDetails()">
                            <label for="noWork">아니오</label>
                        </div>
                    </p>
                </div>
                <div id="workDetails" class="work-details">
                    <label>근로내역 입력</label>
                    <input type="text" id="workDescription" placeholder="근로 내용 입력" required>
                    <input type="number" id="dailyIncome" placeholder="일 소득액" required>
                    <p>근로를 제공하거나 소득이 발생한 사실이 있는 경우 근로내역을 입력하십시오.</p>
                    <p>일 소득액이 구직급여 일액 이상인 경우에 해당 근로일에 대한 구직급여 일액이 감액됩니다. (일용근로자의 경우, 일 소득액과 무관하게 해당 근로일에 대한 구직급여 일액 감액).</p>
                    <p>1개월간 60시간(주 15시간) 이상으로 근로 계약을 하고 일한 경우 또는 1개월간 60시간 미만이라 하더라도, 3개월 이상 계속하여 일하기로 한 경우 취업으로 인정됩니다.</p>
                </div>
            </div>
            <div class="step">
                <div class="form-group">
                    <label>취업 내역</label>
                    <p class="question-text"><span class="bold-question">실업인정 대상 기간 중 취업(예정)이거나 개인 사업을 개시하셨습니까?</span>
                        <div class="radio-group">
                            <input type="radio" id="yesEmployment" name="employmentStatus" value="yes">
                            <label for="yesEmployment">예</label>
                            <input type="radio" id="noEmployment" name="employmentStatus" value="no">
                            <label for="noEmployment">아니오</label>
                        </div>
                    </p>
                    <p class="sub-text">취업 예정으로 신고하고자 하는 경우에는 관할 센터로 문의하시기 바랍니다.</p>
                    <p class="sub-text">임대사업자 중 근로자가 발생하면 취업으로 인정됩니다. 관할센터로 문의하시기 바랍니다.</p>
                </div>
            </div>
            <div class="step">
                <div class="form-group">
                    <label>산재 휴업급여 수급권</label>
                    <p class="question-text"><span class="bold-question">산재 휴업급여를 지급받고 있거나 수급권을 가지고 있습니까?</span>
                        <div class="radio-group">
                            <input type="radio" id="yesInjury" name="injuryStatus" value="yes">
                            <label for="yesInjury">예</label>
                            <input type="radio" id="noInjury" name="injuryStatus" value="no">
                            <label for="noInjury">아니오</label>
                        </div>
                    </p>
                    <p class="sub-text">행정심판(심사청구) 또는 행정소송 등을 통해 소급하여 산재 요양이 승인되어 휴업급여 지급 대상이 되거나 지급받은 경우에는 실업급여를 지급받을 수 없고, 지급받은 실업급여는 반환하여야 합니다.</p>
                </div>
            </div>
        </div>

        <script>
            function toggleWorkDetails() {
                const hasWork = document.querySelector('input[name="workStatus"]:checked')?.value;
                const workDetails = document.getElementById('workDetails');
                workDetails.style.display = hasWork === 'yes' ? 'block' : 'none';
            }
        </script>
    </body>
    </html>
    """, unsafe_allow_html=True)

# 이 파일이 직접 실행될 경우를 위한 코드 (Streamlit에서는 보통 main.py에서 호출되므로 필요 없을 수 있음)
if __name__ == '__main__':
    job_search_faq_app()
