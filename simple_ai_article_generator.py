#!/usr/bin/env python3
"""
실용적인 AI 기사 생성 시스템
AWS Bedrock Claude를 사용한 실제 작동하는 기사 생성
"""

import boto3
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

class SimpleAIArticleGenerator:
    """간단하고 실용적인 AI 기사 생성기"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # AWS Bedrock 클라이언트 초기화
        try:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name='us-east-1'
            )
            self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            self.logger.info("✅ AWS Bedrock 클라이언트 초기화 완료")
        except Exception as e:
            self.logger.warning(f"⚠️ AWS Bedrock 초기화 실패: {str(e)}")
            self.bedrock_client = None
    
    def analyze_events(self, events: List[Dict]) -> Dict[str, Any]:
        """이벤트 데이터 분석"""
        try:
            self.logger.info("📊 이벤트 데이터 분석 시작")
            
            analysis = {
                'total_events': len(events),
                'event_summary': [],
                'market_sentiment': 'neutral',
                'key_symbols': [],
                'price_changes': [],
                'analysis_time': datetime.now().isoformat()
            }
            
            positive_events = 0
            negative_events = 0
            
            for event in events:
                symbol = event.get('symbol', 'Unknown')
                description = event.get('description', '')
                sentiment = event.get('sentiment', 'neutral')
                
                analysis['event_summary'].append({
                    'symbol': symbol,
                    'description': description,
                    'sentiment': sentiment
                })
                
                analysis['key_symbols'].append(symbol)
                
                # change_percent가 있으면 사용, 없으면 설명에서 추출 시도
                change_percent = event.get('change_percent')
                if change_percent is not None:
                    analysis['price_changes'].append({
                        'symbol': symbol,
                        'change': change_percent
                    })
                else:
                    # 설명에서 퍼센트 추출 시도
                    import re
                    percent_match = re.search(r'([-+]?\d+\.?\d*)%', description)
                    if percent_match:
                        try:
                            change_value = float(percent_match.group(1))
                            analysis['price_changes'].append({
                                'symbol': symbol,
                                'change': change_value
                            })
                        except ValueError:
                            pass
                
                if sentiment == 'positive':
                    positive_events += 1
                elif sentiment == 'negative':
                    negative_events += 1
            
            # 전체 시장 감정 판단
            if positive_events > negative_events:
                analysis['market_sentiment'] = 'bullish'
            elif negative_events > positive_events:
                analysis['market_sentiment'] = 'bearish'
            else:
                analysis['market_sentiment'] = 'neutral'
            
            # 중복 제거
            analysis['key_symbols'] = list(set(analysis['key_symbols']))
            
            self.logger.info(f"✅ 분석 완료: {len(events)}개 이벤트, 감정: {analysis['market_sentiment']}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ 이벤트 분석 실패: {str(e)}")
            return {
                'total_events': len(events) if events else 0,
                'event_summary': [],
                'market_sentiment': 'neutral',
                'key_symbols': [],
                'price_changes': [],
                'analysis_time': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def generate_article_with_claude(self, events: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """Claude를 사용한 기사 생성"""
        try:
            self.logger.info("✍️ Claude 기사 생성 시작")
            
            if not self.bedrock_client:
                return self._generate_fallback_article(events, analysis)
            
            # 프롬프트 생성
            prompt = self._create_article_prompt(events, analysis)
            
            # Claude API 호출
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            article_content = response_body['content'][0]['text']
            
            # 기사 구조화
            article = self._structure_article(article_content, events, analysis)
            
            self.logger.info("✅ Claude 기사 생성 완료")
            return article
            
        except Exception as e:
            self.logger.error(f"❌ Claude 기사 생성 실패: {str(e)}")
            return self._generate_fallback_article(events, analysis)
    
    def _create_article_prompt(self, events: List[Dict], analysis: Dict) -> str:
        """기사 생성용 프롬프트 생성 (2000자 이상)"""
        
        # 이벤트 요약
        event_descriptions = []
        for event in events:
            event_descriptions.append(f"- {event.get('description', '')}")
        
        events_text = "\n".join(event_descriptions)
        
        prompt = f"""
