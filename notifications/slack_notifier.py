"""
Slack 알림 시스템
고도화된 이벤트 감지 결과를 Slack으로 전송
"""

import json
import requests
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from enum import Enum

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SlackAlert:
    title: str
    message: str
    priority: AlertPriority
    symbol: str
    severity: float
    timestamp: datetime
    details: Optional[Dict] = None
    chart_url: Optional[str] = None

class SlackNotifier:
    """Slack 알림 전송 클래스"""
    
    def __init__(self, webhook_url: str, channel: str = "#economic-alerts"):
        self.webhook_url = webhook_url
        self.channel = channel
        self.logger = logging.getLogger(__name__)
        
        # 알림 설정
        self.alert_settings = {
            "enabled": True,
            "min_severity": 0.3,  # 최소 심각도
            "cooldown_minutes": 15,  # 동일 심볼 알림 쿨다운
            "max_alerts_per_hour": 20,  # 시간당 최대 알림 수
        }
        
        # 쿨다운 관리
        self.last_alerts = {}
        self.hourly_count = 0
        self.last_hour_reset = datetime.now().hour
        
        # 이모지 매핑
        self.priority_emojis = {
            AlertPriority.LOW: "🟢",
            AlertPriority.MEDIUM: "🟡",
            AlertPriority.HIGH: "🟠",
            AlertPriority.CRITICAL: "🔴"
        }
        
        self.event_emojis = {
            "surge": "📈",
            "drop": "📉",
            "volatility": "⚡",
            "volume_spike": "📊",
            "technical_breakout": "🚀",
            "sentiment_shift": "💭",
            "momentum_divergence": "🔄",
            "sector_rotation": "🔀",
            "market_regime_change": "🌊",
            "liquidity_crisis": "💧",
            "risk_off": "🛡️",
            "risk_on": "⚔️",
            "correlation_break": "🔗"
        }
    
    async def send_market_summary(self, monitoring_result: Dict) -> bool:
        """시장 요약 알림 전송"""
        try:
            risk_level = monitoring_result['risk_assessment']['overall_risk_level']
            total_events = monitoring_result['total_events']
            
            # 위험도에 따른 색상 설정
            color_map = {
                "low": "good",
                "medium": "warning", 
                "high": "danger",
                "very_high": "#FF0000"
            }
            
            # 메인 메시지 구성
            main_text = f"📊 *시장 분석 요약* - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # 첨부 파일 구성
            attachment = {
                "color": color_map.get(risk_level, "warning"),
                "fields": [
                    {
                        "title": "위험도 평가",
                        "value": f"{self._get_risk_emoji(risk_level)} {risk_level.upper().replace('_', ' ')}",
                        "short": True
                    },
                    {
                        "title": "감지된 이벤트",
                        "value": f"{total_events}개",
                        "short": True
                    },
                    {
                        "title": "위험 점수",
                        "value": f"{monitoring_result['risk_assessment']['risk_score']:.2f}/1.00",
                        "short": True
                    }
                ]
            }
            
            # 우선순위 알림 추가
            if monitoring_result.get('priority_alerts'):
                priority_text = "\n*🚨 주요 알림:*\n"
                for i, alert in enumerate(monitoring_result['priority_alerts'][:3], 1):
                    emoji = self.event_emojis.get(alert.get('type', '').split('_')[-1], "⚠️")
                    priority_text += f"{i}. {emoji} `{alert['symbol']}` {alert['message']}\n"
                
                attachment["fields"].append({
                    "title": "우선순위 알림",
                    "value": priority_text,
                    "short": False
                })
            
            # 인사이트 추가
            insights = monitoring_result.get('advanced_analysis', {}).get('analysis_summary', {}).get('key_insights', [])
            if insights:
                insights_text = "\n".join([f"• {insight}" for insight in insights[:3]])
                attachment["fields"].append({
                    "title": "💡 주요 인사이트",
                    "value": insights_text,
                    "short": False
                })
            
            payload = {
                "channel": self.channel,
                "text": main_text,
                "attachments": [attachment],
                "username": "Economic Monitor Bot",
                "icon_emoji": ":chart_with_upwards_trend:"
            }
            
            return await self._send_webhook(payload)
            
        except Exception as e:
            self.logger.error(f"시장 요약 알림 전송 실패: {str(e)}")
            return False
    
    async def send_critical_alert(self, alert: SlackAlert) -> bool:
        """긴급 알림 전송"""
        try:
            # 쿨다운 체크
            if not self._check_cooldown(alert.symbol, alert.priority):
                self.logger.info(f"쿨다운으로 인해 {alert.symbol} 알림 스킵")
                return False
            
            # 시간당 알림 수 체크
            if not self._check_hourly_limit():
                self.logger.warning("시간당 알림 한도 초과")
                return False
            
            # 메시지 구성
            priority_emoji = self.priority_emojis[alert.priority]
            event_emoji = self.event_emojis.get(alert.symbol.lower(), "📊")
            
            main_text = f"{priority_emoji} *{alert.priority.value.upper()} ALERT* {event_emoji}"
            
            # 색상 설정
            color_map = {
                AlertPriority.LOW: "good",
                AlertPriority.MEDIUM: "warning",
                AlertPriority.HIGH: "danger", 
                AlertPriority.CRITICAL: "#FF0000"
            }
            
            attachment = {
                "color": color_map[alert.priority],
                "title": alert.title,
                "text": alert.message,
                "fields": [
                    {
                        "title": "심볼",
                        "value": f"`{alert.symbol}`",
                        "short": True
                    },
                    {
                        "title": "심각도",
                        "value": f"{alert.severity:.2f}",
                        "short": True
                    },
                    {
                        "title": "시간",
                        "value": alert.timestamp.strftime("%H:%M:%S"),
                        "short": True
                    }
                ],
                "footer": "Economic Monitor",
                "ts": int(alert.timestamp.timestamp())
            }
            
            # 상세 정보 추가
            if alert.details:
                details_text = ""
                for key, value in alert.details.items():
                    if isinstance(value, (int, float)):
                        details_text += f"• {key}: {value:.2f}\n"
                    else:
                        details_text += f"• {key}: {value}\n"
                
                if details_text:
                    attachment["fields"].append({
                        "title": "상세 정보",
                        "value": details_text,
                        "short": False
                    })
            
            # 차트 URL 추가
            if alert.chart_url:
                attachment["image_url"] = alert.chart_url
            
            payload = {
                "channel": self.channel,
                "text": main_text,
                "attachments": [attachment],
                "username": "Economic Alert Bot",
                "icon_emoji": ":rotating_light:"
            }
            
            success = await self._send_webhook(payload)
            
            if success:
                self._update_cooldown(alert.symbol, alert.priority)
                self._increment_hourly_count()
            
            return success
            
        except Exception as e:
            self.logger.error(f"긴급 알림 전송 실패: {str(e)}")
            return False
    
    async def send_news_notification(self, article_data: Dict) -> bool:
        """뉴스 생성 완료 알림"""
        try:
            main_text = "📰 *새로운 AI 경제 뉴스가 생성되었습니다*"
            
            # 기사 정보 추출
            headline = "경제 뉴스 업데이트"
            if isinstance(article_data.get('article'), dict):
                headline = article_data['article'].get('headline', headline)
            
            attachment = {
                "color": "#36a64f",
                "title": headline,
                "fields": [
                    {
                        "title": "생성 시간",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "short": True
                    }
                ]
            }
            
            # 주요 포인트 추가
            if isinstance(article_data.get('article'), dict):
                key_points = article_data['article'].get('key_points', [])
                if key_points:
                    points_text = "\n".join([f"• {point}" for point in key_points[:3]])
                    attachment["fields"].append({
                        "title": "주요 포인트",
                        "value": points_text,
                        "short": False
                    })
            
            payload = {
                "channel": self.channel,
                "text": main_text,
                "attachments": [attachment],
                "username": "News Generator Bot",
                "icon_emoji": ":newspaper:"
            }
            
            return await self._send_webhook(payload)
            
        except Exception as e:
            self.logger.error(f"뉴스 알림 전송 실패: {str(e)}")
            return False
    
    async def send_system_status(self, status: Dict) -> bool:
        """시스템 상태 알림"""
        try:
            main_text = "🔧 *시스템 상태 리포트*"
            
            # 상태에 따른 색상
            is_running = status.get('is_running', False)
            color = "good" if is_running else "danger"
            
            attachment = {
                "color": color,
                "fields": [
                    {
                        "title": "시스템 상태",
                        "value": "🟢 실행 중" if is_running else "🔴 중지됨",
                        "short": True
                    },
                    {
                        "title": "모니터링 심볼",
                        "value": f"{status.get('monitoring_symbols_count', 0)}개",
                        "short": True
                    },
                    {
                        "title": "최근 위험도",
                        "value": status.get('latest_risk_level', 'unknown').upper(),
                        "short": True
                    }
                ]
            }
            
            if status.get('last_analysis'):
                attachment["fields"].append({
                    "title": "마지막 분석",
                    "value": status['last_analysis'],
                    "short": False
                })
            
            payload = {
                "channel": self.channel,
                "text": main_text,
                "attachments": [attachment],
                "username": "System Monitor Bot",
                "icon_emoji": ":gear:"
            }
            
            return await self._send_webhook(payload)
            
        except Exception as e:
            self.logger.error(f"시스템 상태 알림 전송 실패: {str(e)}")
            return False
    
    async def _send_webhook(self, payload: Dict) -> bool:
        """웹훅으로 메시지 전송"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        self.logger.info("Slack 알림 전송 성공")
                        return True
                    else:
                        self.logger.error(f"Slack 알림 전송 실패: {response.status}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"웹훅 전송 오류: {str(e)}")
            return False
    
    def _get_risk_emoji(self, risk_level: str) -> str:
        """위험도에 따른 이모지 반환"""
        emoji_map = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠", 
            "very_high": "🔴"
        }
        return emoji_map.get(risk_level, "⚪")
    
    def _check_cooldown(self, symbol: str, priority: AlertPriority) -> bool:
        """쿨다운 체크"""
        if not self.alert_settings["enabled"]:
            return False
        
        now = datetime.now()
        cooldown_key = f"{symbol}_{priority.value}"
        
        if cooldown_key in self.last_alerts:
            last_time = self.last_alerts[cooldown_key]
            minutes_passed = (now - last_time).total_seconds() / 60
            
            # 긴급 알림은 쿨다운 시간 단축
            cooldown_minutes = self.alert_settings["cooldown_minutes"]
            if priority == AlertPriority.CRITICAL:
                cooldown_minutes = 5
            elif priority == AlertPriority.HIGH:
                cooldown_minutes = 10
            
            if minutes_passed < cooldown_minutes:
                return False
        
        return True
    
    def _update_cooldown(self, symbol: str, priority: AlertPriority):
        """쿨다운 업데이트"""
        cooldown_key = f"{symbol}_{priority.value}"
        self.last_alerts[cooldown_key] = datetime.now()
    
    def _check_hourly_limit(self) -> bool:
        """시간당 알림 한도 체크"""
        current_hour = datetime.now().hour
        
        # 시간이 바뀌면 카운트 리셋
        if current_hour != self.last_hour_reset:
            self.hourly_count = 0
            self.last_hour_reset = current_hour
        
        return self.hourly_count < self.alert_settings["max_alerts_per_hour"]
    
    def _increment_hourly_count(self):
        """시간당 알림 카운트 증가"""
        self.hourly_count += 1
    
    def update_settings(self, settings: Dict):
        """알림 설정 업데이트"""
        self.alert_settings.update(settings)
        self.logger.info(f"알림 설정 업데이트: {settings}")

# 유틸리티 함수들
def create_alert_from_event(event_data: Dict) -> SlackAlert:
    """이벤트 데이터로부터 SlackAlert 생성"""
    severity = event_data.get('severity', 0.5)
    
    # 심각도에 따른 우선순위 결정
    if severity >= 0.9:
        priority = AlertPriority.CRITICAL
    elif severity >= 0.7:
        priority = AlertPriority.HIGH
    elif severity >= 0.5:
        priority = AlertPriority.MEDIUM
    else:
        priority = AlertPriority.LOW
    
    return SlackAlert(
        title=f"{event_data.get('symbol', 'UNKNOWN')} - {event_data.get('event_type', 'Event')}",
        message=event_data.get('description', '이벤트가 감지되었습니다.'),
        priority=priority,
        symbol=event_data.get('symbol', 'UNKNOWN'),
        severity=severity,
        timestamp=datetime.fromisoformat(event_data.get('timestamp', datetime.now().isoformat())),
        details={
            'change_percent': event_data.get('change_percent'),
            'current_price': event_data.get('current_price'),
            'volume': event_data.get('volume'),
            'confidence': event_data.get('confidence')
        }
    )

# 테스트 함수
async def test_slack_notifier():
    """Slack 알림 시스템 테스트"""
    # 테스트용 웹훅 URL (실제 사용 시 환경변수나 설정 파일에서 로드)
    webhook_url = "YOUR_SLACK_WEBHOOK_URL_HERE"
    
    if webhook_url == "YOUR_SLACK_WEBHOOK_URL_HERE":
        print("❌ Slack 웹훅 URL을 설정해주세요")
        return
    
    notifier = SlackNotifier(webhook_url)
    
    # 테스트 알림 전송
    test_alert = SlackAlert(
        title="테스트 알림",
        message="Slack 알림 시스템 테스트입니다.",
        priority=AlertPriority.MEDIUM,
        symbol="TEST",
        severity=0.6,
        timestamp=datetime.now(),
        details={"test_value": 123.45}
    )
    
    print("📤 테스트 알림 전송 중...")
    success = await notifier.send_critical_alert(test_alert)
    
    if success:
        print("✅ 테스트 알림 전송 성공!")
    else:
        print("❌ 테스트 알림 전송 실패")

if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    
    # 테스트 실행
    asyncio.run(test_slack_notifier())
