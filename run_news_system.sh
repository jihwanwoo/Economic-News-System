#!/bin/bash

# 경제 뉴스 시스템 통합 실행 스크립트

echo "🚀 경제 뉴스 자동 생성 시스템 시작"
echo "=================================================="

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# Python 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    echo "📦 가상환경 활성화 중..."
    source venv/bin/activate
fi

# 환경 변수 확인
echo "🔑 환경 변수 확인 중..."
if [ -z "$AWS_DEFAULT_REGION" ]; then
    export AWS_DEFAULT_REGION=us-east-1
    echo "  ✅ AWS_DEFAULT_REGION 설정: $AWS_DEFAULT_REGION"
fi

if [ -z "$ALPHA_VANTAGE_API_KEY" ]; then
    echo "  ⚠️ ALPHA_VANTAGE_API_KEY가 설정되지 않음"
else
    echo "  ✅ ALPHA_VANTAGE_API_KEY 설정됨"
fi

if [ -z "$SLACK_WEBHOOK_URL" ]; then
    echo "  ⚠️ SLACK_WEBHOOK_URL이 설정되지 않음 (Slack 알림 비활성화)"
else
    echo "  ✅ SLACK_WEBHOOK_URL 설정됨"
fi

# 출력 디렉토리 생성
echo "📁 출력 디렉토리 확인 중..."
mkdir -p output/automated_articles
mkdir -p output/charts
mkdir -p output/images
mkdir -p streamlit_articles
mkdir -p logs
echo "  ✅ 출력 디렉토리 준비 완료"

# 메인 시스템 실행
echo ""
echo "🔄 전체 시스템 실행 중..."
echo "  1️⃣ 경제 데이터 모니터링"
echo "  2️⃣ 이벤트 감지"
echo "  3️⃣ 기사 작성 (데이터 분석 + 차트 생성)"
echo "  4️⃣ 기사 검수"
echo "  5️⃣ 이미지 생성"
echo "  6️⃣ 광고 추천 (3개)"
echo "  7️⃣ Streamlit 페이지 생성"
echo "  8️⃣ Slack 알림 전송"
echo ""

python run_complete_news_system.py

# 실행 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 시스템 실행 완료!"
    echo ""
    echo "📊 생성된 파일 확인:"
    
    # 최신 생성된 파일들 표시
    if [ -d "output/automated_articles" ] && [ "$(ls -A output/automated_articles)" ]; then
        echo "  📰 기사: $(ls -t output/automated_articles/*.json 2>/dev/null | head -1 | xargs basename 2>/dev/null || echo '없음')"
    fi
    
    if [ -d "output/charts" ] && [ "$(ls -A output/charts)" ]; then
        chart_count=$(ls output/charts/*.html 2>/dev/null | wc -l)
        echo "  📈 차트: ${chart_count}개"
    fi
    
    if [ -d "output/images" ] && [ "$(ls -A output/images)" ]; then
        image_count=$(ls output/images/*.png 2>/dev/null | wc -l)
        echo "  🖼️ 이미지: ${image_count}개"
    fi
    
    if [ -d "streamlit_articles" ] && [ "$(ls -A streamlit_articles)" ]; then
        latest_streamlit=$(ls -t streamlit_articles/article_*.py 2>/dev/null | head -1)
        if [ -n "$latest_streamlit" ]; then
            echo "  🌐 Streamlit: $(basename "$latest_streamlit")"
            echo ""
            echo "💡 생성된 기사 확인하기:"
            echo "   streamlit run $latest_streamlit"
        fi
    fi
    
    echo ""
    echo "📋 추가 명령어:"
    echo "  • 최신 기사 보기: ./run_latest_article.sh"
    echo "  • 시스템 상태 확인: python test_strands_system.py"
    echo "  • 로그 확인: tail -f logs/complete_system_$(date +%Y%m%d).log"
    
else
    echo ""
    echo "❌ 시스템 실행 실패"
    echo "📋 문제 해결:"
    echo "  • 로그 확인: tail logs/complete_system_$(date +%Y%m%d).log"
    echo "  • 환경 변수 확인: python check_env.py"
    echo "  • 시스템 테스트: python test_strands_system.py"
fi

echo "=================================================="
