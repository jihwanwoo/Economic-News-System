"""
경제 데이터 수집 모듈
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp
import logging
from dataclasses import dataclass

@dataclass
class MarketData:
    symbol: str
    name: str
    timestamp: datetime
    current_price: float
    previous_close: float
    change_percent: float
    volume: int
    high_24h: float
    low_24h: float
    market_cap: Optional[float] = None

class EconomicDataCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def collect_yahoo_finance_data(self, symbol: str, period: str = "1d") -> Optional[MarketData]:
        """Yahoo Finance에서 데이터 수집"""
        try:
            ticker = yf.Ticker(symbol)
            
            # 현재 정보 가져오기
            info = ticker.info
            hist = ticker.history(period="2d")  # 최근 2일 데이터
            
            if hist.empty:
                self.logger.warning(f"No data found for symbol: {symbol}")
                return None
            
            current_data = hist.iloc[-1]
            previous_data = hist.iloc[-2] if len(hist) > 1 else current_data
            
            # 변화율 계산
            change_percent = ((current_data['Close'] - previous_data['Close']) / previous_data['Close']) * 100
            
            return MarketData(
                symbol=symbol,
                name=info.get('longName', symbol),
                timestamp=datetime.now(),
                current_price=float(current_data['Close']),
                previous_close=float(previous_data['Close']),
                change_percent=float(change_percent),
                volume=int(current_data['Volume']),
                high_24h=float(current_data['High']),
                low_24h=float(current_data['Low']),
                market_cap=info.get('marketCap')
            )
            
        except Exception as e:
            self.logger.error(f"Error collecting data for {symbol}: {str(e)}")
            return None
    
    async def collect_multiple_symbols(self, symbols: List[str]) -> Dict[str, MarketData]:
        """여러 심볼의 데이터를 동시에 수집"""
        tasks = []
        for symbol in symbols:
            task = asyncio.create_task(
                asyncio.to_thread(self.collect_yahoo_finance_data, symbol)
            )
            tasks.append((symbol, task))
        
        results = {}
        for symbol, task in tasks:
            try:
                data = await task
                if data:
                    results[symbol] = data
            except Exception as e:
                self.logger.error(f"Failed to collect data for {symbol}: {str(e)}")
        
        return results
    
    def calculate_volatility(self, symbol: str, days: int = 30) -> float:
        """변동성 계산 (30일 기준)"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=f"{days}d")
            
            if len(hist) < 2:
                return 0.0
            
            # 일일 수익률 계산
            daily_returns = hist['Close'].pct_change().dropna()
            
            # 연환산 변동성 계산
            volatility = daily_returns.std() * np.sqrt(252) * 100  # 252 trading days
            
            return float(volatility)
            
        except Exception as e:
            self.logger.error(f"Error calculating volatility for {symbol}: {str(e)}")
            return 0.0
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """과거 데이터 조회"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            self.logger.error(f"Error getting historical data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, float]:
        """기술적 지표 계산"""
        if data.empty or len(data) < 20:
            return {}
        
        indicators = {}
        
        try:
            # 이동평균
            indicators['sma_20'] = data['Close'].rolling(window=20).mean().iloc[-1]
            indicators['sma_50'] = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else None
            
            # RSI (Relative Strength Index)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators['rsi'] = (100 - (100 / (1 + rs))).iloc[-1]
            
            # 볼린저 밴드
            sma_20 = data['Close'].rolling(window=20).mean()
            std_20 = data['Close'].rolling(window=20).std()
            indicators['bollinger_upper'] = (sma_20 + (std_20 * 2)).iloc[-1]
            indicators['bollinger_lower'] = (sma_20 - (std_20 * 2)).iloc[-1]
            
            # 현재 가격이 볼린저 밴드 어디에 위치하는지
            current_price = data['Close'].iloc[-1]
            indicators['bollinger_position'] = (current_price - indicators['bollinger_lower']) / (indicators['bollinger_upper'] - indicators['bollinger_lower'])
            
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators: {str(e)}")
        
        return indicators

# 사용 예시
async def test_data_collector():
    async with EconomicDataCollector() as collector:
        # 단일 심볼 테스트
        kospi_data = collector.collect_yahoo_finance_data("^KS11")
        if kospi_data:
            print(f"KOSPI: {kospi_data.current_price}, 변화율: {kospi_data.change_percent:.2f}%")
        
        # 다중 심볼 테스트
        symbols = ["^KS11", "^GSPC", "USDKRW=X"]
        data_dict = await collector.collect_multiple_symbols(symbols)
        
        for symbol, data in data_dict.items():
            print(f"{symbol}: {data.current_price}, 변화율: {data.change_percent:.2f}%")

if __name__ == "__main__":
    asyncio.run(test_data_collector())
