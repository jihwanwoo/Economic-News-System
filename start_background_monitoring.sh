#!/bin/bash

# Slack 경제 알림 백그라운드 모니터링 시작 스크립트

echo "🚀 Slack 경제 알림 백그라운드 모니터링 시작"
echo "============================================"

# 프로젝트 디렉토리로 이동
cd /home/ec2-user/projects/ABP/economic_news_system

# 웹훅 URL 환경변수 설정
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/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"

# 로그 디렉토리 생성
mkdir -p logs

# 기존 프로세스 확인
if pgrep -f "start_slack_monitoring.py" > /dev/null; then
    echo "⚠️  이미 실행 중인 모니터링 프로세스가 있습니다."
    echo "기존 프로세스를 종료하시겠습니까? (y/N): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🔄 기존 프로세스 종료 중..."
        pkill -f "start_slack_monitoring.py"
        sleep 2
    else
        echo "❌ 실행을 취소합니다."
        exit 1
    fi
fi

# 백그라운드에서 모니터링 시작
echo "📱 백그라운드 모니터링 시작..."
nohup python3 start_slack_monitoring.py > logs/background_monitoring.log 2>&1 &

# 프로세스 ID 저장
echo $! > logs/monitoring.pid

echo "✅ 백그라운드 모니터링이 시작되었습니다!"
echo "📋 프로세스 ID: $(cat logs/monitoring.pid)"
echo "📄 로그 파일: logs/background_monitoring.log"
echo ""
echo "📊 상태 확인: tail -f logs/background_monitoring.log"
echo "🔚 중지 방법: ./stop_monitoring.sh"
echo ""
echo "🎉 이제 Slack으로 실시간 경제 알림을 받으실 수 있습니다!"
