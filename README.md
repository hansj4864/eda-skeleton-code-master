# EDA 스켈레톤 코드 마스터

월말 EDA 시험을 준비하는 스터디원을 위한 12문제 Streamlit 학습 앱입니다. 결측치, IQR 이상치 처리, 필터링·그룹 요약, 시각화 개념을 초급부터 고급까지 연습할 수 있습니다.

## 로컬 실행

Python 3.12 환경에서 다음 명령을 실행합니다.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 설계 원칙

- 사용자의 자유 Python 코드는 실행하지 않습니다.
- 코드형 문제는 AST로 분석한 뒤 허용된 pandas 연산만 작은 인터프리터로 처리합니다.
- 답안과 진도는 `st.session_state`에만 저장되며 새 브라우저 세션에는 유지되지 않습니다.
- 오류 발생 시 서버 경로나 전체 Traceback을 표시하지 않습니다.

## Community Cloud 배포

1. 저장소를 GitHub에 올립니다.
2. Streamlit Community Cloud에서 저장소와 `app.py`를 선택합니다.
3. Python 3.12를 선택해 배포합니다.
4. 시험 시작 전에 앱에 접속해 휴면 상태를 해제하고 12문제를 한 번씩 확인합니다.

