#!/usr/bin/env python3
"""
HTML 기사 생성 및 Slack 전송 시스템
AI 에이전트 오류 시 대체 시스템으로 작동
"""

import os
import sys
import json
import requests
import logging
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import boto3
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage

# .env 파일 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HTMLArticleSlackSystem:
    """HTML 기사 생성 및 Slack 전송 시스템"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.output_dirs = {
            'articles': 'output/html_articles',
            'data': 'output/market_data'
        }
        
        for dir_path in self.output_dirs.values():
            os.makedirs(dir_path, exist_ok=True)
        
        # AWS Bedrock 클라이언트 초기화
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
                    "max_tokens": 2000
                }
            )
            self.logger.info("✅ AWS Bedrock 초기화 완료")
        except Exception as e:
            self.logger.error(f"❌ AWS Bedrock 초기화 실패: {e}")
            self.llm = None
        
        # Slack 웹훅 URL
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if self.slack_webhook_url:
            self.logger.info("✅ Slack 웹훅 URL 설정됨")
        else:
            self.logger.warning("⚠️ Slack 웹훅 URL이 설정되지 않음")
    
    def collect_market_data(self, symbols: List[str] = None) -> Dict[str, Any]:
        """시장 데이터 수집"""
        
        if symbols is None:
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', '^GSPC', '^IXIC', '^VIX']
        
        market_data = {
            'timestamp': datetime.now().isoformat(),
            'symbols': {}
        }
        
        self.logger.info(f"📊 {len(symbols)}개 심볼 데이터 수집 중...")
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="5d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    previous_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change_percent = ((current_price - previous_price) / previous_price) * 100
                    
                    market_data['symbols'][symbol] = {
                        'name': info.get('longName', symbol),
                        'current_price': float(current_price),
                        'previous_price': float(previous_price),
                        'change_percent': float(change_percent),
                        'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                        'high_52w': info.get('fiftyTwoWeekHigh', 0),
                        'low_52w': info.get('fiftyTwoWeekLow', 0),
                        'market_cap': info.get('marketCap', 0)
                    }
                    
                    self.logger.info(f"✅ {symbol}: {change_percent:+.2f}%")
                
            except Exception as e:
                self.logger.error(f"❌ {symbol} 데이터 수집 실패: {e}")
                continue
        
        # 데이터 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_file = os.path.join(self.output_dirs['data'], f'market_data_{timestamp}.json')
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(market_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"💾 시장 데이터 저장: {data_file}")
        return market_data
    
    def detect_events(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """이벤트 감지"""
        
        events = []
        
        for symbol, data in market_data['symbols'].items():
            change_percent = data['change_percent']
            
            # 이벤트 감지 조건
            if abs(change_percent) >= 3.0:  # 3% 이상 변동
                severity = 'high' if abs(change_percent) >= 5.0 else 'medium'
                direction = '상승' if change_percent > 0 else '하락'
                
                event = {
                    'symbol': symbol,
                    'name': data['name'],
                    'event_type': 'price_change',
                    'severity': severity,
                    'title': f"{symbol} 주가 {abs(change_percent):.1f}% {direction}",
                    'description': f"{data['name']}이(가) {change_percent:+.2f}% {direction}했습니다.",
                    'current_price': data['current_price'],
                    'change_percent': change_percent,
                    'volume': data['volume'],
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
                'event_type': 'market_update',
                'severity': 'low',
                'title': f"{symbol} 시장 동향",
                'description': f"{data['name']}이(가) {change_percent:+.2f}% {direction}했습니다.",
                'current_price': data['current_price'],
                'change_percent': change_percent,
                'volume': data['volume'],
                'timestamp': datetime.now().isoformat()
            }
            events.append(event)
        
        self.logger.info(f"🚨 {len(events)}개 이벤트 감지됨")
        return events
    
    def generate_article_with_ai(self, event: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """AI를 사용한 기사 생성"""
        
        if not self.llm:
            return self.generate_article_template(event, market_data)
        
        try:
            system_prompt = """당신은 전문 경제 기자입니다. 주어진 시장 데이터와 이벤트를 바탕으로 전문적이고 객관적인 경제 기사를 작성해주세요.

기사 작성 가이드라인:
1. 헤드라인은 간결하고 임팩트 있게
2. 리드 문단에서 핵심 내용 요약
3. 데이터 기반의 객관적 분석
4. 시장 전망 및 투자 시사점 포함
5. 전문적이지만 이해하기 쉬운 언어 사용

기사 구조:
- 헤드라인
- 리드 (핵심 요약)
- 본문 (상세 분석)
- 결론 (시장 전망)"""

            user_prompt = f"""다음 이벤트와 시장 데이터를 바탕으로 경제 기사를 작성해주세요:

