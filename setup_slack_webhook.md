# 🔧 Slack 웹훅 설정 가이드

## 현재 문제
- 기존 웹훅 URL이 "no_service" 응답을 반환
- 웹훅이 비활성화되었거나 삭제된 상태

## 해결 방법

### 1. 새로운 Slack 앱 생성

1. **Slack API 사이트 접속**
   - https://api.slack.com/apps 방문
   - "Create New App" 클릭

2. **앱 생성**
   - "From scratch" 선택
   - App Name: "경제 뉴스 시스템" (또는 원하는 이름)
   - Workspace: 알림을 받을 워크스페이스 선택

### 2. Incoming Webhooks 활성화

1. **Features > Incoming Webhooks** 메뉴 선택
2. **Activate Incoming Webhooks** 토글을 ON으로 설정
3. **Add New Webhook to Workspace** 버튼 클릭
4. 알림을 받을 채널 선택 (예: #general, #경제뉴스)
5. **Allow** 버튼 클릭

### 3. 웹훅 URL 복사

생성된 웹훅 URL을 복사합니다:
```
https://hooks.slack.com/services/T.../B.../...
```

### 4. 시스템에 웹훅 URL 설정

아래 명령어로 새 웹훅 URL을 설정하세요:

```bash
# 웹훅 URL을 파일에 저장
echo "새로운_웹훅_URL" > config/slack_webhook.txt

# 또는 환경변수로 설정
export SLACK_WEBHOOK_URL="새로운_웹훅_URL"
```

### 5. 테스트

```bash
# 웹훅 테스트
python3 test_slack_webhook.py

# 또는 curl로 직접 테스트
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"✅ 새 웹훅 테스트 성공!"}' \
"새로운_웹훅_URL"
```

## 추가 설정 (선택사항)

### 앱 커스터마이징
- **Display Information**: 앱 이름, 아이콘, 설명 설정
- **Bot Users**: 봇 사용자 추가 (고급 기능용)

### 권한 설정
- **OAuth & Permissions**: 필요한 경우 추가 권한 설정

## 문제 해결

### 여전히 "no_service" 오류가 발생하는 경우:
1. 웹훅 URL이 올바르게 복사되었는지 확인
2. 워크스페이스 관리자 권한 확인
3. 앱이 워크스페이스에 정상 설치되었는지 확인

### 메시지가 전송되지 않는 경우:
1. 채널 권한 확인
2. 앱이 해당 채널에 접근 권한이 있는지 확인
3. JSON 형식이 올바른지 확인

## 보안 주의사항
- 웹훅 URL을 공개 저장소에 업로드하지 마세요
- 환경변수나 설정 파일로 안전하게 관리하세요
- 정기적으로 웹훅 URL을 갱신하세요
