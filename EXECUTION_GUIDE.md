# 🚀 전체 프로젝트 실행 가이드

경제 뉴스 자동 생성 시스템의 모든 기능을 실행하는 종합 가이드입니다.

## 📋 목차

1. [빠른 시작](#빠른-시작)
2. [실행 모드별 가이드](#실행-모드별-가이드)
3. [Docker 실행](#docker-실행)
4. [시스템 모니터링](#시스템-모니터링)
5. [문제 해결](#문제-해결)

## 🚀 빠른 시작

### 1. 환경 설정 확인
```bash
# 초기 설정 및 환경 확인
python3 run_complete_system.py --mode setup
```

### 2. 간편 실행 (추천)
```bash
# 대화형 메뉴로 실행
./quick_start.sh
```

### 3. 전체 시스템 실행
```bash
# 모든 기능 통합 실행
python3 run_complete_system.py --mode full
```

## 📊 실행 모드별 가이드

### 🎯 **1. 전체 시스템 모드 (`full`)**
모든 기능을 통합하여 실행합니다.

```bash
python3 run_complete_system.py --mode full
```

**실행 과정:**
1. 📊 고도화된 이벤트 감지 (기술적/감정/상관관계 분석)
2. 🤖 AI 뉴스 생성 (AWS Bedrock Claude)
3. 📱 Slack 알림 전송 (우선순위 알림 + 시장 요약)
4. 💾 결과 저장 (JSON + HTML)

**필요 조건:**
- ✅ AWS 자격증명 설정
- ✅ Slack 웹훅 URL 설정

### 🤖 **2. AI 뉴스 생성 모드 (`news-only`)**
AI 기반 경제 뉴스만 생성합니다.

```bash
python3 run_complete_system.py --mode news-only
```

**특징:**
- AWS Bedrock Claude 모델 사용
- 다중 Agent 시스템 (데이터 수집 → 뉴스 작성 → 콘텐츠 최적화)
- HTML 형식으로 출력

### 📊 **3. 이벤트 모니터링 모드 (`monitoring-only`)**
시장 이벤트 감지 및 분석만 수행합니다.

```bash
python3 run_complete_system.py --mode monitoring-only
```

**분석 항목:**
- 📈 기술적 분석 (RSI, MACD, 볼린저 밴드 등 13가지 지표)
- 💭 감정 분석 (뉴스 피드 기반 시장 심리)
- 🔗 상관관계 분석 (시장 간 상관관계 이탈)
- 🔄 섹터 로테이션 감지

### 📱 **4. Slack 알림 모드 (`slack-only`)**
Slack 알림 시스템만 실행합니다.

```bash
python3 run_complete_system.py --mode slack-only
```

**알림 유형:**
- 🚨 긴급 알림 (심각도 0.6 이상)
- 📋 시장 요약 (1시간마다)
- 📰 뉴스 업데이트
- 🔧 시스템 상태

### 📈 **5. 대시보드 모드 (`dashboard`)**
Streamlit 웹 대시보드를 실행합니다.

```bash
python3 run_complete_system.py --mode dashboard
```

**접속:** http://localhost:8501

**기능:**
- 📊 실시간 시장 데이터 차트
- 📰 AI 생성 기사 뷰어
- 🖼️ 자동 이미지 생성
- 📢 맞춤형 광고

### 🧪 **6. 테스트 모드 (`test`)**
시스템 전체 테스트를 실행합니다.

```bash
python3 run_complete_system.py --mode test
```

### ⚙️ **7. 설정 모드 (`setup`)**
초기 설정 및 환경 확인을 수행합니다.

```bash
python3 run_complete_system.py --mode setup
```

## 🔄 대화형 모드

모든 모드를 대화형으로 선택할 수 있습니다.

```bash
# Python 스크립트
python3 run_complete_system.py --interactive

# 또는 간편 스크립트
./quick_start.sh
```

## 🐳 Docker 실행

### Docker로 실행하기

```bash
# 1. Docker 이미지 빌드
docker build -t economic-news-system .

# 2. 환경 변수 파일 생성
cp .env.example .env
# .env 파일 편집하여 실제 값 입력

# 3. Docker 컨테이너 실행
docker run -d \
  --name economic-news \
  --env-file .env \
  -p 8501:8501 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/output:/app/output \
  economic-news-system

# 4. 로그 확인
docker logs -f economic-news
```

### Docker Compose로 실행하기

```bash
# 1. 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 2. 서비스 시작
docker-compose up -d

# 3. 상태 확인
docker-compose ps

# 4. 로그 확인
docker-compose logs -f economic-news-system

# 5. 서비스 중지
docker-compose down
```

## 📊 시스템 모니터링

### 실시간 시스템 상태 확인

```bash
# 현재 상태 확인
python3 system_monitor.py

# 연속 모니터링 (60초 간격)
python3 system_monitor.py --continuous

# 리포트 저장
python3 system_monitor.py --save
```

### 모니터링 항목

- 💻 **시스템 리소스**: CPU, 메모리, 디스크 사용률
- 🔄 **프로세스 상태**: 관련 프로세스 실행 상태
- 📄 **로그 정보**: 로그 파일 크기 및 라인 수
- 📁 **출력 파일**: 생성된 파일 통계
- 🔧 **서비스 상태**: AWS, Slack, Python 패키지 상태

### 백그라운드 실행 관리

```bash
# Slack 모니터링 시작
./start_background_monitoring.sh

# 상태 확인
./check_monitoring_status.sh

# 중지
./stop_monitoring.sh
```

## 🔧 고급 실행 옵션

### 로그 레벨 조정

```bash
# 디버그 모드
python3 run_complete_system.py --mode full --log-level DEBUG

# 오류만 표시
python3 run_complete_system.py --mode full --log-level ERROR
```

### 사용자 정의 설정 파일

```bash
# 커스텀 설정 파일 사용
python3 run_complete_system.py --mode full --config config/custom.json
```

### 특정 기능 조합

```bash
# 모니터링 + Slack 알림
python3 run_complete_system.py --mode monitoring-only
python3 run_complete_system.py --mode slack-only

# 뉴스 생성 + 대시보드
python3 run_complete_system.py --mode news-only &
python3 run_complete_system.py --mode dashboard
```

## 📋 실행 체크리스트

### 🔧 **사전 준비**
- [ ] Python 3.8+ 설치
- [ ] 의존성 패키지 설치 (`pip install -r requirements.txt`)
- [ ] AWS CLI 설정 (`aws configure`)
- [ ] Slack 웹훅 URL 설정

### ⚙️ **환경 설정**
- [ ] `.env` 파일 생성 및 설정
- [ ] 디렉토리 권한 확인
- [ ] 실행 파일 권한 부여 (`chmod +x *.py *.sh`)

### 🧪 **테스트**
- [ ] 시스템 테스트 실행 (`--mode test`)
- [ ] AWS 연결 확인
- [ ] Slack 알림 테스트

### 🚀 **실행**
- [ ] 원하는 모드 선택
- [ ] 로그 파일 확인
- [ ] 출력 결과 검증

## 🚨 문제 해결

### 일반적인 문제들

**1. AWS 자격증명 오류**
```bash
# 자격증명 확인
aws sts get-caller-identity

# 재설정
aws configure
```

**2. Python 패키지 누락**
```bash
# 의존성 재설치
pip install -r requirements.txt

# 특정 패키지 설치
pip install boto3 streamlit pandas
```

**3. 권한 오류**
```bash
# 실행 권한 부여
chmod +x run_complete_system.py quick_start.sh

# 디렉토리 권한 확인
ls -la logs/ output/
```

**4. Slack 알림 실패**
```bash
# 웹훅 URL 테스트
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"테스트"}' $SLACK_WEBHOOK_URL
```

**5. 메모리 부족**
```bash
# 시스템 리소스 확인
python3 system_monitor.py

# 프로세스 확인
ps aux | grep python
```

### 로그 분석

```bash
# 오류 로그 확인
grep "ERROR" logs/complete_system_*.log

# 최근 로그 확인
tail -f logs/complete_system_$(date +%Y%m%d).log

# 특정 모듈 로그 필터링
grep "slack_notifier" logs/complete_system_*.log
```

### 디버깅 모드

```bash
# 상세 디버그 정보
python3 run_complete_system.py --mode full --log-level DEBUG

# 단계별 실행
python3 run_complete_system.py --mode monitoring-only
python3 run_complete_system.py --mode news-only
python3 run_complete_system.py --mode slack-only
```

## 📞 지원 및 문의

### 로그 파일 위치
- **메인 로그**: `logs/complete_system_YYYYMMDD.log`
- **시스템 모니터**: `logs/system_monitor_YYYYMMDD.log`
- **Slack 모니터링**: `logs/slack_monitoring.log`

### 출력 파일 위치
- **실행 결과**: `output/complete_system_YYYYMMDD_HHMMSS.json`
- **생성 기사**: `output/article_YYYYMMDD_HHMMSS.html`
- **시스템 리포트**: `logs/system_report_YYYYMMDD_HHMMSS.json`

### GitHub Issues
문제 발생 시 다음 정보와 함께 이슈를 생성해주세요:
- 실행 명령어
- 오류 메시지
- 로그 파일 내용
- 시스템 환경 정보

---

## 🎉 성공적인 실행을 위한 팁

1. **단계별 실행**: 처음에는 `setup` → `test` → `monitoring-only` 순으로 테스트
2. **로그 모니터링**: 실행 중 로그를 실시간으로 확인
3. **리소스 관리**: 시스템 모니터로 리소스 사용량 확인
4. **정기 점검**: 주기적으로 시스템 상태 및 로그 파일 정리
5. **백업**: 중요한 설정 파일과 출력 결과 백업

**이제 완전한 경제 뉴스 자동 생성 시스템을 자유롭게 활용하세요!** 🚀✨
