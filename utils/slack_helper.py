"""
Slack 알림 헬퍼 모듈
웹훅 오류를 우아하게 처리하고 대안 제공
"""

import os
import json
import requests
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SlackNotifier:
    """Slack 알림 클래스"""
    
    def __init__(self):
        self.webhook_url = self._load_webhook_url()
        self.is_enabled = bool(self.webhook_url and self.webhook_url not in ["DISABLED", "BACKUP_MODE"])
        self.backup_mode = self.webhook_url == "BACKUP_MODE"
        self.last_error = None
        self.backup_send_message = None
        self.backup_send_alert = None
        
    def _load_webhook_url(self) -> Optional[str]:
        """웹훅 URL 로드"""
        
        # 1. 환경변수에서 확인
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if webhook_url and webhook_url not in ["DISABLED", "BACKUP_MODE"]:
            return webhook_url
        
        # 2. 설정 파일에서 확인
        webhook_file = Path("config/slack_webhook.txt")
        if webhook_file.exists():
            try:
                webhook_url = webhook_file.read_text().strip()
                if webhook_url and webhook_url not in ["DISABLED", "BACKUP_MODE"]:
                    return webhook_url
                elif webhook_url == "BACKUP_MODE":
                    # 백업 모드 활성화
                    self._enable_backup_mode()
                    return "BACKUP_MODE"
            except Exception as e:
                logger.warning(f"웹훅 파일 읽기 오류: {e}")
        
        return None
    
    def _enable_backup_mode(self):
        """백업 모드 활성화"""
        try:
            import sys
            from pathlib import Path
            
            # 프로젝트 루트를 sys.path에 추가
            project_root = Path(__file__).parent.parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
            
            from utils.backup_slack_notifier import send_backup_message, send_backup_alert
            self.backup_send_message = send_backup_message
            self.backup_send_alert = send_backup_alert
            self.backup_mode = True
            logger.info("백업 Slack 알림 모드가 활성화되었습니다")
        except ImportError as e:
            logger.error(f"백업 알림 시스템 로드 실패: {e}")
            self.backup_mode = False
    
    def send_message(self, text: str, blocks: Optional[list] = None, 
                    fallback_to_log: bool = True) -> bool:
        """메시지 전송"""
        
        # 백업 모드인 경우
        if self.backup_mode and self.backup_send_message:
            try:
                return self.backup_send_message(text, blocks)
            except Exception as e:
                logger.error(f"백업 알림 전송 오류: {e}")
                if fallback_to_log:
                    logger.info(f"[백업 알림 실패 → 로그] {text}")
                return False
        
        if not self.is_enabled:
            if fallback_to_log:
                logger.info(f"[Slack 알림 비활성화] {text}")
            return False
        
        try:
            data = {"text": text}
            if blocks:
                data["blocks"] = blocks
            
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200 and response.text == 'ok':
                logger.debug("Slack 메시지 전송 성공")
                return True
            else:
                self.last_error = f"HTTP {response.status_code}: {response.text}"
                if fallback_to_log:
                    logger.warning(f"[Slack 전송 실패 → 로그] {text}")
                    self._handle_webhook_error(response.text)
                return False
                
        except requests.exceptions.Timeout:
            self.last_error = "요청 시간 초과"
            if fallback_to_log:
                logger.warning(f"[Slack 시간초과 → 로그] {text}")
            return False
            
        except Exception as e:
            self.last_error = str(e)
            if fallback_to_log:
                logger.warning(f"[Slack 오류 → 로그] {text}")
            return False
    
    def _handle_webhook_error(self, error_response: str):
        """웹훅 오류 처리"""
        
        error_messages = {
            'no_service': '웹훅이 비활성화되었거나 삭제됨',
            'channel_not_found': '채널을 찾을 수 없음',
            'invalid_payload': '잘못된 메시지 형식',
            'action_prohibited': '권한 없음',
            'posting_to_general_channel_denied': 'general 채널 게시 거부됨'
        }
        
        if error_response in error_messages:
            logger.warning(f"Slack 웹훅 오류: {error_messages[error_response]}")
        else:
            logger.warning(f"Slack 웹훅 알 수 없는 오류: {error_response}")
    
    def send_system_alert(self, title: str, message: str, severity: str = "info") -> bool:
        """시스템 알림 전송"""
        
        # 백업 모드인 경우
        if self.backup_mode and self.backup_send_alert:
            try:
                return self.backup_send_alert(title, message, severity)
            except Exception as e:
                logger.error(f"백업 시스템 알림 전송 오류: {e}")
                return False
        
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅",
            "critical": "🚨"
        }
        
        emoji = emoji_map.get(severity, "📢")
        text = f"{emoji} {title}\n{message}"
        
        return self.send_message(text)
    
    def send_market_alert(self, event_data: Dict[str, Any]) -> bool:
        """시장 이벤트 알림 전송"""
        
        try:
            severity = event_data.get('severity', 0.5)
            event_type = event_data.get('type', 'unknown')
            symbol = event_data.get('symbol', 'N/A')
            
            # 심각도에 따른 이모지 선택
            if severity >= 0.8:
                emoji = "🚨"
            elif severity >= 0.6:
                emoji = "⚠️"
            else:
                emoji = "📊"
            
            text = f"{emoji} 시장 이벤트 감지\n"
            text += f"종목: {symbol}\n"
            text += f"유형: {event_type}\n"
            text += f"심각도: {severity:.2f}"
            
            if 'description' in event_data:
                text += f"\n설명: {event_data['description']}"
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"시장 알림 전송 오류: {e}")
            return False
    
    def test_connection(self) -> tuple[bool, str]:
        """연결 테스트"""
        
        if self.backup_mode:
            success = self.send_message("🧪 백업 모드 연결 테스트", fallback_to_log=False)
            if success:
                return True, "백업 모드 연결 성공"
            else:
                return False, self.last_error or "백업 모드 연결 실패"
        
        if not self.is_enabled:
            return False, "Slack 알림이 비활성화됨"
        
        success = self.send_message("🧪 연결 테스트", fallback_to_log=False)
        
        if success:
            return True, "연결 성공"
        else:
            return False, self.last_error or "알 수 없는 오류"
    
    def get_status(self) -> Dict[str, Any]:
        """상태 정보 반환"""
        
        return {
            "enabled": self.is_enabled or self.backup_mode,
            "backup_mode": self.backup_mode,
            "webhook_configured": bool(self.webhook_url),
            "last_error": self.last_error,
            "webhook_url_preview": f"{self.webhook_url[:50]}..." if self.webhook_url and self.webhook_url != "BACKUP_MODE" else "백업 모드" if self.backup_mode else None
        }

