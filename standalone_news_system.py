#!/usr/bin/env python3
"""
완전히 독립적인 경제 뉴스 생성 시스템
OrchestratorStrand 의존성 없이 작동하는 안정적인 시스템
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

class StandaloneNewsSystem:
    """완전히 독립적인 경제 뉴스 생성 시스템"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.output_dirs = {
            'articles': 'output/standalone_articles',
            'charts': 'output/standalone_charts',
            'images': 'output/standalone_images',
            'data': 'output/standalone_data'
        }
        
        for dir_path in self.output_dirs.values():
            os.makedirs(dir_path, exist_ok=True)
        
        # AWS Bedrock 초기화
        self.init_bedrock()
        
        # Slack 웹훅 URL
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        self.logger.info("✅ 독립적인 뉴스 시스템 초기화 완료")
    
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
        """시장 데이터 수집"""
        
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
                hist = ticker.history(period="10d")
                
                if not hist.empty and len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    previous_price = hist['Close'].iloc[-2]
                    change_percent = ((current_price - previous_price) / previous_price) * 100
                    
                    # 기술적 지표 계산
                    sma_5 = hist['Close'].rolling(window=5).mean().iloc[-1]
                    sma_10 = hist['Close'].rolling(window=min(10, len(hist))).mean().iloc[-1]
                    
                    market_data['symbols'][symbol] = {
                        'name': info.get('longName', symbol),
                        'current_price': float(current_price),
                        'previous_price': float(previous_price),
                        'change_percent': float(change_percent),
                        'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                        'high_52w': info.get('fiftyTwoWeekHigh', 0),
                        'low_52w': info.get('fiftyTwoWeekLow', 0),
                        'market_cap': info.get('marketCap', 0),
                        'sma_5': float(sma_5) if not pd.isna(sma_5) else float(current_price),
                        'sma_10': float(sma_10) if not pd.isna(sma_10) else float(current_price),
                        'historical_data': hist.tail(10).to_dict('records')
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
            
            # 2. 거래량 급증 (간단한 추정)
            if data['volume'] > 0:
                avg_volume = np.mean([d.get('Volume', 0) for d in data.get('historical_data', [])])
                if avg_volume > 0 and data['volume'] > avg_volume * 2:
                    conditions.append("거래량 급증")
            
            # 3. 기술적 신호
            if data['current_price'] > data['sma_5'] * 1.02:
                conditions.append("단기 상승 추세")
            elif data['current_price'] < data['sma_5'] * 0.98:
                conditions.append("단기 하락 추세")
            
            # 이벤트 생성
            if conditions:
                severity = 'critical' if abs(change_percent) >= 7.0 else 'high' if abs(change_percent) >= 5.0 else 'medium' if abs(change_percent) >= 3.0 else 'low'
                
                event = {
                    'symbol': symbol,
                    'name': data['name'],
                    'event_type': 'market_movement',
                    'severity': severity,
                    'title': f"{symbol} {', '.join(conditions)}",
                    'description': f"{data['name']}이(가) {change_percent:+.2f}% 변동하며 {', '.join(conditions)} 상황입니다.",
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
    
    def create_price_chart(self, symbol: str, data: Dict[str, Any]) -> str:
        """가격 차트 생성"""
        
        try:
            historical_data = data.get('historical_data', [])
            if not historical_data:
                return ""
            
            # 데이터 준비
            dates = [datetime.fromisoformat(d['Date'].replace('Z', '+00:00')).date() if isinstance(d['Date'], str) else d['Date'] for d in historical_data]
            prices = [d['Close'] for d in historical_data]
            volumes = [d.get('Volume', 0) for d in historical_data]
            
            # 차트 생성
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
            
            # 가격 차트
            ax1.plot(dates, prices, linewidth=2, color='#1f77b4', label='Close Price')
            ax1.fill_between(dates, prices, alpha=0.3, color='#1f77b4')
            ax1.set_title(f'{symbol} - 가격 추이 (최근 10일)', fontsize=16, fontweight='bold')
            ax1.set_ylabel('가격 ($)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # 현재가 표시
            current_price = data['current_price']
            change_percent = data['change_percent']
            color = 'green' if change_percent > 0 else 'red'
            ax1.axhline(y=current_price, color=color, linestyle='--', alpha=0.7)
            ax1.text(dates[-1], current_price, f'${current_price:.2f} ({change_percent:+.2f}%)', 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7, edgecolor='none'),
                    color='white', fontweight='bold')
            
            # 거래량 차트
            ax2.bar(dates, volumes, alpha=0.7, color='orange')
            ax2.set_title('거래량', fontsize=12)
            ax2.set_ylabel('거래량', fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # 파일 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{symbol}_price_chart_{timestamp}.png"
            filepath = os.path.join(self.output_dirs['charts'], filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            self.logger.info(f"📈 차트 생성: {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"❌ {symbol} 차트 생성 실패: {e}")
            return ""
    
    def generate_comprehensive_article(self, event: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """종합적인 기사 생성"""
        
        if not self.llm:
            return self.generate_template_article(event, market_data)
        
        try:
            # 시장 컨텍스트 준비
            market_summary = market_data.get('market_summary', {})
            symbol_data = market_data['symbols'].get(event['symbol'], {})
            
            # 다른 주요 종목들 정보
            other_symbols = []
            for sym, data in list(market_data['symbols'].items())[:5]:
                if sym != event['symbol']:
                    other_symbols.append(f"{sym}: {data['change_percent']:+.2f}%")
            
            system_prompt = """당신은 경험이 풍부한 경제 전문 기자입니다. 주어진 시장 데이터와 이벤트를 바탕으로 전문적이고 통찰력 있는 경제 기사를 작성해주세요.

기사 작성 원칙:
1. 객관적이고 정확한 정보 전달
2. 데이터 기반의 분석과 해석
3. 투자자들에게 유용한 인사이트 제공
4. 명확하고 이해하기 쉬운 문체
5. 시장 전체적인 맥락에서의 해석

기사 구조:
- 헤드라인 (간결하고 임팩트 있게)
- 리드 (핵심 내용 요약)
- 본문 (상세 분석 및 배경)
- 시장 전망 (향후 전망 및 시사점)"""

            user_prompt = f"""다음 정보를 바탕으로 전문적인 경제 기사를 작성해주세요:

주요 이벤트:
- 종목: {event['symbol']} ({event['name']})
- 현재 상황: {event['title']}
- 가격 변동: {event['change_percent']:+.2f}% (${event['current_price']:.2f})
- 거래량: {event['volume']:,}주
- 감지된 조건: {', '.join(event.get('conditions', []))}

시장 전체 현황:
- 전체 종목 수: {market_summary.get('total_symbols', 0)}개
- 평균 변동률: {market_summary.get('avg_change', 0):+.2f}%
- 상승 종목: {market_summary.get('positive_count', 0)}개
- 하락 종목: {market_summary.get('negative_count', 0)}개

주요 종목 동향:
{chr(10).join(other_symbols)}

기술적 정보:
- 5일 이동평균: ${symbol_data.get('sma_5', 0):.2f}
- 10일 이동평균: ${symbol_data.get('sma_10', 0):.2f}
- 52주 최고가: ${symbol_data.get('high_52w', 0):.2f}
- 52주 최저가: ${symbol_data.get('low_52w', 0):.2f}

작성 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}

전문적이고 통찰력 있는 기사를 작성해주세요."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            self.logger.error(f"❌ AI 기사 생성 실패: {e}")
            return self.generate_template_article(event, market_data)
    
    def generate_template_article(self, event: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """템플릿 기반 기사 생성"""
        
        symbol = event['symbol']
        name = event['name']
        change_percent = event['change_percent']
        current_price = event['current_price']
        conditions = event.get('conditions', [])
        
        direction = '상승' if change_percent > 0 else '하락'
        market_summary = market_data.get('market_summary', {})
        
        article = f"""# {symbol} {abs(change_percent):.1f}% {direction}, {', '.join(conditions[:2])}

## 핵심 요약
{name}이(가) {datetime.now().strftime('%Y년 %m월 %d일')} 거래에서 {change_percent:+.2f}% {direction}하며 ${current_price:.2f}를 기록했습니다. {', '.join(conditions)}이 관찰되고 있습니다.

## 상세 분석
오늘 {name}({symbol}) 주가는 전일 대비 {change_percent:+.2f}% {direction}한 ${current_price:.2f}에 거래되고 있습니다."""

        if abs(change_percent) >= 5:
            article += f" 이는 상당한 변동성을 보이는 움직임으로, {event['severity']} 수준의 시장 이벤트로 분류됩니다."
        elif abs(change_percent) >= 3:
            article += f" 이는 주목할 만한 변동으로 투자자들의 관심이 집중되고 있습니다."
        else:
            article += f" 이는 일반적인 시장 변동 범위 내의 움직임입니다."

        article += f"""

거래량은 {event['volume']:,}주를 기록했으며, 이는 투자자들의 관심도를 나타내는 지표입니다.

## 시장 전체 동향
전체 {market_summary.get('total_symbols', 0)}개 종목 중 {market_summary.get('positive_count', 0)}개 종목이 상승, {market_summary.get('negative_count', 0)}개 종목이 하락했습니다. 시장 전체 평균 변동률은 {market_summary.get('avg_change', 0):+.2f}%를 기록했습니다."""

        # 다른 주요 종목 동향
        article += "\n\n### 주요 종목 동향\n"
        for sym, data in list(market_data['symbols'].items())[:5]:
            if sym != symbol:
                article += f"- {sym}: {data['change_percent']:+.2f}% (${data['current_price']:.2f})\n"

        article += f"""

## 투자 시사점
{name}의 {'상승세' if change_percent > 0 else '하락세'}는 """

        if change_percent > 0:
            article += "긍정적인 시장 심리와 투자자 신뢰를 반영하는 것으로 해석됩니다."
        else:
            article += "시장 조정 과정이나 일시적인 불안 심리를 반영하는 것으로 보입니다."

        article += " 투자자들은 향후 시장 동향과 관련 뉴스를 주의 깊게 관찰할 필요가 있습니다."

        article += f"\n\n---\n*기사 생성: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')} | AI 자동 생성*"
        
        return article
