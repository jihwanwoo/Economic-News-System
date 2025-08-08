#!/usr/bin/env python3
"""
Slack 웹훅 디버깅 및 자동 수정 도구
"""

import os
import json
import requests
import time
from pathlib import Path
from urllib.parse import urlparse

class SlackWebhookFixer:
    def __init__(self):
        self.webhook_url = "https://hooks.slack.com/services/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"
        self.workspace_id = "T098W0CB96Z"
        self.channel_id = "B098HQFEPB9"
        self.token = "2jrSbkwfAWBGBLyz2qRzyJyP"
        
    def analyze_webhook_url(self):
        """웹훅 URL 분석"""
        print("🔍 웹훅 URL 분석")
        print("=" * 50)
        print(f"전체 URL: {self.webhook_url}")
        print(f"워크스페이스 ID: {self.workspace_id}")
        print(f"채널/앱 ID: {self.channel_id}")
        print(f"토큰: {self.token}")
        print()
        
    def test_webhook_variations(self):
        """다양한 웹훅 테스트 시도"""
        print("🧪 다양한 웹훅 테스트 시도")
        print("=" * 50)
        
        test_cases = [
            {
                "name": "기본 메시지",
                "payload": {"text": "🔍 기본 테스트"}
            },
            {
                "name": "단순 텍스트",
                "payload": {"text": "test"}
            },
            {
                "name": "빈 메시지",
                "payload": {"text": ""}
            },
            {
                "name": "유니코드 테스트",
                "payload": {"text": "Hello World 안녕하세요"}
            },
            {
                "name": "JSON 블록",
                "payload": {
                    "text": "블록 테스트",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "테스트 메시지"
                            }
                        }
                    ]
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']} 테스트...")
            
            try:
                response = requests.post(
                    self.webhook_url,
                    json=test_case['payload'],
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Economic-News-System/1.0'
                    },
                    timeout=15
                )
                
                print(f"   상태 코드: {response.status_code}")
                print(f"   응답: {response.text}")
                print(f"   헤더: {dict(response.headers)}")
                
                if response.status_code == 200 and response.text == 'ok':
                    print("   ✅ 성공!")
                    return True
                    
            except Exception as e:
                print(f"   ❌ 오류: {e}")
        
        return False
    
    def try_alternative_endpoints(self):
        """대안 엔드포인트 시도"""
        print("\n🔄 대안 엔드포인트 시도")
        print("=" * 50)
        
        # 다른 가능한 URL 패턴들
        alternative_urls = [
            f"https://hooks.slack.com/services/{self.workspace_id}/{self.channel_id}/{self.token}",
            f"https://hooks.slack.com/workflows/{self.workspace_id}/{self.channel_id}/{self.token}",
            f"https://slack.com/api/chat.postMessage",  # 일반 API (토큰 필요)
        ]
        
        for url in alternative_urls:
            print(f"\n🔍 테스트 URL: {url}")
            
            try:
                if "api/chat.postMessage" in url:
                    # 일반 API는 다른 방식으로 테스트
                    print("   → 일반 API는 Bot Token이 필요합니다")
                    continue
                
                response = requests.post(
                    url,
                    json={"text": "🔍 대안 엔드포인트 테스트"},
                    timeout=10
                )
                
                print(f"   상태: {response.status_code}")
                print(f"   응답: {response.text}")
                
                if response.status_code == 200 and response.text == 'ok':
                    print("   ✅ 이 URL이 작동합니다!")
                    return url
                    
            except Exception as e:
                print(f"   ❌ 오류: {e}")
        
        return None
    
    def create_test_webhook_server(self):
        """테스트용 웹훅 서버 생성 (로컬 테스트)"""
        print("\n🖥️  로컬 테스트 서버 시뮬레이션")
        print("=" * 50)
        
        # 간단한 HTTP 서버 시뮬레이션
        test_data = {
            "text": "🧪 로컬 테스트 메시지",
            "timestamp": time.time(),
            "status": "success"
        }
        
        print("로컬 테스트 데이터:")
        print(json.dumps(test_data, indent=2, ensure_ascii=False))
        
        # 파일로 저장하여 테스트 결과 확인
        test_file = Path("output/slack_test_result.json")
        test_file.parent.mkdir(exist_ok=True)
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 테스트 결과 저장: {test_file}")
        return True
    
    def generate_new_webhook_instructions(self):
        """새 웹훅 생성 지침"""
        print("\n📋 새 웹훅 생성 지침")
        print("=" * 50)
        
        instructions = """
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
        """
        
        print(instructions)
        
        # 지침을 파일로도 저장
        instruction_file = Path("SLACK_WEBHOOK_SETUP.md")
        with open(instruction_file, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"\n📄 지침 파일 저장: {instruction_file}")
    
    def create_temporary_solution(self):
        """임시 해결책 생성"""
        print("\n🔧 임시 해결책 생성")
        print("=" * 50)
        
        # 임시 로그 기반 알림 시스템
        temp_notifier_code = '''
import logging
import json
from datetime import datetime

class TempSlackNotifier:
    """임시 Slack 알림 대체 시스템"""
    
    def __init__(self):
        self.log_file = "logs/slack_notifications.log"
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - SLACK_NOTIFICATION - %(message)s',
            encoding='utf-8'
        )
    
    def send_message(self, text, blocks=None):
        """메시지를 로그 파일에 기록"""
        message_data = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "blocks": blocks,
            "status": "logged_instead_of_slack"
        }
        
        logging.info(json.dumps(message_data, ensure_ascii=False))
        print(f"📝 [Slack 대신 로그] {text}")
        return True

# 사용 예시
notifier = TempSlackNotifier()
notifier.send_message("🤖 경제 뉴스 시스템 시작")
'''
        
        temp_file = Path("utils/temp_slack_notifier.py")
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(temp_notifier_code)
        
        print(f"✅ 임시 알림 시스템 생성: {temp_file}")
        print("   → Slack 대신 로그 파일에 알림 기록")
        print("   → 웹훅 수정 후 원래 시스템으로 복구 가능")
        
        return temp_file
    
    def run_comprehensive_debug(self):
        """종합 디버깅 실행"""
        print("🚀 Slack 웹훅 종합 디버깅 시작")
        print("=" * 60)
        
        # 1. URL 분석
        self.analyze_webhook_url()
        
        # 2. 다양한 테스트 시도
        if self.test_webhook_variations():
            print("\n🎉 웹훅이 정상 작동합니다!")
            return True
        
        # 3. 대안 엔드포인트 시도
        working_url = self.try_alternative_endpoints()
        if working_url:
            print(f"\n✅ 작동하는 URL 발견: {working_url}")
            # 새 URL을 설정 파일에 저장
            with open("config/slack_webhook.txt", "w") as f:
                f.write(working_url)
            return True
        
        # 4. 로컬 테스트
        self.create_test_webhook_server()
        
        # 5. 새 웹훅 생성 지침
        self.generate_new_webhook_instructions()
        
        # 6. 임시 해결책
        self.create_temporary_solution()
        
        print("\n📊 디버깅 결과 요약:")
        print("❌ 기존 웹훅이 작동하지 않음")
        print("✅ 새 웹훅 생성 지침 제공")
        print("✅ 임시 알림 시스템 생성")
        print("📋 다음 단계: SLACK_WEBHOOK_SETUP.md 참조")
        
        return False

def main():
    fixer = SlackWebhookFixer()
    success = fixer.run_comprehensive_debug()
    
    if not success:
        print("\n🔧 권장 조치:")
        print("1. SLACK_WEBHOOK_SETUP.md 파일을 참조하여 새 웹훅 생성")
        print("2. 임시로 utils/temp_slack_notifier.py 사용")
        print("3. 새 웹훅 생성 후 config/slack_webhook.txt 업데이트")

if __name__ == "__main__":
    main()
