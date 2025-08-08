#!/usr/bin/env python3
"""
통합 경제 뉴스 시스템 실행 스크립트
데이터 모니터링 + 이벤트 감지 + Slack 알림 + 기사 작성을 통합 실행
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    """메인 실행 함수"""
    print("🤖 경제 뉴스 통합 시스템 시작")
    print("=" * 50)
    
    # 프로젝트 루트 디렉토리로 이동
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 환경 변수 확인
    print("📋 환경 설정 확인 중...")
    
    required_env_vars = [
        'SLACK_WEBHOOK_URL',
        'ALPHA_VANTAGE_API_KEY',
        'AWS_DEFAULT_REGION'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 다음 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
        print("💡 .env 파일을 확인하거나 환경 변수를 설정해주세요.")
        return
    
    print("✅ 환경 설정 완료")
    
    # 의존성 확인
    print("📦 의존성 확인 중...")
    try:
        import streamlit
        import plotly
        import pandas
        import requests
        from dotenv import load_dotenv
        print("✅ 필수 패키지 확인 완료")
    except ImportError as e:
        print(f"❌ 필수 패키지 누락: {e}")
        print("💡 다음 명령어로 설치하세요: pip install -r requirements.txt")
        return
    
    # Streamlit 대시보드 실행
    print("🚀 통합 대시보드 실행 중...")
    print("📱 브라우저에서 http://localhost:8501 로 접속하세요")
    print("⏹️  종료하려면 Ctrl+C를 누르세요")
    print("=" * 50)
    
    try:
        # Streamlit 실행
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "integrated_dashboard.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️  시스템이 종료되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit 실행 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")

if __name__ == "__main__":
    main()
