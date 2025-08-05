"""
기술적 분석 지표 계산 모듈
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import yfinance as yf
from datetime import datetime, timedelta

class TechnicalSignal(Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    NEUTRAL = "neutral"
    SELL = "sell"
    STRONG_SELL = "strong_sell"

@dataclass
class TechnicalIndicators:
    symbol: str
    timestamp: datetime
    
    # 추세 지표
    sma_20: float  # 20일 단순이동평균
    sma_50: float  # 50일 단순이동평균
    ema_12: float  # 12일 지수이동평균
    ema_26: float  # 26일 지수이동평균
    
    # 모멘텀 지표
    rsi: float  # 상대강도지수 (0-100)
    macd: float  # MACD
    macd_signal: float  # MACD 신호선
    macd_histogram: float  # MACD 히스토그램
    
    # 변동성 지표
    bollinger_upper: float  # 볼린저 밴드 상단
    bollinger_middle: float  # 볼린저 밴드 중간 (20일 SMA)
    bollinger_lower: float  # 볼린저 밴드 하단
    bollinger_width: float  # 볼린저 밴드 폭
    
    # 거래량 지표
    volume_sma: float  # 거래량 이동평균
    volume_ratio: float  # 현재 거래량 / 평균 거래량
    
    # 지지/저항 레벨
    support_level: float
    resistance_level: float
    
    # 종합 신호
    overall_signal: TechnicalSignal
    signal_strength: float  # 0-1 scale

class TechnicalAnalyzer:
    """기술적 분석 지표 계산 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_symbol(self, symbol: str, period: str = "6mo") -> Optional[TechnicalIndicators]:
        """심볼에 대한 기술적 분석 수행"""
        try:
            # 데이터 수집
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty or len(hist) < 50:
                self.logger.warning(f"Insufficient data for {symbol}")
                return None
            
            # 각 지표 계산
            indicators = self._calculate_all_indicators(hist)
            
            # 종합 신호 계산
            overall_signal, signal_strength = self._calculate_overall_signal(indicators)
            
            return TechnicalIndicators(
                symbol=symbol,
                timestamp=datetime.now(),
                **indicators,
                overall_signal=overall_signal,
                signal_strength=signal_strength
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing {symbol}: {str(e)}")
            return None
    
    def _calculate_all_indicators(self, data: pd.DataFrame) -> Dict:
        """모든 기술적 지표 계산"""
        close = data['Close']
        high = data['High']
        low = data['Low']
        volume = data['Volume']
        
        indicators = {}
        
        # 이동평균
        indicators['sma_20'] = close.rolling(window=20).mean().iloc[-1]
        indicators['sma_50'] = close.rolling(window=50).mean().iloc[-1]
        indicators['ema_12'] = close.ewm(span=12).mean().iloc[-1]
        indicators['ema_26'] = close.ewm(span=26).mean().iloc[-1]
        
        # RSI 계산
        indicators['rsi'] = self._calculate_rsi(close)
        
        # MACD 계산
        macd_data = self._calculate_macd(close)
        indicators.update(macd_data)
        
        # 볼린저 밴드 계산
        bollinger_data = self._calculate_bollinger_bands(close)
        indicators.update(bollinger_data)
        
        # 거래량 지표
        indicators['volume_sma'] = volume.rolling(window=20).mean().iloc[-1]
        indicators['volume_ratio'] = volume.iloc[-1] / indicators['volume_sma'] if indicators['volume_sma'] > 0 else 1.0
        
        # 지지/저항 레벨
        support_resistance = self._calculate_support_resistance(high, low, close)
        indicators.update(support_resistance)
        
        return indicators
    
    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> float:
        """RSI 계산"""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50.0
    
    def _calculate_macd(self, close: pd.Series) -> Dict:
        """MACD 계산"""
        ema_12 = close.ewm(span=12).mean()
        ema_26 = close.ewm(span=26).mean()
        
        macd = ema_12 - ema_26
        macd_signal = macd.ewm(span=9).mean()
        macd_histogram = macd - macd_signal
        
        return {
            'macd': macd.iloc[-1] if not pd.isna(macd.iloc[-1]) else 0.0,
            'macd_signal': macd_signal.iloc[-1] if not pd.isna(macd_signal.iloc[-1]) else 0.0,
            'macd_histogram': macd_histogram.iloc[-1] if not pd.isna(macd_histogram.iloc[-1]) else 0.0
        }
    
    def _calculate_bollinger_bands(self, close: pd.Series, period: int = 20, std_dev: int = 2) -> Dict:
        """볼린저 밴드 계산"""
        sma = close.rolling(window=period).mean()
        std = close.rolling(window=period).std()
        
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        width = ((upper - lower) / sma) * 100
        
        return {
            'bollinger_upper': upper.iloc[-1] if not pd.isna(upper.iloc[-1]) else close.iloc[-1] * 1.02,
            'bollinger_middle': sma.iloc[-1] if not pd.isna(sma.iloc[-1]) else close.iloc[-1],
            'bollinger_lower': lower.iloc[-1] if not pd.isna(lower.iloc[-1]) else close.iloc[-1] * 0.98,
            'bollinger_width': width.iloc[-1] if not pd.isna(width.iloc[-1]) else 4.0
        }
    
    def _calculate_support_resistance(self, high: pd.Series, low: pd.Series, close: pd.Series) -> Dict:
        """지지/저항 레벨 계산"""
        # 최근 20일간의 고점/저점 분석
        recent_high = high.rolling(window=20).max().iloc[-1]
        recent_low = low.rolling(window=20).min().iloc[-1]
        
        # 피벗 포인트 계산
        pivot = (recent_high + recent_low + close.iloc[-1]) / 3
        
        # 지지/저항 레벨 (단순화된 계산)
        resistance = pivot + (recent_high - recent_low) * 0.618  # 피보나치 비율 적용
        support = pivot - (recent_high - recent_low) * 0.618
        
        return {
            'support_level': max(support, recent_low),
            'resistance_level': min(resistance, recent_high)
        }
    
    def _calculate_overall_signal(self, indicators: Dict) -> Tuple[TechnicalSignal, float]:
        """종합 매매 신호 계산"""
        signals = []
        weights = []
        
        current_price = indicators.get('bollinger_middle', 0)  # SMA20을 현재가로 근사
        
        # RSI 신호 (가중치: 0.25)
        rsi = indicators.get('rsi', 50)
        if rsi > 70:
            signals.append(-2)  # 과매수
        elif rsi > 60:
            signals.append(-1)
        elif rsi < 30:
            signals.append(2)   # 과매도
        elif rsi < 40:
            signals.append(1)
        else:
            signals.append(0)
        weights.append(0.25)
        
        # MACD 신호 (가중치: 0.25)
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        macd_histogram = indicators.get('macd_histogram', 0)
        
        if macd > macd_signal and macd_histogram > 0:
            signals.append(2)   # 강한 매수
        elif macd > macd_signal:
            signals.append(1)   # 매수
        elif macd < macd_signal and macd_histogram < 0:
            signals.append(-2)  # 강한 매도
        elif macd < macd_signal:
            signals.append(-1)  # 매도
        else:
            signals.append(0)
        weights.append(0.25)
        
        # 이동평균 신호 (가중치: 0.2)
        sma_20 = indicators.get('sma_20', current_price)
        sma_50 = indicators.get('sma_50', current_price)
        
        if sma_20 > sma_50 * 1.02:  # 골든크로스
            signals.append(2)
        elif sma_20 > sma_50:
            signals.append(1)
        elif sma_20 < sma_50 * 0.98:  # 데드크로스
            signals.append(-2)
        elif sma_20 < sma_50:
            signals.append(-1)
        else:
            signals.append(0)
        weights.append(0.2)
        
        # 볼린저 밴드 신호 (가중치: 0.15)
        bollinger_upper = indicators.get('bollinger_upper', current_price * 1.02)
        bollinger_lower = indicators.get('bollinger_lower', current_price * 0.98)
        
        if current_price >= bollinger_upper:
            signals.append(-1)  # 과매수 구간
        elif current_price <= bollinger_lower:
            signals.append(1)   # 과매도 구간
        else:
            signals.append(0)
        weights.append(0.15)
        
        # 거래량 신호 (가중치: 0.15)
        volume_ratio = indicators.get('volume_ratio', 1.0)
        if volume_ratio > 2.0:
            signals.append(1)   # 거래량 급증은 긍정적
        elif volume_ratio < 0.5:
            signals.append(-1)  # 거래량 급감은 부정적
        else:
            signals.append(0)
        weights.append(0.15)
        
        # 가중 평균 계산
        weighted_signal = sum(s * w for s, w in zip(signals, weights))
        signal_strength = abs(weighted_signal) / 2.0  # 0-1 정규화
        
        # 신호 분류
        if weighted_signal >= 1.5:
            return TechnicalSignal.STRONG_BUY, signal_strength
        elif weighted_signal >= 0.5:
            return TechnicalSignal.BUY, signal_strength
        elif weighted_signal <= -1.5:
            return TechnicalSignal.STRONG_SELL, signal_strength
        elif weighted_signal <= -0.5:
            return TechnicalSignal.SELL, signal_strength
        else:
            return TechnicalSignal.NEUTRAL, signal_strength
    
    def get_signal_description(self, indicators: TechnicalIndicators) -> str:
        """기술적 분석 결과 설명 생성"""
        desc_parts = []
        
        # RSI 분석
        if indicators.rsi > 70:
            desc_parts.append(f"RSI {indicators.rsi:.1f}로 과매수 상태")
        elif indicators.rsi < 30:
            desc_parts.append(f"RSI {indicators.rsi:.1f}로 과매도 상태")
        
        # MACD 분석
        if indicators.macd > indicators.macd_signal:
            desc_parts.append("MACD 상승 추세")
        else:
            desc_parts.append("MACD 하락 추세")
        
        # 볼린저 밴드 분석
        current_price = indicators.bollinger_middle
        if current_price >= indicators.bollinger_upper:
            desc_parts.append("볼린저 밴드 상단 돌파")
        elif current_price <= indicators.bollinger_lower:
            desc_parts.append("볼린저 밴드 하단 접촉")
        
        # 거래량 분석
        if indicators.volume_ratio > 2.0:
            desc_parts.append(f"거래량 {indicators.volume_ratio:.1f}배 급증")
        
        return ", ".join(desc_parts) if desc_parts else "기술적 지표 중립"

# 테스트 함수
def test_technical_analyzer():
    analyzer = TechnicalAnalyzer()
    
    symbols = ["AAPL", "GOOGL", "MSFT", "^GSPC"]
    
    for symbol in symbols:
        print(f"\n=== {symbol} 기술적 분석 ===")
        indicators = analyzer.analyze_symbol(symbol)
        
        if indicators:
            print(f"RSI: {indicators.rsi:.2f}")
            print(f"MACD: {indicators.macd:.4f}")
            print(f"볼린저 밴드: {indicators.bollinger_lower:.2f} - {indicators.bollinger_upper:.2f}")
            print(f"종합 신호: {indicators.overall_signal.value} (강도: {indicators.signal_strength:.2f})")
            print(f"설명: {analyzer.get_signal_description(indicators)}")
        else:
            print("분석 실패")

if __name__ == "__main__":
    test_technical_analyzer()