당신은 전문 경제 기자입니다. 다음 시장 이벤트들을 바탕으로 심층적인 경제 뉴스 기사를 작성해주세요.

**감지된 시장 이벤트:**
{events_text}

**시장 분석 정보:**
- 전체 이벤트 수: {analysis.get('total_events', 0)}개
- 시장 감정: {analysis.get('market_sentiment', 'neutral')}
- 주요 종목: {', '.join(analysis.get('key_symbols', [])[:5])}
- 가격 변화: {analysis.get('price_changes', [])}

**기사 작성 요구사항 (최소 2000자 이상):**

1. **제목 (50자 이내)**: 흥미롭고 정확한 헤드라인

2. **리드 문단 (150-200자)**: 
   - 핵심 내용을 요약한 첫 문단
   - 5W1H 포함

3. **본문 1단락 - 현황 분석 (400-500자)**:
   - 현재 시장 상황 상세 분석
   - 구체적인 수치와 데이터 제시
   - 주요 종목별 움직임 설명

4. **본문 2단락 - 원인 분석 (400-500자)**:
   - 시장 변화의 근본 원인 분석
   - 거시경제적 요인 고려
   - 업계 전문가 관점 포함

5. **본문 3단락 - 파급효과 (400-500자)**:
   - 다른 섹터/시장에 미치는 영향
   - 연관 종목들의 반응
   - 글로벌 시장과의 연관성

6. **본문 4단락 - 전망 및 분석 (400-500자)**:
   - 단기/중기 전망
   - 주요 변수들과 리스크 요인
   - 시나리오별 분석

7. **결론 (200-300자)**:
   - 투자자들을 위한 핵심 시사점
   - 주의사항 및 투자 전략 제안

**작성 스타일:**
- 객관적이고 전문적인 톤
- 구체적인 수치와 데이터 활용
- 투자자들이 이해하기 쉬운 언어 사용
- 과도한 추측이나 단정적 표현 지양
- 각 문단은 논리적으로 연결되어야 함
- 풍부한 배경 정보와 맥락 제공
- **반드시 2000자 이상으로 작성** (매우 중요!)

**중요: 각 섹션별 최소 글자 수를 준수해주세요:**
- 리드 문단: 최소 150자
- 본문 1단락: 최소 400자
- 본문 2단락: 최소 400자  
- 본문 3단락: 최소 400자
- 본문 4단락: 최소 400자
- 결론: 최소 250자

다음 형식으로 작성해주세요:

제목: [기사 제목]

리드: [150자 이상의 리드 문단]

본문1: [400자 이상의 현황 분석]

본문2: [400자 이상의 원인 분석]

본문3: [400자 이상의 파급효과 분석]

본문4: [400자 이상의 전망 및 분석]

결론: [250자 이상의 결론]

**주의사항: 전체 기사는 반드시 2000자 이상이어야 합니다. 각 섹션의 최소 글자 수를 반드시 준수해주세요.**

