#!/bin/bash

# 가장 최근 생성된 뉴스 기사 Streamlit 페이지 실행

echo "🚀 가장 최근 뉴스 기사 페이지를 실행합니다..."

# streamlit_articles 디렉토리로 이동
cd /home/ec2-user/projects/ABP/economic_news_system

# 가장 최근 파일 찾기
LATEST_ARTICLE=$(ls -t streamlit_articles/article_*.py 2>/dev/null | head -n 1)

if [ -z "$LATEST_ARTICLE" ]; then
    echo "❌ 생성된 기사가 없습니다."
    echo "💡 먼저 다음 명령어로 기사를 생성하세요:"
    echo "   python test_full_automation.py"
    exit 1
fi

echo "📰 실행할 기사: $(basename "$LATEST_ARTICLE")"
echo "🌐 URL: http://localhost:8501"
echo "⏹️  중지하려면 Ctrl+C를 누르세요"
echo "=" * 50

# Streamlit 실행
streamlit run "$LATEST_ARTICLE" --server.port 8501
