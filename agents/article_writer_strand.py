"""
기사 작성 Strand Agent
이벤트와 데이터 분석을 바탕으로 경제 기사 작성
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from .strands_framework import BaseStrandAgent, StrandContext, StrandMessage, MessageType

class ArticleWriterStrand(BaseStrandAgent):
    """기사 작성 Strand Agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="article_writer",
            name="기사 작성 에이전트"
        )
        
        self.capabilities = [
            "economic_article_writing",
            "market_analysis_writing",
            "technical_analysis_writing",
            "news_summarization",
            "content_structuring"
        ]
        
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
                'lead_template': "{symbol}이(가) {volatility:.1f}%의 높은 변동성을 보이며 투자자들의 관심이 집중되고 있습니다.",
                'focus_areas': ['변동성 원인', '시장 불안 요인', '투자 전략', '리스크 관리']
            }
        }
    
    def get_capabilities(self) -> List[str]:
        """에이전트 능력 반환"""
        return self.capabilities
    
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """기사 작성 처리"""
        
        # 필요한 데이터 수집
        event_data = context.input_data.get('event')
        data_analysis = await self.get_shared_data(context, 'data_analysis')
        
        if not event_data:
            raise Exception("이벤트 데이터가 없습니다")
        
        symbol = event_data.get('symbol')
        self.logger.info(f"✍️ {symbol} 기사 작성 시작")
        
        try:
            # 1. 기사 구조 생성
            article_structure = await self._create_article_structure(event_data, data_analysis)
            
            # 2. 기사 내용 생성
            article_content = await self._generate_article_content(article_structure, event_data, data_analysis)
            
            # 3. 기사 메타데이터 생성
            article_metadata = await self._create_article_metadata(event_data, article_content)
            
            # 4. 최종 기사 패키지 생성
            article_package = {
                'title': article_content['title'],
                'lead': article_content['lead'],
                'body': article_content['body'],
                'conclusion': article_content['conclusion'],
                'metadata': article_metadata,
                'word_count': len(article_content['body'].split()),
                'created_at': datetime.now().isoformat(),
                'symbol': symbol,
                'event_type': event_data.get('event_type')
            }
            
            # 공유 메모리에 저장
            await self.set_shared_data(context, 'article', article_package)
            
            self.logger.info(f"✅ {symbol} 기사 작성 완료 ({article_package['word_count']}단어)")
            return article_package
            
        except Exception as e:
            self.logger.error(f"❌ 기사 작성 실패: {e}")
            raise
    
    async def _create_article_structure(self, event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """기사 구조 생성"""
        
        event_type = event_data.get('event_type', 'unknown')
        symbol = event_data.get('symbol', 'Unknown')
        
        # 템플릿 선택
        template = self.article_templates.get(event_type, self.article_templates['price_change'])
        
        # 기본 구조
        structure = {
            'event_type': event_type,
            'symbol': symbol,
            'template': template,
            'sections': [
                'title',
                'lead',
                'event_description',
                'data_analysis',
                'technical_analysis',
                'market_impact',
                'conclusion'
            ]
        }
        
        # 데이터 분석이 있으면 추가 섹션 포함
        if data_analysis:
            structure['sections'].extend(['chart_analysis', 'statistical_insights'])
        
        return structure
    
    async def _generate_article_content(self, structure: Dict[str, Any], event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """기사 내용 생성"""
        
        symbol = event_data.get('symbol', 'Unknown')
        event_type = event_data.get('event_type', 'unknown')
        
        # 시스템 프롬프트
        system_prompt = self._create_system_prompt()
        
        # 사용자 프롬프트 생성
        user_prompt = await self._create_user_prompt(structure, event_data, data_analysis)
        
        # LLM 호출
        if self.llm:
            try:
                article_text = await self.call_llm(system_prompt, user_prompt)
                
                # 기사 파싱
                parsed_article = await self._parse_article_response(article_text)
                return parsed_article
                
            except Exception as e:
                self.logger.error(f"LLM 호출 실패: {e}")
                # 폴백: 템플릿 기반 기사 생성
                return await self._generate_template_article(structure, event_data, data_analysis)
        else:
            # LLM이 없으면 템플릿 기반 생성
            return await self._generate_template_article(structure, event_data, data_analysis)
    
    def _create_system_prompt(self) -> str:
        """시스템 프롬프트 생성"""
        return """당신은 전문 경제 기자입니다. 주어진 경제 이벤트와 데이터 분석을 바탕으로 정확하고 객관적인 경제 기사를 작성해주세요.

기사 작성 가이드라인:
1. 객관적이고 정확한 정보 전달
2. 전문적이면서도 이해하기 쉬운 문체
3. 데이터와 분석에 기반한 내용
4. 투자 조언은 피하고 정보 제공에 집중
5. 한국어로 작성
6. 최소 2000자 이상의 상세한 기사 작성
7. 배경 설명, 시장 분석, 전문가 의견, 향후 전망 등을 포함

기사 구조:
- 제목: 간결하고 핵심을 담은 제목
- 리드: 핵심 내용을 요약한 첫 문단 (100-150자)
- 본문: 상세한 분석과 설명 (1500자 이상)
  * 이벤트 배경 및 원인 분석
  * 시장 데이터 및 기술적 분석
  * 업계 동향 및 영향 분석
  * 관련 기업 및 섹터 영향
  * 투자자 반응 및 시장 심리
  * 전문가 분석 및 의견
- 결론: 요약 및 시사점 (200-300자)

응답 형식:
TITLE: [제목]
LEAD: [리드 문단]
BODY: [본문 - 최소 1500자]
CONCLUSION: [결론]
IMAGE_PROMPT: [기사 내용을 바탕으로 한 이미지 생성 프롬프트 - 영어로 작성]"""
    
    async def _create_user_prompt(self, structure: Dict[str, Any], event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> str:
        """사용자 프롬프트 생성"""
        
        symbol = event_data.get('symbol', 'Unknown')
        event_type = event_data.get('event_type', 'unknown')
        description = event_data.get('description', '')
        severity = event_data.get('severity', 'low')
        
        prompt = f"""다음 경제 이벤트에 대한 기사를 작성해주세요:

=== 이벤트 정보 ===
심볼: {symbol}
이벤트 유형: {event_type}
설명: {description}
심각도: {severity}
발생시간: {event_data.get('timestamp', 'Unknown')}
"""
        
        # 추가 이벤트 데이터
        if 'change_percent' in event_data:
            prompt += f"변화율: {event_data['change_percent']:.2f}%\n"
        
        # 데이터 분석 정보 추가
        if data_analysis:
            prompt += "\n=== 데이터 분석 결과 ===\n"
            
            # 기본 데이터
            raw_data = data_analysis.get('raw_data', {})
            if raw_data:
                prompt += f"현재가: {raw_data.get('current_price', 'N/A')}\n"
                prompt += f"거래량: {raw_data.get('volume', 'N/A')}\n"
            
            # 기술적 지표
            technical = data_analysis.get('technical_indicators', {})
            if technical:
                prompt += "\n기술적 지표:\n"
                if technical.get('rsi'):
                    prompt += f"- RSI: {technical['rsi']:.1f}\n"
                if technical.get('sma_20'):
                    prompt += f"- 20일 이동평균: {technical['sma_20']:.2f}\n"
                if technical.get('macd'):
                    prompt += f"- MACD: {technical['macd']:.2f}\n"
            
            # 통계 정보
            stats = data_analysis.get('statistics', {})
            if stats:
                prompt += "\n통계 정보:\n"
                if stats.get('volatility_annualized'):
                    prompt += f"- 연율 변동성: {stats['volatility_annualized']:.1f}%\n"
                if stats.get('volume_ratio'):
                    prompt += f"- 거래량 비율: {stats['volume_ratio']:.1f}배\n"
            
            # 시장 비교
            market_comp = data_analysis.get('market_comparison', {})
            if market_comp:
                prompt += "\n시장 비교:\n"
                if market_comp.get('beta'):
                    prompt += f"- 베타: {market_comp['beta']:.2f}\n"
                if market_comp.get('correlation_with_spy'):
                    prompt += f"- SPY 상관관계: {market_comp['correlation_with_spy']:.2f}\n"
        
        prompt += "\n위 정보를 바탕으로 전문적이고 객관적인 경제 기사를 작성해주세요."
        
        return prompt
    
    async def _parse_article_response(self, article_text: str) -> Dict[str, Any]:
        """LLM 응답 파싱"""
        
        try:
            lines = article_text.strip().split('\n')
            
            title = ""
            lead = ""
            body = ""
            conclusion = ""
            image_prompt = ""
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()
                    current_section = 'title'
                elif line.startswith('LEAD:'):
                    lead = line.replace('LEAD:', '').strip()
                    current_section = 'lead'
                elif line.startswith('BODY:'):
                    body = line.replace('BODY:', '').strip()
                    current_section = 'body'
                elif line.startswith('CONCLUSION:'):
                    conclusion = line.replace('CONCLUSION:', '').strip()
                    current_section = 'conclusion'
                elif line.startswith('IMAGE_PROMPT:'):
                    image_prompt = line.replace('IMAGE_PROMPT:', '').strip()
                    current_section = 'image_prompt'
                else:
                    # 현재 섹션에 내용 추가
                    if current_section == 'lead' and lead:
                        lead += " " + line
                    elif current_section == 'body' and body:
                        body += " " + line
                    elif current_section == 'conclusion' and conclusion:
                        conclusion += " " + line
                    elif current_section == 'image_prompt' and image_prompt:
                        image_prompt += " " + line
            
            return {
                'title': title or "경제 뉴스",
                'lead': lead or "경제 이벤트가 발생했습니다.",
                'body': body or "상세한 분석이 진행 중입니다.",
                'conclusion': conclusion or "지속적인 모니터링이 필요합니다.",
                'image_prompt': image_prompt or "economic news, financial market, stock chart"
            }
            
        except Exception as e:
            self.logger.error(f"기사 파싱 실패: {e}")
            return await self._generate_fallback_article()
    
    async def _generate_template_article(self, structure: Dict[str, Any], event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """템플릿 기반 기사 생성"""
        
        symbol = event_data.get('symbol', 'Unknown')
        event_type = event_data.get('event_type', 'unknown')
        template = structure.get('template', self.article_templates['price_change'])
        
        # 기본 변수들
        variables = {
            'symbol': symbol,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'direction': '상승' if event_data.get('change_percent', 0) > 0 else '하락',
            'change_percent': abs(event_data.get('change_percent', 0)),
            'impact_description': '시장 관심 집중',
            'volume_ratio': 1.0,
            'volatility': 10.0
        }
        
        # 데이터 분석에서 추가 변수 추출
        if data_analysis:
            stats = data_analysis.get('statistics', {})
            if stats.get('volume_ratio'):
                variables['volume_ratio'] = stats['volume_ratio']
            if stats.get('volatility_annualized'):
                variables['volatility'] = stats['volatility_annualized'] * 100
        
        # 제목 생성
        try:
            title = template['title_template'].format(**variables)
        except:
            title = f"{symbol} 시장 동향"
        
        # 리드 생성
        try:
            lead = template['lead_template'].format(**variables)
        except:
            lead = f"{symbol}에 대한 시장 관심이 높아지고 있습니다."
        
        # 본문 생성
        body = await self._generate_template_body(event_data, data_analysis, template)
        
        # 결론 생성
        conclusion = await self._generate_template_conclusion(event_data, data_analysis)
        
        return {
            'title': title,
            'lead': lead,
            'body': body,
            'conclusion': conclusion
        }
    
    async def _generate_template_body(self, event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]], template: Dict[str, Any]) -> str:
        """템플릿 기반 본문 생성 (2000자 이상)"""
        
        symbol = event_data.get('symbol', 'Unknown')
        body_parts = []
        
        # 1. 이벤트 개요 및 배경
        body_parts.append("## 📊 이벤트 개요")
        if event_data.get('description'):
            body_parts.append(f"{event_data['description']} 이번 움직임은 시장 참여자들의 주목을 받고 있으며, 다양한 요인들이 복합적으로 작용한 결과로 분석됩니다.")
        
        # 2. 현재 시장 상황 분석
        body_parts.append("\n## 💹 현재 시장 상황")
        if data_analysis:
            raw_data = data_analysis.get('raw_data', {})
            if raw_data.get('current_price'):
                body_parts.append(f"{symbol}의 현재 가격은 {raw_data['current_price']:.2f}달러로 거래되고 있습니다. 이는 시장 개장 이후 지속적인 관심을 받고 있는 수준입니다.")
            
            if raw_data.get('volume'):
                body_parts.append(f"오늘 거래량은 {raw_data['volume']:,}주를 기록하고 있어, 평소보다 활발한 거래가 이루어지고 있음을 보여줍니다.")
        
        # 3. 기술적 분석 상세
        body_parts.append("\n## 📈 기술적 분석")
        if data_analysis:
            technical = data_analysis.get('technical_indicators', {})
            if technical:
                body_parts.append("주요 기술적 지표들을 종합적으로 분석한 결과는 다음과 같습니다.")
                
                if technical.get('rsi'):
                    rsi = technical['rsi']
                    if rsi > 70:
                        body_parts.append(f"RSI 지표는 {rsi:.1f}로 과매수 구간에 진입했습니다. 이는 단기적으로 조정 압력이 있을 수 있음을 시사하며, 투자자들은 신중한 접근이 필요한 시점입니다.")
                    elif rsi < 30:
                        body_parts.append(f"RSI 지표는 {rsi:.1f}로 과매도 구간에 있습니다. 이는 기술적 반등 가능성을 제시하고 있어, 저점 매수 기회로 해석될 수 있습니다.")
                    else:
                        body_parts.append(f"RSI 지표는 {rsi:.1f}로 중립 구간에 위치하고 있어, 현재 기술적으로 균형 잡힌 상태를 보이고 있습니다.")
                
                if technical.get('sma_20'):
                    current_price = technical.get('current_price', 0)
                    sma_20 = technical['sma_20']
                    if current_price > sma_20:
                        body_parts.append(f"20일 이동평균선({sma_20:.2f}달러)을 상회하며 거래되고 있어 단기 상승 추세가 유지되고 있습니다. 이는 투자자들의 긍정적인 심리를 반영하는 신호로 해석됩니다.")
                    else:
                        body_parts.append(f"20일 이동평균선({sma_20:.2f}달러)을 하회하고 있어 단기적으로 약세 흐름을 보이고 있습니다. 추가적인 하락 압력에 대한 주의가 필요한 상황입니다.")
                
                if technical.get('macd') and technical.get('macd_signal'):
                    macd = technical['macd']
                    macd_signal = technical['macd_signal']
                    if macd > macd_signal:
                        body_parts.append(f"MACD 지표에서는 본선({macd:.2f})이 신호선({macd_signal:.2f})을 상향 돌파하며 매수 신호를 보이고 있습니다.")
                    else:
                        body_parts.append(f"MACD 지표에서는 본선({macd:.2f})이 신호선({macd_signal:.2f}) 아래에 위치하며 약세 신호를 나타내고 있습니다.")
        
        # 4. 시장 비교 및 상대적 성과
        body_parts.append("\n## 🔄 시장 비교 분석")
        if data_analysis:
            market_comp = data_analysis.get('market_comparison', {})
            if market_comp:
                body_parts.append("주요 시장 지수와의 비교 분석을 통해 상대적 성과를 살펴보겠습니다.")
                
                if market_comp.get('beta'):
                    beta = market_comp['beta']
                    if beta > 1:
                        body_parts.append(f"베타 계수는 {beta:.2f}로 시장 대비 높은 변동성을 보이고 있습니다. 이는 시장 상승 시 더 큰 상승폭을, 하락 시 더 큰 하락폭을 보일 가능성이 높음을 의미합니다.")
                    elif beta < 1:
                        body_parts.append(f"베타 계수는 {beta:.2f}로 시장 대비 안정적인 움직임을 보이고 있습니다. 이는 상대적으로 보수적인 투자 성향의 투자자들에게 적합할 수 있습니다.")
                
                if market_comp.get('correlation_with_spy'):
                    correlation = market_comp['correlation_with_spy']
                    if abs(correlation) > 0.7:
                        body_parts.append(f"S&P 500 지수와의 상관관계는 {correlation:.2f}로 {'높은 양의 상관관계' if correlation > 0 else '높은 음의 상관관계'}를 보이고 있습니다.")
                    else:
                        body_parts.append(f"S&P 500 지수와의 상관관계는 {correlation:.2f}로 상대적으로 독립적인 움직임을 보이고 있어 포트폴리오 다변화 효과를 기대할 수 있습니다.")
        
        # 5. 통계적 분석 및 변동성
        body_parts.append("\n## 📊 통계적 분석")
        if data_analysis:
            stats = data_analysis.get('statistics', {})
            if stats:
                if stats.get('volatility_annualized'):
                    vol = stats['volatility_annualized'] * 100
                    if vol > 30:
                        body_parts.append(f"연율 변동성은 {vol:.1f}%로 높은 수준을 기록하고 있습니다. 이는 단기적으로 큰 가격 변동 가능성을 시사하며, 리스크 관리에 각별한 주의가 필요합니다.")
                    elif vol > 20:
                        body_parts.append(f"연율 변동성은 {vol:.1f}%로 보통 수준을 보이고 있습니다. 이는 적정한 수준의 리스크와 수익 기회를 제공하는 것으로 평가됩니다.")
                    else:
                        body_parts.append(f"연율 변동성은 {vol:.1f}%로 낮은 수준을 유지하고 있어 상대적으로 안정적인 투자 환경을 제공하고 있습니다.")
                
                if stats.get('volume_ratio') and stats['volume_ratio'] > 1.5:
                    volume_ratio = stats['volume_ratio']
                    body_parts.append(f"거래량이 평균 대비 {volume_ratio:.1f}배 증가한 것은 기관투자자들의 관심 증가와 개인투자자들의 적극적인 참여를 동시에 보여주는 신호입니다. 이러한 거래량 증가는 향후 주가 방향성에 대한 중요한 단서를 제공합니다.")
        
        # 6. 업계 동향 및 영향 요인
        body_parts.append("\n## 🏢 업계 동향 및 영향 요인")
        body_parts.append(f"{symbol}이 속한 업계는 현재 다양한 내외부 요인들의 영향을 받고 있습니다. 거시경제 환경의 변화, 업계 특성, 그리고 개별 기업의 펀더멘털 요소들이 복합적으로 작용하고 있는 상황입니다.")
        
        # 7. 투자자 심리 및 시장 반응
        body_parts.append("\n## 💭 투자자 심리 및 시장 반응")
        body_parts.append("현재 시장 참여자들의 반응을 종합해보면, 단기적인 관망세와 함께 중장기적인 관점에서의 투자 기회를 모색하는 움직임이 동시에 나타나고 있습니다. 기관투자자들은 펀더멘털 분석에 기반한 신중한 접근을 보이고 있으며, 개인투자자들은 기술적 분석과 시장 모멘텀에 더 민감하게 반응하고 있는 것으로 관찰됩니다.")
        
        # 8. 리스크 요인 및 주의사항
        body_parts.append("\n## ⚠️ 리스크 요인 및 주의사항")
        body_parts.append("투자 시 고려해야 할 주요 리스크 요인들로는 거시경제 불확실성, 업계 내 경쟁 심화, 규제 환경 변화, 그리고 글로벌 경제 동향 등이 있습니다. 특히 현재와 같은 변동성이 높은 시장 환경에서는 포지션 사이징과 리스크 관리가 더욱 중요합니다.")
        
        return "\n".join(body_parts)
    
    async def _generate_template_conclusion(self, event_data: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> str:
        """템플릿 기반 결론 생성"""
        
        symbol = event_data.get('symbol', 'Unknown')
        event_type = event_data.get('event_type', 'unknown')
        
        conclusions = []
        
        # 이벤트 유형별 결론
        if event_type == 'volume_spike':
            conclusions.append(f"{symbol}의 거래량 급증은 시장 참여자들의 관심 증가를 의미합니다.")
        elif event_type == 'price_change':
            change = event_data.get('change_percent', 0)
            if abs(change) > 5:
                conclusions.append(f"{symbol}의 {'급등' if change > 0 else '급락'}은 투자자들의 주목을 받고 있습니다.")
        elif event_type == 'high_volatility':
            conclusions.append(f"{symbol}의 높은 변동성은 시장 불확실성을 반영하고 있습니다.")
        
        # 일반적인 결론
        conclusions.append("투자자들은 충분한 분석과 리스크 관리를 통해 신중한 투자 결정을 내리시기 바랍니다.")
        
        return " ".join(conclusions)
    
    async def _generate_fallback_article(self) -> Dict[str, Any]:
        """폴백 기사 생성 (2000자 이상)"""
        
        body = """## 📊 시장 개요

경제 시장에서 주목할 만한 움직임이 관찰되고 있습니다. 최근 시장 참여자들은 다양한 경제 지표와 기업 실적, 그리고 거시경제 환경 변화에 민감하게 반응하고 있는 상황입니다.

## 💹 현재 시장 상황

글로벌 금융시장은 여러 복합적인 요인들의 영향을 받으며 변동성을 보이고 있습니다. 주요 중앙은행들의 통화정책 방향성, 인플레이션 동향, 그리고 지정학적 리스크 등이 시장 심리에 영향을 미치고 있는 것으로 분석됩니다.

투자자들은 단기적인 시장 노이즈보다는 중장기적인 펀더멘털 요소들에 더욱 주목하고 있으며, 이는 건전한 투자 환경 조성에 긍정적인 신호로 해석됩니다.

## 📈 기술적 분석

주요 기술적 지표들을 종합적으로 분석한 결과, 현재 시장은 방향성을 모색하는 단계에 있는 것으로 판단됩니다. 이동평균선들의 배열과 모멘텀 지표들의 움직임을 통해 향후 시장 방향성에 대한 단서를 찾을 수 있습니다.

특히 거래량 패턴의 변화는 시장 참여자들의 심리 변화를 반영하는 중요한 지표로 작용하고 있으며, 이를 통해 향후 시장 흐름을 예측하는 데 도움이 될 것으로 예상됩니다.

## 🔄 시장 비교 분석

국내외 주요 시장 지수들과의 비교 분석을 통해 상대적 성과를 평가해보면, 각 시장별로 서로 다른 특성과 움직임을 보이고 있습니다. 이는 지역별 경제 상황과 정책 환경의 차이에서 기인하는 것으로 분석됩니다.

## 🏢 업계 동향

각 업종별로 서로 다른 성과를 보이고 있으며, 이는 업종별 특성과 시장 환경 변화에 대한 민감도 차이에서 비롯되는 것으로 보입니다. 특히 기술주와 전통적인 가치주 간의 성과 격차가 주목받고 있습니다.

## 💭 투자자 심리

현재 투자자들은 신중한 접근을 보이고 있으며, 이는 불확실한 시장 환경에서 나타나는 자연스러운 현상으로 해석됩니다. 기관투자자들은 장기적인 관점에서의 투자 기회를 모색하고 있으며, 개인투자자들은 리스크 관리에 더욱 신경을 쓰고 있는 것으로 관찰됩니다.

## ⚠️ 리스크 요인

투자 시 고려해야 할 주요 리스크 요인들로는 거시경제 불확실성, 지정학적 리스크, 통화정책 변화 가능성 등이 있습니다. 이러한 요인들은 시장 변동성을 증가시킬 수 있는 요소들로, 투자자들은 이에 대한 충분한 준비와 대응 방안을 마련해야 합니다.

## 📊 전문가 의견

시장 전문가들은 현재 상황에 대해 신중한 낙관론을 표명하고 있습니다. 단기적으로는 변동성이 지속될 가능성이 있지만, 중장기적으로는 펀더멘털 개선과 함께 안정적인 성장 궤도에 진입할 것으로 전망하고 있습니다.

## 🎯 향후 전망

앞으로의 시장 전망은 여러 변수들에 따라 달라질 수 있지만, 전반적으로는 점진적인 회복세를 보일 것으로 예상됩니다. 다만 이 과정에서 일시적인 조정과 변동성은 불가피할 것으로 보이며, 투자자들은 이에 대한 충분한 준비가 필요합니다."""
        
        return {
            'title': "경제 시장 종합 분석",
            'lead': "경제 시장에서 주목할 만한 움직임이 관찰되고 있으며, 다양한 요인들이 현재 시장 상황에 복합적으로 영향을 미치고 있는 것으로 나타났습니다.",
            'body': body,
            'conclusion': "현재 시장 상황을 종합해보면, 단기적인 불확실성은 존재하지만 중장기적으로는 안정적인 성장 가능성을 보이고 있습니다. 투자자들은 신중한 투자 접근과 체계적인 리스크 관리를 통해 시장 변화에 대응할 필요가 있으며, 전문가들과의 상담을 통한 투자 결정을 권장합니다.",
            'image_prompt': "professional financial market analysis, economic charts, business growth, modern financial illustration"
        }
    
    async def _create_article_metadata(self, event_data: Dict[str, Any], article_content: Dict[str, Any]) -> Dict[str, Any]:
        """기사 메타데이터 생성"""
        
        return {
            'author': 'AI 경제 뉴스 시스템',
            'category': '경제',
            'tags': [
                event_data.get('symbol', 'market'),
                event_data.get('event_type', 'analysis'),
                'economic_news',
                'market_analysis'
            ],
            'language': 'ko',
            'source': 'Economic News AI System',
            'confidence_score': 0.85,
            'reading_time_minutes': max(1, len(article_content.get('body', '').split()) // 200)
        }
