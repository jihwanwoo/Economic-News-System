#!/usr/bin/env python3
"""
통합 이벤트 감지 및 Slack 알림 시스템
실시간으로 경제 이벤트를 감지하고 Slack으로 알림 전송
"""

import os
import sys
import json
import requests
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import numpy as np

# .env 파일 로드
load_dotenv()

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EventSeverity(Enum):
    """이벤트 심각도"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class EconomicEvent:
    """경제 이벤트 데이터 클래스"""
    symbol: str
    event_type: str
    severity: EventSeverity
    title: str
    description: str
    current_value: float
    previous_value: float
    change_percent: float
    timestamp: datetime
    details: Dict[str, Any] = None

class EventDetector:
    """경제 이벤트 감지기"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 모니터링 대상 심볼
        self.symbols = [
            # 주요 지수
            "^GSPC",  # S&P 500
            "^IXIC",  # NASDAQ
            "^DJI",   # Dow Jones
            "^VIX",   # VIX
            
            # 주요 주식
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA",
            
            # 통화
            "USDKRW=X", "USDJPY=X", "EURUSD=X",
            
            # 원자재
            "GC=F",   # Gold
            "CL=F",   # Oil
            "BTC-USD" # Bitcoin
        ]
        
        # 이벤트 감지 임계값
        self.thresholds = {
            'price_change': {
                'medium': 2.0,    # 2% 변화
                'high': 5.0,      # 5% 변화
                'critical': 10.0  # 10% 변화
            },
            'volume_spike': {
                'medium': 1.5,    # 평균 대비 1.5배
                'high': 2.0,      # 평균 대비 2배
                'critical': 3.0   # 평균 대비 3배
            },
            'volatility': {
                'medium': 15.0,   # 15% 변동성
                'high': 25.0,     # 25% 변동성
                'critical': 40.0  # 40% 변동성
            }
        }
        
        self.logger.info("✅ 이벤트 감지기 초기화 완료")
    
    def detect_events(self) -> List[EconomicEvent]:
        """이벤트 감지 실행"""
        
        self.logger.info("🔍 경제 이벤트 감지 시작")
        events = []
        
        for symbol in self.symbols:
            try:
                # 데이터 수집
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d", interval="1d")
                
                if len(hist) < 2:
                    continue
                
                # 현재값과 이전값
                current_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2]
                current_volume = hist['Volume'].iloc[-1]
                
                # 변화율 계산
                price_change = ((current_price - previous_price) / previous_price) * 100
                
                # 평균 거래량 계산
                avg_volume = hist['Volume'].mean()
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                
                # 변동성 계산 (5일 기준)
                volatility = hist['Close'].pct_change().std() * 100
                
                # 이벤트 감지
                detected_events = self._analyze_metrics(
                    symbol, current_price, previous_price, price_change,
                    volume_ratio, volatility, current_volume
                )
                
                events.extend(detected_events)
                
            except Exception as e:
                self.logger.warning(f"⚠️ {symbol} 데이터 수집 실패: {e}")
                continue
        
        # 심각도별 정렬
        events.sort(key=lambda x: self._get_severity_score(x.severity), reverse=True)
        
        self.logger.info(f"✅ 이벤트 감지 완료: {len(events)}개 이벤트 발견")
        return events
    
    def _analyze_metrics(self, symbol: str, current_price: float, previous_price: float,
                        price_change: float, volume_ratio: float, volatility: float,
                        current_volume: float) -> List[EconomicEvent]:
        """메트릭 분석 및 이벤트 생성"""
        
        events = []
        
        # 1. 가격 변화 이벤트
        price_severity = self._get_price_change_severity(abs(price_change))
        if price_severity != EventSeverity.LOW:
            direction = "급등" if price_change > 0 else "급락"
            events.append(EconomicEvent(
                symbol=symbol,
                event_type="price_change",
                severity=price_severity,
                title=f"{symbol} {direction} 감지",
                description=f"{symbol}이(가) {price_change:.2f}% {direction}했습니다.",
                current_value=current_price,
                previous_value=previous_price,
                change_percent=price_change,
                timestamp=datetime.now(),
                details={
                    'direction': direction,
                    'volume': current_volume,
                    'volume_ratio': volume_ratio
                }
            ))
        
        # 2. 거래량 급증 이벤트
        volume_severity = self._get_volume_spike_severity(volume_ratio)
        if volume_severity != EventSeverity.LOW:
            events.append(EconomicEvent(
                symbol=symbol,
                event_type="volume_spike",
                severity=volume_severity,
                title=f"{symbol} 거래량 급증",
                description=f"{symbol}의 거래량이 평균 대비 {volume_ratio:.1f}배 증가했습니다.",
                current_value=current_volume,
                previous_value=current_volume / volume_ratio,
                change_percent=(volume_ratio - 1) * 100,
                timestamp=datetime.now(),
                details={
                    'volume_ratio': volume_ratio,
                    'price_change': price_change
                }
            ))
        
        # 3. 변동성 이벤트
        volatility_severity = self._get_volatility_severity(volatility)
        if volatility_severity != EventSeverity.LOW:
            events.append(EconomicEvent(
                symbol=symbol,
                event_type="high_volatility",
                severity=volatility_severity,
                title=f"{symbol} 높은 변동성",
                description=f"{symbol}의 변동성이 {volatility:.1f}%로 증가했습니다.",
                current_value=volatility,
                previous_value=0,  # 기준값
                change_percent=volatility,
                timestamp=datetime.now(),
                details={
                    'volatility': volatility,
                    'price_change': price_change
                }
            ))
        
        return events
    
    def _get_price_change_severity(self, abs_change: float) -> EventSeverity:
        """가격 변화 심각도 결정"""
        if abs_change >= self.thresholds['price_change']['critical']:
            return EventSeverity.CRITICAL
        elif abs_change >= self.thresholds['price_change']['high']:
            return EventSeverity.HIGH
        elif abs_change >= self.thresholds['price_change']['medium']:
            return EventSeverity.MEDIUM
        else:
            return EventSeverity.LOW
    
    def _get_volume_spike_severity(self, volume_ratio: float) -> EventSeverity:
        """거래량 급증 심각도 결정"""
        if volume_ratio >= self.thresholds['volume_spike']['critical']:
            return EventSeverity.CRITICAL
        elif volume_ratio >= self.thresholds['volume_spike']['high']:
            return EventSeverity.HIGH
        elif volume_ratio >= self.thresholds['volume_spike']['medium']:
            return EventSeverity.MEDIUM
        else:
            return EventSeverity.LOW
    
    def _get_volatility_severity(self, volatility: float) -> EventSeverity:
        """변동성 심각도 결정"""
        if volatility >= self.thresholds['volatility']['critical']:
            return EventSeverity.CRITICAL
        elif volatility >= self.thresholds['volatility']['high']:
            return EventSeverity.HIGH
        elif volatility >= self.thresholds['volatility']['medium']:
            return EventSeverity.MEDIUM
        else:
            return EventSeverity.LOW
    
    def _get_severity_score(self, severity: EventSeverity) -> int:
        """심각도 점수 반환"""
        scores = {
            EventSeverity.LOW: 1,
            EventSeverity.MEDIUM: 2,
            EventSeverity.HIGH: 3,
            EventSeverity.CRITICAL: 4
        }
        return scores.get(severity, 1)

