# 실업급여 도우미

Streamlit 기반 실업급여 자격 판단 애플리케이션

## 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash
streamlit run app/app.py
```

## 디렉토리 구조
- app/app.py: 메인 애플리케이션
- app/early_reemployment.py: 조기재취업수당 로직
- app/remote_assignment.py: 원거리 발령 로직
- app/wage_delay.py: 임금 체불 로직
- app/unemployment_recognition.py: 실업인정 로직
- app/questions.py: 공통 질문 함수
- static/styles.css: 스타일링
- requirements.txt: 의존성
- README.md: 프로젝트 설명

## 주의
- `Nanum Gothic` 폰트는 `styles.css`에서 CDN으로 로드됩니다.
- Streamlit 1.36.0 이상 사용 권장.