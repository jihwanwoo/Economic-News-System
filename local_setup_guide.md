# 🖥️ 로컬 PC에서 실행하기 가이드

## 방법 1: SCP로 파일 복사

### Windows (PowerShell)
```powershell
# 프로젝트 폴더 생성
mkdir C:\economic_news_system
cd C:\economic_news_system

# EC2에서 전체 프로젝트 복사
scp -r -i "C:\path\to\your-key.pem" ec2-user@[EC2-IP]:/home/ec2-user/projects/ABP/economic_news_system/* .
```

### Mac/Linux
```bash
# 프로젝트 폴더 생성
mkdir ~/economic_news_system
cd ~/economic_news_system

# EC2에서 전체 프로젝트 복사
scp -r -i ~/.ssh/your-key.pem ec2-user@[EC2-IP]:/home/ec2-user/projects/ABP/economic_news_system/* .
```

## 방법 2: rsync 사용 (더 효율적)

### Mac/Linux
```bash
# 초기 동기화
rsync -avz -e "ssh -i ~/.ssh/your-key.pem" \
  ec2-user@[EC2-IP]:/home/ec2-user/projects/ABP/economic_news_system/ \
  ~/economic_news_system/

# 업데이트 시 (변경된 파일만 동기화)
rsync -avz --delete -e "ssh -i ~/.ssh/your-key.pem" \
  ec2-user@[EC2-IP]:/home/ec2-user/projects/ABP/economic_news_system/ \
  ~/economic_news_system/
```

## 방법 3: GitHub 사용 (권장)

### EC2에서 GitHub에 푸시
```bash
cd /home/ec2-user/projects/ABP/economic_news_system

# Git 설정 (처음만)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 변경사항 커밋
git add .
git commit -m "Update economic news system"
git push origin main
```

### 로컬에서 클론
```bash
# 로컬 PC에서
git clone https://github.com/your-username/economic_news_system.git
cd economic_news_system
```

## 로컬 환경 설정

### 1. Python 가상환경 생성
```bash
# Python 3.8+ 필요
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 로컬에 복사하거나 새로 생성:
```bash
# .env 파일 내용
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
ALPHA_VANTAGE_API_KEY=your_api_key
FRED_API_KEY=your_fred_key
AWS_DEFAULT_REGION=us-east-1
```

### 4. AWS 자격 증명 설정
```bash
# AWS CLI 설치 및 설정
pip install awscli
aws configure
```

### 5. 시스템 테스트
```bash
python test_integrated_dashboard.py
```

### 6. Streamlit 실행
```bash
streamlit run integrated_dashboard.py
```

### 7. 브라우저 접속
자동으로 브라우저가 열리거나 `http://localhost:8501` 접속