class SlackNotifier:
    """Slack 알림 전송기"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # Slack Webhook URL 로드
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if not self.webhook_url:
            # config 파일에서 백업 로드
            try:
                with open('config/slack_webhook.txt', 'r') as f:
                    self.webhook_url = f.read().strip()
            except:
                raise ValueError("Slack Webhook URL이 설정되지 않았습니다")
        
        # 알림 설정
        self.min_severity = EventSeverity.MEDIUM  # 최소 알림 심각도
        self.cooldown_minutes = 10  # 동일 심볼 알림 쿨다운
        self.last_alerts = {}  # 마지막 알림 시간 추적
        
        self.logger.info("✅ Slack 알림 시스템 초기화 완료")
    
    def send_event_alert(self, event: EconomicEvent) -> bool:
        """이벤트 알림 전송"""
        
        # 심각도 필터링
        if self._get_severity_score(event.severity) < self._get_severity_score(self.min_severity):
            return False
        
        # 쿨다운 체크
        if not self._check_cooldown(event.symbol):
            return False
        
        try:
            # Slack 메시지 생성
            message = self._create_slack_message(event)
            
            # Slack 전송
            response = requests.post(
                self.webhook_url,
                json=message,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"✅ Slack 알림 전송 성공: {event.symbol} - {event.title}")
                self._update_cooldown(event.symbol)
                return True
            else:
                self.logger.error(f"❌ Slack 알림 전송 실패: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Slack 알림 전송 오류: {e}")
            return False
    
    def send_summary_alert(self, events: List[EconomicEvent]) -> bool:
        """이벤트 요약 알림 전송"""
        
        if not events:
            return False
        
        try:
            # 요약 메시지 생성
            message = self._create_summary_message(events)
            
            # Slack 전송
            response = requests.post(
                self.webhook_url,
                json=message,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"✅ Slack 요약 알림 전송 성공: {len(events)}개 이벤트")
                return True
            else:
                self.logger.error(f"❌ Slack 요약 알림 전송 실패: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Slack 요약 알림 전송 오류: {e}")
            return False
    
    def _create_slack_message(self, event: EconomicEvent) -> Dict[str, Any]:
        """개별 이벤트 Slack 메시지 생성"""
        
        # 심각도별 색상 및 이모지
        severity_config = {
            EventSeverity.LOW: {"color": "#36a64f", "emoji": "ℹ️"},
            EventSeverity.MEDIUM: {"color": "#ff9500", "emoji": "⚠️"},
            EventSeverity.HIGH: {"color": "#ff0000", "emoji": "🚨"},
            EventSeverity.CRITICAL: {"color": "#8B0000", "emoji": "🔥"}
        }
        
        config = severity_config[event.severity]
        
        # 메시지 구성
        message = {
            "text": f"{config['emoji']} 경제 이벤트 감지: {event.title}",
            "attachments": [
                {
                    "color": config["color"],
                    "title": f"{config['emoji']} {event.title}",
                    "text": event.description,
                    "fields": [
                        {
                            "title": "심볼",
                            "value": event.symbol,
                            "short": True
                        },
                        {
                            "title": "심각도",
                            "value": event.severity.value.upper(),
                            "short": True
                        },
                        {
                            "title": "현재값",
                            "value": f"{event.current_value:.2f}",
                            "short": True
                        },
                        {
                            "title": "변화율",
                            "value": f"{event.change_percent:+.2f}%",
                            "short": True
                        }
                    ],
                    "footer": "경제 이벤트 모니터링 시스템",
                    "ts": int(event.timestamp.timestamp())
                }
            ]
        }
        
        # 추가 세부사항
        if event.details:
            additional_fields = []
            for key, value in event.details.items():
                if key == 'volume_ratio':
                    additional_fields.append({
                        "title": "거래량 비율",
                        "value": f"{value:.1f}x",
                        "short": True
                    })
                elif key == 'volatility':
                    additional_fields.append({
                        "title": "변동성",
                        "value": f"{value:.1f}%",
                        "short": True
                    })
            
            message["attachments"][0]["fields"].extend(additional_fields)
        
        return message
    
    def _create_summary_message(self, events: List[EconomicEvent]) -> Dict[str, Any]:
        """이벤트 요약 메시지 생성"""
        
        # 심각도별 집계
        severity_counts = {
            EventSeverity.CRITICAL: 0,
            EventSeverity.HIGH: 0,
            EventSeverity.MEDIUM: 0,
            EventSeverity.LOW: 0
        }
        
        for event in events:
            severity_counts[event.severity] += 1
        
        # 요약 텍스트 생성
        summary_text = f"📊 경제 이벤트 요약 ({len(events)}개 이벤트)\n"
        
        if severity_counts[EventSeverity.CRITICAL] > 0:
            summary_text += f"🔥 긴급: {severity_counts[EventSeverity.CRITICAL]}개\n"
        if severity_counts[EventSeverity.HIGH] > 0:
            summary_text += f"🚨 높음: {severity_counts[EventSeverity.HIGH]}개\n"
        if severity_counts[EventSeverity.MEDIUM] > 0:
            summary_text += f"⚠️ 보통: {severity_counts[EventSeverity.MEDIUM]}개\n"
        
        # 상위 이벤트 목록
        top_events = events[:5]  # 상위 5개
        event_list = "\n".join([
            f"• {event.symbol}: {event.title} ({event.change_percent:+.1f}%)"
            for event in top_events
        ])
        
        message = {
            "text": "📊 경제 이벤트 요약 보고서",
            "attachments": [
                {
                    "color": "#36a64f",
                    "title": f"📊 경제 이벤트 요약 ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
                    "text": summary_text,
                    "fields": [
                        {
                            "title": "주요 이벤트",
                            "value": event_list,
                            "short": False
                        }
                    ],
                    "footer": "경제 이벤트 모니터링 시스템",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        return message
    
    def _check_cooldown(self, symbol: str) -> bool:
        """쿨다운 체크"""
        now = datetime.now()
        last_alert = self.last_alerts.get(symbol)
        
        if last_alert is None:
            return True
        
        time_diff = (now - last_alert).total_seconds() / 60
        return time_diff >= self.cooldown_minutes
    
    def _update_cooldown(self, symbol: str):
        """쿨다운 업데이트"""
        self.last_alerts[symbol] = datetime.now()
    
    def _get_severity_score(self, severity: EventSeverity) -> int:
        """심각도 점수 반환"""
        scores = {
            EventSeverity.LOW: 1,
            EventSeverity.MEDIUM: 2,
            EventSeverity.HIGH: 3,
            EventSeverity.CRITICAL: 4
        }
        return scores.get(severity, 1)

class EventMonitoringSystem:
    """통합 이벤트 모니터링 시스템"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        self.detector = EventDetector()
        self.notifier = SlackNotifier()
        
        self.logger.info("✅ 통합 이벤트 모니터링 시스템 초기화 완료")
    
    def run_single_scan(self) -> Dict[str, Any]:
        """단일 스캔 실행"""
        
        self.logger.info("🔍 이벤트 스캔 시작")
        
        try:
            # 이벤트 감지
            events = self.detector.detect_events()
            
            # 결과 정리
            result = {
                'timestamp': datetime.now().isoformat(),
                'total_events': len(events),
                'events_by_severity': {
                    'critical': len([e for e in events if e.severity == EventSeverity.CRITICAL]),
                    'high': len([e for e in events if e.severity == EventSeverity.HIGH]),
                    'medium': len([e for e in events if e.severity == EventSeverity.MEDIUM]),
                    'low': len([e for e in events if e.severity == EventSeverity.LOW])
                },
                'events': []
            }
            
            # 이벤트 정보 추가
            for event in events:
                result['events'].append({
                    'symbol': event.symbol,
                    'type': event.event_type,
                    'severity': event.severity.value,
                    'title': event.title,
                    'description': event.description,
                    'change_percent': event.change_percent,
                    'timestamp': event.timestamp.isoformat()
                })
            
            # Slack 알림 전송
            if events:
                # 개별 중요 이벤트 알림
                critical_high_events = [e for e in events if e.severity in [EventSeverity.CRITICAL, EventSeverity.HIGH]]
                for event in critical_high_events[:3]:  # 최대 3개
                    self.notifier.send_event_alert(event)
                
                # 요약 알림 (이벤트가 많을 때)
                if len(events) >= 3:
                    self.notifier.send_summary_alert(events)
            
            self.logger.info(f"✅ 이벤트 스캔 완료: {len(events)}개 이벤트")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 이벤트 스캔 실패: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'total_events': 0
            }
    
    def run_continuous_monitoring(self, interval_minutes: int = 15):
        """연속 모니터링 실행"""
        
        self.logger.info(f"🔄 연속 모니터링 시작 (간격: {interval_minutes}분)")
        
        try:
            while True:
                # 스캔 실행
                result = self.run_single_scan()
                
                # 결과 로깅
                if result.get('total_events', 0) > 0:
                    self.logger.info(f"📊 이벤트 발견: {result['total_events']}개")
                else:
                    self.logger.info("😴 이벤트 없음")
                
                # 대기
                import time
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            self.logger.info("⏹️ 모니터링 중단됨")
        except Exception as e:
            self.logger.error(f"❌ 연속 모니터링 오류: {e}")

