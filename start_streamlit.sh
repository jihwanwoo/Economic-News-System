#!/bin/bash
# Streamlit 자동 실행 스크립트

echo "🚀 Streamlit Intelligence 대시보드 시작"
cd /home/ec2-user/projects/ABP/economic_news_system
source /home/ec2-user/dl_env/bin/activate

export ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3

echo "📊 대시보드 실행 중..."
echo "접근 URL: http://:8501"
echo "로컬 터널: http://localhost:8501"

streamlit run streamlit_intelligence_dashboard.py --server.address 0.0.0.0 --server.port 8501
