#!/usr/bin/env python3
"""
이미지 생성 에이전트
기사 내용에 맞는 이미지 생성
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


from agents.enhanced_image_generator import EnhancedImageGenerator

class ImageGeneratorAgent(EnhancedImageGenerator):
    """이미지 생성 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.images_dir = "output/images"
        os.makedirs(self.images_dir, exist_ok=True)
        
        # 이미지 스타일 설정
        self.style_config = {
            'width': 800,
            'height': 600,
            'dpi': 100,
            'background_color': '#f8f9fa',
            'primary_color': '#007bff',
            'secondary_color': '#6c757d',
            'success_color': '#28a745',
            'danger_color': '#dc3545',
            'font_size_title': 24,
            'font_size_subtitle': 16,
            'font_size_body': 12
        }
        
        self.logger.info("✅ 이미지 생성 에이전트 초기화 완료")
    
    async def generate_article_image(self, article: Dict[str, Any]) -> str:
        """기사 관련 이미지 생성"""
        
        self.logger.info("🖼️ 기사 이미지 생성 시작")
        
        try:
            # 기사 메타데이터 추출
            metadata = article.get('metadata', {})
            symbol = metadata.get('symbol', 'UNKNOWN')
            event_type = metadata.get('event_type', 'price_change')
            change_percent = metadata.get('change_percent', 0)
            
            # 이미지 유형 결정
            if event_type == 'price_change':
                image_path = await self._create_price_change_image(symbol, change_percent, article)
            elif event_type == 'volume_spike':
                image_path = await self._create_volume_spike_image(symbol, article)
            elif event_type == 'high_volatility':
                image_path = await self._create_volatility_image(symbol, article)
            else:
                image_path = await self._create_generic_market_image(symbol, article)
            
            self.logger.info(f"✅ 기사 이미지 생성 완료: {image_path}")
            return image_path
            
        except Exception as e:
            self.logger.error(f"❌ 이미지 생성 실패: {e}")
            return ""
    
    async def _create_price_change_image(self, symbol: str, change_percent: float, article: Dict[str, Any]) -> str:
        """가격 변동 이미지 생성"""
        
        try:
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_price_change_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            # 이미지 생성
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(self.style_config['background_color'])
            
            # 가격 변동 시각화 (간단한 화살표)
            if change_percent > 0:
                color = self.style_config['success_color']
                arrow_direction = 'up'
                symbol_text = '↗'
            else:
                color = self.style_config['danger_color']
                arrow_direction = 'down'
                symbol_text = '↘'
            
            # 중앙에 큰 화살표와 퍼센트 표시
            ax.text(0.5, 0.6, symbol_text, fontsize=120, ha='center', va='center', 
                   color=color, transform=ax.transAxes)
            
            ax.text(0.5, 0.4, f"{change_percent:+.2f}%", fontsize=48, ha='center', va='center',
                   color=color, weight='bold', transform=ax.transAxes)
            
            # 제목
            title = article.get('title', f'{symbol} 가격 변동')
            ax.text(0.5, 0.85, title, fontsize=20, ha='center', va='center',
                   weight='bold', transform=ax.transAxes)
            
            # 심볼
            ax.text(0.5, 0.15, symbol, fontsize=32, ha='center', va='center',
                   color=self.style_config['secondary_color'], weight='bold', transform=ax.transAxes)
            
            # 축 제거
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # 저장
            plt.tight_layout()
            plt.savefig(filepath, dpi=self.style_config['dpi'], bbox_inches='tight',
                       facecolor=self.style_config['background_color'])
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"가격 변동 이미지 생성 실패: {e}")
            return ""
    
    async def _create_volume_spike_image(self, symbol: str, article: Dict[str, Any]) -> str:
        """거래량 급증 이미지 생성"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_volume_spike_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            # 거래량 차트 시뮬레이션
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(self.style_config['background_color'])
            
            # 가상의 거래량 데이터 생성
            days = np.arange(1, 21)
            normal_volume = np.random.normal(100, 20, 19)
            spike_volume = 300  # 급증한 거래량
            
            volumes = np.append(normal_volume, spike_volume)
            colors = ['lightblue'] * 19 + ['red']
            
            # 바 차트
            bars = ax.bar(days, volumes, color=colors, alpha=0.7)
            
            # 마지막 바 강조
            bars[-1].set_color(self.style_config['danger_color'])
            bars[-1].set_alpha(1.0)
            
            # 제목과 레이블
            ax.set_title(f'{symbol} 거래량 급증', fontsize=20, weight='bold', pad=20)
            ax.set_xlabel('일자', fontsize=14)
            ax.set_ylabel('거래량', fontsize=14)
            
            # 급증 표시
            ax.annotate('거래량 급증!', xy=(20, spike_volume), xytext=(15, spike_volume + 50),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2),
                       fontsize=16, color='red', weight='bold')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=self.style_config['dpi'], bbox_inches='tight',
                       facecolor=self.style_config['background_color'])
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"거래량 급증 이미지 생성 실패: {e}")
            return ""
    
    async def _create_volatility_image(self, symbol: str, article: Dict[str, Any]) -> str:
        """변동성 이미지 생성"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_volatility_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            # 변동성 시각화
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(self.style_config['background_color'])
            
            # 가상의 가격 데이터 (높은 변동성)
            time_points = np.linspace(0, 10, 100)
            price_data = 100 + 10 * np.sin(time_points) + 5 * np.random.randn(100)
            
            # 라인 차트
            ax.plot(time_points, price_data, color=self.style_config['danger_color'], 
                   linewidth=2, alpha=0.8)
            
            # 변동성 영역 표시
            upper_bound = price_data + 5
            lower_bound = price_data - 5
            ax.fill_between(time_points, lower_bound, upper_bound, 
                           color=self.style_config['danger_color'], alpha=0.2)
            
            # 제목과 레이블
            ax.set_title(f'{symbol} 높은 변동성', fontsize=20, weight='bold', pad=20)
            ax.set_xlabel('시간', fontsize=14)
            ax.set_ylabel('가격', fontsize=14)
            
            # 변동성 경고 텍스트
            ax.text(0.02, 0.98, '⚠️ 높은 변동성 주의', transform=ax.transAxes,
                   fontsize=16, color='red', weight='bold', va='top')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=self.style_config['dpi'], bbox_inches='tight',
                       facecolor=self.style_config['background_color'])
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"변동성 이미지 생성 실패: {e}")
            return ""
    
    async def _create_generic_market_image(self, symbol: str, article: Dict[str, Any]) -> str:
        """일반 시장 이미지 생성"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_market_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            # 일반적인 시장 차트
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(self.style_config['background_color'])
            
            # 가상의 시장 데이터
            time_points = np.arange(1, 31)
            market_data = 100 + np.cumsum(np.random.randn(30) * 0.5)
            
            # 라인 차트
            ax.plot(time_points, market_data, color=self.style_config['primary_color'], 
                   linewidth=3, marker='o', markersize=4)
            
            # 제목
            title = article.get('title', f'{symbol} 시장 분석')
            ax.set_title(title, fontsize=18, weight='bold', pad=20)
            
            # 레이블
            ax.set_xlabel('일자', fontsize=14)
            ax.set_ylabel('가격', fontsize=14)
            
            # 그리드
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=self.style_config['dpi'], bbox_inches='tight',
                       facecolor=self.style_config['background_color'])
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"일반 시장 이미지 생성 실패: {e}")
            return ""