# 전역 인스턴스
slack_notifier = SlackNotifier()

# 편의 함수들
def send_slack_message(text: str, blocks: Optional[list] = None) -> bool:
    """간단한 메시지 전송"""
    return slack_notifier.send_message(text, blocks)

def send_system_alert(title: str, message: str, severity: str = "info") -> bool:
    """시스템 알림 전송"""
    return slack_notifier.send_system_alert(title, message, severity)

def send_market_alert(event_data: Dict[str, Any]) -> bool:
    """시장 알림 전송"""
    return slack_notifier.send_market_alert(event_data)

def test_slack_connection() -> tuple[bool, str]:
    """Slack 연결 테스트"""
    return slack_notifier.test_connection()

def get_slack_status() -> Dict[str, Any]:
    """Slack 상태 정보"""
    return slack_notifier.get_status()

if __name__ == "__main__":
    # 테스트 실행
    print("🔍 Slack 헬퍼 테스트")
    print("=" * 30)
    
    status = get_slack_status()
    print(f"상태: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    if status['enabled']:
        print("\n🔍 연결 테스트 중...")
        success, message = test_slack_connection()
        print(f"결과: {'성공' if success else '실패'} - {message}")
    else:
        print("\n⚠️  Slack 알림이 비활성화되어 있습니다")
        print("setup_slack_webhook.md 가이드를 참조하여 설정하세요")
