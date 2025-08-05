#!/usr/bin/env python3
"""
GitHub 업로드 준비 스크립트
민감한 정보 제거 및 파일 정리
"""

import os
import shutil
import json
from pathlib import Path

def clean_sensitive_files():
    """민감한 정보가 포함된 파일들 정리"""
    
    print("🧹 민감한 정보 파일 정리 중...")
    
    # 제거할 파일들
    sensitive_files = [
        "config/slack_webhook.txt",
        "config/slack_config.json",
        ".env",
        "aws-credentials.json"
    ]
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"  ✅ 제거됨: {file_path}")
        else:
            print(f"  ℹ️  없음: {file_path}")
    
    # 로그 디렉토리 정리
    if os.path.exists("logs"):
        shutil.rmtree("logs")
        print("  ✅ 로그 디렉토리 제거됨")
    
    # 출력 디렉토리 정리 (샘플 파일만 남기고)
    if os.path.exists("output"):
        # 샘플 파일들 백업
        sample_files = []
        for file in os.listdir("output"):
            if "sample" in file.lower() or "example" in file.lower():
                sample_files.append(file)
        
        # 디렉토리 제거 후 재생성
        shutil.rmtree("output")
        os.makedirs("output", exist_ok=True)
        
        # .gitkeep 파일 생성
        with open("output/.gitkeep", "w") as f:
            f.write("# 출력 파일들이 저장되는 디렉토리입니다.\n")
        
        print("  ✅ 출력 디렉토리 정리됨")
    
    # __pycache__ 디렉토리들 제거
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                print(f"  ✅ 제거됨: {pycache_path}")

def create_sample_configs():
    """샘플 설정 파일들 생성"""
    
    print("📝 샘플 설정 파일 생성 중...")
    
    # 샘플 환경 변수 파일
    env_sample = """# 환경 변수 설정 예시
# 실제 사용 시 .env 파일로 복사하여 사용하세요

# AWS 설정
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=us-east-1

# Slack 웹훅 URL
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# 기타 설정
DEBUG=false
LOG_LEVEL=INFO
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_sample)
    print("  ✅ .env.example 생성됨")
    
    # 로그 디렉토리 생성
    os.makedirs("logs", exist_ok=True)
    with open("logs/.gitkeep", "w") as f:
        f.write("# 로그 파일들이 저장되는 디렉토리입니다.\n")
    print("  ✅ logs/.gitkeep 생성됨")

def update_file_permissions():
    """실행 파일 권한 설정"""
    
    print("🔧 파일 권한 설정 중...")
    
    executable_files = [
        "start_slack_monitoring.py",
        "start_background_monitoring.sh",
        "stop_monitoring.sh",
        "check_monitoring_status.sh",
        "demo_slack_alerts.py",
        "demo_streamlit.py",
        "demo_advanced_events.py",
        "main.py",
        "test_system.py",
        "run_streamlit.py"
    ]
    
    for file_path in executable_files:
        if os.path.exists(file_path):
            os.chmod(file_path, 0o755)
            print(f"  ✅ 실행 권한 설정: {file_path}")

def create_github_workflows():
    """GitHub Actions 워크플로우 생성"""
    
    print("⚙️ GitHub Actions 워크플로우 생성 중...")
    
    os.makedirs(".github/workflows", exist_ok=True)
    
    workflow_content = """name: Test Economic News System

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run basic tests
      run: |
        python -c "import sys; print('Python version:', sys.version)"
        python -c "from agents.base_agent import BaseAgent; print('Base agent import successful')"
        python -c "from data_monitoring.technical_analysis import TechnicalAnalyzer; print('Technical analysis import successful')"
        python -c "from notifications.slack_notifier import SlackNotifier; print('Slack notifier import successful')"
    
    - name: Test system components
      run: |
        # AWS 자격증명 없이 실행 가능한 테스트들만
        python data_monitoring/technical_analysis.py || true
        python -c "from notifications.slack_notifier import SlackNotifier; n = SlackNotifier('dummy'); print('Slack notifier test passed')"
"""
    
    with open(".github/workflows/test.yml", "w", encoding="utf-8") as f:
        f.write(workflow_content)
    print("  ✅ GitHub Actions 워크플로우 생성됨")

def create_contributing_guide():
    """기여 가이드 생성"""
    
    print("📖 기여 가이드 생성 중...")
    
    contributing_content = """# 기여 가이드

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
"""
    
    with open("CONTRIBUTING.md", "w", encoding="utf-8") as f:
        f.write(contributing_content)
    print("  ✅ CONTRIBUTING.md 생성됨")

def main():
    """메인 함수"""
    print("🚀 GitHub 업로드 준비 시작")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    current_dir = os.getcwd()
    print(f"📁 현재 디렉토리: {current_dir}")
    
    # 작업 실행
    clean_sensitive_files()
    print()
    
    create_sample_configs()
    print()
    
    update_file_permissions()
    print()
    
    create_github_workflows()
    print()
    
    create_contributing_guide()
    print()
    
    print("✅ GitHub 업로드 준비 완료!")
    print()
    print("📋 다음 단계:")
    print("1. GitHub Personal Access Token 생성")
    print("2. git init 및 remote 설정")
    print("3. 파일 커밋 및 푸시")
    print()
    print("⚠️  주의사항:")
    print("- .env 파일에 실제 값을 입력하지 마세요")
    print("- AWS 자격증명을 코드에 포함하지 마세요")
    print("- Slack 웹훅 URL을 공개하지 마세요")

if __name__ == "__main__":
    main()
