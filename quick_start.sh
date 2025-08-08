#!/bin/bash

# 경제 뉴스 자동 생성 시스템 - 빠른 시작 스크립트

echo "🤖 경제 뉴스 자동 생성 시스템 - 빠른 시작"
echo "================================================"

# 현재 디렉토리 확인
if [ ! -f "run_complete_system.py" ]; then
    echo "❌ 프로젝트 루트 디렉토리에서 실행해주세요."
    exit 1
fi

# Python 버전 확인
python_version=$(python3 --version 2>&1)
echo "🐍 Python 버전: $python_version"

# 가상환경 활성화 (있는 경우)
if [ -d "/home/ec2-user/dl_env" ]; then
    echo "🔧 dl_env 가상환경 활성화 중..."
    source /home/ec2-user/dl_env/bin/activate
elif [ -d "venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "🔧 가상환경 활성화 중..."
    source .venv/bin/activate
fi

# 환경 변수 로드 (.env 파일이 있는 경우)
if [ -f ".env" ]; then
    echo "⚙️ 환경 변수 로드 중..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Slack 웹훅 URL 자동 로드
if [ -f "config/slack_webhook.txt" ]; then
    echo "📱 Slack 웹훅 URL 로드 중..."
    export SLACK_WEBHOOK_URL=$(cat config/slack_webhook.txt)
    echo "✅ Slack 웹훅 설정 완료"
fi

# AWS 자격증명 확인 (configure 파일 우선)
echo "🔍 AWS 자격증명 확인 중..."

# configure 파일에서 AWS 자격증명 로드
if [ -f "configure" ]; then
    echo "📄 configure 파일에서 AWS 자격증명 로드 중..."
    
    # configure 파일에서 AWS 자격증명 추출
    if grep -q "\[aws\]" configure; then
        export AWS_ACCESS_KEY_ID=$(grep "aws_access_key_id" configure | cut -d'=' -f2 | tr -d ' ')
        export AWS_SECRET_ACCESS_KEY=$(grep "aws_secret_access_key" configure | cut -d'=' -f2 | tr -d ' ')
        export AWS_DEFAULT_REGION=$(grep "aws_default_region" configure | cut -d'=' -f2 | tr -d ' ')
        
        if [ ! -z "$AWS_ACCESS_KEY_ID" ] && [ ! -z "$AWS_SECRET_ACCESS_KEY" ]; then
            echo "✅ configure 파일에서 AWS 자격증명 로드 완료"
            echo "   Access Key: ${AWS_ACCESS_KEY_ID:0:10}..."
            echo "   Region: $AWS_DEFAULT_REGION"
        else
            echo "❌ configure 파일에 AWS 자격증명이 불완전합니다"
            exit 1
        fi
    else
        echo "❌ configure 파일에 [aws] 섹션이 없습니다"
        exit 1
    fi
else
    echo "⚠️  configure 파일이 없습니다. AWS CLI 자격증명을 확인합니다..."
    
    # 기존 AWS CLI 확인 로직
    if command -v aws &> /dev/null; then
        aws_identity=$(timeout 10s aws sts get-caller-identity 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "✅ AWS CLI 자격증명 확인됨"
            account_id=$(echo "$aws_identity" | grep -o '"Account": "[^"]*"' | cut -d'"' -f4)
            user_arn=$(echo "$aws_identity" | grep -o '"Arn": "[^"]*"' | cut -d'"' -f4)
            echo "   계정: $account_id"
            echo "   사용자: $(basename "$user_arn")"
        else
            echo "❌ AWS 자격증명 설정이 필요합니다"
            echo "   1. configure 파일을 생성하거나"
            echo "   2. aws configure 명령을 실행하세요"
            exit 1
        fi
    else
        echo "❌ AWS CLI가 설치되지 않았고 configure 파일도 없습니다."
        exit 1
    fi
fi

# Slack 웹훅 테스트
if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
    echo "🔍 Slack 연결 테스트 중..."
    test_response=$(timeout 10s curl -s -X POST -H 'Content-type: application/json' \
        --data '{"text":"🚀 경제 뉴스 시스템 시작 - 연결 테스트"}' \
        "$SLACK_WEBHOOK_URL" 2>/dev/null)
    
    if [ "$test_response" = "ok" ]; then
        echo "✅ Slack 연결 테스트 성공!"
    elif [ "$test_response" = "no_service" ]; then
        echo "⚠️  Slack 웹훅이 비활성화됨 (no_service)"
        echo "   → setup_slack_webhook.md 가이드를 참조하여 새 웹훅을 생성하세요"
        echo "   → 시스템은 Slack 알림 없이 계속 실행됩니다"
    else
        echo "⚠️  Slack 연결 응답: ${test_response:-'연결 실패'}"
        echo "   → Slack 알림이 작동하지 않을 수 있습니다"
    fi
else
    echo "⚠️  Slack 웹훅 URL이 설정되지 않았습니다"
    echo "   → config/slack_webhook.txt 파일을 확인하거나"
    echo "   → SLACK_WEBHOOK_URL 환경변수를 설정하세요"
fi

# 메뉴 표시
echo ""
echo "🎯 실행할 모드를 선택하세요:"
echo "1. 🚀 전체 시스템 (뉴스 생성 + Slack 알림)"
echo "2. 🤖 AI 뉴스 생성만"
echo "3. 📊 이벤트 모니터링만"
echo "4. 📱 Slack 알림만"
echo "5. 📈 Streamlit 대시보드"
echo "6. 🧪 시스템 테스트"
echo "7. ⚙️ 초기 설정"
echo "8. 🔄 대화형 모드"
echo "0. 종료"

read -p "선택하세요 (0-8): " choice

case $choice in
    1)
        echo "🚀 전체 시스템 실행 중..."
        python3 run_complete_system.py --mode full
        ;;
    2)
        echo "🤖 AI 뉴스 생성 실행 중..."
        python3 run_complete_system.py --mode news-only
        ;;
    3)
        echo "📊 이벤트 모니터링 실행 중..."
        python3 run_complete_system.py --mode monitoring-only
        ;;
    4)
        echo "📱 Slack 알림 실행 중..."
        python3 run_complete_system.py --mode slack-only
        ;;
    5)
        echo "📈 Streamlit 대시보드 실행 중..."
        python3 run_complete_system.py --mode dashboard
        ;;
    6)
        echo "🧪 시스템 테스트 실행 중..."
        python3 run_complete_system.py --mode test
        ;;
    7)
        echo "⚙️ 초기 설정 실행 중..."
        python3 run_complete_system.py --mode setup
        ;;
    8)
        echo "🔄 대화형 모드 시작..."
        python3 run_complete_system.py --interactive
        ;;
    0)
        echo "👋 종료합니다."
        exit 0
        ;;
    *)
        echo "❌ 잘못된 선택입니다."
        exit 1
        ;;
esac

echo ""
echo "✅ 실행 완료!"
echo "📄 로그 파일: logs/complete_system_$(date +%Y%m%d).log"
echo "📁 출력 파일: output/ 디렉토리 확인"
