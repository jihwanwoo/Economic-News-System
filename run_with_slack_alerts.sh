#!/bin/bash

# 경제 뉴스 시스템 + Slack 알림 통합 실행 스크립트

echo "🚀 경제 뉴스 자동 생성 시스템 + Slack 알림"
echo "=================================================="

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# .env 파일 로드 확인
if [ -f ".env" ]; then
    echo "✅ .env 파일 발견"
    source .env
    
    # Slack 웹훅 URL 확인
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        echo "✅ Slack 웹훅 URL 설정됨: ${SLACK_WEBHOOK_URL:0:50}..."
    else
        echo "⚠️ Slack 웹훅 URL이 .env 파일에 설정되지 않음"
    fi
    
    # AWS 설정 확인
    if [ -n "$AWS_DEFAULT_REGION" ]; then
        echo "✅ AWS 리전 설정: $AWS_DEFAULT_REGION"
    else
        export AWS_DEFAULT_REGION=us-east-1
        echo "✅ AWS 리전 기본값 설정: $AWS_DEFAULT_REGION"
    fi
    
else
    echo "❌ .env 파일을 찾을 수 없습니다."
    echo "💡 .env.example을 참조하여 .env 파일을 생성해주세요."
    exit 1
fi

# Python 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    echo "📦 가상환경 활성화 중..."
    source venv/bin/activate
fi

# 출력 디렉토리 생성
echo "📁 출력 디렉토리 확인 중..."
mkdir -p output/automated_articles
mkdir -p output/charts
mkdir -p output/images
mkdir -p streamlit_articles
mkdir -p logs
echo "  ✅ 출력 디렉토리 준비 완료"

# Slack 연결 테스트
echo ""
echo "📱 Slack 연결 테스트 중..."
python -c "
import os
import requests
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv('SLACK_WEBHOOK_URL')

if webhook_url:
    try:
        response = requests.post(webhook_url, json={'text': '🤖 경제 뉴스 시스템 시작 - 연결 테스트'}, timeout=5)
        if response.status_code == 200:
            print('✅ Slack 연결 테스트 성공')
        else:
            print(f'⚠️ Slack 연결 테스트 실패: {response.status_code}')
    except Exception as e:
        print(f'⚠️ Slack 연결 오류: {e}')
else:
    print('⚠️ Slack 웹훅 URL이 설정되지 않음')
"

# 메인 시스템 실행
echo ""
echo "🔄 전체 시스템 실행 중..."
echo "  📊 1단계: 경제 데이터 모니터링 및 이벤트 감지"
echo "  ✍️ 2단계: AI 기사 작성 (데이터 분석 + 차트 + 이미지 + 광고)"
echo "  📢 3단계: Slack 알림 전송"
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
        latest_article=$(ls -t output/automated_articles/*.json 2>/dev/null | head -1)
        if [ -n "$latest_article" ]; then
            echo "  📰 기사: $(basename "$latest_article")"
        fi
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
            echo "💡 생성된 기사 웹에서 보기:"
            echo "   streamlit run $latest_streamlit"
        fi
    fi
    
    # 최신 실행 결과 파일 확인
    latest_result=$(ls -t output/complete_system_execution_*.json 2>/dev/null | head -1)
    if [ -n "$latest_result" ]; then
        echo ""
        echo "📋 실행 결과 요약:"
        python -c "
import json
try:
    with open('$latest_result', 'r', encoding='utf-8') as f:
        result = json.load(f)
    print(f\"  상태: {result.get('status', 'unknown')}\")
    print(f\"  실행 시간: {result.get('execution_time', 0):.1f}초\")
    print(f\"  감지된 이벤트: {result.get('events_detected', 0)}개\")
    print(f\"  생성된 기사: {result.get('articles_generated', 0)}개\")
    print(f\"  Slack 알림: {result.get('slack_notifications', 0)}개\")
    
    # Slack 알림 결과 확인
    slack_results = result.get('slack_results', [])
    success_count = sum(1 for r in slack_results if r.get('status') == 'success')
    if success_count > 0:
        print(f\"  📱 Slack 알림 성공: {success_count}개\")
    else:
        print(f\"  ⚠️ Slack 알림 실패\")
        
except Exception as e:
    print(f\"  결과 파일 읽기 실패: {e}\")
"
    fi
    
    echo ""
    echo "📱 Slack 채널을 확인하여 알림을 확인하세요!"
    echo ""
    echo "📋 추가 명령어:"
    echo "  • 최신 기사 보기: ./run_latest_article.sh"
    echo "  • Slack 알림 테스트: python test_slack_notification.py"
    echo "  • 시스템 상태 확인: python test_agents_system.py"
    echo "  • 로그 확인: tail -f logs/complete_system_$(date +%Y%m%d).log"
    
else
    echo ""
    echo "❌ 시스템 실행 실패"
    echo "📋 문제 해결:"
    echo "  • 로그 확인: tail logs/complete_system_$(date +%Y%m%d).log"
    echo "  • 환경 변수 확인: python check_env.py"
    echo "  • Slack 연결 테스트: python test_slack_notification.py"
    echo "  • 시스템 테스트: python test_agents_system.py"
fi

echo "=================================================="
