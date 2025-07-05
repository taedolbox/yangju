import streamlit as st

def mobile_device_detect_component():
    html_code = """
    <div>디바이스 정보를 확인 중입니다. 잠시만 기다려주세요...</div>
    <script>
    console.log("디바이스 감지 시작 (모바일 버전)");

    window.onload = function() {
        console.log("페이지 로드 완료");
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        console.log("User Agent:", userAgent);

        const isMobile = /Mobi|Android/i.test(userAgent);
        console.log("모바일 여부:", isMobile);

        if (!isMobile) {
            console.log("PC 페이지로 이동");
            window.location.href = "/pc_app_url";  // PC 앱 URL로 변경
        } else {
            console.log("모바일 페이지 유지");
            // 모바일 버전 페이지 유지 - 현재 페이지
        }
    };
    </script>
    """
    st.components.v1.html(html_code, height=100)
