import streamlit as st
from datetime import datetime, timedelta

def early_reemployment_allowance_app():
    # 앱 제목 (일용직 앱과 동일 스타일)
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 조기재취업수당 신청 가능 시점 판단</span>",
        unsafe_allow_html=True
    )

    # 모바일 줌 비활성화 (일용직 앱과 동일)
    st.markdown(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
        unsafe_allow_html=True
    )

    # 입력 섹션
    st.markdown("<h4>🏗️ 입력 정보</h4>", unsafe_allow_html=True)
    employment_date = st.date_input("📅 재취업 날짜")
    allowance_amount = st.number_input("💰 예상 수당 금액", min_value=0, step=10000)

    if st.button("계산"):
        # 결과 출력 (일용직 앱 스타일 반영)
        result_html = """
        <div id='resultContainer'>
            <h3>🏗️ 계산 결과</h3>
            <p>재취업 날짜: """ + str(employment_date) + """</p>
            <p>예상 수당: """ + f"{allowance_amount:,}원" + """</p>
            <p>🏗️ 신청 가능: 조건 충족 시 가능</p>
        </div>
        """
        st.components.v1.html(result_html, height=300)

    # CSS (일용직 앱과 동일)
    css = """
    <style>
    body {
        color: #111;
        touch-action: none; /* 터치 줌 비활성화 */
    }

    #resultContainer {
        color: #111;
        font-size: 16px;
        padding: 10px;
        max-width: 600px;
        margin: 0 auto;
    }

    h3, h4 {
        font-size: 22px; /* 일용직 앱과 동일 */
        font-weight: 600;
        margin: 10px 0;
    }

    p {
        font-size: 16px;
        margin: 10px 0;
    }

    @media (prefers-color-scheme: dark) {
        body {
            color: #ddd;
            background: #000;
        }
        #resultContainer {
            color: #eee;
        }
    }

    @media (max-width: 768px) {
        #resultContainer {
            padding: 8px;
            font-size: 12px;
            max-width: 90vw;
        }
        h3, h4 {
            font-size: 18px;
        }
        p {
            font-size: 12px;
        }
    }

    @media (max-width: 480px) {
        #resultContainer {
            padding: 6px;
            font-size: 12px;
            max-width: 95vw;
        }
        h3, h4 {
            font-size: 16px;
        }
        p {
            font-size: 12px;
        }
    }

    @media (orientation: landscape) and (max-width: 768px) {
        #resultContainer {
            padding: 6px;
            font-size: 12px;
            max-width: 95vw;
        }
        h3, h4 {
            font-size: 18px;
        }
        p {
            font-size: 12px;
        }
    }
    </style>
    """
    st.components.v1.html(css, height=100)
