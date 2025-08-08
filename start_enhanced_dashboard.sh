#!/bin/bash
# 강화된 대시보드 시작 스크립트 (실제 FRED 데이터 포함)

echo "🚀 강화된 경제 모니터링 대시보드 시작"
echo "=" * 50

# 프로젝트 디렉토리로 이동
cd /home/ec2-user/projects/ABP/economic_news_system

# 가상환경 활성화
source /home/ec2-user/dl_env/bin/activate

# 환경변수 설정
export ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3
export FRED_API_KEY=d4235fa1b67058fff90f8a9cc43793c8

echo "🔑 API 키 설정 완료"
echo "  Alpha Vantage: ${ALPHA_VANTAGE_API_KEY:0:8}..."
echo "  FRED: ${FRED_API_KEY:0:8}..."
echo ""

echo "📊 데이터 소스:"
echo "  ✅ Alpha Vantage Intelligence API"
echo "  ✅ FRED 경제 데이터 (실제 API)"
echo "  ✅ 강화된 뉴스 & SNS 모니터링"
echo ""

echo "🌐 대시보드 시작 중..."
echo "접근 URL: http://localhost:8501"
echo ""
echo "⚠️ SSH 터널링이 설정되어 있는지 확인하세요!"
echo "🛑 종료: Ctrl+C"
echo ""

# 강화된 대시보드 실행
streamlit run streamlit_enhanced_dashboard.py --server.address localhost --server.port 8501
