#!/usr/bin/env python3
"""
Streamlit 애플리케이션 실행 스크립트
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Streamlit 애플리케이션 실행"""
    
    # 현재 디렉토리를 프로젝트 루트로 설정
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Streamlit 앱 경로
    app_path = "streamlit_app/app.py"
    
    # Streamlit 실행 명령
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.address", "0.0.0.0",
        "--server.port", "8501",
        "--theme.primaryColor", "#1f77b4",
        "--theme.backgroundColor", "#ffffff",
        "--theme.secondaryBackgroundColor", "#f0f2f6",
        "--theme.textColor", "#262730"
    ]
    
    print("🚀 경제 뉴스 AI 대시보드를 시작합니다...")
    print(f"📍 URL: http://localhost:8501")
    print("⏹️  종료하려면 Ctrl+C를 누르세요.")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 대시보드가 종료되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"❌ 실행 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
