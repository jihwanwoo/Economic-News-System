# 📱 Slack 경제 알림 시스템 사용법

웹훅 URL이 설정되어 Slack 알림 시스템이 준비되었습니다!

## 🎯 **설정 완료 상태**

✅ **웹훅 URL**: `https://hooks.slack.com/services/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`  
✅ **설정 파일**: `config/slack_config.json`  
✅ **연결 테스트**: 성공  
✅ **실제 알림 테스트**: 성공 (8개 이벤트 감지, 위험도 VERY_HIGH)

## 🚀 **사용 방법**

### **1. 즉시 테스트 (단일 실행)**
```bash
# 현재 시장 상황 분석 + Slack 알림 전송
python demo_slack_alerts.py
# 실행 시 'y' 입력하면 실제 Slack으로 알림 전송
```

### **2. 연속 모니터링 시작**
```bash
# 포그라운드 실행 (터미널에서 직접 확인)
python start_slack_monitoring.py

# 백그라운드 실행 (서버용)
./start_background_monitoring.sh
```

### **3. 모니터링 관리**
```bash
# 상태 확인
./check_monitoring_status.sh

# 모니터링 중지
./stop_monitoring.sh

# 로그 실시간 확인
tail -f logs/background_monitoring.log
```

## 📊 **받게 될 알림 유형**

### **1. 시장 요약 알림 (1시간마다)**
```
📊 Market Analysis Summary - 2025-08-05 11:30

위험도: 🔴 VERY HIGH
감지된 이벤트: 8개
위험 점수: 1.00/1.00

🚨 주요 알림:
1. [^VIX] CBOE Volatility Index: ^VIX MACD 강세 신호
2. [GOOGL] Alphabet Inc.: GOOGL MACD 강세 신호
3. [MSFT] Microsoft Corporation: MSFT MACD 강세 신호

💡 주요 인사이트:
• 가장 빈번한 이벤트: momentum_divergence (6회)
• 고심각도 이벤트 5개 발생
```

### **2. 긴급 알림 (심각도 0.6 이상)**
```
🔴 CRITICAL ALERT 📈

AAPL - Technical Breakout
심볼: AAPL
심각도: 0.85
시간: 11:30:15

상세 정보:
• change_percent: -2.5
• current_price: 202.38
• volume: 104301700
• confidence: 0.8
```

### **3. 뉴스 업데이트 알림**
```
📰 새로운 AI 경제 뉴스가 생성되었습니다

AI 생성 경제 뉴스 업데이트
생성 시간: 2025-08-05 11:30:00
```

### **4. 시스템 상태 알림**
```
🔧 System Status Report

시스템 상태: 🟢 실행 중
모니터링 심볼: 13개
최근 위험도: VERY_HIGH
마지막 분석: 2025-08-05T11:30:00
```

## ⚙️ **알림 설정 커스터마이징**

### **현재 설정 (`config/slack_config.json`)**
```json
{
  "notification_settings": {
    "send_summary": true,              // 시장 요약 알림
    "send_critical_alerts": true,      // 긴급 알림
    "send_news_updates": true,         // 뉴스 업데이트
    "summary_interval_minutes": 60,    // 요약 알림 간격 (1시간)
    "min_alert_severity": 0.6,         // 최소 알림 심각도
    "max_alerts_per_hour": 15,         // 시간당 최대 알림 수
    "cooldown_minutes": 15             // 동일 심볼 쿨다운 (15분)
  }
}
```

### **설정 변경 방법**
```bash
# 설정 파일 편집
nano config/slack_config.json

# 변경 후 모니터링 재시작
./stop_monitoring.sh
./start_background_monitoring.sh
```

### **추천 설정 조합**

**🔥 적극적 알림 (트레이더용)**
```json
{
  "min_alert_severity": 0.5,
  "max_alerts_per_hour": 25,
  "cooldown_minutes": 10,
  "summary_interval_minutes": 30
}
```

