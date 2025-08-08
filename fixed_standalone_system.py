#!/usr/bin/env python3
"""
차트 생성 오류 수정된 완전히 독립적인 경제 뉴스 생성 시스템
"""

import os
import sys
import json
import requests
import logging
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import boto3
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage

# matplotlib 설정
matplotlib.use('Agg')
plt.rcParams['font.family'] = 'DejaVu Sans'

# .env 파일 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FixedStandaloneNewsSystem:
    """차트 생성 오류 수정된 독립적인 경제 뉴스 생성 시스템"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.output_dirs = {
            'articles': 'output/fixed_articles',
            'charts': 'output/fixed_charts',
            'images': 'output/fixed_images',
            'data': 'output/fixed_data'
        }
        
        for dir_path in self.output_dirs.values():
            os.makedirs(dir_path, exist_ok=True)
        
        # AWS Bedrock 초기화
        self.init_bedrock()
        
        # Slack 웹훅 URL
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        self.logger.info("✅ 수정된 독립적인 뉴스 시스템 초기화 완료")
    
    def init_bedrock(self):
        """AWS Bedrock 초기화"""
        try:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            )
            
            self.llm = ChatBedrock(
                client=self.bedrock_client,
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                model_kwargs={
                    "temperature": 0.7,
                    "max_tokens": 3000
                }
            )
            self.logger.info("✅ AWS Bedrock 초기화 완료")
        except Exception as e:
            self.logger.error(f"❌ AWS Bedrock 초기화 실패: {e}")
            self.llm = None
    
    def collect_market_data(self, symbols: List[str] = None) -> Dict[str, Any]:
        """시장 데이터 수집 (차트 생성을 위한 데이터 구조 개선)"""
        
        if symbols is None:
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'META', 'AMZN', '^GSPC', '^IXIC', '^VIX']
        
        self.logger.info(f"📊 {len(symbols)}개 심볼 데이터 수집 중...")
        
        market_data = {
            'timestamp': datetime.now().isoformat(),
            'symbols': {},
            'market_summary': {}
        }
        
        successful_symbols = 0
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="30d")  # 30일 데이터로 확장
                
                if not hist.empty and len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    previous_price = hist['Close'].iloc[-2]
                    change_percent = ((current_price - previous_price) / previous_price) * 100
                    
                    # 기술적 지표 계산
                    sma_5 = hist['Close'].rolling(window=5).mean().iloc[-1]
                    sma_10 = hist['Close'].rolling(window=min(10, len(hist))).mean().iloc[-1]
                    
                    # 차트용 데이터 준비 (수정된 부분)
                    chart_data = []
                    for date, row in hist.tail(20).iterrows():  # 최근 20일
                        chart_data.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'timestamp': date,
                            'open': float(row['Open']),
                            'high': float(row['High']),
                            'low': float(row['Low']),
                            'close': float(row['Close']),
                            'volume': int(row['Volume']) if 'Volume' in row and not pd.isna(row['Volume']) else 0
                        })
                    
                    market_data['symbols'][symbol] = {
                        'name': info.get('longName', symbol),
                        'current_price': float(current_price),
                        'previous_price': float(previous_price),
                        'change_percent': float(change_percent),
                        'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns and not pd.isna(hist['Volume'].iloc[-1]) else 0,
                        'high_52w': info.get('fiftyTwoWeekHigh', 0),
                        'low_52w': info.get('fiftyTwoWeekLow', 0),
                        'market_cap': info.get('marketCap', 0),
                        'sma_5': float(sma_5) if not pd.isna(sma_5) else float(current_price),
                        'sma_10': float(sma_10) if not pd.isna(sma_10) else float(current_price),
                        'chart_data': chart_data  # 수정된 차트 데이터
                    }
                    
                    successful_symbols += 1
                    self.logger.info(f"✅ {symbol}: {change_percent:+.2f}%")
                
            except Exception as e:
                self.logger.error(f"❌ {symbol} 데이터 수집 실패: {e}")
                continue
        
        # 시장 요약 생성
        if market_data['symbols']:
            changes = [data['change_percent'] for data in market_data['symbols'].values()]
            market_data['market_summary'] = {
                'total_symbols': successful_symbols,
                'avg_change': np.mean(changes),
                'positive_count': sum(1 for c in changes if c > 0),
                'negative_count': sum(1 for c in changes if c < 0),
                'max_gainer': max(market_data['symbols'].items(), key=lambda x: x[1]['change_percent']),
                'max_loser': min(market_data['symbols'].items(), key=lambda x: x[1]['change_percent'])
            }
        
        # 데이터 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = os.path.join(self.output_dirs['data'], f'market_data_{timestamp}.json')
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(market_data, f, ensure_ascii=False, indent=2, default=str)
        
        self.logger.info(f"💾 시장 데이터 저장: {data_file}")
        return market_data
    
    def detect_significant_events(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """중요한 이벤트 감지"""
        
        events = []
        
        for symbol, data in market_data['symbols'].items():
            change_percent = data['change_percent']
            
            # 이벤트 감지 조건들
            conditions = []
            
            # 1. 큰 가격 변동
            if abs(change_percent) >= 3.0:
                severity = 'critical' if abs(change_percent) >= 7.0 else 'high' if abs(change_percent) >= 5.0 else 'medium'
                direction = '급등' if change_percent > 0 else '급락'
                conditions.append(f"{abs(change_percent):.1f}% {direction}")
            
            # 2. 거래량 급증 (개선된 계산)
            if data['volume'] > 0 and data.get('chart_data'):
                volumes = [d['volume'] for d in data['chart_data'] if d['volume'] > 0]
                if len(volumes) > 5:
                    avg_volume = np.mean(volumes[:-1])  # 오늘 제외한 평균
                    if avg_volume > 0 and data['volume'] > avg_volume * 2:
                        conditions.append("거래량 급증")
            
            # 3. 기술적 신호
            if data['current_price'] > data['sma_5'] * 1.02:
                conditions.append("단기 상승 추세")
            elif data['current_price'] < data['sma_5'] * 0.98:
                conditions.append("단기 하락 추세")
            
            # 4. 52주 고점/저점 근접
            if data.get('high_52w', 0) > 0:
                if data['current_price'] > data['high_52w'] * 0.95:
                    conditions.append("52주 고점 근접")
            if data.get('low_52w', 0) > 0:
                if data['current_price'] < data['low_52w'] * 1.05:
                    conditions.append("52주 저점 근접")
            
            # 이벤트 생성
            if conditions:
                severity = 'critical' if abs(change_percent) >= 7.0 else 'high' if abs(change_percent) >= 5.0 else 'medium' if abs(change_percent) >= 3.0 else 'low'
                
                event = {
                    'symbol': symbol,
                    'name': data['name'],
                    'event_type': 'market_movement',
                    'severity': severity,
                    'title': f"{symbol} {', '.join(conditions[:2])}",
                    'description': f"{data['name']}이(가) {change_percent:+.2f}% 변동하며 {', '.join(conditions[:3])} 상황입니다.",
                    'current_price': data['current_price'],
                    'change_percent': change_percent,
                    'volume': data['volume'],
                    'conditions': conditions,
                    'timestamp': datetime.now().isoformat()
                }
                events.append(event)
        
        # 이벤트가 없으면 가장 큰 변동 종목으로 이벤트 생성
        if not events and market_data['symbols']:
            max_change_symbol = max(
                market_data['symbols'].items(),
                key=lambda x: abs(x[1]['change_percent'])
            )
            
            symbol, data = max_change_symbol
            change_percent = data['change_percent']
            direction = '상승' if change_percent > 0 else '하락'
            
            event = {
                'symbol': symbol,
                'name': data['name'],
                'event_type': 'daily_update',
                'severity': 'low',
                'title': f"{symbol} 일일 시장 동향",
                'description': f"{data['name']}이(가) {change_percent:+.2f}% {direction}했습니다.",
                'current_price': data['current_price'],
                'change_percent': change_percent,
                'volume': data['volume'],
                'conditions': [f"{abs(change_percent):.1f}% {direction}"],
                'timestamp': datetime.now().isoformat()
            }
            events.append(event)
        
        # 심각도 순으로 정렬
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        events.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        self.logger.info(f"🚨 {len(events)}개 이벤트 감지됨")
        return events
    
    def create_enhanced_price_chart(self, symbol: str, data: Dict[str, Any]) -> str:
        """향상된 가격 차트 생성 (오류 수정)"""
        
        try:
            chart_data = data.get('chart_data', [])
            if not chart_data or len(chart_data) < 2:
                self.logger.warning(f"⚠️ {symbol} 차트 데이터 부족")
                return ""
            
            # 데이터 준비 (수정된 부분)
            dates = []
            prices = []
            volumes = []
            highs = []
            lows = []
            
            for item in chart_data:
                try:
                    # 날짜 처리
                    if 'timestamp' in item and item['timestamp']:
                        date = item['timestamp']
                        if isinstance(date, str):
                            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    else:
                        date = datetime.strptime(item['date'], '%Y-%m-%d')
                    
                    dates.append(date)
                    prices.append(float(item['close']))
                    volumes.append(int(item.get('volume', 0)))
                    highs.append(float(item.get('high', item['close'])))
                    lows.append(float(item.get('low', item['close'])))
                    
                except (ValueError, KeyError, TypeError) as e:
                    self.logger.warning(f"⚠️ {symbol} 데이터 파싱 오류: {e}")
                    continue
            
            if len(dates) < 2:
                self.logger.warning(f"⚠️ {symbol} 유효한 데이터 부족")
                return ""
            
            # 차트 생성
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])
            fig.suptitle(f'{symbol} - 가격 및 거래량 분석', fontsize=16, fontweight='bold')
            
            # 가격 차트 (캔들스틱 스타일)
            ax1.plot(dates, prices, linewidth=2.5, color='#1f77b4', label='종가', marker='o', markersize=3)
            ax1.fill_between(dates, lows, highs, alpha=0.2, color='#1f77b4', label='고가-저가 범위')
            
            # 이동평균선 추가
            if len(prices) >= 5:
                sma_5 = pd.Series(prices).rolling(window=5).mean()
                ax1.plot(dates, sma_5, '--', color='orange', alpha=0.8, label='5일 이평선')
            
            if len(prices) >= 10:
                sma_10 = pd.Series(prices).rolling(window=10).mean()
                ax1.plot(dates, sma_10, '--', color='red', alpha=0.8, label='10일 이평선')
            
            # 현재가 강조
            current_price = data['current_price']
            change_percent = data['change_percent']
            color = '#28a745' if change_percent > 0 else '#dc3545'
            
            ax1.axhline(y=current_price, color=color, linestyle='-', alpha=0.8, linewidth=2)
            ax1.text(dates[-1], current_price, f'${current_price:.2f}\n({change_percent:+.2f}%)', 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.8, edgecolor='none'),
                    color='white', fontweight='bold', ha='right', va='bottom')
            
            ax1.set_title(f'가격 추이 (최근 {len(dates)}일)', fontsize=14)
            ax1.set_ylabel('가격 ($)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.legend(loc='upper left')
            
            # 날짜 포맷팅
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//7)))
            
            # 거래량 차트
            colors = ['#28a745' if p >= prices[i-1] else '#dc3545' if i > 0 else '#6c757d' for i, p in enumerate(prices)]
            bars = ax2.bar(dates, volumes, alpha=0.7, color=colors)
            
            ax2.set_title('거래량', fontsize=12)
            ax2.set_ylabel('거래량', fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            # 거래량 평균선
            if len(volumes) > 1:
                avg_volume = np.mean(volumes)
                ax2.axhline(y=avg_volume, color='purple', linestyle='--', alpha=0.7, label=f'평균: {avg_volume:,.0f}')
                ax2.legend()
            
            # 날짜 포맷팅
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax2.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//7)))
            
            # 레이아웃 조정
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            plt.tight_layout()
            
            # 파일 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{symbol}_enhanced_chart_{timestamp}.png"
            filepath = os.path.join(self.output_dirs['charts'], filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
            plt.close()
            
            self.logger.info(f"📈 향상된 차트 생성 성공: {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"❌ {symbol} 차트 생성 실패: {e}")
            import traceback
            self.logger.error(f"상세 오류: {traceback.format_exc()}")
            return ""
