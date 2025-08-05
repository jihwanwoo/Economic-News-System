"""
시장 감정 분석 모듈
"""

import re
import requests
import feedparser
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import logging
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

class SentimentScore(Enum):
    VERY_POSITIVE = "very_positive"  # 0.6 ~ 1.0
    POSITIVE = "positive"            # 0.2 ~ 0.6
    NEUTRAL = "neutral"              # -0.2 ~ 0.2
    NEGATIVE = "negative"            # -0.6 ~ -0.2
    VERY_NEGATIVE = "very_negative"  # -1.0 ~ -0.6

@dataclass
class NewsItem:
    title: str
    content: str
    source: str
    published_date: datetime
    url: str
    sentiment_score: float  # -1.0 to 1.0
    keywords: List[str]

@dataclass
class MarketSentiment:
    symbol: str
    timestamp: datetime
    overall_sentiment: SentimentScore
    sentiment_score: float  # -1.0 to 1.0
    confidence: float  # 0.0 to 1.0
    
    # 뉴스 기반 감정
    news_sentiment: float
    news_count: int
    
    # 감정 변화 추이
    sentiment_trend: str  # "improving", "declining", "stable"
    
    # 소셜 미디어 감정 (향후 확장용)
    social_sentiment: Optional[float] = None
    
    # VIX 기반 공포/탐욕 지수
    fear_greed_index: float = 50.0  # 0-100 scale
    
    # 주요 뉴스 항목들
    key_news: Optional[List[NewsItem]] = None

