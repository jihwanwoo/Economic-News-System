#!/usr/bin/env python3
"""
향상된 이미지 생성 에이전트
기사 내용 기반 맞춤 이미지 생성
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

class EnhancedImageGenerator:
    """향상된 이미지 생성 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.images_dir = "output/images"
        os.makedirs(self.images_dir, exist_ok=True)
        
        # matplotlib 폰트 설정
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        self.logger.info("✅ 향상된 이미지 생성 에이전트 초기화 완료")
    
    async def generate_article_illustration(self, article: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """기사 내용 기반 일러스트레이션 생성"""
        
        self.logger.info("🎨 기사 일러스트레이션 생성 시작")
        
        try:
            # 기사 내용 분석
            content = article.get('content', '')
            title = article.get('title', 'Market Analysis')
            symbol = event_data.get('symbol', 'MARKET')
            change_percent = event_data.get('change_percent', 0)
            
            # 기사 내용 요약 및 키워드 추출
            summary = self._analyze_article_content(content, title)
            
            # 요약 기반 이미지 생성
            image_path = await self._create_content_based_image(symbol, title, summary, change_percent)
            
            self.logger.info(f"✅ 기사 일러스트레이션 생성 완료: {image_path}")
            return image_path
            
        except Exception as e:
            self.logger.error(f"❌ 기사 일러스트레이션 생성 실패: {e}")
            return await self._create_fallback_image(event_data.get('symbol', 'MARKET'))
    
    def _analyze_article_content(self, content: str, title: str) -> Dict[str, Any]:
        """기사 내용 분석 및 요약"""
        
        try:
            # 키워드 분석
            keywords = {
                'bullish': ['상승', '증가', '급등', 'rise', 'increase', 'surge', 'bull'],
                'bearish': ['하락', '감소', '급락', 'fall', 'decrease', 'drop', 'bear'],
                'volatile': ['변동성', '불안정', 'volatility', 'unstable', 'fluctuation'],
                'volume': ['거래량', '물량', 'volume', 'trading'],
                'technical': ['기술적', '지표', 'technical', 'indicator', 'RSI', 'MACD'],
                'market': ['시장', '증시', 'market', 'stock', 'index']
            }
            
            content_lower = content.lower()
            title_lower = title.lower()
            
            analysis = {
                'trend': 'neutral',
                'sentiment': 'neutral',
                'volatility': 'normal',
                'volume_activity': 'normal',
                'technical_focus': False,
                'market_wide': False
            }
            
            # 트렌드 분석
            bullish_count = sum(1 for word in keywords['bullish'] if word in content_lower or word in title_lower)
            bearish_count = sum(1 for word in keywords['bearish'] if word in content_lower or word in title_lower)
            
            if bullish_count > bearish_count:
                analysis['trend'] = 'bullish'
                analysis['sentiment'] = 'positive'
            elif bearish_count > bullish_count:
                analysis['trend'] = 'bearish'
                analysis['sentiment'] = 'negative'
            
            # 변동성 분석
            if any(word in content_lower for word in keywords['volatile']):
                analysis['volatility'] = 'high'
            
            # 거래량 분석
            if any(word in content_lower for word in keywords['volume']):
                analysis['volume_activity'] = 'high'
            
            # 기술적 분석 포함 여부
            if any(word in content_lower for word in keywords['technical']):
                analysis['technical_focus'] = True
            
            # 시장 전반 분석 여부
            if any(word in content_lower for word in keywords['market']):
                analysis['market_wide'] = True
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"기사 내용 분석 실패: {e}")
            return {'trend': 'neutral', 'sentiment': 'neutral', 'volatility': 'normal'}
    
    async def _create_content_based_image(self, symbol: str, title: str, analysis: Dict[str, Any], change_percent: float) -> str:
        """내용 기반 맞춤 이미지 생성"""
        
        try:
            # 이미지 스타일 결정
            if analysis['trend'] == 'bullish':
                primary_color = '#2E8B57'  # Sea Green
                secondary_color = '#90EE90'  # Light Green
                arrow_direction = 'up'
            elif analysis['trend'] == 'bearish':
                primary_color = '#DC143C'  # Crimson
                secondary_color = '#FFB6C1'  # Light Pink
                arrow_direction = 'down'
            else:
                primary_color = '#4682B4'  # Steel Blue
                secondary_color = '#87CEEB'  # Sky Blue
                arrow_direction = 'neutral'
            
            # 그림 생성
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'{symbol} Market Analysis Illustration', fontsize=16, fontweight='bold')
            
            # 1. 가격 트렌드 시뮬레이션
            self._create_trend_chart(ax1, analysis, primary_color, change_percent)
            
            # 2. 시장 감정 게이지
            self._create_sentiment_gauge(ax2, analysis, primary_color)
            
            # 3. 거래량 활동
            self._create_volume_chart(ax3, analysis, secondary_color)
            
            # 4. 기술적 지표 요약
            self._create_technical_summary(ax4, analysis, primary_color)
            
            # 레이아웃 조정
            plt.tight_layout()
            
            # 파일 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_article_illustration_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"내용 기반 이미지 생성 실패: {e}")
            return await self._create_fallback_image(symbol)
    
    def _create_trend_chart(self, ax, analysis, color, change_percent):
        """트렌드 차트 생성"""
        
        x = np.linspace(0, 30, 100)
        
        if analysis['trend'] == 'bullish':
            y = 100 + np.cumsum(np.random.normal(0.5, 1, 100))
        elif analysis['trend'] == 'bearish':
            y = 100 + np.cumsum(np.random.normal(-0.5, 1, 100))
        else:
            y = 100 + np.cumsum(np.random.normal(0, 0.8, 100))
        
        ax.plot(x, y, color=color, linewidth=2.5, alpha=0.8)
        ax.fill_between(x, y, alpha=0.3, color=color)
        ax.set_title('Price Trend Simulation', fontweight='bold')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Price Level')
        ax.grid(True, alpha=0.3)
        
        # 변화율 표시
        ax.text(0.02, 0.98, f'Change: {change_percent:+.2f}%', 
                transform=ax.transAxes, fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def _create_sentiment_gauge(self, ax, analysis, color):
        """시장 감정 게이지 생성"""
        
        # 감정 점수 계산
        if analysis['sentiment'] == 'positive':
            sentiment_score = 0.7
        elif analysis['sentiment'] == 'negative':
            sentiment_score = 0.3
        else:
            sentiment_score = 0.5
        
        # 게이지 차트
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        ax.plot(theta, r, 'k-', linewidth=2)
        
        # 감정 영역 색칠
        fill_theta = np.linspace(0, sentiment_score * np.pi, 50)
        fill_r = np.ones_like(fill_theta)
        ax.fill_between(fill_theta, 0, fill_r, color=color, alpha=0.6)
        
        # 바늘 추가
        needle_theta = sentiment_score * np.pi
        ax.plot([needle_theta, needle_theta], [0, 1], 'r-', linewidth=3)
        
        ax.set_title('Market Sentiment Gauge', fontweight='bold')
        ax.set_ylim(0, 1.2)
        ax.set_xlim(0, np.pi)
        ax.set_xticks([0, np.pi/2, np.pi])
        ax.set_xticklabels(['Bearish', 'Neutral', 'Bullish'])
        ax.set_yticks([])
    
    def _create_volume_chart(self, ax, analysis, color):
        """거래량 차트 생성"""
        
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        
        if analysis['volume_activity'] == 'high':
            volumes = np.random.normal(150, 30, 5)
        else:
            volumes = np.random.normal(100, 20, 5)
        
        volumes = np.abs(volumes)  # 음수 제거
        
        bars = ax.bar(days, volumes, color=color, alpha=0.7)
        ax.set_title('Trading Volume Activity', fontweight='bold')
        ax.set_ylabel('Volume (Millions)')
        ax.grid(True, alpha=0.3, axis='y')
        
        # 평균선 추가
        avg_volume = np.mean(volumes)
        ax.axhline(y=avg_volume, color='red', linestyle='--', alpha=0.7, label=f'Avg: {avg_volume:.0f}M')
        ax.legend()
    
    def _create_technical_summary(self, ax, analysis, color):
        """기술적 지표 요약"""
        
        indicators = ['RSI', 'MACD', 'SMA', 'Bollinger']
        
        # 분석 결과에 따른 지표 값 생성
        if analysis['trend'] == 'bullish':
            values = [65, 0.5, 1.02, 0.8]
        elif analysis['trend'] == 'bearish':
            values = [35, -0.5, 0.98, 0.2]
        else:
            values = [50, 0, 1.0, 0.5]
        
        # 정규화 (0-1 범위)
        normalized_values = [(v - min(values)) / (max(values) - min(values)) if max(values) != min(values) else 0.5 for v in values]
        
        bars = ax.barh(indicators, normalized_values, color=color, alpha=0.7)
        ax.set_title('Technical Indicators Summary', fontweight='bold')
        ax.set_xlabel('Strength (Normalized)')
        ax.set_xlim(0, 1)
        
        # 중립선 추가
        ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, label='Neutral')
        ax.legend()
    
    async def _create_fallback_image(self, symbol: str) -> str:
        """기본 이미지 생성"""
        
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # 간단한 차트
            x = np.linspace(0, 10, 50)
            y = np.sin(x) + np.random.normal(0, 0.1, 50)
            
            ax.plot(x, y, color='#4682B4', linewidth=2)
            ax.fill_between(x, y, alpha=0.3, color='#4682B4')
            ax.set_title(f'{symbol} Market Analysis', fontsize=14, fontweight='bold')
            ax.set_xlabel('Time Period')
            ax.set_ylabel('Market Value')
            ax.grid(True, alpha=0.3)
            
            # 파일 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_fallback_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"기본 이미지 생성 실패: {e}")
            return ""

# 기존 ImageGeneratorAgent 클래스 업데이트
class ImageGeneratorAgent(EnhancedImageGenerator):
    """기존 ImageGeneratorAgent를 향상된 버전으로 업데이트"""
    
    async def generate_article_image(self, article: Dict[str, Any]) -> str:
        """기사 관련 이미지 생성 (향상된 버전)"""
        
        # 메타데이터에서 이벤트 정보 추출
        metadata = article.get('metadata', {})
        event_data = {
            'symbol': metadata.get('symbol', 'MARKET'),
            'change_percent': metadata.get('change_percent', 0),
            'event_type': metadata.get('event_type', 'market_analysis')
        }
        
        return await self.generate_article_illustration(article, event_data)
