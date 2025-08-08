
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
