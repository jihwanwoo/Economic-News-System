# 기여 가이드

Economic News System 프로젝트에 기여해주셔서 감사합니다!

## 🚀 시작하기

1. 저장소를 포크합니다
2. 새로운 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📋 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/jihwanwoo/Economic-News-System.git
cd Economic-News-System

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 실제 값 입력

# 테스트 실행
python test_system.py
```

## 🧪 테스트

새로운 기능을 추가할 때는 반드시 테스트를 포함해주세요.

```bash
# 기본 테스트
python test_system.py

# 개별 컴포넌트 테스트
python data_monitoring/technical_analysis.py
python notifications/slack_notifier.py
```

## 📝 코딩 스타일

- Python PEP 8 스타일 가이드를 따릅니다
- 함수와 클래스에는 docstring을 작성합니다
- 변수명은 명확하고 의미있게 작성합니다
- 주석은 한국어로 작성합니다

## 🐛 버그 리포트

버그를 발견하셨다면 다음 정보를 포함하여 이슈를 생성해주세요:

- 운영체제 및 Python 버전
- 오류 메시지 전문
- 재현 단계
- 예상 동작과 실제 동작

## 💡 기능 제안

새로운 기능을 제안하실 때는:

- 기능의 목적과 필요성 설명
- 구현 방법에 대한 아이디어
- 관련 예시나 참고 자료

## 📞 문의

질문이나 도움이 필요하시면 GitHub Issues를 통해 문의해주세요.
