#!/bin/bash

# 완전히 독립적인 경제 뉴스 생성 시스템 실행 스크립트
# OrchestratorStrand 오류 없이 안정적으로 작동

echo "🚀 완전히 독립적인 경제 뉴스 생성 시스템"
echo "=================================================="
echo "✅ OrchestratorStrand 의존성 없음"
echo "✅ 안정적인 독립 실행"
echo "✅ AI 기사 생성 + 차트 + Slack 알림"
echo "=================================================="

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# .env 파일 확인
if [ -f ".env" ]; then
    echo "✅ .env 파일 로드됨"
    source .env
else
    echo "❌ .env 파일을 찾을 수 없습니다."
    exit 1
fi

# 출력 디렉토리 생성
mkdir -p output/standalone_articles
mkdir -p output/standalone_charts
mkdir -p output/standalone_images
mkdir -p output/standalone_data

echo ""
echo "🔄 독립 시스템 실행 중..."
echo "  📊 1단계: 실시간 시장 데이터 수집 (10개 주요 종목)"
echo "  🚨 2단계: 중요 이벤트 감지 (3% 이상 변동)"
echo "  ✍️ 3단계: AI 종합 기사 작성"
echo "  📄 4단계: 고급 HTML 파일 생성"
echo "  📈 5단계: 가격 차트 생성"
echo "  📱 6단계: 향상된 Slack 알림 전송"
echo ""

# 독립 시스템 실행
python complete_standalone_system.py

# 실행 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 독립 시스템 실행 완료!"
    echo ""
    
    # 생성된 HTML 파일 목록
    if [ -d "output/standalone_articles" ] && [ "$(ls -A output/standalone_articles)" ]; then
        echo "📄 생성된 HTML 기사:"
        ls -t output/standalone_articles/*.html 2>/dev/null | head -5 | while read file; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                symbol=$(echo "$filename" | cut -d'_' -f1)
                echo "  📰 $symbol: $filename"
            fi
        done
        
        echo ""
        echo "💡 HTML 기사 보는 방법:"
        latest_html=$(ls -t output/standalone_articles/*.html 2>/dev/null | head -1)
        if [ -n "$latest_html" ]; then
            echo "  🌐 최신 기사: open $latest_html"
            echo "  📱 모든 기사: open output/standalone_articles/"
        fi
    fi
    
    # 차트 파일 확인
    if [ -d "output/standalone_charts" ] && [ "$(ls -A output/standalone_charts)" ]; then
        chart_count=$(ls output/standalone_charts/*.png 2>/dev/null | wc -l)
        echo "  📈 생성된 차트: ${chart_count}개"
    fi
    
    # 시장 데이터 파일
    if [ -d "output/standalone_data" ] && [ "$(ls -A output/standalone_data)" ]; then
        latest_data=$(ls -t output/standalone_data/market_data_*.json 2>/dev/null | head -1)
        if [ -n "$latest_data" ]; then
            echo "  📊 시장 데이터: $(basename "$latest_data")"
        fi
        
        latest_result=$(ls -t output/standalone_data/execution_result_*.json 2>/dev/null | head -1)
        if [ -n "$latest_result" ]; then
            echo "  📋 실행 결과: $(basename "$latest_result")"
        fi
    fi
    
    echo ""
    echo "📱 Slack 채널을 확인하여 3개의 알림을 확인하세요!"
    echo ""
    echo "📋 추가 명령어:"
    echo "  • 다시 실행: ./run_standalone_news.sh"
    echo "  • Slack 테스트: python test_slack_notification.py"
    echo "  • 최신 HTML 보기: open \$(ls -t output/standalone_articles/*.html | head -1)"
    echo "  • 시장 데이터 보기: cat \$(ls -t output/standalone_data/market_data_*.json | head -1) | jq ."
    
else
    echo ""
    echo "❌ 독립 시스템 실행 실패"
    echo "📋 문제 해결:"
    echo "  • AWS 자격 증명 확인: aws sts get-caller-identity"
    echo "  • Bedrock 모델 확인: aws bedrock list-foundation-models --region us-east-1"
    echo "  • Slack 웹훅 테스트: python test_slack_notification.py"
    echo "  • 인터넷 연결 확인"
    echo "  • Python 패키지 확인: pip install -r requirements.txt"
fi

echo "=================================================="
