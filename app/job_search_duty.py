# app/job_search_duty.py

import streamlit as st

def job_search_duty_app():
    st.markdown(
        """
        <style>
        .duty-section {
            background-color: #f9f9f9;
            border-left: 5px solid #2196F3;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .duty-section h3 {
            color: #0d47a1;
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 20px;
        }
        .duty-section p {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .duty-item {
            background-color: #ffffff;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
        }
        .duty-item .icon {
            font-size: 24px;
            margin-right: 15px;
            color: #4CAF50; /* Green for accepted */
        }
        .duty-item .icon-warning {
            color: #FFC107; /* Amber for warning */
        }
        .duty-item .icon-reject {
            color: #F44336; /* Red for not accepted */
        }
        .duty-item .text {
            flex-grow: 1;
            font-size: 16px;
            font-weight: 500;
        }
        .proof-box {
            background-color: #fff3e0; /* Light orange */
            border-left: 5px solid #ff9800; /* Orange */
            padding: 15px;
            margin-top: 20px;
            border-radius: 5px;
            font-size: 15px;
            line-height: 1.6;
        }
        .proof-box strong {
            color: #e65100; /* Darker orange */
        }

        /* Dark mode compatibility */
        html[data-theme="dark"] .duty-section {
            background-color: #2e303d;
            border-left-color: #64B5F6;
        }
        html[data-theme="dark"] .duty-section h3 {
            color: #90CAF9;
        }
        html[data-theme="dark"] .duty-section p {
            color: #FAFAFA;
        }
        html[data-theme="dark"] .duty-item {
            background-color: #31333F;
            border-color: #4B4B4B;
        }
        html[data-theme="dark"] .duty-item .text {
            color: #FAFAFA;
        }
        html[data-theme="dark"] .proof-box {
            background-color: #4A3C2E; /* Darker orange for dark mode */
            border-left-color: #FFB74D; /* Lighter orange for dark mode */
            color: #FAFAFA;
        }
        html[data-theme="dark"] .proof-box strong {
            color: #FFCC80; /* Lighter orange for dark mode */
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align: center; color: #0d47a1;'>🔍 실업급여 구직 활동 의무 안내</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown(
        """
        <p style='font-size:17px; line-height:1.6; text-align: center;'>
            실업급여 수급은 **적극적인 재취업 노력**이 필수입니다.<br>
            아래에서 구직 활동의 범위와 제출 서류를 확인하고 <b>꼼꼼히 준비하세요!</b>
        </p>
        """, unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown("<h3>1. 구직 활동이란? (✅ 인정되는 활동)</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="duty-section">
            <p>실업급여를 받기 위해 **새로운 일자리를 찾으려는 노력**을 말합니다. 주로 다음과 같은 활동들이 인정됩니다.</p>
            <div class="duty-item">
                <span class="icon">📝</span><span class="text">워크넷, 채용사이트(사람인, 잡코리아 등)를 통한 **입사 지원**</span>
            </div>
            <div class="duty-item">
                <span class="icon">🤝</span><span class="text">회사 면접에 **실제 참여**</span>
            </div>
            <div class="duty-item">
                <span class="icon">💼</span><span class="text">채용 박람회 또는 채용 설명회 **참가**</span>
            </div>
            <div class="duty-item">
                <span class="icon">🎓</span><span class="text">고용센터가 인정하는 **직업 훈련 과정 수강**</span>
            </div>
            <div class="duty-item">
                <span class="icon">💡</span><span class="text">고용센터 주관 **취업 특강/상담 프로그램 참여**</span>
            </div>
            <div class="duty-item">
                <span class="icon">📈</span><span class="text">자영업 준비 활동 (고용센터 사전 승인 및 계획서 제출 필수)</span>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("<h3>2. 구직 활동 외 활동이란? (⚠️ 추가 노력, ❌ 불인정 활동)</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="duty-section">
            <p>재취업에 도움이 되지만, **단독으로는 구직 활동으로 인정되기 어려운 활동**이거나, **아예 인정되지 않는 활동**입니다. 주의가 필요해요.</p>
            <div class="duty-item">
                <span class="icon icon-warning">🔍</span><span class="text">**단순히 채용 공고를 검색**하거나 열람만 하는 활동</span>
            </div>
            <div class="duty-item">
                <span class="icon icon-warning">✉️</span><span class="text">회사명, 담당자 정보 불분명한 **형식적인 입사 지원**</span>
            </div>
            <div class="duty-item">
                <span class="icon icon-reject">🚫</span><span class="text">이력서/자기소개서 작성만 하고 **제출하지 않은 경우**</span>
            </div>
            <div class="duty-item">
                <span class="icon icon-reject">❌</span><span class="text">고용센터 **사전 승인 없는 자격증 학원 수강**</span>
            </div>
            <div class="duty-item">
                <span class="icon icon-reject">⛔</span><span class="text">친척, 지인 회사에 **형식적으로 제출한 경우**</span>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("<h3>3. 구직 활동 증빙 서류는? (꼼꼼히 준비!)</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="proof-box">
            <p>활동 내용에 따라 제출해야 하는 증빙 서류가 다릅니다. **정확하고 객관적인 증빙**이 가장 중요합니다. 아래를 꼭 확인하세요!</p>
            <ul>
                <li><strong>온라인 입사 지원:</strong> 워크넷 또는 취업포털(사람인, 잡코리아 등)의 **'입사 지원 확인 내역'** 페이지 캡쳐본</li>
                <li><strong>이메일/우편/방문 지원:</strong> 채용 공고문, 회사 사업자등록번호, 회사 담당자 명함 또는 연락처, 입사 지원 확인서 등</li>
                <li><strong>면접 참여:</strong> 면접 확인서, 면접 참석 확인 문자/메일, 담당자 명함 등</li>
                <li><strong>취업 특강/상담:</strong> 교육 수료증, 수강 확인증 또는 고용센터 전산 확인</li>
                <li><strong>직업 훈련:</strong> 훈련기관의 출석부, 수료증 또는 훈련내역 확인서</li>
                <li><strong>채용 박람회:</strong> 참가 확인증, 업체 면담 확인서 등</li>
            </ul>
            <p style="margin-top:10px;">
                💡 <strong>팁:</strong> 증빙 서류는 **정확한 날짜, 회사명, 담당자 정보, 직종**이 명확하게 기재되어야 합니다.<br>
                헷갈리는 경우, 미리 관할 고용센터에 문의하여 확인하는 것이 가장 안전합니다.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown(
        """
        <p style='font-size:15px; text-align: center; color: #555;'>
            더 자세한 내용은 고용보험 홈페이지 또는 관할 고용센터에 문의해주세요.<br>
            ☎️ 고용노동부 고객상담센터: <b>국번없이 1350</b>
        </p>
        """, unsafe_allow_html=True
    )
