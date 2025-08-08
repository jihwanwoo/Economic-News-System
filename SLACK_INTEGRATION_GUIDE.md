# 📱 Slack 알림 통합 가이드

## 🎯 개요

경제 뉴스 자동 생성 시스템이 .env 파일의 Slack 웹훅 URL을 사용하여 실시간 알림을 전송합니다.

## ✅ 설정 완료 상태

### .env 파일 설정 확인됨
```bash
# Slack 알림 설정
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/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

# AWS 설정
AWS_DEFAULT_REGION=us-east-1

# 기타 API 키들
ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3
FRED_API_KEY=d4235fa1b67058fff90f8a9cc43793c8
```

## 🚀 실행 방법

### 1️⃣ **Slack 알림 포함 통합 실행 (추천)**
```bash
./run_with_slack_alerts.sh
```

### 2️⃣ **기본 통합 실행**
```bash
./run_news_system.sh
# 또는
python run_complete_news_system.py
```

### 3️⃣ **Slack 알림만 테스트**
```bash
python test_slack_notification.py
```

## 📱 Slack 알림 유형

### 1. 시스템 시작 알림
```
🤖 경제 뉴스 시스템 시작 - 연결 테스트
```

### 2. 시스템 실행 요약 알림
```
🤖 AI 경제 뉴스 시스템
📊 감지된 이벤트: 1개
📰 생성된 기사: 1개
🎯 대상 심볼: AAPL
⏰ 실행 시간: 2025-08-07 07:27
```

### 3. 개별 기사 완성 알림
```
📰 새 기사: 애플 주가 상승, 신제품 출시 기대감 반영

애플이 올해 한 달러를 기록했다. 이는 올해 새로운 아이폰 모델 출시에 대한 기대감이 반영된 것으로 보인다...

📊 심볼: AAPL
📈 이벤트: price_change  
⭐ 품질점수: 7.9/10
📢 광고 추천: 3개
```

## 📊 실행 결과 예시

### 성공적인 실행
```json
{
  "status": "success",
  "execution_time": 31.9,
  "events_detected": 1,
  "articles_generated": 1,
  "slack_notifications": 2,
  "slack_results": [
    {"status": "success", "message": "Slack 알림 전송 성공"},
    {"status": "success", "message": "Slack 알림 전송 성공"}
  ]
}
```

## 🔧 문제 해결

### Slack 알림이 오지 않는 경우

1. **웹훅 URL 확인**
```bash
# .env 파일 확인
cat .env | grep SLACK_WEBHOOK_URL

# 연결 테스트
python test_slack_notification.py
```

2. **수동 테스트**
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"테스트 메시지"}' \
"https://hooks.slack.com/services/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"
```

3. **로그 확인**
```bash
# 실행 로그에서 Slack 관련 오류 확인
grep -i "slack" logs/complete_system_$(date +%Y%m%d).log
```

### 일반적인 오류들

**오류 1: 웹훅 URL 만료**
```
❌ Slack 알림 전송 실패: 404
```
→ Slack 앱에서 새 웹훅 URL 생성 필요

**오류 2: 네트워크 연결 문제**
```
❌ 네트워크 오류: Connection timeout
```
→ 인터넷 연결 및 방화벽 설정 확인

**오류 3: 메시지 형식 오류**
```
❌ Slack 알림 전송 실패: 400
```
→ 메시지 JSON 형식 확인

## 🎯 자동화 설정

### Cron으로 정기 실행 + Slack 알림
```bash
# 매시간 실행하여 Slack 알림 전송
0 * * * * cd /path/to/economic_news_system && ./run_with_slack_alerts.sh

# 매일 오전 9시 실행
0 9 * * * cd /path/to/economic_news_system && ./run_with_slack_alerts.sh

# 주식 시장 개장 시간에만 실행 (월-금 9:30-16:00)
30 9-15 * * 1-5 cd /path/to/economic_news_system && ./run_with_slack_alerts.sh
```

### 백그라운드 실행
```bash
# 백그라운드에서 실행하며 Slack 알림 전송
nohup ./run_with_slack_alerts.sh > logs/background_slack.log 2>&1 &

# 실행 상태 확인
ps aux | grep run_complete_news_system
```

## 📈 Slack 알림 최적화

### 알림 빈도 조절
- **긴급 이벤트**: 즉시 알림
- **일반 이벤트**: 1시간마다 요약 알림
- **시스템 상태**: 매일 1회 요약

### 알림 내용 커스터마이징
`run_complete_news_system.py`의 메시지 생성 함수를 수정하여 알림 내용을 조절할 수 있습니다.

## 🔒 보안 고려사항

1. **웹훅 URL 보안**
   - .env 파일을 .gitignore에 추가
   - 웹훅 URL을 공개 저장소에 커밋하지 않음

2. **접근 권한 관리**
   - Slack 앱 권한을 필요한 채널로만 제한
   - 정기적으로 웹훅 URL 갱신

## 📞 지원

### 테스트 명령어들
```bash
# 전체 Slack 알림 테스트
python test_slack_notification.py

# 통합 시스템 + Slack 실행
./run_with_slack_alerts.sh

# 시스템 상태 확인
python test_agents_system.py
```

### 로그 파일 위치
- 실행 로그: `logs/complete_system_YYYYMMDD.log`
- 백그라운드 로그: `logs/background_slack.log`

## 🎉 성공 확인

시스템이 정상 작동하면 Slack 채널에서 다음과 같은 알림들을 받게 됩니다:

1. ✅ **연결 테스트 메시지** (시스템 시작 시)
2. 📊 **시스템 실행 요약** (전체 파이프라인 완료 시)
3. 📰 **개별 기사 알림** (기사 생성 완료 시)

**현재 상태**: ✅ 모든 설정 완료, 테스트 성공!
