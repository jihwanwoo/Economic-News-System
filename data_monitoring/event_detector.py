"""
경제 이벤트 탐지 모듈
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from .data_collector import MarketData, EconomicDataCollector
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.monitoring_config import ECONOMIC_INDICATORS, SEVERITY_WEIGHTS

class EventType(Enum):
    SURGE = "surge"  # 급등
    DROP = "drop"    # 급락
    VOLATILITY = "volatility"  # 높은 변동성
    VOLUME_SPIKE = "volume_spike"  # 거래량 급증
    CORRELATION_BREAK = "correlation_break"  # 상관관계 이탈

@dataclass
class EconomicEvent:
    event_id: str
    symbol: str
    name: str
    event_type: EventType
    severity: float  # 0-1 scale
    timestamp: datetime
    current_price: float
    change_percent: float
    volume: int
    description: str
    technical_indicators: Dict[str, float]
    market_context: Dict[str, any]

class EventDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_collector = EconomicDataCollector()
        self.event_history = []  # 최근 이벤트 기록
        self.alert_cooldown = {}  # 알림 쿨다운 관리
    
    def detect_events(self, market_data: Dict[str, MarketData]) -> List[EconomicEvent]:
        """시장 데이터에서 이벤트 탐지"""
        events = []
        
        for symbol, data in market_data.items():
            # 각 지표별 임계값 확인
            indicator_config = self._get_indicator_config(symbol)
            if not indicator_config:
                continue
            
            # 1. 가격 변동 이벤트 탐지
            price_events = self._detect_price_events(data, indicator_config)
            events.extend(price_events)
            
            # 2. 거래량 이벤트 탐지
            volume_events = self._detect_volume_events(data, symbol)
            events.extend(volume_events)
            
            # 3. 변동성 이벤트 탐지
            volatility_events = self._detect_volatility_events(data, indicator_config, symbol)
            events.extend(volatility_events)
        
        # 4. 시장 간 상관관계 이벤트 탐지
        correlation_events = self._detect_correlation_events(market_data)
        events.extend(correlation_events)
        
        # 5. 이벤트 필터링 및 우선순위 정렬
        filtered_events = self._filter_and_prioritize_events(events)
        
        return filtered_events
    
    def _get_indicator_config(self, symbol: str) -> Optional[Dict]:
        """심볼에 해당하는 설정 찾기"""
        for category, indicators in ECONOMIC_INDICATORS.items():
            for key, config in indicators.items():
                if config['symbol'] == symbol:
                    return config
        return None
    
    def _detect_price_events(self, data: MarketData, config: Dict) -> List[EconomicEvent]:
        """가격 변동 이벤트 탐지"""
        events = []
        change_percent = data.change_percent
        
        # 급등 탐지
        if change_percent >= config['threshold_surge']:
            severity = min(abs(change_percent) / 10.0, 1.0)  # 10% 변동을 최대로 정규화
            
            event = EconomicEvent(
                event_id=f"{data.symbol}_SURGE_{int(datetime.now().timestamp())}",
                symbol=data.symbol,
                name=data.name,
                event_type=EventType.SURGE,
                severity=severity,
                timestamp=data.timestamp,
                current_price=data.current_price,
                change_percent=change_percent,
                volume=data.volume,
                description=f"{data.name}이(가) {change_percent:.2f}% 급등했습니다.",
                technical_indicators=self._get_technical_indicators(data.symbol),
                market_context=self._get_market_context(data)
            )
            events.append(event)
        
        # 급락 탐지
        elif change_percent <= config['threshold_drop']:
            severity = min(abs(change_percent) / 10.0, 1.0)
            
            event = EconomicEvent(
                event_id=f"{data.symbol}_DROP_{int(datetime.now().timestamp())}",
                symbol=data.symbol,
                name=data.name,
                event_type=EventType.DROP,
                severity=severity,
                timestamp=data.timestamp,
                current_price=data.current_price,
                change_percent=change_percent,
                volume=data.volume,
                description=f"{data.name}이(가) {change_percent:.2f}% 급락했습니다.",
                technical_indicators=self._get_technical_indicators(data.symbol),
                market_context=self._get_market_context(data)
            )
            events.append(event)
        
        return events
    
    def _detect_volume_events(self, data: MarketData, symbol: str) -> List[EconomicEvent]:
        """거래량 급증 이벤트 탐지"""
        events = []
        
        try:
            # 최근 20일 평균 거래량과 비교
            historical_data = self.data_collector.get_historical_data(symbol, "1mo")
            if historical_data.empty or len(historical_data) < 20:
                return events
            
            avg_volume = historical_data['Volume'].rolling(window=20).mean().iloc[-2]  # 전일까지의 평균
            volume_ratio = data.volume / avg_volume if avg_volume > 0 else 0
            
            # 거래량이 평균의 3배 이상인 경우
            if volume_ratio >= 3.0:
                severity = min(volume_ratio / 10.0, 1.0)  # 10배를 최대로 정규화
                
                event = EconomicEvent(
                    event_id=f"{data.symbol}_VOLUME_{int(datetime.now().timestamp())}",
                    symbol=data.symbol,
                    name=data.name,
                    event_type=EventType.VOLUME_SPIKE,
                    severity=severity,
                    timestamp=data.timestamp,
                    current_price=data.current_price,
                    change_percent=data.change_percent,
                    volume=data.volume,
                    description=f"{data.name}의 거래량이 평균 대비 {volume_ratio:.1f}배 급증했습니다.",
                    technical_indicators=self._get_technical_indicators(symbol),
                    market_context={'volume_ratio': volume_ratio, 'avg_volume': avg_volume}
                )
                events.append(event)
        
        except Exception as e:
            self.logger.error(f"Error detecting volume events for {symbol}: {str(e)}")
        
        return events
    
    def _detect_volatility_events(self, data: MarketData, config: Dict, symbol: str) -> List[EconomicEvent]:
        """변동성 이벤트 탐지"""
        events = []
        
        try:
            # 일중 변동성 계산 (고가-저가)/종가
            intraday_volatility = ((data.high_24h - data.low_24h) / data.current_price) * 100
            
            if intraday_volatility >= config['volatility_threshold']:
                severity = min(intraday_volatility / 20.0, 1.0)  # 20% 변동성을 최대로 정규화
                
                event = EconomicEvent(
                    event_id=f"{data.symbol}_VOLATILITY_{int(datetime.now().timestamp())}",
                    symbol=data.symbol,
                    name=data.name,
                    event_type=EventType.VOLATILITY,
                    severity=severity,
                    timestamp=data.timestamp,
                    current_price=data.current_price,
                    change_percent=data.change_percent,
                    volume=data.volume,
                    description=f"{data.name}의 변동성이 {intraday_volatility:.2f}%로 높습니다.",
                    technical_indicators=self._get_technical_indicators(symbol),
                    market_context={'intraday_volatility': intraday_volatility}
                )
                events.append(event)
        
        except Exception as e:
            self.logger.error(f"Error detecting volatility events for {symbol}: {str(e)}")
        
        return events
    
    def _detect_correlation_events(self, market_data: Dict[str, MarketData]) -> List[EconomicEvent]:
        """시장 간 상관관계 이탈 이벤트 탐지"""
        events = []
        
        # 주요 지수 간 상관관계 확인 (KOSPI, S&P500, NASDAQ)
        major_indices = {}
        for symbol, data in market_data.items():
            if symbol in ['^KS11', '^GSPC', '^IXIC']:
                major_indices[symbol] = data
        
        if len(major_indices) >= 2:
            # 변화율 방향성 확인
            changes = {symbol: data.change_percent for symbol, data in major_indices.items()}
            
            # 일반적으로 같은 방향으로 움직이는데 반대로 움직이는 경우 탐지
            positive_changes = sum(1 for change in changes.values() if change > 1.0)
            negative_changes = sum(1 for change in changes.values() if change < -1.0)
            
            # 강한 반대 움직임이 있는 경우
            if positive_changes > 0 and negative_changes > 0:
                max_change = max(abs(change) for change in changes.values())
                severity = min(max_change / 5.0, 1.0)
                
                event = EconomicEvent(
                    event_id=f"CORRELATION_BREAK_{int(datetime.now().timestamp())}",
                    symbol="MARKET_CORRELATION",
                    name="시장 상관관계",
                    event_type=EventType.CORRELATION_BREAK,
                    severity=severity,
                    timestamp=datetime.now(),
                    current_price=0,
                    change_percent=0,
                    volume=0,
                    description="주요 지수 간 상관관계에서 이탈이 발생했습니다.",
                    technical_indicators={},
                    market_context={'market_changes': changes}
                )
                events.append(event)
        
        return events
    
    def _get_technical_indicators(self, symbol: str) -> Dict[str, float]:
        """기술적 지표 계산"""
        try:
            historical_data = self.data_collector.get_historical_data(symbol, "3mo")
            return self.data_collector.calculate_technical_indicators(historical_data)
        except Exception as e:
            self.logger.error(f"Error getting technical indicators for {symbol}: {str(e)}")
            return {}
    
    def _get_market_context(self, data: MarketData) -> Dict[str, any]:
        """시장 컨텍스트 정보"""
        return {
            'market_cap': data.market_cap,
            'price_range_24h': {
                'high': data.high_24h,
                'low': data.low_24h,
                'range_percent': ((data.high_24h - data.low_24h) / data.current_price) * 100
            },
            'previous_close': data.previous_close
        }
    
    def _filter_and_prioritize_events(self, events: List[EconomicEvent]) -> List[EconomicEvent]:
        """이벤트 필터링 및 우선순위 정렬"""
        # 쿨다운 필터링
        filtered_events = []
        current_time = datetime.now()
        
        for event in events:
            cooldown_key = f"{event.symbol}_{event.event_type.value}"
            
            # 쿨다운 체크
            if cooldown_key in self.alert_cooldown:
                last_alert = self.alert_cooldown[cooldown_key]
                if (current_time - last_alert).seconds < 300:  # 5분 쿨다운
                    continue
            
            self.alert_cooldown[cooldown_key] = current_time
            filtered_events.append(event)
        
        # 심각도 순으로 정렬
        filtered_events.sort(key=lambda x: x.severity, reverse=True)
        
        return filtered_events

# 테스트 함수
async def test_event_detector():
    detector = EventDetector()
    
    # 샘플 데이터로 테스트
    async with EconomicDataCollector() as collector:
        symbols = ["^KS11", "^GSPC", "USDKRW=X"]
        market_data = await collector.collect_multiple_symbols(symbols)
        
        events = detector.detect_events(market_data)
        
        print(f"탐지된 이벤트 수: {len(events)}")
        for event in events:
            print(f"- {event.name}: {event.event_type.value}, 심각도: {event.severity:.2f}")
            print(f"  {event.description}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_event_detector())
