"""
경제 데이터 수집 Agent
"""

import yfinance as yf
import requests
import feedparser
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import json

from .base_agent import BaseAgent, AgentConfig


class DataCollectorAgent(BaseAgent):
    """경제 데이터 수집을 담당하는 Agent"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        
        # 경제 데이터 소스 설정
        self.stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'SPY', 'QQQ']
        self.economic_indicators = ['^GSPC', '^DJI', '^IXIC', '^VIX']
        
        # 뉴스 RSS 피드
        self.news_feeds = [
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://feeds.reuters.com/reuters/businessNews',
            'https://rss.cnn.com/rss/money_latest.rss'
        ]
    
    def get_system_prompt(self) -> str:
        return """
        당신은 경제 데이터 수집 전문가입니다. 
        주식 시장 데이터, 경제 지표, 뉴스 정보를 수집하고 분석하여 
        경제 기사 작성에 필요한 핵심 정보를 추출합니다.
        
        수집된 데이터를 바탕으로:
        1. 주요 시장 동향 파악
        2. 중요한 경제 이벤트 식별
        3. 투자자 관심사 분석
        4. 시장 센티먼트 평가
        
        정확하고 객관적인 데이터 분석을 제공하세요.
        """
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 수집 및 분석 프로세스"""
        self.log_activity("데이터 수집 시작")
        
        try:
            # 1. 주식 데이터 수집
            stock_data = self.collect_stock_data()
            
            # 2. 경제 지표 수집
            economic_data = self.collect_economic_indicators()
            
            # 3. 뉴스 데이터 수집
            news_data = self.collect_news_data()
            
            # 4. 데이터 분석 및 요약
            analysis = self.analyze_collected_data(stock_data, economic_data, news_data)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "stock_data": stock_data,
                "economic_data": economic_data,
                "news_data": news_data,
                "analysis": analysis
            }
            
            self.log_activity("데이터 수집 완료", {"items_collected": len(result)})
            return result
            
        except Exception as e:
            self.logger.error(f"데이터 수집 중 오류: {str(e)}")
            raise
    
    def collect_stock_data(self) -> Dict[str, Any]:
        """주식 데이터 수집"""
        stock_data = {}
        
        try:
            for symbol in self.stock_symbols + self.economic_indicators:
                ticker = yf.Ticker(symbol)
                
                # 최근 5일 데이터
                hist = ticker.history(period="5d")
                if not hist.empty:
                    latest = hist.iloc[-1]
                    prev = hist.iloc[-2] if len(hist) > 1 else latest
                    
                    stock_data[symbol] = {
                        "current_price": float(latest['Close']),
                        "previous_price": float(prev['Close']),
                        "change": float(latest['Close'] - prev['Close']),
                        "change_percent": float((latest['Close'] - prev['Close']) / prev['Close'] * 100),
                        "volume": int(latest['Volume']) if 'Volume' in latest else 0,
                        "high": float(latest['High']),
                        "low": float(latest['Low']),
                        "timestamp": latest.name.isoformat()
                    }
                    
                # 기본 정보
                info = ticker.info
                if info:
                    stock_data[symbol].update({
                        "name": info.get('longName', symbol),
                        "sector": info.get('sector', 'N/A'),
                        "market_cap": info.get('marketCap', 0)
                    })
                    
        except Exception as e:
            self.logger.error(f"주식 데이터 수집 오류: {str(e)}")
        
        return stock_data
    
    def collect_economic_indicators(self) -> Dict[str, Any]:
        """경제 지표 수집"""
        indicators = {}
        
        try:
            # VIX (공포 지수)
            vix = yf.Ticker("^VIX")
            vix_hist = vix.history(period="5d")
            if not vix_hist.empty:
                latest_vix = vix_hist.iloc[-1]
                indicators["VIX"] = {
                    "value": float(latest_vix['Close']),
                    "interpretation": self.interpret_vix(float(latest_vix['Close']))
                }
            
            # 달러 인덱스
            dxy = yf.Ticker("DX-Y.NYB")
            dxy_hist = dxy.history(period="5d")
            if not dxy_hist.empty:
                latest_dxy = dxy_hist.iloc[-1]
                indicators["DXY"] = {
                    "value": float(latest_dxy['Close']),
                    "interpretation": "달러 강세" if latest_dxy['Close'] > 100 else "달러 약세"
                }
                
        except Exception as e:
            self.logger.error(f"경제 지표 수집 오류: {str(e)}")
        
        return indicators
    
    def collect_news_data(self) -> List[Dict[str, Any]]:
        """뉴스 데이터 수집"""
        news_items = []
        
        for feed_url in self.news_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # 최신 5개 기사
                    news_item = {
                        "title": entry.title,
                        "summary": entry.get('summary', ''),
                        "link": entry.link,
                        "published": entry.get('published', ''),
                        "source": feed.feed.get('title', 'Unknown')
                    }
                    news_items.append(news_item)
                    
            except Exception as e:
                self.logger.error(f"뉴스 수집 오류 ({feed_url}): {str(e)}")
        
        return news_items[:20]  # 최대 20개 기사
    
    def analyze_collected_data(self, stock_data: Dict, economic_data: Dict, news_data: List) -> Dict[str, Any]:
        """수집된 데이터 분석"""
        
        # LLM을 사용한 데이터 분석
        analysis_prompt = f"""
        다음 경제 데이터를 분석하여 주요 시장 동향과 투자 포인트를 요약해주세요:
        
        주식 데이터:
        {json.dumps(stock_data, ensure_ascii=False, indent=2)}
        
        경제 지표:
        {json.dumps(economic_data, ensure_ascii=False, indent=2)}
        
        최신 뉴스 헤드라인:
        {[item['title'] for item in news_data[:10]]}
        
        다음 형식으로 분석 결과를 제공해주세요:
        1. 주요 시장 동향
        2. 주목할 만한 종목/섹터
        3. 경제 지표 해석
        4. 투자자 관심사
        5. 리스크 요인
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": analysis_prompt}
        ]
        
        analysis_result = self.invoke_llm(messages)
        
        return {
            "llm_analysis": analysis_result,
            "data_summary": {
                "stocks_analyzed": len(stock_data),
                "news_items": len(news_data),
                "indicators_count": len(economic_data)
            }
        }
    
    def interpret_vix(self, vix_value: float) -> str:
        """VIX 값 해석"""
        if vix_value < 20:
            return "낮은 변동성 - 시장 안정"
        elif vix_value < 30:
            return "보통 변동성 - 시장 불확실성"
        else:
            return "높은 변동성 - 시장 공포"
