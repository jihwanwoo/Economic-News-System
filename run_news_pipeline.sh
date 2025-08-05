#!/bin/bash

# 경제 뉴스 자동 생성 파이프라인 실행 스크립트

echo "🚀 경제 뉴스 자동 생성 파이프라인 시작"
echo "=================================================="

# 현재 디렉토리 확인
if [ ! -f "run_full_pipeline.py" ]; then
    echo "❌ run_full_pipeline.py 파일을 찾을 수 없습니다."
    echo "올바른 디렉토리에서 실행해주세요."
    exit 1
fi

# Python 가상환경 확인 (선택사항)
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ 가상환경 활성화됨: $VIRTUAL_ENV"
else
    echo "⚠️ 가상환경이 활성화되지 않았습니다."
fi

# AWS 자격증명 확인
if aws sts get-caller-identity >/dev/null 2>&1; then
    echo "✅ AWS 자격증명 확인됨"
else
    echo "❌ AWS 자격증명을 확인할 수 없습니다."
    echo "aws configure를 실행하여 자격증명을 설정해주세요."
    exit 1
fi

echo ""
echo "📊 파이프라인 실행 중..."
echo "=================================================="

# 파이프라인 실행
python run_full_pipeline.py "$@"

# 실행 결과 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 파이프라인 실행 완료!"
    echo "📁 결과 파일은 output/ 디렉토리에서 확인하세요."
    
    # 최신 결과 파일 표시
    if [ -d "output" ]; then
        echo ""
        echo "📄 생성된 파일:"
        ls -la output/ | grep "$(date +%Y%m%d)" | tail -5
    fi
else
    echo ""
    echo "❌ 파이프라인 실행 실패"
    echo "로그를 확인하여 문제를 해결해주세요."
    exit 1
fi
