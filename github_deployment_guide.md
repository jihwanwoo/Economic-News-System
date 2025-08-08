# 🐙 GitHub을 통한 로컬 실행 가이드

## 1️⃣ EC2에서 GitHub에 업로드

```bash
# 프로젝트 디렉토리에서
cd /home/ec2-user/projects/ABP/economic_news_system

# Git 초기화 (아직 안했다면)
git init
git add .
git commit -m "Add Intelligence Dashboard"

# GitHub 리포지토리 생성 후
git remote add origin https://github.com/your-username/economic-news-system.git
git push -u origin main
```

## 2️⃣ 로컬 컴퓨터에서 클론 및 실행

```bash
# 로컬 컴퓨터에서
git clone https://github.com/your-username/economic-news-system.git
cd economic-news-system

# Python 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# API 키 설정
export ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3

# Streamlit 실행
streamlit run streamlit_intelligence_dashboard.py
```

## 3️⃣ 필요한 파일들

### requirements.txt
```
streamlit
plotly
pandas
requests
aiohttp
yfinance
feedparser
numpy
textblob
```

### .env 파일 (선택사항)
```
ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3
```

### .gitignore
```
__pycache__/
*.pyc
.env
logs/
output/
venv/
```
