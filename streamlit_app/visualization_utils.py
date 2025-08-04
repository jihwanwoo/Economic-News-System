"""
시각화 유틸리티 모듈
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from typing import Dict, List, Any, Optional
import streamlit as st


class ChartGenerator:
    """차트 생성 클래스"""
    
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17a2b8'
        }
    
    def create_stock_price_chart(self, stock_data: Dict[str, Any], symbols: List[str] = None) -> go.Figure:
        """주식 가격 차트 생성"""
        if not symbols:
            symbols = list(stock_data.keys())[:5]  # 상위 5개 종목
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('주식 가격 변화', '거래량'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # 가격 차트
        for i, symbol in enumerate(symbols):
            if symbol in stock_data:
                data = stock_data[symbol]
                color = list(self.colors.values())[i % len(self.colors)]
                
                fig.add_trace(
                    go.Scatter(
                        x=[symbol],
                        y=[data.get('current_price', 0)],
                        mode='markers+text',
                        name=f"{data.get('name', symbol)}",
                        text=[f"${data.get('current_price', 0):.2f}"],
                        textposition="top center",
                        marker=dict(
                            size=15,
                            color=color,
                            line=dict(width=2, color='white')
                        )
                    ),
                    row=1, col=1
                )
                
                # 거래량 차트
                fig.add_trace(
                    go.Bar(
                        x=[symbol],
                        y=[data.get('volume', 0)],
                        name=f"{symbol} 거래량",
                        marker_color=color,
                        showlegend=False
                    ),
                    row=2, col=1
                )
        
        fig.update_layout(
            title="주요 종목 현황",
            height=600,
            showlegend=True,
            template="plotly_white"
        )
        
        fig.update_xaxes(title_text="종목", row=2, col=1)
        fig.update_yaxes(title_text="가격 ($)", row=1, col=1)
        fig.update_yaxes(title_text="거래량", row=2, col=1)
        
        return fig
    
    def create_market_overview_chart(self, stock_data: Dict[str, Any]) -> go.Figure:
        """시장 개요 차트 생성"""
        # 주요 지수 데이터 추출
        indices = {'^GSPC': 'S&P 500', '^DJI': '다우존스', '^IXIC': '나스닥', '^VIX': 'VIX'}
        
        index_data = []
        for symbol, name in indices.items():
            if symbol in stock_data:
                data = stock_data[symbol]
                index_data.append({
                    'Index': name,
                    'Value': data.get('current_price', 0),
                    'Change': data.get('change_percent', 0),
                    'Color': 'green' if data.get('change_percent', 0) >= 0 else 'red'
                })
        
        if not index_data:
            return go.Figure()
        
        df = pd.DataFrame(index_data)
        
        fig = go.Figure()
        
        # 지수 값 차트
        fig.add_trace(
            go.Bar(
                x=df['Index'],
                y=df['Value'],
                name='지수 값',
                marker_color=df['Color'],
                text=[f"{val:.2f}" for val in df['Value']],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title="주요 지수 현황",
            xaxis_title="지수",
            yaxis_title="값",
            height=400,
            template="plotly_white"
        )
        
        return fig
    
    def create_change_percentage_chart(self, stock_data: Dict[str, Any]) -> go.Figure:
        """변화율 차트 생성"""
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
        
        change_data = []
        for symbol in symbols:
            if symbol in stock_data:
                data = stock_data[symbol]
                change_data.append({
                    'Symbol': data.get('name', symbol),
                    'Change%': data.get('change_percent', 0),
                    'Color': 'green' if data.get('change_percent', 0) >= 0 else 'red'
                })
        
        if not change_data:
            return go.Figure()
        
        df = pd.DataFrame(change_data)
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=df['Symbol'],
                y=df['Change%'],
                name='변화율 (%)',
                marker_color=df['Color'],
                text=[f"{val:.2f}%" for val in df['Change%']],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title="주요 종목 변화율",
            xaxis_title="종목",
            yaxis_title="변화율 (%)",
            height=400,
            template="plotly_white"
        )
        
        # 0선 추가
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        return fig
    
    def create_sector_performance_chart(self, stock_data: Dict[str, Any]) -> go.Figure:
        """섹터별 성과 차트"""
        sector_data = {}
        
        for symbol, data in stock_data.items():
            sector = data.get('sector', 'Unknown')
            if sector != 'Unknown' and sector:
                if sector not in sector_data:
                    sector_data[sector] = []
                sector_data[sector].append(data.get('change_percent', 0))
        
        # 섹터별 평균 계산
        sector_avg = {sector: np.mean(changes) for sector, changes in sector_data.items()}
        
        if not sector_avg:
            return go.Figure()
        
        sectors = list(sector_avg.keys())
        changes = list(sector_avg.values())
        colors = ['green' if change >= 0 else 'red' for change in changes]
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Bar(
                x=sectors,
                y=changes,
                name='섹터 평균 변화율',
                marker_color=colors,
                text=[f"{val:.2f}%" for val in changes],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title="섹터별 성과",
            xaxis_title="섹터",
            yaxis_title="평균 변화율 (%)",
            height=400,
            template="plotly_white"
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        return fig
    
    def create_vix_fear_greed_gauge(self, economic_data: Dict[str, Any]) -> go.Figure:
        """VIX 공포/탐욕 게이지 차트"""
        vix_value = economic_data.get('VIX', {}).get('value', 20)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = vix_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "VIX 공포 지수"},
            delta = {'reference': 20},
            gauge = {
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 20], 'color': "lightgreen"},
                    {'range': [20, 30], 'color': "yellow"},
                    {'range': [30, 50], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        
        fig.update_layout(height=300)
        
        return fig
    
    def create_market_cap_pie_chart(self, stock_data: Dict[str, Any]) -> go.Figure:
        """시가총액 파이 차트"""
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
        
        cap_data = []
        for symbol in symbols:
            if symbol in stock_data:
                data = stock_data[symbol]
                market_cap = data.get('market_cap', 0)
                if market_cap > 0:
                    cap_data.append({
                        'Symbol': data.get('name', symbol),
                        'MarketCap': market_cap / 1e12  # 조 달러 단위
                    })
        
        if not cap_data:
            return go.Figure()
        
        df = pd.DataFrame(cap_data)
        
        fig = go.Figure(data=[go.Pie(
            labels=df['Symbol'],
            values=df['MarketCap'],
            hole=.3,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="주요 종목 시가총액 비중",
            height=400,
            showlegend=True
        )
        
        return fig


class NewsImageGenerator:
    """뉴스 관련 이미지 생성 클래스"""
    
    def __init__(self):
        self.bedrock_client = None
        try:
            import boto3
            self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        except:
            pass
    
    def generate_article_illustration(self, article_content: str, article_type: str = "market_summary") -> Optional[str]:
        """기사 내용 기반 일러스트레이션 생성"""
        # 실제 구현에서는 AWS Bedrock의 이미지 생성 모델을 사용
        # 여기서는 플레이스홀더 이미지 URL 반환
        
        image_prompts = {
            "market_summary": "https://via.placeholder.com/600x300/1f77b4/ffffff?text=Market+Analysis",
            "stock_focus": "https://via.placeholder.com/600x300/ff7f0e/ffffff?text=Stock+Focus",
            "economic_outlook": "https://via.placeholder.com/600x300/2ca02c/ffffff?text=Economic+Outlook",
            "sector_analysis": "https://via.placeholder.com/600x300/d62728/ffffff?text=Sector+Analysis"
        }
        
        return image_prompts.get(article_type, image_prompts["market_summary"])
    
    def create_wordcloud_from_article(self, article_content: str) -> Optional[str]:
        """기사 내용으로부터 워드클라우드 생성"""
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            import io
            import base64
            
            # 한글 폰트 설정 (시스템에 따라 조정 필요)
            wordcloud = WordCloud(
                width=800, 
                height=400, 
                background_color='white',
                max_words=100,
                colormap='viridis'
            ).generate(article_content)
            
            # 이미지를 base64로 인코딩
            img_buffer = io.BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            plt.close()
            
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.read()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            st.error(f"워드클라우드 생성 오류: {str(e)}")
            return None


class AdGenerator:
    """광고 생성 클래스"""
    
    def __init__(self):
        self.ad_templates = {
            "investment": [
                {
                    "title": "스마트 투자 플랫폼",
                    "description": "AI 기반 포트폴리오 관리로 더 나은 수익을 경험하세요",
                    "cta": "무료 체험하기",
                    "image": "https://via.placeholder.com/300x200/007cba/ffffff?text=Smart+Investment",
                    "link": "#"
                },
                {
                    "title": "로보어드바이저",
                    "description": "전문가 수준의 자산 관리를 자동으로",
                    "cta": "지금 시작하기",
                    "image": "https://via.placeholder.com/300x200/28a745/ffffff?text=Robo+Advisor",
                    "link": "#"
                }
            ],
            "trading": [
                {
                    "title": "실시간 트레이딩",
                    "description": "수수료 0원으로 시작하는 주식 투자",
                    "cta": "계좌 개설하기",
                    "image": "https://via.placeholder.com/300x200/dc3545/ffffff?text=Real+Time+Trading",
                    "link": "#"
                },
                {
                    "title": "프리미엄 차트",
                    "description": "전문 트레이더를 위한 고급 분석 도구",
                    "cta": "무료 체험",
                    "image": "https://via.placeholder.com/300x200/6f42c1/ffffff?text=Premium+Charts",
                    "link": "#"
                }
            ],
            "education": [
                {
                    "title": "투자 교육 과정",
                    "description": "기초부터 고급까지, 체계적인 투자 학습",
                    "cta": "수강 신청",
                    "image": "https://via.placeholder.com/300x200/fd7e14/ffffff?text=Investment+Education",
                    "link": "#"
                },
                {
                    "title": "경제 뉴스 구독",
                    "description": "매일 아침 받아보는 핵심 경제 소식",
                    "cta": "구독하기",
                    "image": "https://via.placeholder.com/300x200/20c997/ffffff?text=Economic+News",
                    "link": "#"
                }
            ]
        }
    
    def generate_contextual_ads(self, article_content: str, article_tags: List[str]) -> List[Dict[str, str]]:
        """기사 내용 기반 맞춤 광고 생성"""
        ads = []
        
        # 기사 내용과 태그 분석
        content_lower = article_content.lower()
        tags_lower = [tag.lower() for tag in article_tags]
        
        # 투자 관련 키워드 확인
        investment_keywords = ['투자', '수익', '포트폴리오', '자산', 'investment', 'portfolio']
        trading_keywords = ['거래', '매매', '트레이딩', '차트', 'trading', 'chart']
        education_keywords = ['분석', '전망', '교육', '학습', 'analysis', 'education']
        
        # 키워드 매칭으로 광고 카테고리 결정
        if any(keyword in content_lower or keyword in ' '.join(tags_lower) for keyword in investment_keywords):
            ads.extend(self.ad_templates["investment"])
        
        if any(keyword in content_lower or keyword in ' '.join(tags_lower) for keyword in trading_keywords):
            ads.extend(self.ad_templates["trading"])
        
        if any(keyword in content_lower or keyword in ' '.join(tags_lower) for keyword in education_keywords):
            ads.extend(self.ad_templates["education"])
        
        # 기본 광고 (매칭되는 것이 없을 경우)
        if not ads:
            ads = self.ad_templates["investment"] + self.ad_templates["education"]
        
        # 최대 3개 광고 반환
        return ads[:3]
    
    def create_ad_html(self, ad: Dict[str, str]) -> str:
        """광고 HTML 생성"""
        return f"""
        <div style="
            border: 1px solid #ddd; 
            border-radius: 8px; 
            padding: 15px; 
            margin: 10px 0; 
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center;">
                <img src="{ad['image']}" style="
                    width: 80px; 
                    height: 60px; 
                    border-radius: 4px; 
                    margin-right: 15px;
                    object-fit: cover;
                " />
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0; color: #333; font-size: 16px;">{ad['title']}</h4>
                    <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">{ad['description']}</p>
                    <a href="{ad['link']}" style="
                        background-color: #007cba; 
                        color: white; 
                        padding: 6px 12px; 
                        text-decoration: none; 
                        border-radius: 4px; 
                        font-size: 12px;
                        display: inline-block;
                    ">{ad['cta']}</a>
                </div>
            </div>
        </div>
        """
