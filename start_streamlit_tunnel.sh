#!/bin/bash
# SSH 터널링용 Streamlit 시작 스크립트

echo "🚀 Streamlit Intelligence 대시보드 시작 (SSH 터널링 모드)"
echo "=" * 60

# 프로젝트 디렉토리로 이동
cd /home/ec2-user/projects/ABP/economic_news_system

# 가상환경 활성화
echo "📦 가상환경 활성화 중..."
source /home/ec2-user/dl_env/bin/activate

# API 키 설정
export ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3

echo "🔑 API 키 설정 완료"
echo "📊 대시보드 시작 중..."
echo ""
echo "🌐 접근 방법:"
echo "  로컬 브라우저에서: http://localhost:8501"
echo "  또는: http://127.0.0.1:8501"
echo ""
echo "⚠️ 주의: SSH 터널 연결을 유지하세요!"
echo "🛑 종료: Ctrl+C"
echo ""

# Streamlit 실행 (로컬호스트 모드)
streamlit run streamlit_intelligence_dashboard.py --server.address localhost --server.port 8501
