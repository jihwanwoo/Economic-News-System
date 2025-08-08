#!/bin/bash

echo "📱 실제 Reddit 데이터 기반 네트워크 분석 대시보드 시작"
echo "=================================================="

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "❌ .env 파일이 없습니다."
    echo "Reddit API 키를 설정해주세요."
    exit 1
fi

# Reddit API 키 확인
if ! grep -q "REDDIT_CLIENT_ID" .env; then
    echo "❌ .env 파일에 REDDIT_CLIENT_ID가 설정되지 않았습니다."
    exit 1
fi

if ! grep -q "REDDIT_CLIENT_SECRET" .env; then
    echo "❌ .env 파일에 REDDIT_CLIENT_SECRET이 설정되지 않았습니다."
    exit 1
fi

echo "✅ Reddit API 키 확인 완료"

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 가상환경 활성화됨"
fi

# 필요한 패키지 확인 및 설치
echo "📦 필요한 패키지 확인 중..."
pip install -q streamlit plotly networkx pandas numpy praw python-dotenv

# Reddit 연결 테스트
echo "🔍 Reddit 연결 테스트 중..."
python -c "
from dotenv import load_dotenv
load_dotenv()
from data_monitoring.real_reddit_collector import RealRedditCollector
try:
    collector = RealRedditCollector()
    print('✅ Reddit API 연결 성공')
except Exception as e:
    print(f'❌ Reddit API 연결 실패: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Reddit 연결 테스트 실패"
    echo "🔧 해결 방법:"
    echo "1. .env 파일의 Reddit API 키 확인"
    echo "2. 인터넷 연결 상태 확인"
    echo "3. Reddit API 사용량 제한 확인"
    exit 1
fi

# Streamlit 실행
echo "🌐 실제 Reddit 네트워크 분석 대시보드 실행 중..."
echo "📍 URL: http://localhost:8501"
echo "🔧 종료하려면 Ctrl+C를 누르세요"
echo ""
echo "📱 실제 Reddit 데이터를 사용하여 경제 네트워크를 분석합니다."
echo "🕸️ 8개 경제 서브레딧에서 실시간 데이터를 수집합니다."
echo ""

streamlit run run_real_reddit_network.py --server.port 8501 --server.address 0.0.0.0
