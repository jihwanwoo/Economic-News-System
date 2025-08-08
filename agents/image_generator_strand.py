"""
이미지 생성 Strand Agent
기사 내용을 바탕으로 관련 이미지를 생성
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
from wordcloud import WordCloud
import re

from .strands_framework import BaseStrandAgent, StrandContext, StrandMessage, MessageType

class ImageGeneratorStrand(BaseStrandAgent):
    """이미지 생성 Strand Agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="image_generator",
            name="이미지 생성 에이전트"
        )
        
        # 출력 디렉토리 설정
        self.images_dir = "output/images"
        os.makedirs(self.images_dir, exist_ok=True)
        
        self.capabilities = [
            "article_illustration",
            "data_visualization",
            "wordcloud_generation",
            "chart_annotation",
            "infographic_creation"
        ]
        
        # 이미지 스타일 설정
        plt.style.use('default')
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
    
    def get_capabilities(self) -> List[str]:
        """에이전트 능력 반환"""
        return self.capabilities
    
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """이미지 생성 처리"""
        
        # 필요한 데이터 수집
        event_data = context.input_data.get('event')
        article = await self.get_shared_data(context, 'article')
        data_analysis = await self.get_shared_data(context, 'data_analysis')
        
        if not event_data or not article:
            raise Exception("이미지 생성에 필요한 데이터가 없습니다")
        
        symbol = event_data.get('symbol', 'Unknown')
        event_type = event_data.get('event_type', 'unknown')
        
        self.logger.info("🖼️ 기사 이미지 생성 시작")
        
        try:
            # 1. 기사 내용 기반 이미지 생성
            article_image = await self._generate_article_based_image(article, symbol, event_data)
            
            # 2. 이벤트 유형별 이미지 생성
            event_image = None
            if event_type == 'volume_spike':
                event_image = await self._create_volume_spike_image(symbol, event_data, data_analysis)
            elif event_type == 'price_change':
                event_image = await self._create_price_change_image(symbol, event_data, data_analysis)
            elif event_type == 'high_volatility':
                event_image = await self._create_volatility_image(symbol, event_data, data_analysis)
            else:
                event_image = await self._create_default_image(symbol, event_data, article)
            
            # 3. 워드클라우드 생성
            wordcloud_path = await self._create_wordcloud(article, symbol)
            
            result = {
                'article_image': article_image,  # 기사 내용 기반 이미지
                'event_image': event_image,      # 이벤트 유형별 이미지
                'wordcloud': wordcloud_path,     # 워드클라우드
                'image_type': event_type,
                'created_at': datetime.now().isoformat()
            }
            
            # 공유 메모리에 저장
            await self.set_shared_data(context, 'article_images', result)
            
            self.logger.info(f"✅ 기사 이미지 생성 완료: {len([x for x in result.values() if x and isinstance(x, str) and x.endswith('.png')])}개")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 이미지 생성 실패: {e}")
            raise
    
    async def _generate_article_based_image(self, article: Dict[str, Any], symbol: str, event_data: Dict[str, Any]) -> str:
        """기사 내용을 바탕으로 한 이미지 생성"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_article_illustration_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        try:
            # 기사에서 이미지 프롬프트 추출
            image_prompt = article.get('image_prompt', '')
            
            if not image_prompt:
                # 기사 내용을 바탕으로 프롬프트 생성
                title = article.get('title', '')
                body = article.get('body', '')
                
                # 키워드 추출
                keywords = []
                if 'price' in body.lower() or '가격' in body:
                    keywords.append('stock price chart')
                if 'volume' in body.lower() or '거래량' in body:
                    keywords.append('trading volume')
                if 'market' in body.lower() or '시장' in body:
                    keywords.append('financial market')
                if symbol:
                    keywords.append(f'{symbol} stock')
                
                image_prompt = f"professional financial illustration, {', '.join(keywords)}, modern business style, blue and green color scheme"
            
            # 텍스트 기반 이미지 생성 (실제 AI 이미지 생성 대신 정보 이미지 생성)
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            
            # 배경 설정
            ax.set_facecolor('#f8f9fa')
            fig.patch.set_facecolor('#ffffff')
            
            # 제목
            title_text = article.get('title', '경제 뉴스')
            ax.text(0.5, 0.85, title_text, ha='center', va='center',
                   fontsize=20, fontweight='bold', transform=ax.transAxes,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
            
            # 주요 내용 요약
            lead_text = article.get('lead', '')[:200] + "..."
            ax.text(0.5, 0.65, lead_text, ha='center', va='center',
                   fontsize=14, transform=ax.transAxes, wrap=True,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.7))
            
            # 심볼 및 이벤트 정보
            info_text = f"심볼: {symbol}\n이벤트: {event_data.get('event_type', 'N/A')}\n생성시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            ax.text(0.5, 0.35, info_text, ha='center', va='center',
                   fontsize=12, transform=ax.transAxes,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))
            
            # 이미지 프롬프트 표시
            if image_prompt:
                ax.text(0.5, 0.15, f"이미지 컨셉: {image_prompt[:100]}...", 
                       ha='center', va='center', fontsize=10, 
                       transform=ax.transAxes, style='italic',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.5))
            
            # 장식 요소 추가
            ax.add_patch(patches.Rectangle((0.05, 0.05), 0.9, 0.9, 
                                         linewidth=3, edgecolor='navy', 
                                         facecolor='none', transform=ax.transAxes))
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            self.logger.info(f"📰 기사 기반 이미지 생성: {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"기사 기반 이미지 생성 실패: {e}")
            return await self._create_simple_fallback_image(symbol, "기사 일러스트", timestamp)
    
    async def _create_volume_spike_image(self, symbol: str, event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> str:
        """거래량 급증 이미지 생성"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_volume_spike_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # 상단: 거래량 비교 차트
            if data_analysis and data_analysis.get('statistics', {}).get('volume_ratio'):
                volume_ratio = data_analysis['statistics']['volume_ratio']
                
                categories = ['평균 거래량', '현재 거래량']
                values = [1.0, volume_ratio]
                colors = ['lightblue', 'red' if volume_ratio > 2 else 'orange']
                
                bars = ax1.bar(categories, values, color=colors, alpha=0.7)
                ax1.set_title(f'{symbol} 거래량 비교', fontsize=16, fontweight='bold')
                ax1.set_ylabel('거래량 비율')
                ax1.grid(True, alpha=0.3)
                
                # 값 표시
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{value:.1f}배', ha='center', va='bottom', fontweight='bold')
            
            # 하단: 이벤트 정보
            ax2.axis('off')
            
            # 정보 박스 생성
            info_text = f"""
거래량 급증 이벤트

심볼: {symbol}
이벤트 시간: {event_data.get('timestamp', 'Unknown')[:19]}
심각도: {event_data.get('severity', 'Unknown').upper()}
설명: {event_data.get('description', 'N/A')}
            """.strip()
            
            # 텍스트 박스 추가
            props = dict(boxstyle='round', facecolor='lightgray', alpha=0.8)
            ax2.text(0.05, 0.95, info_text, transform=ax2.transAxes, fontsize=11,
                    verticalalignment='top', bbox=props, family='monospace')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"거래량 급증 이미지 생성 실패: {e}")
            # 간단한 폴백 이미지 생성
            return await self._create_simple_fallback_image(symbol, "거래량 급증", timestamp)
    
    async def _create_price_change_image(self, symbol: str, event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> str:
        """가격 변동 이미지 생성"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_price_change_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # 좌측: 가격 변동 화살표
            change_percent = event_data.get('change_percent', 0)
            
            if change_percent > 0:
                # 상승 화살표
                ax1.arrow(0.5, 0.2, 0, 0.6, head_width=0.1, head_length=0.1, 
                         fc='green', ec='green', linewidth=3)
                ax1.text(0.5, 0.1, f'+{change_percent:.1f}%', ha='center', va='center',
                        fontsize=20, fontweight='bold', color='green')
                direction_text = "상승"
                color = 'green'
            else:
                # 하락 화살표
                ax1.arrow(0.5, 0.8, 0, -0.6, head_width=0.1, head_length=0.1,
                         fc='red', ec='red', linewidth=3)
                ax1.text(0.5, 0.9, f'{change_percent:.1f}%', ha='center', va='center',
                        fontsize=20, fontweight='bold', color='red')
                direction_text = "하락"
                color = 'red'
            
            ax1.set_xlim(0, 1)
            ax1.set_ylim(0, 1)
            ax1.set_title(f'{symbol} 가격 {direction_text}', fontsize=16, fontweight='bold')
            ax1.axis('off')
            
            # 우측: 기술적 정보
            ax2.axis('off')
            
            info_lines = [f"{symbol} 가격 변동 분석", ""]
            
            if data_analysis:
                raw_data = data_analysis.get('raw_data', {})
                if raw_data.get('current_price'):
                    info_lines.append(f"현재가: ${raw_data['current_price']:.2f}")
                
                technical = data_analysis.get('technical_indicators', {})
                if technical.get('rsi'):
                    rsi = technical['rsi']
                    rsi_status = "과매수" if rsi > 70 else "과매도" if rsi < 30 else "중립"
                    info_lines.append(f"RSI: {rsi:.1f} ({rsi_status})")
                
                if technical.get('sma_20'):
                    info_lines.append(f"20일 이평: ${technical['sma_20']:.2f}")
            
            info_lines.extend(["", f"분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}"])
            
            info_text = "\n".join(info_lines)
            ax2.text(0.05, 0.95, info_text, transform=ax2.transAxes, fontsize=12,
                    verticalalignment='top', family='monospace')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"가격 변동 이미지 생성 실패: {e}")
            return await self._create_simple_fallback_image(symbol, "가격 변동", timestamp)
    
    async def _create_volatility_image(self, symbol: str, event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> str:
        """변동성 이미지 생성"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_volatility_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        try:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            
            # 변동성 게이지 생성
            if data_analysis and data_analysis.get('statistics', {}).get('volatility_annualized'):
                volatility = data_analysis['statistics']['volatility_annualized'] * 100
            else:
                volatility = 25.0  # 기본값
            
            # 게이지 차트 생성
            theta = np.linspace(0, np.pi, 100)
            
            # 배경 호
            ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=8, alpha=0.3)
            
            # 변동성 수준에 따른 색상 구간
            low_theta = theta[theta <= np.pi/3]
            med_theta = theta[(theta > np.pi/3) & (theta <= 2*np.pi/3)]
            high_theta = theta[theta > 2*np.pi/3]
            
            ax.plot(np.cos(low_theta), np.sin(low_theta), 'g-', linewidth=8, label='낮음 (0-20%)')
            ax.plot(np.cos(med_theta), np.sin(med_theta), 'y-', linewidth=8, label='보통 (20-40%)')
            ax.plot(np.cos(high_theta), np.sin(high_theta), 'r-', linewidth=8, label='높음 (40%+)')
            
            # 현재 변동성 위치 표시
            vol_angle = np.pi * (1 - min(volatility / 60, 1))  # 60%를 최대로 정규화
            needle_x = np.cos(vol_angle)
            needle_y = np.sin(vol_angle)
            
            ax.arrow(0, 0, needle_x*0.8, needle_y*0.8, head_width=0.05, head_length=0.05,
                    fc='black', ec='black', linewidth=3)
            
            # 중앙에 변동성 값 표시
            ax.text(0, -0.3, f'{volatility:.1f}%', ha='center', va='center',
                   fontsize=24, fontweight='bold')
            ax.text(0, -0.45, '연율 변동성', ha='center', va='center',
                   fontsize=14)
            
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-0.6, 1.2)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'{symbol} 변동성 분석', fontsize=18, fontweight='bold', pad=20)
            ax.legend(loc='upper right')
            
            # 추가 정보 텍스트
            info_text = f"""
변동성 수준: {'높음' if volatility > 40 else '보통' if volatility > 20 else '낮음'}
위험도: {'고위험' if volatility > 40 else '중위험' if volatility > 20 else '저위험'}
분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """.strip()
            
            ax.text(-1.1, -0.5, info_text, fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"변동성 이미지 생성 실패: {e}")
            return await self._create_simple_fallback_image(symbol, "변동성 분석", timestamp)
    
    async def _create_default_image(self, symbol: str, event_data: Dict[str, Any], article: Dict[str, Any]) -> str:
        """기본 이미지 생성"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_default_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        try:
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            
            # 심플한 정보 표시 이미지
            ax.text(0.5, 0.7, symbol, ha='center', va='center',
                   fontsize=36, fontweight='bold', transform=ax.transAxes)
            
            ax.text(0.5, 0.5, article.get('title', '경제 뉴스'), ha='center', va='center',
                   fontsize=16, transform=ax.transAxes, wrap=True)
            
            ax.text(0.5, 0.3, f"이벤트: {event_data.get('event_type', 'Unknown')}", 
                   ha='center', va='center', fontsize=14, transform=ax.transAxes)
            
            ax.text(0.5, 0.1, f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                   ha='center', va='center', fontsize=12, transform=ax.transAxes)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # 배경 색상
            ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor='lightblue', alpha=0.3))
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"기본 이미지 생성 실패: {e}")
            return await self._create_simple_fallback_image(symbol, "경제 뉴스", timestamp)
    
    async def _create_wordcloud(self, article: Dict[str, Any], symbol: str) -> Optional[str]:
        """워드클라우드 생성"""
        
        try:
            # 기사 텍스트 추출
            text_parts = []
            if article.get('title'):
                text_parts.append(article['title'])
            if article.get('body'):
                text_parts.append(article['body'])
            if article.get('conclusion'):
                text_parts.append(article['conclusion'])
            
            full_text = ' '.join(text_parts)
            
            if not full_text or len(full_text) < 50:
                return None
            
            # 불용어 제거 및 텍스트 정제
            stopwords = {
                '이', '가', '을', '를', '에', '의', '와', '과', '도', '는', '은',
                '하다', '있다', '되다', '이다', '그', '것', '수', '등', '및', '또한',
                '하지만', '그러나', '따라서', '또는', '그리고', '때문에'
            }
            
            # 한글과 영문만 추출
            clean_text = re.sub(r'[^가-힣a-zA-Z\s]', ' ', full_text)
            words = clean_text.split()
            filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]
            
            if len(filtered_words) < 10:
                return None
            
            # 워드클라우드 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_wordcloud_{timestamp}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            wordcloud = WordCloud(
                width=800, height=400,
                background_color='white',
                max_words=50,
                font_path=None,  # 시스템 기본 폰트 사용
                colormap='viridis'
            ).generate(' '.join(filtered_words))
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'{symbol} 기사 키워드', fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"워드클라우드 생성 실패: {e}")
            return None
    
    async def _create_simple_fallback_image(self, symbol: str, title: str, timestamp: str) -> str:
        """간단한 폴백 이미지 생성"""
        
        filename = f"{symbol}_fallback_{timestamp}.png"
        filepath = os.path.join(self.images_dir, filename)
        
        try:
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
            
            ax.text(0.5, 0.6, symbol, ha='center', va='center',
                   fontsize=32, fontweight='bold', transform=ax.transAxes)
            
            ax.text(0.5, 0.4, title, ha='center', va='center',
                   fontsize=18, transform=ax.transAxes)
            
            ax.text(0.5, 0.2, f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                   ha='center', va='center', fontsize=12, transform=ax.transAxes)
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"폴백 이미지 생성 실패: {e}")
            # 최후의 수단: 빈 파일 생성
            with open(filepath, 'w') as f:
                f.write("Image generation failed")
            return filepath