class SentimentAnalyzer:
    """시장 감정 분석 클래스"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 감정 분석용 키워드 사전
        self.positive_keywords = {
            'surge', 'rally', 'gain', 'rise', 'up', 'bull', 'bullish', 'growth', 
            'profit', 'earnings', 'beat', 'strong', 'robust', 'solid', 'positive',
            'optimistic', 'confident', 'breakthrough', 'success', 'record', 'high',
            '상승', '급등', '호조', '성장', '수익', '이익', '강세', '긍정', '낙관'
        }
        
        self.negative_keywords = {
            'fall', 'drop', 'decline', 'crash', 'bear', 'bearish', 'loss', 'losses',
            'weak', 'poor', 'disappointing', 'concern', 'worry', 'fear', 'risk',
            'uncertainty', 'volatile', 'pressure', 'struggle', 'challenge', 'low',
            '하락', '급락', '부진', '손실', '약세', '우려', '불안', '위험', '부정'
        }
        
        # 뉴스 피드 URL들
        self.news_feeds = [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://feeds.reuters.com/reuters/businessNews",
            "https://rss.cnn.com/rss/money_latest.rss",
            "https://feeds.marketwatch.com/marketwatch/topstories/"
        ]
    
    async def analyze_market_sentiment(self, symbol: str) -> Optional[MarketSentiment]:
        """특정 심볼에 대한 시장 감정 분석"""
        try:
            # 뉴스 데이터 수집
            news_items = await self._collect_news_data(symbol)
            
            if not news_items:
                self.logger.warning(f"No news data found for {symbol}")
                return None
            
            # 뉴스 감정 분석
            news_sentiment = self._analyze_news_sentiment(news_items)
            
            # VIX 기반 공포/탐욕 지수 계산
            fear_greed_index = await self._calculate_fear_greed_index()
            
            # 감정 추이 분석
            sentiment_trend = self._analyze_sentiment_trend(symbol, news_sentiment)
            
            # 종합 감정 점수 계산
            overall_score = self._calculate_overall_sentiment(
                news_sentiment, fear_greed_index
            )
            
            # 감정 분류
            sentiment_category = self._classify_sentiment(overall_score)
            
            # 신뢰도 계산
            confidence = self._calculate_confidence(news_items, overall_score)
            
            return MarketSentiment(
                symbol=symbol,
                timestamp=datetime.now(),
                overall_sentiment=sentiment_category,
                sentiment_score=overall_score,
                confidence=confidence,
                news_sentiment=news_sentiment,
                news_count=len(news_items),
                fear_greed_index=fear_greed_index,
                sentiment_trend=sentiment_trend,
                key_news=news_items[:5]  # 상위 5개 뉴스만 저장
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment for {symbol}: {str(e)}")
            return None
    
    async def _collect_news_data(self, symbol: str) -> List[NewsItem]:
        """뉴스 데이터 수집"""
        news_items = []
        
        # RSS 피드에서 뉴스 수집
        for feed_url in self.news_feeds:
            try:
                feed_items = await self._parse_rss_feed(feed_url, symbol)
                news_items.extend(feed_items)
            except Exception as e:
                self.logger.error(f"Error parsing feed {feed_url}: {str(e)}")
                continue
        
        # 중복 제거 및 날짜순 정렬
        unique_news = {}
        for item in news_items:
            if item.title not in unique_news:
                unique_news[item.title] = item
        
        sorted_news = sorted(
            unique_news.values(), 
            key=lambda x: x.published_date, 
            reverse=True
        )
        
        return sorted_news[:20]  # 최신 20개만 반환
    
    async def _parse_rss_feed(self, feed_url: str, symbol: str) -> List[NewsItem]:
        """RSS 피드 파싱"""
        news_items = []
        
        try:
            # RSS 피드 파싱
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:10]:  # 최신 10개만 처리
                # 심볼 관련성 확인
                if not self._is_relevant_to_symbol(entry.title + " " + entry.get('summary', ''), symbol):
                    continue
                
                # 감정 점수 계산
                content = entry.title + " " + entry.get('summary', '')
                sentiment_score = self._calculate_text_sentiment(content)
                
                # 키워드 추출
                keywords = self._extract_keywords(content)
                
                # 발행 날짜 파싱
                published_date = datetime.now()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                
                news_item = NewsItem(
                    title=entry.title,
                    content=entry.get('summary', ''),
                    source=feed.feed.get('title', 'Unknown'),
                    published_date=published_date,
                    url=entry.get('link', ''),
                    sentiment_score=sentiment_score,
                    keywords=keywords
                )
                
                news_items.append(news_item)
                
        except Exception as e:
            self.logger.error(f"Error parsing RSS feed {feed_url}: {str(e)}")
        
        return news_items
    
    def _is_relevant_to_symbol(self, text: str, symbol: str) -> bool:
        """텍스트가 심볼과 관련있는지 확인"""
        text_lower = text.lower()
        symbol_lower = symbol.lower()
        
        # 심볼 직접 매칭
        if symbol_lower in text_lower:
            return True
        
        # 회사명 매칭 (간단한 매핑)
        symbol_mappings = {
            'aapl': ['apple', 'iphone', 'mac', 'ipad'],
            'googl': ['google', 'alphabet', 'android', 'youtube'],
            'msft': ['microsoft', 'windows', 'azure', 'office'],
            'tsla': ['tesla', 'elon musk', 'electric vehicle', 'ev'],
            'nvda': ['nvidia', 'gpu', 'ai chip', 'graphics'],
            '^gspc': ['s&p 500', 'sp500', 'market index'],
            '^ixic': ['nasdaq', 'tech stock', 'technology'],
            '^vix': ['vix', 'volatility', 'fear index']
        }
        
        if symbol_lower in symbol_mappings:
            for keyword in symbol_mappings[symbol_lower]:
                if keyword in text_lower:
                    return True
        
        # 일반적인 시장 관련 키워드
        market_keywords = ['stock', 'market', 'trading', 'investor', 'economy', 'financial']
        return any(keyword in text_lower for keyword in market_keywords)
    
    def _calculate_text_sentiment(self, text: str) -> float:
        """텍스트의 감정 점수 계산 (간단한 키워드 기반)"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        total_words = len(text.split())
        
        if total_words == 0:
            return 0.0
        
        # 정규화된 감정 점수 계산
        positive_ratio = positive_count / total_words
        negative_ratio = negative_count / total_words
        
        sentiment_score = (positive_ratio - negative_ratio) * 10  # 스케일 조정
        
        # -1.0 ~ 1.0 범위로 클리핑
        return max(-1.0, min(1.0, sentiment_score))
    
    def _extract_keywords(self, text: str) -> List[str]:
        """텍스트에서 키워드 추출"""
        # 간단한 키워드 추출 (불용어 제거 및 중요 단어 추출)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # 불용어 제거
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        
        keywords = [word for word in words if word not in stop_words]
        
        # 빈도수 기반으로 상위 키워드 반환
        from collections import Counter
        word_counts = Counter(keywords)
        
        return [word for word, count in word_counts.most_common(10)]
    
    def _analyze_news_sentiment(self, news_items: List[NewsItem]) -> float:
        """뉴스 항목들의 종합 감정 분석"""
        if not news_items:
            return 0.0
        
        # 시간 가중치 적용 (최신 뉴스에 더 높은 가중치)
        total_weighted_sentiment = 0.0
        total_weight = 0.0
        
        now = datetime.now()
        
        for item in news_items:
            # 시간 차이에 따른 가중치 계산 (24시간 이내는 1.0, 그 이후는 감소)
            time_diff = (now - item.published_date).total_seconds() / 3600  # 시간 단위
            weight = max(0.1, 1.0 - (time_diff / 48))  # 48시간에 걸쳐 가중치 감소
            
            total_weighted_sentiment += item.sentiment_score * weight
            total_weight += weight
        
        return total_weighted_sentiment / total_weight if total_weight > 0 else 0.0
    
    async def _calculate_fear_greed_index(self) -> float:
        """VIX 기반 공포/탐욕 지수 계산"""
        try:
            import yfinance as yf
            
            # VIX 데이터 수집
            vix = yf.Ticker("^VIX")
            vix_data = vix.history(period="5d")
            
            if vix_data.empty:
                return 50.0  # 중립값
            
            current_vix = vix_data['Close'].iloc[-1]
            
            # VIX를 0-100 공포/탐욕 지수로 변환
            # VIX 10 이하: 극도의 탐욕 (90-100)
            # VIX 20 이하: 탐욕 (60-90)
            # VIX 30 이하: 중립 (40-60)
            # VIX 40 이하: 공포 (20-40)
            # VIX 40 이상: 극도의 공포 (0-20)
            
            if current_vix <= 10:
                fear_greed_index = 90 + (10 - current_vix)  # 90-100
            elif current_vix <= 20:
                fear_greed_index = 60 + (20 - current_vix) * 3  # 60-90
            elif current_vix <= 30:
                fear_greed_index = 40 + (30 - current_vix) * 2  # 40-60
            elif current_vix <= 40:
                fear_greed_index = 20 + (40 - current_vix) * 2  # 20-40
            else:
                fear_greed_index = max(0, 20 - (current_vix - 40))  # 0-20
            
            return min(100, max(0, fear_greed_index))
            
        except Exception as e:
            self.logger.error(f"Error calculating fear/greed index: {str(e)}")
            return 50.0  # 중립값 반환
    
    def _analyze_sentiment_trend(self, symbol: str, current_sentiment: float) -> str:
        """감정 추이 분석 (간단한 구현)"""
        # 실제로는 과거 데이터와 비교해야 하지만, 여기서는 간단히 구현
        if current_sentiment > 0.3:
            return "improving"
        elif current_sentiment < -0.3:
            return "declining"
        else:
            return "stable"
    
    def _calculate_overall_sentiment(self, news_sentiment: float, fear_greed_index: float) -> float:
        """종합 감정 점수 계산"""
        # 뉴스 감정 (70%)과 공포/탐욕 지수 (30%) 가중 평균
        fear_greed_normalized = (fear_greed_index - 50) / 50  # -1 ~ 1로 정규화
        
        overall_sentiment = (news_sentiment * 0.7) + (fear_greed_normalized * 0.3)
        
        return max(-1.0, min(1.0, overall_sentiment))
    
    def _classify_sentiment(self, sentiment_score: float) -> SentimentScore:
        """감정 점수를 카테고리로 분류"""
        if sentiment_score >= 0.6:
            return SentimentScore.VERY_POSITIVE
        elif sentiment_score >= 0.2:
            return SentimentScore.POSITIVE
        elif sentiment_score <= -0.6:
            return SentimentScore.VERY_NEGATIVE
        elif sentiment_score <= -0.2:
            return SentimentScore.NEGATIVE
        else:
            return SentimentScore.NEUTRAL
    
    def _calculate_confidence(self, news_items: List[NewsItem], overall_score: float) -> float:
        """신뢰도 계산"""
        if not news_items:
            return 0.0
        
        # 뉴스 개수가 많을수록 신뢰도 증가
        count_factor = min(1.0, len(news_items) / 10)
        
        # 감정 점수의 일관성 확인
        sentiment_scores = [item.sentiment_score for item in news_items]
        sentiment_std = np.std(sentiment_scores) if len(sentiment_scores) > 1 else 0
        consistency_factor = max(0.3, 1.0 - sentiment_std)
        
        # 최신성 확인 (24시간 이내 뉴스 비율)
        now = datetime.now()
        recent_news = sum(1 for item in news_items 
                         if (now - item.published_date).total_seconds() < 86400)
        recency_factor = recent_news / len(news_items)
        
        confidence = (count_factor * 0.4 + consistency_factor * 0.4 + recency_factor * 0.2)
        
        return min(1.0, max(0.0, confidence))
    
    def get_sentiment_description(self, sentiment: MarketSentiment) -> str:
        """감정 분석 결과 설명 생성"""
        desc_parts = []
        
        # 전체 감정
        sentiment_desc = {
            SentimentScore.VERY_POSITIVE: "매우 긍정적",
            SentimentScore.POSITIVE: "긍정적",
            SentimentScore.NEUTRAL: "중립적",
            SentimentScore.NEGATIVE: "부정적",
            SentimentScore.VERY_NEGATIVE: "매우 부정적"
        }
        
        desc_parts.append(f"시장 감정: {sentiment_desc[sentiment.overall_sentiment]}")
        desc_parts.append(f"신뢰도: {sentiment.confidence:.1%}")
        
        # 공포/탐욕 지수
        if sentiment.fear_greed_index > 70:
            desc_parts.append("극도의 탐욕 상태")
        elif sentiment.fear_greed_index > 55:
            desc_parts.append("탐욕 상태")
        elif sentiment.fear_greed_index < 30:
            desc_parts.append("극도의 공포 상태")
        elif sentiment.fear_greed_index < 45:
            desc_parts.append("공포 상태")
        
        # 뉴스 개수
        desc_parts.append(f"분석 뉴스: {sentiment.news_count}개")
        
        return ", ".join(desc_parts)

# 테스트 함수
async def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer()
    
    symbols = ["AAPL", "^GSPC"]
    
    for symbol in symbols:
        print(f"\n=== {symbol} 감정 분석 ===")
        sentiment = await analyzer.analyze_market_sentiment(symbol)
        
        if sentiment:
            print(f"전체 감정: {sentiment.overall_sentiment.value}")
            print(f"감정 점수: {sentiment.sentiment_score:.3f}")
            print(f"공포/탐욕 지수: {sentiment.fear_greed_index:.1f}")
            print(f"감정 추이: {sentiment.sentiment_trend}")
            print(f"설명: {analyzer.get_sentiment_description(sentiment)}")
            
            if sentiment.key_news:
                print("\n주요 뉴스:")
                for i, news in enumerate(sentiment.key_news[:3], 1):
                    print(f"{i}. {news.title} (감정: {news.sentiment_score:.2f})")
        else:
            print("분석 실패")

if __name__ == "__main__":
    asyncio.run(test_sentiment_analyzer())
