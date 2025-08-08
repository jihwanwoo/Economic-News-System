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
                        'chart_data': [
                            {
                                'date': date.strftime('%Y-%m-%d'),
                                'timestamp': date,
                                'open': float(row['Open']),
                                'high': float(row['High']),
                                'low': float(row['Low']),
                                'close': float(row['Close']),
                                'volume': int(row['Volume']) if 'Volume' in row and not pd.isna(row['Volume']) else 0
                            }
                            for date, row in hist.tail(20).iterrows()
                        ]
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
                avg_volume = np.mean([d.get('volume', 0) for d in data.get('chart_data', [])])
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
                    # 날짜 처리 - pandas DataFrame의 인덱스를 올바르게 처리
                    if 'timestamp' in item and item['timestamp']:
                        date = item['timestamp']
                        if isinstance(date, str):
                            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    elif 'date' in item:
                        date = datetime.strptime(item['date'], '%Y-%m-%d')
                    else:
                        continue  # 날짜 정보가 없으면 스킵
                    
                    dates.append(date)
                    prices.append(float(item.get('close', item.get('Close', 0))))
                    volumes.append(int(item.get('volume', item.get('Volume', 0))))
                    highs.append(float(item.get('high', item.get('High', item.get('close', item.get('Close', 0))))))
                    lows.append(float(item.get('low', item.get('Low', item.get('close', item.get('Close', 0))))))
                    
                except (ValueError, KeyError, TypeError) as e:
                    self.logger.warning(f"⚠️ {symbol} 데이터 파싱 오류: {e}")
                    continue
            
            if len(dates) < 2:
                self.logger.warning(f"⚠️ {symbol} 유효한 데이터 부족")
                return ""
            
            # 차트 생성
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
            
            # 가격 차트
            ax1.plot(dates, prices, linewidth=2, color='#1f77b4', label='Close Price')
            ax1.fill_between(dates, prices, alpha=0.3, color='#1f77b4')
            ax1.set_title(f'{symbol} - 가격 추이 (최근 {len(dates)}일)', fontsize=16, fontweight='bold')
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
            filename = f"{symbol}_fixed_chart_{timestamp}.png"
            filepath = os.path.join(self.output_dirs['charts'], filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            self.logger.info(f"📈 수정된 차트 생성 성공: {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"❌ {symbol} 차트 생성 실패: {e}")
            import traceback
            self.logger.error(f"상세 오류: {traceback.format_exc()}")
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
    def create_html_article(self, article_content: str, event: Dict[str, Any], chart_path: str = "") -> str:
        """HTML 기사 생성"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        symbol = event['symbol']
        
        # 차트 이미지 HTML
        chart_html = ""
        if chart_path and os.path.exists(chart_path):
            chart_filename = os.path.basename(chart_path)
            chart_html = f'''
            <div class="chart-container">
                <h3>📈 가격 차트</h3>
                <img src="../standalone_charts/{chart_filename}" alt="{symbol} 차트" style="width: 100%; max-width: 800px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            </div>
            '''
        
        html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{event['title']} - 경제 뉴스</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .article-container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .header {{
            border-bottom: 4px solid #007bff;
            padding-bottom: 25px;
            margin-bottom: 35px;
            background: linear-gradient(90deg, #007bff, #0056b3);
            margin: -40px -40px 35px -40px;
            padding: 25px 40px;
            border-radius: 15px 15px 0 0;
            color: white;
        }}
        .title {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        .meta-info {{
            font-size: 14px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            opacity: 0.9;
        }}
        .meta-item {{
            background: rgba(255,255,255,0.2);
            padding: 8px 12px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }}
        .price-info {{
            background: {'linear-gradient(135deg, #d4edda, #c3e6cb)' if event['change_percent'] > 0 else 'linear-gradient(135deg, #f8d7da, #f1b0b7)'};
            color: {'#155724' if event['change_percent'] > 0 else '#721c24'};
            padding: 20px;
            border-radius: 12px;
            margin: 25px 0;
            font-weight: bold;
            font-size: 18px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .severity-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            margin-left: 10px;
        }}
        .severity-critical {{ background: #dc3545; color: white; }}
        .severity-high {{ background: #fd7e14; color: white; }}
        .severity-medium {{ background: #ffc107; color: #212529; }}
        .severity-low {{ background: #28a745; color: white; }}
        .content {{
            font-size: 17px;
            line-height: 1.8;
            color: #333;
        }}
        .content h1 {{
            color: #007bff;
            border-bottom: 3px solid #007bff;
            padding-bottom: 12px;
            margin-top: 35px;
        }}
        .content h2 {{
            color: #0056b3;
            margin-top: 30px;
            font-size: 24px;
        }}
        .content h3 {{
            color: #495057;
            margin-top: 25px;
        }}
        .chart-container {{
            margin: 30px 0;
            text-align: center;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
        }}
        .conditions-list {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2196f3;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 25px;
            border-top: 2px solid #eee;
            color: #666;
            font-size: 14px;
            text-align: center;
            background: #f8f9fa;
            margin-left: -40px;
            margin-right: -40px;
            margin-bottom: -40px;
            padding-left: 40px;
            padding-right: 40px;
            padding-bottom: 25px;
            border-radius: 0 0 15px 15px;
        }}
        .highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 3px 6px;
            border-radius: 4px;
            font-weight: 500;
        }}
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .data-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        .data-value {{
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
        }}
        .data-label {{
            font-size: 12px;
            color: #6c757d;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="article-container">
        <div class="header">
            <div class="title">{event['title']}</div>
            <div class="meta-info">
                <div class="meta-item">📊 종목: {symbol}</div>
                <div class="meta-item">⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div class="meta-item">🤖 AI 자동 생성</div>
                <div class="meta-item">📈 실시간 데이터</div>
            </div>
        </div>
        
        <div class="price-info">
            💰 현재가: ${event['current_price']:.2f} 
            ({event['change_percent']:+.2f}% {'📈' if event['change_percent'] > 0 else '📉'})
            | 거래량: {event['volume']:,}
            <span class="severity-badge severity-{event['severity']}">{event['severity']}</span>
        </div>
        
        <div class="conditions-list">
            <strong>🔍 감지된 조건:</strong>
            <ul>
                {chr(10).join([f'<li>{condition}</li>' for condition in event.get('conditions', [])])}
            </ul>
        </div>
        
        {chart_html}
        
        <div class="content">
            {self.markdown_to_html(article_content)}
        </div>
        
        <div class="footer">
            <p><strong>🤖 이 기사는 AI가 실시간 시장 데이터를 분석하여 자동 생성했습니다.</strong></p>
            <p>📊 데이터 출처: Yahoo Finance | 생성 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}</p>
            <p>⚠️ 이 정보는 투자 조언이 아니며, 투자 결정은 신중히 하시기 바랍니다.</p>
        </div>
    </div>
</body>
</html>'''
        
        # HTML 파일 저장
        filename = f"{symbol}_standalone_{timestamp}.html"
        filepath = os.path.join(self.output_dirs['articles'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"📄 HTML 기사 생성: {filepath}")
        return filepath
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """마크다운을 HTML로 변환"""
        
        html = markdown_text
        
        # 헤더 변환
        html = html.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
        html = html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')  
        html = html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        
        # 마지막 헤더 닫기
        if '<h1>' in html and html.count('<h1>') > html.count('</h1>'):
            html += '</h1>'
        if '<h2>' in html and html.count('<h2>') > html.count('</h2>'):
            html += '</h2>'
        if '<h3>' in html and html.count('<h3>') > html.count('</h3>'):
            html += '</h3>'
        
        # 문단 변환
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<h') and not p.startswith('*') and not p.startswith('---'):
                if p.startswith('- '):
                    # 리스트 처리
                    items = p.split('\n- ')
                    list_html = '<ul class="content-list">'
                    for item in items:
                        item = item.replace('- ', '').strip()
                        if item:
                            list_html += f'<li>{item}</li>'
                    list_html += '</ul>'
                    html_paragraphs.append(list_html)
                else:
                    html_paragraphs.append(f'<p>{p}</p>')
            elif p.startswith('*') and p.endswith('*'):
                html_paragraphs.append(f'<p class="footer-note"><em>{p[1:-1]}</em></p>')
            elif p.startswith('---'):
                html_paragraphs.append('<hr>')
            else:
                html_paragraphs.append(p)
        
        return '\n'.join(html_paragraphs)
    
    def send_enhanced_slack_notification(self, article_filepath: str, event: Dict[str, Any], chart_path: str = "") -> bool:
        """향상된 Slack 알림 전송"""
        
        if not self.slack_webhook_url:
            self.logger.warning("⚠️ Slack 웹훅 URL이 설정되지 않음")
            return False
        
        try:
            # 심각도별 이모지
            severity_emojis = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '📊',
                'low': '📈'
            }
            
            severity_colors = {
                'critical': '#dc3545',
                'high': '#fd7e14', 
                'medium': '#ffc107',
                'low': '#28a745'
            }
            
            emoji = severity_emojis.get(event['severity'], '📊')
            color = severity_colors.get(event['severity'], '#007bff')
            
            # Slack 메시지 생성
            message = {
                "text": f"{emoji} 경제 뉴스: {event['title']}",
                "attachments": [
                    {
                        "color": color,
                        "blocks": [
                            {
                                "type": "header",
                                "text": {
                                    "type": "plain_text",
                                    "text": f"{emoji} 독립 AI 뉴스 시스템"
                                }
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"*{event['title']}*\n\n{event['description']}"
                                }
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*종목:* {event['symbol']}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*변동률:* {event['change_percent']:+.2f}%"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*현재가:* ${event['current_price']:.2f}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*심각도:* {event['severity'].upper()}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*거래량:* {event['volume']:,}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*감지 조건:* {len(event.get('conditions', []))}개"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
            
            # 감지된 조건들 추가
            if event.get('conditions'):
                conditions_text = "\\n".join([f"• {condition}" for condition in event['conditions']])
                message["attachments"][0]["blocks"].append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🔍 감지된 조건들:*\\n{conditions_text}"
                    }
                })
            
            # 파일 정보 추가
            message["attachments"][0]["blocks"].extend([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"📄 *HTML 기사:* `{os.path.basename(article_filepath)}`\\n{'📈 *차트:* 포함됨' if chart_path else '📈 *차트:* 생성 실패'}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🤖 독립 AI 뉴스 시스템 | ✅ 오류 없음"
                        }
                    ]
                }
            ])
            
            # Slack으로 전송
            response = requests.post(
                self.slack_webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info("✅ Slack 알림 전송 성공")
                return True
            else:
                self.logger.error(f"❌ Slack 알림 전송 실패: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Slack 알림 전송 오류: {e}")
            return False
    
    def run_complete_system(self) -> Dict[str, Any]:
        """전체 시스템 실행"""
        
        start_time = datetime.now()
        self.logger.info("🚀 독립적인 뉴스 시스템 시작")
        
        try:
            # 1. 시장 데이터 수집
            self.logger.info("📊 1단계: 시장 데이터 수집")
            market_data = self.collect_market_data()
            
            if not market_data['symbols']:
                raise Exception("시장 데이터 수집 실패")
            
            # 2. 이벤트 감지
            self.logger.info("🚨 2단계: 중요 이벤트 감지")
            events = self.detect_significant_events(market_data)
            
            if not events:
                raise Exception("감지된 이벤트 없음")
            
            # 3. 기사 생성 및 처리
            self.logger.info("✍️ 3단계: 종합 기사 생성")
            results = []
            
            for event in events[:3]:  # 최대 3개 이벤트 처리
                self.logger.info(f"📝 {event['symbol']} 처리 중...")
                
                # 차트 생성
                chart_path = self.create_enhanced_price_chart(event['symbol'], market_data['symbols'][event['symbol']])
                
                # AI 기사 생성
                article_content = self.generate_comprehensive_article(event, market_data)
                
                # HTML 파일 생성
                html_filepath = self.create_html_article(article_content, event, chart_path)
                
                # Slack 알림 전송
                slack_success = self.send_enhanced_slack_notification(html_filepath, event, chart_path)
                
                results.append({
                    'event': event,
                    'article_content': article_content,
                    'html_file': html_filepath,
                    'chart_file': chart_path,
                    'slack_sent': slack_success
                })
                
                self.logger.info(f"✅ {event['symbol']} 처리 완료")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'status': 'success',
                'execution_time': execution_time,
                'events_processed': len(results),
                'articles_generated': len(results),
                'charts_generated': sum(1 for r in results if r['chart_file']),
                'slack_notifications': sum(1 for r in results if r['slack_sent']),
                'results': results,
                'market_summary': market_data.get('market_summary', {}),
                'timestamp': datetime.now().isoformat()
            }
            
            # 결과 저장
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            result_file = os.path.join(self.output_dirs['data'], f'execution_result_{timestamp}.json')
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"🎉 독립 시스템 실행 완료 ({execution_time:.1f}초)")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"❌ 시스템 실행 실패: {e}")
            
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat()
            }

def main():
    """메인 함수"""
    
    print("🚀 완전히 독립적인 경제 뉴스 생성 시스템")
    print("=" * 70)
    print("✅ OrchestratorStrand 의존성 없음")
    print("✅ 안정적인 독립 실행")
    print("✅ AI 기사 생성 + 차트 + Slack 알림")
    print("=" * 70)
    
    # 시스템 초기화
    system = StandaloneNewsSystem()
    
    # 전체 시스템 실행
    result = system.run_complete_system()
    
    # 결과 출력
    print("\n📊 실행 결과:")
    print(f"상태: {result.get('status', 'unknown')}")
    print(f"실행 시간: {result.get('execution_time', 0):.1f}초")
    print(f"처리된 이벤트: {result.get('events_processed', 0)}개")
    print(f"생성된 기사: {result.get('articles_generated', 0)}개")
    print(f"생성된 차트: {result.get('charts_generated', 0)}개")
    print(f"Slack 알림: {result.get('slack_notifications', 0)}개")
    
    if result.get('status') == 'success':
        print("\n🎉 독립 시스템 실행 완료!")
        
        # 시장 요약
        market_summary = result.get('market_summary', {})
        if market_summary:
            print(f"\n📈 시장 요약:")
            print(f"  전체 종목: {market_summary.get('total_symbols', 0)}개")
            print(f"  평균 변동률: {market_summary.get('avg_change', 0):+.2f}%")
            print(f"  상승 종목: {market_summary.get('positive_count', 0)}개")
            print(f"  하락 종목: {market_summary.get('negative_count', 0)}개")
        
        # 생성된 파일 목록
        results = result.get('results', [])
        if results:
            print("\n💡 생성된 파일:")
            for i, res in enumerate(results):
                event = res.get('event', {})
                html_file = res.get('html_file', '')
                chart_file = res.get('chart_file', '')
                
                print(f"  {i+1}. {event.get('symbol', 'Unknown')} ({event.get('severity', 'unknown')})")
                if html_file:
                    print(f"     📄 HTML: {html_file}")
                if chart_file:
                    print(f"     📈 차트: {chart_file}")
                print(f"     📱 Slack: {'✅' if res.get('slack_sent') else '❌'}")
        
        print("\n🌐 HTML 기사 보기:")
        if results and results[0].get('html_file'):
            latest_html = results[0]['html_file']
            print(f"  open {latest_html}")
        
        print("\n📱 Slack 채널에서 알림을 확인하세요!")
    else:
        print(f"\n❌ 실행 실패: {result.get('error', 'Unknown error')}")
        print("\n🔧 문제 해결:")
        print("  • AWS 자격 증명: aws sts get-caller-identity")
        print("  • Slack 웹훅: python test_slack_notification.py")
        print("  • 인터넷 연결 확인")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
