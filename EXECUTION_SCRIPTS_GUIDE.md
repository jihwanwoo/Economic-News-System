# 🚀 경제 뉴스 자동 생성 시스템 실행 가이드

## 📋 주요 실행 스크립트 목록

### 🎯 **1. 전체 자동화 시스템 (추천)**

#### 🔥 **가장 완전한 실행**
```bash
# 전체 자동화 테스트 (이벤트 감지 → 기사 생성 → Slack 알림)
python test_full_automation.py
```
**포함 기능:**
- ✅ 이벤트 자동 감지
- ✅ 데이터 분석 및 차트 생성
- ✅ AI 기사 작성
- ✅ 이미지 생성
- ✅ 기사 검수
- ✅ 광고 추천
- ✅ Streamlit 페이지 생성
- ✅ Slack 다중 메시지 전송

#### 🎭 **오케스트레이터 직접 실행**
```bash
# 통합 오케스트레이터 에이전트 실행
python agents/orchestrator_agent.py
```

### 🎨 **2. Streamlit 대시보드**

#### 📊 **기본 대시보드**
```bash
# 기본 Streamlit 대시보드
python demo_streamlit.py
# 또는
python run_streamlit.py
```

#### 🌐 **종합 대시보드**
```bash
# 종합 대시보드 (여러 페이지)
python streamlit_comprehensive_dashboard.py
# 또는
./start_comprehensive_dashboard.sh
```

#### 🔗 **SSH 터널과 함께 실행**
```bash
# SSH 터널을 통한 외부 접근
./start_streamlit_tunnel.sh
```

### 📱 **3. Slack 알림 시스템**

#### ⚡ **즉시 Slack 알림 테스트**
```bash
# Slack 알림 기능 테스트
python demo_slack_alerts.py
```

#### 🔄 **백그라운드 모니터링**
```bash
# 백그라운드 모니터링 시작
./start_background_monitoring.sh

# 상태 확인
./check_monitoring_status.sh

# 모니터링 중지
./stop_monitoring.sh
```

#### 📧 **Slack 연결 테스트**
```bash
# Slack 웹훅 연결 테스트
python test_slack_connection.py
```

### 🔍 **4. 개별 컴포넌트 테스트**

#### 🧪 **시스템 전체 테스트**
```bash
# 전체 시스템 상태 확인
python test_system.py

# AWS 연결만 테스트
python test_system.py aws

# 데이터 수집만 테스트
python test_system.py data
```

#### 📊 **이벤트 감지 테스트**
```bash
# 고급 이벤트 감지 시스템
python demo_advanced_events.py

# 이벤트 감지 + Slack 시스템
python event_detection_slack_system.py
```

### 🛠️ **5. 개발 및 디버깅**

#### 🔧 **메인 파이프라인**
```bash
# 기본 파이프라인 실행
python main.py --mode full

# 특정 모드 실행
python main.py --mode data          # 데이터 수집만
python main.py --mode article       # 기사 작성만
```

#### 📈 **완전한 파이프라인**
```bash
# 전체 파이프라인 (구버전)
python run_full_pipeline.py

# 완전한 시스템 (신버전)
python run_complete_system.py
```

### 🚀 **6. 빠른 시작 스크립트**

#### ⚡ **원클릭 실행**
```bash
# 빠른 시작 (모든 설정 자동)
./quick_start.sh
```

#### 🔄 **뉴스 파이프라인**
```bash
# 뉴스 생성 파이프라인
./run_news_pipeline.sh
```

---

## 📝 **실행 순서 추천**

### 🥇 **초보자용 (처음 실행)**
```bash
# 1. 시스템 상태 확인
python test_system.py

# 2. Slack 연결 테스트
python test_slack_connection.py

# 3. 전체 시스템 실행
python test_full_automation.py

# 4. Streamlit 대시보드 확인
python demo_streamlit.py
```

### 🥈 **일반 사용자용**
```bash
# 1. 전체 자동화 실행
python test_full_automation.py

# 2. 대시보드에서 결과 확인
python streamlit_comprehensive_dashboard.py
```

### 🥉 **고급 사용자용**
```bash
# 1. 백그라운드 모니터링 시작
./start_background_monitoring.sh

# 2. 대시보드 실행
./start_comprehensive_dashboard.sh

# 3. 상태 모니터링
./check_monitoring_status.sh
```

---

## 🔧 **환경 설정 확인**

### 📋 **필수 환경 변수**
```bash
# 환경 변수 확인
python check_env.py

# AWS 설정 확인
python test_aws_quick.py
```

### 🔑 **API 키 설정 확인**
```bash
# Alpha Vantage API 테스트
python test_alphavantage_simple.py

# FRED API 테스트
python test_fred_connection.py
```

---

## 📊 **출력 결과 확인**

### 📁 **생성된 파일 위치**
- **기사 파일**: `output/automated_articles/`
- **차트 이미지**: `output/images/`
- **Streamlit 페이지**: `streamlit_articles/`
- **로그 파일**: `logs/`

### 🔗 **접근 URL**
- **로컬 Streamlit**: `http://localhost:8501`
- **SSH 터널**: `http://localhost:8501` (터널 설정 후)

---

## ⚠️ **문제 해결**

### 🚨 **일반적인 오류**
```bash
# AWS 자격 증명 문제
aws configure list

# Python 패키지 문제
pip install -r requirements.txt

# 포트 충돌 문제
lsof -i :8501
```

### 📞 **도움말**
```bash
# 각 스크립트의 도움말
python main.py --help
python test_system.py --help
```

---

## 🎯 **권장 실행 명령어**

### 🔥 **가장 추천하는 실행 방법**
```bash
# 터미널 1: 전체 자동화 시스템
python test_full_automation.py

# 터미널 2: Streamlit 대시보드
python streamlit_comprehensive_dashboard.py

# 터미널 3: 백그라운드 모니터링 (선택사항)
./start_background_monitoring.sh
```

이렇게 실행하면:
1. 📰 자동으로 경제 기사가 생성됩니다
2. 📱 Slack에 알림이 전송됩니다
3. 🌐 웹 대시보드에서 결과를 확인할 수 있습니다
4. 📊 실시간 모니터링이 가능합니다

---

**💡 팁**: 처음 실행할 때는 `python test_full_automation.py`를 사용하여 전체 시스템이 정상 작동하는지 확인한 후, 필요에 따라 다른 스크립트들을 사용하세요!
