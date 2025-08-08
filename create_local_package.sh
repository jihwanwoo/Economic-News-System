#!/bin/bash

# 로컬 PC용 설치 패키지 생성 스크립트

echo "📦 로컬 PC용 설치 패키지 생성 중..."

# 패키지 디렉토리 생성
PACKAGE_DIR="economic_news_local_package"
mkdir -p $PACKAGE_DIR

# 필수 파일들 복사
echo "📋 필수 파일 복사 중..."

# Python 파일들
cp *.py $PACKAGE_DIR/
cp -r agents/ $PACKAGE_DIR/
cp -r data_monitoring/ $PACKAGE_DIR/
cp -r notifications/ $PACKAGE_DIR/
cp -r utils/ $PACKAGE_DIR/
cp -r config/ $PACKAGE_DIR/
cp -r streamlit_app/ $PACKAGE_DIR/

# 설정 파일들
cp requirements.txt $PACKAGE_DIR/
cp .env.example $PACKAGE_DIR/.env
cp README.md $PACKAGE_DIR/

# 로컬 실행용 스크립트 생성
cat > $PACKAGE_DIR/setup_local.sh << 'EOF'
#!/bin/bash

echo "🖥️ 경제 뉴스 시스템 로컬 설치"
echo "=============================="

# Python 버전 확인
python_version=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ -z "$python_version" ]]; then
    echo "❌ Python 3이 설치되지 않았습니다."
    echo "   Python 3.8 이상을 설치해주세요."
    exit 1
fi

echo "✅ Python $python_version 감지됨"

# 가상환경 생성
echo "🔧 가상환경 생성 중..."
python3 -m venv venv

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 의존성 설치
echo "📦 의존성 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt

# 환경 변수 설정 안내
echo ""
echo "⚙️ 환경 변수 설정이 필요합니다:"
echo "   .env 파일을 편집하여 다음 값들을 설정하세요:"
echo "   - SLACK_WEBHOOK_URL"
echo "   - AWS 자격 증명"
echo "   - API 키들"

echo ""
echo "✅ 설치가 완료되었습니다!"
echo ""
echo "🚀 실행 방법:"
echo "   1. .env 파일 편집"
echo "   2. ./run_local.sh 실행"
EOF

# 로컬 실행 스크립트 생성
cat > $PACKAGE_DIR/run_local.sh << 'EOF'
#!/bin/bash

echo "🚀 경제 뉴스 시스템 실행"
echo "======================"

# 가상환경 활성화
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 환경 변수 확인
if [ ! -f ".env" ]; then
    echo "❌ .env 파일이 없습니다."
    echo "   .env.example을 .env로 복사하고 설정을 완료해주세요."
    exit 1
fi

# 시스템 테스트
echo "🔍 시스템 테스트 중..."
python test_integrated_dashboard.py

if [ $? -eq 0 ]; then
    echo "✅ 테스트 통과!"
    echo "🌐 Streamlit 대시보드 시작 중..."
    streamlit run integrated_dashboard.py
else
    echo "❌ 테스트 실패. 설정을 확인해주세요."
fi
EOF

# Windows용 배치 파일 생성
cat > $PACKAGE_DIR/run_local.bat << 'EOF'
@echo off
echo 🚀 경제 뉴스 시스템 실행
echo ======================

REM 가상환경 활성화
call venv\Scripts\activate

REM 환경 변수 확인
if not exist ".env" (
    echo ❌ .env 파일이 없습니다.
    echo    .env.example을 .env로 복사하고 설정을 완료해주세요.
    pause
    exit /b 1
)

REM 시스템 테스트
echo 🔍 시스템 테스트 중...
python test_integrated_dashboard.py

if %errorlevel% equ 0 (
    echo ✅ 테스트 통과!
    echo 🌐 Streamlit 대시보드 시작 중...
    streamlit run integrated_dashboard.py
) else (
    echo ❌ 테스트 실패. 설정을 확인해주세요.
    pause
)
EOF

# 실행 권한 부여
chmod +x $PACKAGE_DIR/setup_local.sh
chmod +x $PACKAGE_DIR/run_local.sh

# README 파일 생성
cat > $PACKAGE_DIR/LOCAL_README.md << 'EOF'
# 🖥️ 경제 뉴스 시스템 - 로컬 실행 가이드

## 🚀 빠른 시작

### 1단계: 설치
```bash
# Linux/Mac
./setup_local.sh

# Windows
setup_local.bat
```

### 2단계: 환경 설정
`.env` 파일을 편집하여 필요한 설정을 완료하세요:
- Slack 웹훅 URL
- AWS 자격 증명
- API 키들

### 3단계: 실행
```bash
# Linux/Mac
./run_local.sh

# Windows
run_local.bat
```

### 4단계: 브라우저 접속
자동으로 브라우저가 열리거나 `http://localhost:8501` 접속

## 📋 시스템 요구사항
- Python 3.8 이상
- 인터넷 연결
- 최소 4GB RAM

## 🛠️ 문제 해결
- 의존성 오류: `pip install -r requirements.txt` 재실행
- 포트 충돌: 다른 8501 포트 사용 프로그램 종료
- AWS 오류: `aws configure` 실행하여 자격 증명 설정

## 📞 지원
문제가 발생하면 로그 파일을 확인하거나 GitHub 이슈를 생성해주세요.
EOF

# 압축 파일 생성
echo "📦 압축 파일 생성 중..."
tar -czf economic_news_local_package.tar.gz $PACKAGE_DIR/

echo "✅ 로컬 설치 패키지가 생성되었습니다!"
echo "📁 패키지 위치: $PACKAGE_DIR/"
echo "📦 압축 파일: economic_news_local_package.tar.gz"
echo ""
echo "🚀 사용 방법:"
echo "1. 압축 파일을 로컬 PC로 다운로드"
echo "2. 압축 해제 후 setup_local.sh 실행"
echo "3. .env 파일 설정"
echo "4. run_local.sh 실행"
