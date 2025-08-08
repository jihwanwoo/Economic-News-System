
🔧 Slack 웹훅 재생성 단계:

1. 📱 Slack 워크스페이스 접속
   - 워크스페이스: T098W0CB96Z
   - https://app.slack.com/client/T098W0CB96Z

2. 🛠️ 앱 관리 페이지 접속
   - https://api.slack.com/apps
   - 기존 앱이 있다면 확인, 없다면 새로 생성

3. 🆕 새 앱 생성 (필요한 경우)
   - "Create New App" → "From scratch"
   - App Name: "경제뉴스시스템" 
   - Workspace: 해당 워크스페이스 선택

4. 📨 Incoming Webhooks 설정
   - Features → Incoming Webhooks
   - "Activate Incoming Webhooks" ON
   - "Add New Webhook to Workspace"
   - 채널 선택 (예: #general, #alerts)

5. 🔗 새 웹훅 URL 복사
   - 생성된 URL을 복사
   - 형식: https://hooks.slack.com/services/T.../B.../...

6. ⚙️ 시스템에 적용
   echo "새_웹훅_URL" > config/slack_webhook.txt
   python3 test_slack_webhook.py

🚨 중요 사항:
- 기존 웹훅이 삭제되었거나 비활성화됨
- 워크스페이스 관리자 권한 필요할 수 있음
- 앱이 워크스페이스에서 제거되었을 가능성
        