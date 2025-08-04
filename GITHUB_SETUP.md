# 🚀 GitHub 저장소 설정 가이드

## 📋 현재 상태
✅ Git 저장소 초기화 완료  
✅ 모든 파일 커밋 완료 (33개 파일, 6,820줄)  
✅ 커밋 메시지: "🎉 Initial commit: Economic News AI System with Streamlit Dashboard"

## 🔗 GitHub 저장소 생성 및 연결

### 1단계: GitHub에서 새 저장소 생성
1. GitHub (https://github.com)에 로그인
2. "New repository" 클릭
3. 저장소 정보 입력:
   - **Repository name**: `economic-news-ai-system`
   - **Description**: `AWS Bedrock과 Strands Agent를 활용한 지능형 경제 기사 자동 생성 시스템`
   - **Visibility**: Public (또는 Private)
   - **Initialize**: ❌ README, .gitignore, license 체크 해제 (이미 있음)

### 2단계: 원격 저장소 연결 및 푸시
```bash
# 현재 디렉토리에서 실행
cd /home/ec2-user/projects/ABP/economic_news_system

# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/economic-news-ai-system.git

# 기본 브랜치를 main으로 변경 (선택사항)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3단계: 인증 (필요시)
GitHub 인증이 필요한 경우:
```bash
# Personal Access Token 사용 (추천)
# GitHub Settings > Developer settings > Personal access tokens에서 토큰 생성
# Username: GitHub 사용자명
# Password: 생성한 Personal Access Token

# 또는 SSH 키 사용
ssh-keygen -t ed25519 -C "your_email@example.com"
# 생성된 공개키를 GitHub Settings > SSH and GPG keys에 추가
```

## 📊 저장소 내용

### 📁 주요 디렉토리 구조
```
economic-news-ai-system/
├── agents/                     # 🤖 Multi-agent system
├── streamlit_app/             # 📊 Web dashboard
├── config/                    # ⚙️ Configuration files
├── output/                    # 📄 Generated articles
├── data_monitoring/           # 📈 Data collection
├── logs/                      # 📝 System logs
├── README.md                  # 📖 Project documentation
├── PROJECT_SUMMARY.md         # 📋 Detailed project summary
└── requirements.txt           # 📦 Dependencies
```

### 🎯 주요 기능
- **🤖 Multi-agent System**: AWS Bedrock 기반 지능형 Agent들
- **📊 Streamlit Dashboard**: 인터랙티브 웹 인터페이스
- **📈 Real-time Data**: 실시간 주식 및 경제 데이터 수집
- **📰 AI Article Generation**: Claude 3 Sonnet으로 고품질 기사 생성
- **🖼️ Image Generation**: 자동 일러스트레이션 및 워드클라우드
- **📢 Smart Ads**: 기사 내용 기반 맞춤형 광고 추천

### 📈 성능 지표
- **시스템 테스트**: 6/6 통과 (100%)
- **기사 생성 시간**: 평균 107초
- **품질 점수**: 평균 83/100점
- **데이터 소스**: 11개 주식, 2개 경제지표, 5개 뉴스피드

## 🚀 사용법

### 즉시 실행
```bash
# Streamlit 대시보드 실행
python demo_streamlit.py

# 전체 파이프라인 실행
python main.py --mode full --market-summary

# 시스템 테스트
python test_system.py
```

### 설치
```bash
# 의존성 설치
pip install -r requirements.txt

# AWS 자격 증명 설정
aws configure
```

## 🏷️ 추천 GitHub 태그
`aws-bedrock` `ai-agents` `economic-news` `streamlit` `langchain` `claude-3` `financial-data` `automated-journalism` `data-visualization` `python`

## 📝 라이선스
MIT License (LICENSE 파일 추가 권장)

---

**💡 팁**: 저장소 생성 후 GitHub Actions를 설정하여 자동 테스트 및 배포 파이프라인을 구축할 수 있습니다.
