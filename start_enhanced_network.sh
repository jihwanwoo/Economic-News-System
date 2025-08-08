#!/bin/bash

echo "🚀 개선된 경제 네트워크 분석 대시보드 시작"
echo "============================================"

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 가상환경 활성화됨"
fi

# 필요한 패키지 확인 및 설치
echo "📦 필요한 패키지 확인 중..."
pip install -q streamlit plotly networkx textblob pandas numpy

# Streamlit 실행
echo "🌐 Streamlit 대시보드 실행 중..."
echo "📍 URL: http://localhost:8501"
echo "🔧 종료하려면 Ctrl+C를 누르세요"
echo ""

streamlit run run_enhanced_network_dashboard.py --server.port 8501 --server.address 0.0.0.0