**🛡️ 보수적 알림 (장기투자자용)**
```json
{
  "min_alert_severity": 0.8,
  "max_alerts_per_hour": 8,
  "cooldown_minutes": 30,
  "summary_interval_minutes": 120
}
```

## 📱 **모바일 알림 최적화**

### **Slack 모바일 앱 설정**
1. **Slack 앱 설치** (iOS/Android)
2. 워크스페이스 로그인
3. **설정 → 알림 → 모바일 푸시 알림**
4. **"모든 새 메시지"** 또는 **"직접 메시지, 멘션, 키워드"** 선택

### **키워드 알림 설정**
- **"CRITICAL"**, **"긴급"**, **"HIGH"** 등 키워드 알림 설정
- 관심 종목 심볼 추가 (예: "AAPL", "TSLA", "NVDA")

## 📊 **모니터링 현황 확인**

### **실시간 상태 확인**
```bash
# 전체 상태 확인
./check_monitoring_status.sh

# 로그 실시간 모니터링
tail -f logs/background_monitoring.log

# 오류 로그만 확인
grep ERROR logs/background_monitoring.log
```

### **알림 통계 확인**
```bash
# 오늘 전송된 알림 수
grep "Slack 알림 전송 성공" logs/slack_monitoring.log | wc -l

# 최근 오류 확인
grep "ERROR" logs/slack_monitoring.log | tail -5
```

## 🔧 **문제 해결**

### **일반적인 문제들**

**1. 알림이 오지 않음**
```bash
# 프로세스 상태 확인
./check_monitoring_status.sh

# 웹훅 URL 테스트
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"테스트 메시지"}' \
"https://hooks.slack.com/services/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"
```

**2. 알림이 너무 많음**
```bash
# 설정 파일에서 조정
nano config/slack_config.json
# min_alert_severity를 0.6에서 0.8로 증가
# max_alerts_per_hour를 15에서 8로 감소
```

**3. 프로세스가 중지됨**
```bash
# 로그 확인
tail -20 logs/background_monitoring.log

# 재시작
./start_background_monitoring.sh
```

### **고급 디버깅**
```bash
# 상세 로그 활성화
export SLACK_DEBUG=true
python start_slack_monitoring.py

# 네트워크 연결 확인
ping hooks.slack.com

# 디스크 공간 확인
df -h
```

## 🎯 **최적 사용 팁**

### **1. 시간대별 알림 관리**
- **장중 (9:30-16:00)**: 적극적 알림 (심각도 0.5 이상)
- **장후 (16:00-9:30)**: 보수적 알림 (심각도 0.8 이상)

### **2. 종목별 관심도 설정**
- **핵심 종목**: 모든 알림 수신
- **관심 종목**: 중요 알림만 수신
- **기타 종목**: 긴급 알림만 수신

### **3. 알림 피로도 관리**
- 주말/휴일에는 알림 빈도 감소
- 중요한 회의/이벤트 시간에는 일시 중지

## 📞 **지원 및 문의**

### **로그 파일 위치**
- **메인 로그**: `logs/background_monitoring.log`
- **Slack 로그**: `logs/slack_monitoring.log`
- **이벤트 로그**: `logs/advanced_events_*.json`

### **백업 및 복구**
```bash
# 설정 백업
cp config/slack_config.json config/slack_config_backup.json

# 로그 아카이브
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

---

## 🎉 **축하합니다!**

이제 **24/7 실시간 경제 알림 시스템**이 완전히 설정되었습니다!

**다음과 같은 상황에서 즉시 Slack 알림을 받게 됩니다:**
- 📈 주식 급등/급락 (5% 이상)
- ⚡ 높은 변동성 감지 (15% 이상)
- 📊 거래량 급증 (평균 대비 3배 이상)
- 🚀 기술적 돌파 (볼린저 밴드, RSI 과매수/과매도)
- 💭 시장 감정 급변 (공포/탐욕 지수 극값)
- 🔄 모멘텀 다이버전스 (MACD 신호 변화)
- 🌊 시장 체제 변화 (VIX 20% 이상 변동)

**모바일에서도 즉시 알림을 받으실 수 있습니다!** 📱✨