이벤트 정보:
- 종목: {event['symbol']} ({event['name']})
- 변동률: {event['change_percent']:+.2f}%
- 현재가: ${event['current_price']:.2f}
- 거래량: {event['volume']:,}

시장 전체 상황:
"""
            
            # 주요 종목 데이터 추가
            for symbol, data in list(market_data['symbols'].items())[:5]:
                user_prompt += f"- {symbol}: {data['change_percent']:+.2f}%\n"
            
            user_prompt += f"\n시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            self.logger.error(f"❌ AI 기사 생성 실패: {e}")
            return self.generate_article_template(event, market_data)
    
    def generate_article_template(self, event: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """템플릿 기반 기사 생성 (AI 실패 시 대체)"""
        
        symbol = event['symbol']
        name = event['name']
        change_percent = event['change_percent']
        current_price = event['current_price']
        direction = '상승' if change_percent > 0 else '하락'
        
        article = f"""# {symbol} 주가 {abs(change_percent):.1f}% {direction}, 시장 주목

## 핵심 요약
{name}이(가) {datetime.now().strftime('%Y년 %m월 %d일')} 거래에서 {change_percent:+.2f}% {direction}하며 ${current_price:.2f}를 기록했습니다.

## 상세 분석
오늘 {name}({symbol}) 주가는 전일 대비 {change_percent:+.2f}% {direction}한 ${current_price:.2f}에 거래를 마쳤습니다. 이는 최근 시장 동향과 """
        
        if abs(change_percent) >= 3:
            article += "상당한 변동성을 보이는 움직임으로 해석됩니다."
        else:
            article += "안정적인 흐름을 보이는 것으로 분석됩니다."
        
        article += f"""

거래량은 {event['volume']:,}주를 기록했으며, 이는 투자자들의 관심이 집중되고 있음을 시사합니다.

