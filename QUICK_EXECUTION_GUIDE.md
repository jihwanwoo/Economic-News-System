# ⚡ 빠른 실행 가이드

경제 뉴스 자동 생성 시스템을 즉시 실행하는 방법입니다.

## 🚀 1분 만에 시작하기

### 1️⃣ **환경 설정 확인**
```bash
python3 run_complete_system.py --mode setup
```

### 2️⃣ **간편 실행 메뉴**
```bash
./quick_start.sh
```

### 3️⃣ **전체 시스템 실행**
```bash
python3 run_complete_system.py --mode full
```

## 📋 주요 실행 명령어

| 명령어 | 설명 | 필요 조건 |
|--------|------|-----------|
| `./quick_start.sh` | 🎯 대화형 메뉴 | 없음 |
| `--mode full` | 🚀 전체 시스템 | AWS + Slack |
| `--mode news-only` | 🤖 AI 뉴스만 | AWS |
| `--mode monitoring-only` | 📊 모니터링만 | 없음 |
| `--mode slack-only` | 📱 Slack 알림만 | Slack |
| `--mode dashboard` | 📈 웹 대시보드 | 없음 |
| `--mode test` | 🧪 시스템 테스트 | 없음 |

## 🔧 필수 설정

### AWS 설정 (AI 뉴스 생성용)
```bash
aws configure
# 또는
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"
```

### Slack 설정 (알림용)
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

## 📊 실행 결과 확인

### 로그 파일
```bash
tail -f logs/complete_system_$(date +%Y%m%d).log
```

### 출력 파일
```bash
ls -la output/
```

### 시스템 상태
```bash
python3 system_monitor.py
```

## 🚨 문제 해결

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 권한 설정
```bash
chmod +x *.py *.sh
```

### AWS 연결 테스트
```bash
aws sts get-caller-identity
```

### Slack 연결 테스트
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"테스트"}' $SLACK_WEBHOOK_URL
```

## 🎯 추천 실행 순서

1. **초기 설정**: `--mode setup`
2. **시스템 테스트**: `--mode test`  
3. **모니터링 테스트**: `--mode monitoring-only`
4. **뉴스 생성 테스트**: `--mode news-only`
5. **전체 시스템**: `--mode full`

## 📱 백그라운드 실행

### Slack 연속 모니터링
```bash
./start_background_monitoring.sh    # 시작
./check_monitoring_status.sh        # 상태 확인
./stop_monitoring.sh                # 중지
```

## 🎉 성공 확인

실행이 성공하면 다음을 확인할 수 있습니다:

- ✅ **로그 파일**: `logs/` 디렉토리에 실행 로그
- ✅ **출력 파일**: `output/` 디렉토리에 JSON/HTML 결과
- ✅ **Slack 알림**: 설정된 채널에 실시간 알림
- ✅ **대시보드**: http://localhost:8501 에서 웹 인터페이스

---

**🚀 이제 완전한 경제 뉴스 자동 생성 시스템을 사용할 준비가 되었습니다!**
