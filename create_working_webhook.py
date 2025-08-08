#!/usr/bin/env python3
"""
작동하는 Slack 웹훅 자동 생성 도구
"""

import os
import json
import requests
import webbrowser
from pathlib import Path

class SlackWebhookCreator:
    def __init__(self):
        self.workspace_id = "T098W0CB96Z"
        
    def create_webhook_instructions(self):
        """웹훅 생성 지침 출력"""
        print("🔧 새로운 Slack 웹훅 생성 가이드")
        print("=" * 60)
        
        instructions = f"""
📋 단계별 웹훅 생성 방법:

1. 🌐 Slack API 앱 관리 페이지 열기
   브라우저에서 다음 URL을 열어주세요:
   https://api.slack.com/apps

2. 🆕 새 앱 생성
   - "Create New App" 버튼 클릭
   - "From scratch" 선택
   - App Name: "경제뉴스시스템" (또는 원하는 이름)
   - Pick a workspace: 워크스페이스 선택 (ID: {self.workspace_id})

3. 📨 Incoming Webhooks 활성화
   - 왼쪽 메뉴에서 "Incoming Webhooks" 클릭
   - "Activate Incoming Webhooks" 토글을 ON으로 설정
   - "Add New Webhook to Workspace" 버튼 클릭

4. 📍 채널 선택
   - 알림을 받을 채널 선택 (예: #general, #alerts, #경제뉴스)
   - "Allow" 버튼 클릭

5. 🔗 웹훅 URL 복사
   - 생성된 웹훅 URL을 복사하세요
   - 형식: https://hooks.slack.com/services/T.../B.../...

6. ⚙️ 시스템에 적용
   복사한 웹훅 URL을 아래 명령어로 설정하세요:
   
   echo "새로운_웹훅_URL" > config/slack_webhook.txt
   
   또는 Python으로:
   python3 -c "
   webhook_url = input('웹훅 URL을 입력하세요: ')
   with open('config/slack_webhook.txt', 'w') as f:
       f.write(webhook_url)
   print('✅ 웹훅 URL이 저장되었습니다!')
   "

7. 🧪 테스트
   python3 test_slack_webhook.py
        """
        
        print(instructions)
        
        # 브라우저에서 Slack API 페이지 열기
        try:
            print("\n🌐 브라우저에서 Slack API 페이지를 여는 중...")
            webbrowser.open("https://api.slack.com/apps")
            print("✅ 브라우저가 열렸습니다!")
        except Exception as e:
            print(f"⚠️  브라우저 열기 실패: {e}")
            print("수동으로 https://api.slack.com/apps 를 열어주세요")
    
    def interactive_webhook_setup(self):
        """대화형 웹훅 설정"""
        print("\n🤖 대화형 웹훅 설정")
        print("=" * 40)
        
        print("위의 지침을 따라 새 웹훅을 생성한 후, 여기에 URL을 입력하세요.")
        print("(Ctrl+C로 취소 가능)")
        
        try:
            webhook_url = input("\n웹훅 URL을 입력하세요: ").strip()
            
            if not webhook_url:
                print("❌ 웹훅 URL이 입력되지 않았습니다.")
                return False
            
            if not webhook_url.startswith("https://hooks.slack.com/services/"):
                print("❌ 올바른 Slack 웹훅 URL 형식이 아닙니다.")
                print("형식: https://hooks.slack.com/services/T.../B.../...")
                return False
            
            # 웹훅 URL 테스트
            print("\n🧪 웹훅 URL 테스트 중...")
            test_success = self.test_webhook_url(webhook_url)
            
            if test_success:
                # 설정 파일에 저장
                config_file = Path("config/slack_webhook.txt")
                config_file.parent.mkdir(exist_ok=True)
                
                with open(config_file, 'w') as f:
                    f.write(webhook_url)
                
                print(f"✅ 웹훅 URL이 {config_file}에 저장되었습니다!")
                
                # 환경변수로도 설정
                os.environ['SLACK_WEBHOOK_URL'] = webhook_url
                print("✅ 환경변수 SLACK_WEBHOOK_URL도 설정되었습니다!")
                
                return True
            else:
                print("❌ 웹훅 테스트 실패. URL을 다시 확인해주세요.")
                return False
                
        except KeyboardInterrupt:
            print("\n\n⚠️  설정이 취소되었습니다.")
            return False
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            return False
    
    def test_webhook_url(self, webhook_url):
        """웹훅 URL 테스트"""
        try:
            test_message = {
                "text": "🎉 새 웹훅 테스트 성공!",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*경제 뉴스 시스템* 🤖\n\n✅ 새로운 웹훅이 성공적으로 설정되었습니다!"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*상태:* 정상 작동"
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*설정 시간:* 방금 전"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                webhook_url,
                json=test_message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200 and response.text == 'ok':
                print("✅ 웹훅 테스트 성공!")
                return True
            else:
                print(f"❌ 웹훅 테스트 실패:")
                print(f"   상태 코드: {response.status_code}")
                print(f"   응답: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 웹훅 테스트 오류: {e}")
            return False
    
    def create_backup_notifier(self):
        """백업 알림 시스템 생성"""
        print("\n🔧 백업 알림 시스템 생성")
        print("=" * 40)
        
        backup_code = '''#!/usr/bin/env python3
"""
백업 Slack 알림 시스템
실제 Slack 대신 로그 파일과 콘솔에 메시지 출력
"""

import json
import logging
from datetime import datetime
from pathlib import Path

class BackupSlackNotifier:
    def __init__(self):
        self.log_file = Path("logs/slack_backup.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SLACK_BACKUP - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, text, blocks=None):
        """메시지를 로그와 콘솔에 출력"""
        message_data = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "blocks": blocks,
            "status": "backup_notification"
        }
        
        # 로그 파일에 JSON 형태로 저장
        self.logger.info(json.dumps(message_data, ensure_ascii=False, indent=2))
        
        # 콘솔에 보기 좋게 출력
        print("\\n" + "="*50)
        print("📢 [백업 Slack 알림]")
        print("="*50)
        print(f"📝 메시지: {text}")
        if blocks:
            print("📋 블록 데이터:")
            print(json.dumps(blocks, ensure_ascii=False, indent=2))
        print("⏰ 시간:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*50)
        
        return True
    
    def send_system_alert(self, title, message, severity="info"):
        """시스템 알림 전송"""
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️", 
            "error": "❌",
            "success": "✅",
            "critical": "🚨"
        }
        
        emoji = emoji_map.get(severity, "📢")
        full_message = f"{emoji} {title}\\n{message}"
        
        return self.send_message(full_message)

# 전역 인스턴스
backup_notifier = BackupSlackNotifier()

def send_backup_message(text, blocks=None):
    """백업 메시지 전송"""
    return backup_notifier.send_message(text, blocks)

def send_backup_alert(title, message, severity="info"):
    """백업 알림 전송"""
    return backup_notifier.send_system_alert(title, message, severity)

if __name__ == "__main__":
    # 테스트
    send_backup_message("🧪 백업 알림 시스템 테스트")
    send_backup_alert("시스템 시작", "경제 뉴스 시스템이 시작되었습니다", "success")
'''
        
        backup_file = Path("utils/backup_slack_notifier.py")
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(backup_code)
        
        print(f"✅ 백업 알림 시스템 생성: {backup_file}")
        print("   → Slack 웹훅 대신 로그 파일과 콘솔에 메시지 출력")
        print("   → 웹훅 수정 후 원래 시스템으로 복구 가능")
        
        # 백업 시스템 테스트
        print("\n🧪 백업 시스템 테스트 중...")
        try:
            exec(open(backup_file).read())
            print("✅ 백업 시스템 테스트 성공!")
        except Exception as e:
            print(f"❌ 백업 시스템 테스트 실패: {e}")
        
        return backup_file

def main():
    creator = SlackWebhookCreator()
    
    print("🚀 Slack 웹훅 자동 생성 도구")
    print("=" * 60)
    
    print("\n현재 상황:")
    print("❌ 기존 웹훅이 'no_service' 오류로 작동하지 않음")
    print("✅ 새로운 웹훅을 생성하여 문제 해결")
    
    print("\n선택하세요:")
    print("1. 🔧 새 웹훅 생성 가이드 보기")
    print("2. 🤖 대화형 웹훅 설정")
    print("3. 📝 백업 알림 시스템 생성")
    print("4. 🏃 모든 작업 실행")
    
    try:
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == "1":
            creator.create_webhook_instructions()
            
        elif choice == "2":
            success = creator.interactive_webhook_setup()
            if success:
                print("\n🎉 웹훅 설정 완료!")
                print("이제 ./quick_start.sh를 실행하여 시스템을 테스트하세요.")
            
        elif choice == "3":
            creator.create_backup_notifier()
            
        elif choice == "4":
            print("\n🔧 모든 작업 실행 중...")
            creator.create_webhook_instructions()
            print("\n" + "="*60)
            success = creator.interactive_webhook_setup()
            print("\n" + "="*60)
            creator.create_backup_notifier()
            
            if success:
                print("\n🎉 모든 작업 완료!")
                print("새 웹훅이 설정되었고 백업 시스템도 준비되었습니다.")
            else:
                print("\n⚠️  웹훅 설정은 실패했지만 백업 시스템은 사용 가능합니다.")
        else:
            print("❌ 잘못된 선택입니다.")
            
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
