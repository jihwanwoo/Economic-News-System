#!/usr/bin/env python3
"""
기사 작성 에이전트
이벤트와 데이터 분석을 바탕으로 경제 기사 작성
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError


from agents.enhanced_article_writer import create_enhanced_article_prompt

class ArticleWriterAgent:
    """기사 작성 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # AWS Bedrock 클라이언트 초기화
        try:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            )
            self.logger.info("✅ AWS Bedrock 클라이언트 초기화 완료")
        except Exception as e:
            self.logger.error(f"❌ AWS Bedrock 초기화 실패: {e}")
            self.bedrock_client = None
        
        # 기사 템플릿
        self.article_templates = {
            'price_change': {
                'title_template': "{symbol} {direction} {change_percent:.1f}%, {impact_description}",
                'lead_template': "{symbol}이(가) {timestamp}에 {change_percent:+.2f}% {direction}하며 시장의 주목을 받고 있습니다.",
                'focus_areas': ['가격 변동 원인', '시장 반응', '기술적 분석', '향후 전망']
            },
            'volume_spike': {
                'title_template': "{symbol} 거래량 급증, {volume_ratio:.1f}배 증가",
                'lead_template': "{symbol}의 거래량이 평균 대비 {volume_ratio:.1f}배 급증하며 이상 거래 패턴을 보이고 있습니다.",
                'focus_areas': ['거래량 급증 원인', '기관 투자자 동향', '시장 심리', '주가 영향']
            },
            'high_volatility': {
                'title_template': "{symbol} 높은 변동성, {volatility:.1f}% 기록",
                'lead_template': "{symbol}이(가) {volatility:.1f}%의 높은 변동성을 기록하며 불안정한 모습을 보이고 있습니다.",
                'focus_areas': ['변동성 증가 원인', '리스크 요인', '투자자 대응', '안정화 전망']
            }
        }
        
        self.logger.info("✅ 기사 작성 에이전트 초기화 완료")
    
    async def write_article(self, event, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """기사 작성"""
        
        self.logger.info(f"✍️ {event.symbol} 기사 작성 시작")
        
        try:
            # 1. 기사 구조 계획
            article_plan = self._plan_article_structure(event, analysis_data)
            
            # 2. 제목 생성
            title = self._generate_title(event, analysis_data, article_plan)
            
            # 3. 리드 문단 작성
            lead_paragraph = self._generate_lead_paragraph(event, analysis_data)
            
            # 4. 본문 작성
            body_content = await self._generate_body_content(event, analysis_data, article_plan)
            
            # 5. 결론 작성
            conclusion = self._generate_conclusion(event, analysis_data)
            
            # 6. 메타데이터 생성
            metadata = self._generate_metadata(event, analysis_data)
            
            # 기사 패키지 구성
            article = {
                'title': title,
                'lead_paragraph': lead_paragraph,
                'body_content': body_content,
                'conclusion': conclusion,
                'metadata': metadata,
                'content': self._assemble_full_content(title, lead_paragraph, body_content, conclusion),
                'word_count': len(body_content.split()) + len(lead_paragraph.split()) + len(conclusion.split()),
                'created_at': datetime.now().isoformat(),
                'author': 'AI 경제 뉴스 시스템',
                'tags': self._generate_tags(event, analysis_data)
            }
            
            self.logger.info(f"✅ {event.symbol} 기사 작성 완료 ({article['word_count']}단어)")
            return article
            
        except Exception as e:
            self.logger.error(f"❌ 기사 작성 실패: {e}")
            return {
                'error': str(e),
                'symbol': event.symbol,
                'created_at': datetime.now().isoformat()
            }
    
    def _plan_article_structure(self, event, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """기사 구조 계획"""
        
        template = self.article_templates.get(event.event_type, self.article_templates['price_change'])
        
        # 분석 데이터 기반 중요도 결정
        technical_indicators = analysis_data.get('technical_indicators', {})
        market_comparison = analysis_data.get('market_comparison', {})
        forecast = analysis_data.get('forecast', {})
        
        plan = {
            'article_type': event.event_type,
            'focus_areas': template['focus_areas'],
            'key_data_points': {
                'current_price': analysis_data.get('raw_data', {}).get('current_price'),
                'change_percent': event.change_percent,
                'volume_info': analysis_data.get('statistics', {}).get('volume_ratio'),
                'technical_signals': technical_indicators,
                'market_context': market_comparison,
                'outlook': forecast.get('outlook')
            },
            'tone': self._determine_article_tone(event, analysis_data),
            'target_length': 'medium',  # short, medium, long
            'include_charts': True,
            'include_technical_analysis': True
        }
        
        return plan
    
    def _generate_title(self, event, analysis_data: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """제목 생성"""
        
        try:
            template = self.article_templates.get(event.event_type, self.article_templates['price_change'])
            
            # 방향 결정
            direction = "급등" if event.change_percent > 0 else "급락"
            
            # 영향 설명
            abs_change = abs(event.change_percent)
            if abs_change > 10:
                impact_description = "시장 충격"
            elif abs_change > 5:
                impact_description = "큰 폭 변동"
            elif abs_change > 2:
                impact_description = "주목받는 움직임"
            else:
                impact_description = "변동 관찰"
            
            # 템플릿 적용
            if event.event_type == 'price_change':
                title = template['title_template'].format(
                    symbol=event.symbol,
                    direction=direction,
                    change_percent=abs(event.change_percent),
                    impact_description=impact_description
                )
            elif event.event_type == 'volume_spike':
                volume_ratio = analysis_data.get('statistics', {}).get('volume_ratio', 1)
                title = template['title_template'].format(
                    symbol=event.symbol,
                    volume_ratio=volume_ratio
                )
            elif event.event_type == 'high_volatility':
                volatility = analysis_data.get('statistics', {}).get('volatility_annualized', 0)
                title = template['title_template'].format(
                    symbol=event.symbol,
                    volatility=volatility
                )
            else:
                title = f"{event.symbol} {event.title}"
            
            return title
            
        except Exception as e:
            self.logger.error(f"제목 생성 실패: {e}")
            return f"{event.symbol} 시장 동향 분석"
    
    def _generate_lead_paragraph(self, event, analysis_data: Dict[str, Any]) -> str:
        """리드 문단 생성"""
        
        try:
            template = self.article_templates.get(event.event_type, self.article_templates['price_change'])
            
            # 기본 정보
            current_price = analysis_data.get('raw_data', {}).get('current_price', 0)
            timestamp = event.timestamp.strftime("%Y년 %m월 %d일")
            
            # 방향 및 설명
            direction = "상승" if event.change_percent > 0 else "하락"
            
            # 템플릿 기반 리드 생성
            if event.event_type == 'price_change':
                lead = template['lead_template'].format(
                    symbol=event.symbol,
                    timestamp=timestamp,
                    change_percent=event.change_percent,
                    direction=direction
                )
                
                # 추가 컨텍스트
                if current_price > 0:
                    lead += f" 현재 주가는 {current_price:.2f}달러를 기록하고 있습니다."
                
            elif event.event_type == 'volume_spike':
                volume_ratio = analysis_data.get('statistics', {}).get('volume_ratio', 1)
                lead = template['lead_template'].format(
                    symbol=event.symbol,
                    volume_ratio=volume_ratio
                )
                
            elif event.event_type == 'high_volatility':
                volatility = analysis_data.get('statistics', {}).get('volatility_annualized', 0)
                lead = template['lead_template'].format(
                    symbol=event.symbol,
                    volatility=volatility
                )
            else:
                lead = f"{event.symbol}에서 {event.description}"
            
            return lead
            
        except Exception as e:
            self.logger.error(f"리드 문단 생성 실패: {e}")
            return f"{event.symbol}에서 주목할 만한 움직임이 관찰되고 있습니다."
    
    async def _generate_body_content(self, event, analysis_data: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """본문 내용 생성"""
        
        try:
            if not self.bedrock_client:
                return self._generate_body_content_fallback(event, analysis_data, plan)
            
            # AWS Bedrock을 사용한 본문 생성
            prompt = self._create_article_prompt(event, analysis_data, plan)
            
            # Claude 모델 호출
            response = self.bedrock_client.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 3500,  # 더 긴 기사를 위해 토큰 수 증가
                    'temperature': 0.7,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                })
            )
            
            # 응답 파싱
            response_body = json.loads(response['body'].read())
            body_content = response_body['content'][0]['text']
            
            return body_content
            
        except Exception as e:
            self.logger.error(f"AWS Bedrock 본문 생성 실패: {e}")
            return self._generate_body_content_fallback(event, analysis_data, plan)
    
    def _generate_body_content_fallback(self, event, analysis_data: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """본문 내용 생성 (백업 방식)"""
        
        sections = []
        
        # 1. 현재 상황 분석
        sections.append("## 현재 상황 분석")
        
        raw_data = analysis_data.get('raw_data', {})
        current_price = raw_data.get('current_price', 0)
        
        if current_price > 0:
            sections.append(f"{event.symbol}의 현재 주가는 {current_price:.2f}달러로, "
                          f"전일 대비 {event.change_percent:+.2f}%의 변화를 보이고 있습니다.")
        
        # 2. 기술적 분석
        technical_indicators = analysis_data.get('technical_indicators', {})
        if technical_indicators:
            sections.append("## 기술적 분석")
            
            rsi = technical_indicators.get('rsi')
            if rsi:
                if rsi > 70:
                    sections.append(f"RSI 지표는 {rsi:.1f}로 과매수 구간에 진입했습니다.")
                elif rsi < 30:
                    sections.append(f"RSI 지표는 {rsi:.1f}로 과매도 구간에 있습니다.")
                else:
                    sections.append(f"RSI 지표는 {rsi:.1f}로 중립 구간을 유지하고 있습니다.")
            
            sma_20 = technical_indicators.get('sma_20')
            if sma_20 and current_price > 0:
                if current_price > sma_20:
                    sections.append(f"주가는 20일 이동평균선({sma_20:.2f}달러) 위에서 거래되고 있어 단기 상승 추세를 보이고 있습니다.")
                else:
                    sections.append(f"주가는 20일 이동평균선({sma_20:.2f}달러) 아래에서 거래되고 있어 단기 하락 추세에 있습니다.")
        
        # 3. 시장 비교
        market_comparison = analysis_data.get('market_comparison', {})
        if market_comparison:
            sections.append("## 시장 대비 성과")
            
            beta = market_comparison.get('beta', 1)
            correlation = market_comparison.get('correlation_with_spy', 0)
            relative_performance = market_comparison.get('relative_performance_1m', 0)
            
            sections.append(f"{event.symbol}의 베타는 {beta:.2f}로, "
                          f"시장 대비 {'높은' if beta > 1 else '낮은'} 변동성을 보입니다.")
            
            if relative_performance != 0:
                performance_desc = "우수한" if relative_performance > 0 else "부진한"
                sections.append(f"최근 1개월간 S&P 500 대비 {relative_performance:+.1f}%의 {performance_desc} 성과를 기록했습니다.")
        
        # 4. 향후 전망
        forecast = analysis_data.get('forecast', {})
        if forecast:
            sections.append("## 향후 전망")
            
            outlook = forecast.get('outlook', '중립')
            confidence = forecast.get('confidence_level', 50)
            
            sections.append(f"기술적 분석을 바탕으로 한 단기 전망은 '{outlook}'이며, "
                          f"신뢰도는 {confidence:.0f}%입니다.")
            
            key_levels = forecast.get('key_levels', {})
            support = key_levels.get('support')
            resistance = key_levels.get('resistance')
            
            if support and resistance:
                sections.append(f"주요 지지선은 {support:.2f}달러, 저항선은 {resistance:.2f}달러로 예상됩니다.")
        
        return "\n\n".join(sections)
    
    def _create_article_prompt(self, event, analysis_data: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """기사 작성용 프롬프트 생성 (확장된 버전)"""
        
        prompt = f"""
다음 정보를 바탕으로 상세하고 전문적인 경제 기사의 본문을 작성해주세요:

**이벤트 정보:**
- 심볼: {event.symbol}
- 이벤트 유형: {event.event_type}
- 변화율: {event.change_percent:+.2f}%
- 심각도: {event.severity.value}
- 설명: {event.description}

**분석 데이터:**
- 현재 가격: {analysis_data.get('raw_data', {}).get('current_price', 'N/A')}
- 기술적 지표: {json.dumps(analysis_data.get('technical_indicators', {}), indent=2)}
- 통계 정보: {json.dumps(analysis_data.get('statistics', {}), indent=2)}
- 시장 비교: {json.dumps(analysis_data.get('market_comparison', {}), indent=2)}
- 전망: {json.dumps(analysis_data.get('forecast', {}), indent=2)}

**작성 요구사항:**
1. 전문적이고 객관적인 톤으로 작성
2. 데이터와 분석 결과를 근거로 제시
3. 투자자들에게 유용한 인사이트 제공
4. **1200-1500단어 분량의 상세한 기사** (기존 대비 2배 확장)
5. 다음 섹션들을 상세히 포함:

   **## 시장 상황 분석** (300-400단어)
   - 현재 시장 환경과 배경 상황
   - 해당 종목의 최근 동향 및 주요 변화 요인
   - 거래량 분석 및 투자자 심리
   - 업계 전반의 동향과 영향

   **## 기술적 분석** (300-400단어)
   - RSI, MACD, 이동평균 등 주요 기술적 지표 상세 해석
   - 차트 패턴 분석 및 의미
   - 지지선과 저항선 분석
   - 모멘텀 지표 및 추세 분석

   **## 시장 비교 및 상관관계 분석** (200-300단어)
   - S&P 500 대비 베타 및 상관관계 분석
   - 동종 업계 대비 상대적 성과
   - 시장 지수와의 연동성 분석
   - 섹터별 비교 분석

   **## 펀더멘털 요인 및 배경** (200-300단어)
   - 경제적 배경 및 거시경제 영향 요인
   - 기업 실적 및 재무 상황 (해당되는 경우)
   - 정책적 영향 및 규제 환경
   - 글로벌 시장 동향의 영향

   **## 향후 전망 및 투자 전략** (200-300단어)
   - 단기 및 중기 전망
   - 주요 리스크 요인 및 기회 요소
   - 투자자별 관점 (기관/개인)
   - 주의 깊게 관찰해야 할 지표들

각 섹션은 구체적인 수치와 데이터를 인용하여 신뢰성을 높이고, 
경제 전문지 수준의 깊이 있는 분석을 제공해주세요.
문체는 전문적이면서도 일반 투자자가 이해할 수 있도록 작성해주세요.
"""
        
        return prompt

기사 본문만 작성해주세요 (제목과 리드는 제외):
"""
        
        return prompt
    
    def _generate_conclusion(self, event, analysis_data: Dict[str, Any]) -> str:
        """결론 생성"""
        
        try:
            forecast = analysis_data.get('forecast', {})
            outlook = forecast.get('outlook', '중립')
            
            # 투자자 관점에서의 결론
            if event.change_percent > 5:
                conclusion = f"{event.symbol}의 급등은 투자자들의 관심을 끌고 있으며, "
            elif event.change_percent < -5:
                conclusion = f"{event.symbol}의 급락은 주의 깊은 관찰이 필요한 상황이며, "
            else:
                conclusion = f"{event.symbol}의 현재 움직임은 "
            
            conclusion += f"기술적 분석 결과 '{outlook}' 전망을 보이고 있습니다. "
            
            # 리스크 경고
            conclusion += "투자자들은 충분한 분석과 리스크 관리를 통해 신중한 투자 결정을 내리시기 바랍니다."
            
            return conclusion
            
        except Exception as e:
            self.logger.error(f"결론 생성 실패: {e}")
            return "투자자들은 시장 상황을 지속적으로 모니터링하며 신중한 투자 결정을 내리시기 바랍니다."
    
    def _generate_metadata(self, event, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """메타데이터 생성"""
        
        return {
            'symbol': event.symbol,
            'event_type': event.event_type,
            'severity': event.severity.value,
            'change_percent': event.change_percent,
            'analysis_timestamp': analysis_data.get('analysis_timestamp'),
            'data_quality': analysis_data.get('data_quality', {}),
            'sources': ['Yahoo Finance', 'Technical Analysis', 'Market Data'],
            'disclaimer': '본 기사는 AI 시스템에 의해 자동 생성되었으며, 투자 조언이 아닙니다.'
        }
    
    def _generate_tags(self, event, analysis_data: Dict[str, Any]) -> List[str]:
        """태그 생성"""
        
        tags = [event.symbol, event.event_type]
        
        # 심각도 기반 태그
        if event.severity.value in ['high', 'critical']:
            tags.append('긴급')
        
        # 변화율 기반 태그
        abs_change = abs(event.change_percent)
        if abs_change > 10:
            tags.append('급변동')
        elif abs_change > 5:
            tags.append('큰폭변동')
        
        # 기술적 분석 기반 태그
        technical_indicators = analysis_data.get('technical_indicators', {})
        rsi = technical_indicators.get('rsi')
        if rsi:
            if rsi > 70:
                tags.append('과매수')
            elif rsi < 30:
                tags.append('과매도')
        
        # 전망 기반 태그
        forecast = analysis_data.get('forecast', {})
        outlook = forecast.get('outlook')
        if outlook:
            tags.append(outlook)
        
        return tags
    
    def _determine_article_tone(self, event, analysis_data: Dict[str, Any]) -> str:
        """기사 톤 결정"""
        
        if event.severity.value == 'critical':
            return 'urgent'
        elif event.severity.value == 'high':
            return 'serious'
        elif abs(event.change_percent) > 5:
            return 'analytical'
        else:
            return 'neutral'
    
    def _assemble_full_content(self, title: str, lead: str, body: str, conclusion: str) -> str:
        """전체 기사 내용 조합"""
        
        full_content = f"""# {title}

{lead}

{body}

## 결론

{conclusion}

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
"""
        
        return full_content