def main():
    """메인 함수"""
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 경제 이벤트 감지 및 Slack 알림 시스템")
    print("=" * 60)
    
    # 시스템 초기화
    monitor = EventMonitoringSystem()
    
    # 단일 스캔 실행
    print("\n1️⃣ 단일 스캔 테스트 실행 중...")
    result = monitor.run_single_scan()
    
    print(f"\n📊 스캔 결과:")
    print(f"   총 이벤트: {result.get('total_events', 0)}개")
    
    if result.get('events_by_severity'):
        severity_counts = result['events_by_severity']
        print(f"   🔥 긴급: {severity_counts.get('critical', 0)}개")
        print(f"   🚨 높음: {severity_counts.get('high', 0)}개")
        print(f"   ⚠️ 보통: {severity_counts.get('medium', 0)}개")
        print(f"   ℹ️ 낮음: {severity_counts.get('low', 0)}개")
    
    if result.get('events'):
        print(f"\n📋 주요 이벤트:")
        for event in result['events'][:5]:
            print(f"   • {event['symbol']}: {event['title']} ({event['change_percent']:+.1f}%)")
    
    # 연속 모니터링 옵션
    print(f"\n2️⃣ 연속 모니터링 옵션:")
    print("   연속 모니터링을 시작하려면 'y'를 입력하세요 (Ctrl+C로 중단)")
    
    try:
        choice = input("   선택: ").strip().lower()
        if choice == 'y':
            monitor.run_continuous_monitoring(interval_minutes=5)  # 5분 간격
    except KeyboardInterrupt:
        print("\n👋 프로그램 종료")

if __name__ == "__main__":
    main()