태그: [관련 키워드 5개를 쉼표로 구분]
"""
        
        return prompt
    
    def _structure_article(self, content: str, events: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """기사 내용을 구조화"""
        
        try:
            # 기본 구조
            article = {
                'title': '',
                'lead': '',
                'content': '',
                'conclusion': '',
                'tags': [],
                'metadata': {
                    'events_count': len(events),
                    'market_sentiment': analysis.get('market_sentiment', 'neutral'),
                    'key_symbols': analysis.get('key_symbols', []),
                    'generated_at': datetime.now().isoformat(),
                    'word_count': len(content.split())
                }
            }
            
            # 내용 파싱
            lines = content.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('제목:'):
                    article['title'] = line.replace('제목:', '').strip()
                elif line.startswith('리드:'):
                    article['lead'] = line.replace('리드:', '').strip()
                elif line.startswith('본문:'):
                    current_section = 'content'
                elif line.startswith('결론:'):
                    article['conclusion'] = line.replace('결론:', '').strip()
                elif line.startswith('태그:'):
                    tags_text = line.replace('태그:', '').strip()
                    article['tags'] = [tag.strip() for tag in tags_text.split(',')]
                elif current_section == 'content':
                    if article['content']:
                        article['content'] += '\n\n' + line
                    else:
                        article['content'] = line
            
            # 기본값 설정
            if not article['title']:
                article['title'] = f"시장 동향: {', '.join(analysis.get('key_symbols', ['주요 종목'])[:3])} 분석"
            
            if not article['lead']:
                article['lead'] = f"오늘 {analysis.get('total_events', 0)}개의 주요 시장 이벤트가 감지되었습니다."
            
            if not article['content']:
                article['content'] = content
            
            if not article['tags']:
                article['tags'] = ['시장분석', '주식', '투자', '경제뉴스', '시장동향']
            
            return article
            
        except Exception as e:
            self.logger.error(f"기사 구조화 실패: {str(e)}")
            return {
                'title': f"시장 분석: {datetime.now().strftime('%Y-%m-%d')}",
                'lead': f"{len(events)}개의 시장 이벤트 분석",
                'content': content,
                'conclusion': "투자 결정 시 신중한 검토가 필요합니다.",
                'tags': ['시장분석', '주식', '투자'],
                'metadata': {
                    'events_count': len(events),
                    'generated_at': datetime.now().isoformat(),
                    'word_count': len(content.split())
                }
            }
    
    def _generate_fallback_article(self, events: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """Claude 사용 불가 시 대체 기사 생성"""
        
        self.logger.info("📝 대체 기사 생성 시작")
        
        # 기본 템플릿 기반 기사 생성
        symbols = analysis.get('key_symbols', ['시장'])[:3]
        sentiment = analysis.get('market_sentiment', 'neutral')
        
        sentiment_text = {
            'bullish': '상승세',
            'bearish': '하락세', 
            'neutral': '혼조세'
        }.get(sentiment, '혼조세')
        
        title = f"{', '.join(symbols)} 등 주요 종목 {sentiment_text} 지속"
        
        lead = f"오늘 {analysis.get('total_events', 0)}개의 주요 시장 이벤트가 감지되며 {sentiment_text}를 보이고 있습니다."
        
        # 이벤트 기반 본문 생성
        content_parts = []
        
        for event in events[:3]:  # 상위 3개 이벤트만
            symbol = event.get('symbol', 'Unknown')
            description = event.get('description', '')
            
            if 'change_percent' in event:
                change = event['change_percent']
                if change > 0:
                    content_parts.append(f"{symbol}은 {change:.2f}% 상승하며 강세를 보였습니다.")
                else:
                    content_parts.append(f"{symbol}은 {abs(change):.2f}% 하락하며 약세를 나타냈습니다.")
            else:
                content_parts.append(f"{symbol}에서 {description} 상황이 발생했습니다.")
        
        content = "\n\n".join(content_parts)
        
        if not content:
            content = "오늘 시장에서는 다양한 이벤트들이 발생하며 투자자들의 관심을 끌고 있습니다. 각 종목별로 서로 다른 움직임을 보이며 시장 전체적으로는 혼조세를 나타내고 있습니다."
        
        conclusion = "투자자들은 각 종목의 펀더멘털과 시장 상황을 종합적으로 고려하여 신중한 투자 결정을 내리시기 바랍니다."
        
        return {
            'title': title,
            'lead': lead,
            'content': content,
            'conclusion': conclusion,
            'tags': ['시장분석', '주식', '투자', '경제뉴스'] + symbols,
            'metadata': {
                'events_count': len(events),
                'market_sentiment': sentiment,
                'key_symbols': symbols,
                'generated_at': datetime.now().isoformat(),
                'generation_method': 'template_based',
                'word_count': len(content.split())
            }
        }
    
    def create_simple_charts(self, events: List[Dict], analysis: Dict) -> List[Dict]:
        """간단한 차트 생성"""
        try:
            self.logger.info("📊 차트 생성 시작")
            
            charts = []
            
            # 1. 가격 변화 차트
            price_changes = analysis.get('price_changes', [])
            if price_changes:
                symbols = [item['symbol'] for item in price_changes]
                changes = [item['change'] for item in price_changes]
                
                fig = px.bar(
                    x=symbols,
                    y=changes,
                    title="주요 종목 가격 변화율",
                    labels={'x': '종목', 'y': '변화율 (%)'},
                    color=changes,
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                
                charts.append({
                    'type': 'price_change',
                    'title': '주요 종목 가격 변화율',
                    'figure': fig,
                    'description': f"{len(symbols)}개 종목의 가격 변화율을 보여줍니다."
                })
            
            # 2. 시장 감정 파이 차트
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            for event in events:
                sentiment = event.get('sentiment', 'neutral')
                sentiment_counts[sentiment] += 1
            
            if sum(sentiment_counts.values()) > 0:
                fig = px.pie(
                    values=list(sentiment_counts.values()),
                    names=['긍정적', '부정적', '중립적'],
                    title="시장 감정 분포"
                )
                
                charts.append({
                    'type': 'sentiment_distribution',
                    'title': '시장 감정 분포',
                    'figure': fig,
                    'description': "감지된 이벤트들의 감정 분포를 나타냅니다."
                })
            
            self.logger.info(f"✅ {len(charts)}개 차트 생성 완료")
            return charts
            
        except Exception as e:
            self.logger.error(f"❌ 차트 생성 실패: {str(e)}")
            return []
    
    def generate_simple_review(self, article: Dict) -> Dict[str, Any]:
        """간단한 기사 검수"""
        try:
            self.logger.info("🔍 기사 검수 시작")
            
            review = {
                'quality_score': 0.0,
                'quality_assessment': {},
                'suggestions': [],
                'review_time': datetime.now().isoformat()
            }
            
            # 기본 품질 점수 계산
            score = 5.0  # 기본 점수
            
            # 제목 검사
            title = article.get('title', '')
            if len(title) > 10:
                score += 1.0
                review['quality_assessment']['title'] = '적절한 길이'
            else:
                review['suggestions'].append('제목을 더 구체적으로 작성하세요')
                review['quality_assessment']['title'] = '너무 짧음'
            
            # 내용 검사
            content = article.get('content', '')
            word_count = len(content.split())
            
            if word_count > 100:
                score += 1.5
                review['quality_assessment']['content_length'] = '충분한 분량'
            else:
                review['suggestions'].append('본문 내용을 더 자세히 작성하세요')
                review['quality_assessment']['content_length'] = '분량 부족'
            
            # 태그 검사
            tags = article.get('tags', [])
            if len(tags) >= 3:
                score += 0.5
                review['quality_assessment']['tags'] = '적절한 태그'
            else:
                review['suggestions'].append('관련 태그를 더 추가하세요')
                review['quality_assessment']['tags'] = '태그 부족'
            
            # 구조 검사
            if article.get('lead') and article.get('conclusion'):
                score += 1.0
                review['quality_assessment']['structure'] = '완전한 구조'
            else:
                review['suggestions'].append('리드와 결론을 명확히 구분하세요')
                review['quality_assessment']['structure'] = '구조 개선 필요'
            
            # 최종 점수 (10점 만점)
            review['quality_score'] = min(score, 10.0)
            
            # 전반적 평가
            if review['quality_score'] >= 8.0:
                review['overall_assessment'] = '우수'
            elif review['quality_score'] >= 6.0:
                review['overall_assessment'] = '양호'
            else:
                review['overall_assessment'] = '개선 필요'
            
            self.logger.info(f"✅ 검수 완료: {review['quality_score']:.1f}/10점")
            return review
            
        except Exception as e:
            self.logger.error(f"❌ 기사 검수 실패: {str(e)}")
            return {
                'quality_score': 5.0,
                'quality_assessment': {'error': str(e)},
                'suggestions': ['검수 과정에서 오류가 발생했습니다'],
                'review_time': datetime.now().isoformat()
            }
    
    def generate_simple_ads(self, article: Dict) -> Dict[str, Any]:
        """간단한 광고 추천"""
        try:
            self.logger.info("📢 광고 추천 시작")
            
            # 기사 내용 기반 키워드 추출
            content = article.get('content', '') + ' ' + article.get('title', '')
            tags = article.get('tags', [])
            
            # 광고 템플릿
            ad_templates = [
                {
                    'title': '스마트 투자 플랫폼',
                    'description': 'AI 기반 투자 추천으로 더 스마트한 투자를 시작하세요',
                    'keywords': ['투자', '주식', '포트폴리오'],
                    'category': 'investment_platform'
                },
                {
                    'title': '실시간 시장 분석 도구',
                    'description': '전문가 수준의 시장 분석을 실시간으로 받아보세요',
                    'keywords': ['분석', '시장', '차트'],
                    'category': 'analysis_tool'
                },
                {
                    'title': '경제 뉴스 프리미엄',
                    'description': '빠르고 정확한 경제 뉴스로 투자 기회를 놓치지 마세요',
                    'keywords': ['뉴스', '경제', '정보'],
                    'category': 'news_service'
                },
                {
                    'title': '자동 거래 시스템',
                    'description': '24시간 자동 거래로 수익 기회를 극대화하세요',
                    'keywords': ['거래', '자동', '시스템'],
                    'category': 'trading_system'
                }
            ]
            
            # 관련도 계산 및 광고 선택
            recommendations = []
            
            for ad in ad_templates:
                relevance_score = 0.0
                
                # 키워드 매칭
                for keyword in ad['keywords']:
                    if keyword in content.lower() or keyword in ' '.join(tags).lower():
                        relevance_score += 2.0
                
                # 기본 관련도
                relevance_score += random.uniform(3.0, 7.0)
                
                recommendations.append({
                    'title': ad['title'],
                    'description': ad['description'],
                    'category': ad['category'],
                    'relevance_score': min(relevance_score, 10.0),
                    'click_url': f"https://example.com/{ad['category']}"
                })
            
            # 관련도 순으로 정렬
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            result = {
                'recommendations': recommendations[:3],  # 상위 3개만
                'total_ads': len(recommendations),
                'generated_at': datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ {len(result['recommendations'])}개 광고 추천 완료")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 광고 추천 실패: {str(e)}")
            return {
                'recommendations': [
                    {
                        'title': '투자 정보 서비스',
                        'description': '전문적인 투자 정보를 제공합니다',
                        'category': 'general',
                        'relevance_score': 5.0,
                        'click_url': 'https://example.com'
                    }
                ],
                'total_ads': 1,
                'generated_at': datetime.now().isoformat()
            }

def main():
    """테스트 실행"""
    logging.basicConfig(level=logging.INFO)
    
    generator = SimpleAIArticleGenerator()
    
    # 테스트 이벤트
    test_events = [
        {
            'type': 'price_movement',
            'symbol': 'AAPL',
            'description': 'AAPL 주가 2.5% 상승',
            'severity': 0.7,
            'sentiment': 'positive',
            'change_percent': 2.5
        },
        {
            'type': 'price_movement', 
            'symbol': 'TSLA',
            'description': 'TSLA 주가 1.8% 하락',
            'severity': 0.6,
            'sentiment': 'negative',
            'change_percent': -1.8
        }
    ]
    
    print("=== 실용적인 AI 기사 생성 시스템 테스트 ===")
    
    # 1. 이벤트 분석
    analysis = generator.analyze_events(test_events)
    print(f"\n📊 분석 결과: {analysis['market_sentiment']} 감정")
    
    # 2. 기사 생성
    article = generator.generate_article_with_claude(test_events, analysis)
    print(f"\n📰 기사 제목: {article['title']}")
    print(f"📝 내용 길이: {len(article['content'])}자")
    
    # 3. 차트 생성
    charts = generator.create_simple_charts(test_events, analysis)
    print(f"\n📊 생성된 차트: {len(charts)}개")
    
    # 4. 검수
    review = generator.generate_simple_review(article)
    print(f"\n🔍 품질 점수: {review['quality_score']:.1f}/10")
    
    # 5. 광고 추천
    ads = generator.generate_simple_ads(article)
    print(f"\n📢 추천 광고: {len(ads['recommendations'])}개")
    
    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    main()
