#!/usr/bin/env python3
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
        print("\n" + "="*50)
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
        full_message = f"{emoji} {title}\n{message}"
        
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