## 시장 전망
"""
        
        if change_percent > 0:
            article += f"{name}의 상승세는 긍정적인 시장 심리를 반영하는 것으로 보입니다. "
        else:
            article += f"{name}의 하락세는 시장 조정 과정의 일환으로 해석됩니다. "
        
        article += "투자자들은 향후 시장 동향을 주의 깊게 관찰할 필요가 있습니다."
        
        # 다른 주요 종목 동향 추가
        article += "\n\n## 주요 종목 동향\n"
        for sym, data in list(market_data['symbols'].items())[:5]:
            if sym != symbol:
                article += f"- {sym}: {data['change_percent']:+.2f}%\n"
        
        article += f"\n*기사 생성 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}*"
        
        return article
    
    def create_html_article(self, article_content: str, event: Dict[str, Any]) -> str:
        """HTML 기사 생성"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        symbol = event['symbol']
        
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{event['title']} - 경제 뉴스</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .article-container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .title {{
            color: #333;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .meta-info {{
            color: #666;
            font-size: 14px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .meta-item {{
            background: #f8f9fa;
            padding: 5px 10px;
            border-radius: 5px;
        }}
        .price-info {{
            background: {'#d4edda' if event['change_percent'] > 0 else '#f8d7da'};
            color: {'#155724' if event['change_percent'] > 0 else '#721c24'};
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            font-weight: bold;
        }}
        .content {{
            font-size: 16px;
            line-height: 1.8;
            color: #333;
        }}
        .content h1 {{
            color: #007bff;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .content h2 {{
            color: #0056b3;
            margin-top: 30px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 14px;
            text-align: center;
        }}
        .highlight {{
            background: #fff3cd;
            padding: 2px 4px;
            border-radius: 3px;
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
            </div>
        </div>
        
        <div class="price-info">
            💰 현재가: ${event['current_price']:.2f} 
            ({event['change_percent']:+.2f}% {'📈' if event['change_percent'] > 0 else '📉'})
            | 거래량: {event['volume']:,}
        </div>
        
        <div class="content">
            {self.markdown_to_html(article_content)}
        </div>
        
        <div class="footer">
            <p>🤖 이 기사는 AI가 실시간 시장 데이터를 분석하여 자동 생성했습니다.</p>
            <p>📊 데이터 출처: Yahoo Finance | 생성 시간: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}</p>
        </div>
    </div>
</body>
</html>"""
        
        # HTML 파일 저장
        filename = f"{symbol}_article_{timestamp}.html"
        filepath = os.path.join(self.output_dirs['articles'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"📄 HTML 기사 생성: {filepath}")
        return filepath
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """간단한 마크다운을 HTML로 변환"""
        
        html = markdown_text
        
        # 헤더 변환
        html = html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        html = html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
        
        # 마지막 헤더 닫기
        if '<h1>' in html and '</h1>' not in html.split('<h1>')[-1]:
            html += '</h1>'
        if '<h2>' in html and '</h2>' not in html.split('<h2>')[-1]:
            html += '</h2>'
        
        # 문단 변환
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<h') and not p.startswith('*'):
                if p.startswith('- '):
                    # 리스트 처리
                    items = p.split('\n- ')
                    list_html = '<ul>'
                    for item in items:
                        item = item.replace('- ', '')
                        if item:
                            list_html += f'<li>{item}</li>'
                    list_html += '</ul>'
                    html_paragraphs.append(list_html)
                else:
                    html_paragraphs.append(f'<p>{p}</p>')
            elif p.startswith('*') and p.endswith('*'):
                html_paragraphs.append(f'<p><em>{p[1:-1]}</em></p>')
            else:
                html_paragraphs.append(p)
        
        return '\n'.join(html_paragraphs)
    
    def send_slack_notification(self, article_filepath: str, event: Dict[str, Any]) -> bool:
        """Slack으로 기사 알림 전송"""
        
        if not self.slack_webhook_url:
            self.logger.warning("⚠️ Slack 웹훅 URL이 설정되지 않음")
            return False
        
        try:
            # 기사 파일 읽기
            with open(article_filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 기사 요약 추출 (첫 번째 문단)
            summary = event['description']
            if len(summary) > 200:
                summary = summary[:200] + "..."
            
            # Slack 메시지 생성
            message = {
                "text": f"📰 새 기사 생성: {event['title']}",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "📰 AI 경제 기사 생성 완료"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{event['title']}*\n\n{summary}"
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
                                "text": f"*심각도:* {event['severity']}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"📄 *HTML 파일:* `{os.path.basename(article_filepath)}`\n🤖 AI가 실시간 데이터를 분석하여 자동 생성한 기사입니다."
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
                                "text": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🤖 HTML 기사 생성 시스템"
                            }
                        ]
                    }
                ]
            }
            
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
        self.logger.info("🚀 HTML 기사 생성 시스템 시작")
        
        try:
            # 1. 시장 데이터 수집
            self.logger.info("📊 1단계: 시장 데이터 수집")
            market_data = self.collect_market_data()
            
            if not market_data['symbols']:
                raise Exception("시장 데이터 수집 실패")
            
            # 2. 이벤트 감지
            self.logger.info("🚨 2단계: 이벤트 감지")
            events = self.detect_events(market_data)
            
            if not events:
                raise Exception("감지된 이벤트 없음")
            
            # 3. 기사 생성 및 HTML 변환
            self.logger.info("✍️ 3단계: 기사 생성")
            results = []
            
            for event in events[:2]:  # 최대 2개 이벤트 처리
                self.logger.info(f"📝 {event['symbol']} 기사 생성 중...")
                
                # AI 기사 생성
                article_content = self.generate_article_with_ai(event, market_data)
                
                # HTML 파일 생성
                html_filepath = self.create_html_article(article_content, event)
                
                # Slack 알림 전송
                slack_success = self.send_slack_notification(html_filepath, event)
                
                results.append({
                    'event': event,
                    'article_content': article_content,
                    'html_file': html_filepath,
                    'slack_sent': slack_success
                })
                
                self.logger.info(f"✅ {event['symbol']} 처리 완료")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'status': 'success',
                'execution_time': execution_time,
                'events_processed': len(results),
                'articles_generated': len(results),
                'slack_notifications': sum(1 for r in results if r['slack_sent']),
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"🎉 시스템 실행 완료 ({execution_time:.1f}초)")
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
    
    print("🚀 HTML 기사 생성 및 Slack 전송 시스템")
    print("=" * 60)
    
    # 시스템 초기화
    system = HTMLArticleSlackSystem()
    
    # 전체 시스템 실행
    result = system.run_complete_system()
    
    # 결과 출력
    print("\n📊 실행 결과:")
    print(f"상태: {result.get('status', 'unknown')}")
    print(f"실행 시간: {result.get('execution_time', 0):.1f}초")
    print(f"처리된 이벤트: {result.get('events_processed', 0)}개")
    print(f"생성된 기사: {result.get('articles_generated', 0)}개")
    print(f"Slack 알림: {result.get('slack_notifications', 0)}개")
    
    if result.get('status') == 'success':
        print("\n🎉 HTML 기사 생성 및 Slack 전송 완료!")
        
        # 생성된 파일 목록
        results = result.get('results', [])
        if results:
            print("\n💡 생성된 HTML 기사:")
            for i, res in enumerate(results):
                html_file = res.get('html_file', '')
                if html_file:
                    print(f"  {i+1}. {html_file}")
                    print(f"     브라우저에서 열기: open {html_file}")
        
        print("\n📱 Slack 채널에서 알림을 확인하세요!")
    else:
        print(f"\n❌ 실행 실패: {result.get('error', 'Unknown error')}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
