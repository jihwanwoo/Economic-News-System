#!/bin/bash

# 통합 경제 뉴스 시스템 시작 스크립트

echo "🤖 경제 뉴스 통합 시스템 시작"
echo "=================================="

# 프로젝트 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    echo "📦 가상환경 활성화 중..."
    source venv/bin/activate
fi

# 환경 변수 로드
if [ -f ".env" ]; then
    echo "⚙️  환경 변수 로드 중..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env 파일이 없습니다. 환경 변수를 확인하세요."
fi

# Python 경로 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 통합 대시보드 실행
echo "🚀 통합 대시보드 실행 중..."
echo "📱 브라우저에서 http://localhost:8501 로 접속하세요"
echo "⏹️  종료하려면 Ctrl+C를 누르세요"
echo "=================================="

python3 run_integrated_dashboard.py
