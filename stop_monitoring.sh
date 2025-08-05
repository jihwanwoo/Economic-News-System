#!/bin/bash

# Slack 경제 알림 모니터링 중지 스크립트

echo "🔚 Slack 경제 알림 모니터링 중지"
echo "================================"

cd /home/ec2-user/projects/ABP/economic_news_system

# PID 파일 확인
if [ -f "logs/monitoring.pid" ]; then
    PID=$(cat logs/monitoring.pid)
    
    # 프로세스가 실행 중인지 확인
    if ps -p $PID > /dev/null 2>&1; then
        echo "📋 모니터링 프로세스 발견 (PID: $PID)"
        echo "🔄 프로세스 종료 중..."
        
        # 프로세스 종료
        kill $PID
        
        # 종료 확인
        sleep 2
        if ps -p $PID > /dev/null 2>&1; then
            echo "⚠️  정상 종료되지 않아 강제 종료합니다..."
            kill -9 $PID
        fi
        
        echo "✅ 모니터링 프로세스가 종료되었습니다."
        
        # PID 파일 삭제
        rm -f logs/monitoring.pid
        
    else
        echo "ℹ️  PID 파일은 있지만 프로세스가 실행되지 않고 있습니다."
        rm -f logs/monitoring.pid
    fi
else
    echo "ℹ️  PID 파일을 찾을 수 없습니다."
fi

# 관련 프로세스 모두 확인 및 종료
PROCESSES=$(pgrep -f "start_slack_monitoring.py")
if [ ! -z "$PROCESSES" ]; then
    echo "🔄 관련 프로세스 추가 종료 중..."
    pkill -f "start_slack_monitoring.py"
    echo "✅ 모든 관련 프로세스가 종료되었습니다."
fi

echo ""
echo "📊 현재 상태:"
if pgrep -f "start_slack_monitoring.py" > /dev/null; then
    echo "🔴 아직 실행 중인 프로세스가 있습니다."
    echo "   수동 확인: ps aux | grep start_slack_monitoring"
else
    echo "🟢 모든 모니터링 프로세스가 중지되었습니다."
fi

echo ""
echo "🚀 다시 시작하려면: ./start_background_monitoring.sh"
