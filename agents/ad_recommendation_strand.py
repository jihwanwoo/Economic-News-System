"""
광고 추천 Strand Agent
기사 내용을 분석하여 관련 광고 3개를 추천
"""

import random
from typing import Dict, List, Any, Optional
from datetime import datetime

from .strands_framework import BaseStrandAgent, StrandContext, StrandMessage, MessageType

class AdRecommendationStrand(BaseStrandAgent):
    """광고 추천 Strand Agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="ad_recommender",
            name="광고 추천 에이전트"
        )
        
        self.capabilities = [
            "contextual_ad_matching",
            "financial_product_recommendation",
            "content_based_targeting",
            "audience_segmentation",
            "ad_performance_optimization"
        ]
        
        # 광고 데이터베이스
        self.ad_database = {
            'investment_platforms': [
                {
                    'id': 'inv_001',
                    'title': '스마트 투자 플랫폼',
                    'description': 'AI 기반 포트폴리오 관리로 안전하고 수익성 높은 투자를 시작하세요.',
                    'cta': '무료 투자 상담 받기',
                    'keywords': ['투자', '포트폴리오', '수익', '자산관리'],
                    'target_events': ['price_change', 'volume_spike'],
                    'risk_level': 'medium'
                },
                {
                    'id': 'inv_002',
                    'title': '로보어드바이저 서비스',
                    'description': '전문가 수준의 자동 투자 관리로 시간과 노력을 절약하세요.',
                    'cta': '1개월 무료 체험',
                    'keywords': ['자동투자', '로보어드바이저', '전문가', '관리'],
                    'target_events': ['high_volatility'],
                    'risk_level': 'low'
                }
            ],
            'trading_tools': [
                {
                    'id': 'tool_001',
                    'title': '실시간 트레이딩 도구',
                    'description': '전문 트레이더들이 사용하는 고급 차트와 분석 도구를 경험하세요.',
                    'cta': '프리미엄 도구 체험',
                    'keywords': ['트레이딩', '차트', '분석', '실시간'],
                    'target_events': ['volume_spike', 'high_volatility'],
                    'risk_level': 'high'
                },
                {
                    'id': 'tool_002',
                    'title': '모바일 트레이딩 앱',
                    'description': '언제 어디서나 빠르고 안전한 모바일 거래를 즐기세요.',
                    'cta': '앱 다운로드',
                    'keywords': ['모바일', '거래', '앱', '편리함'],
                    'target_events': ['price_change'],
                    'risk_level': 'medium'
                }
            ],
            'education_services': [
                {
                    'id': 'edu_001',
                    'title': '투자 교육 아카데미',
                    'description': '기초부터 고급까지, 체계적인 투자 교육으로 전문가가 되세요.',
                    'cta': '무료 강의 수강',
                    'keywords': ['교육', '학습', '기초', '전문가'],
                    'target_events': ['price_change', 'volume_spike', 'high_volatility'],
                    'risk_level': 'low'
                },
                {
                    'id': 'edu_002',
                    'title': '경제 뉴스 구독 서비스',
                    'description': '실시간 경제 분석과 전문가 의견으로 시장을 앞서가세요.',
                    'cta': '프리미엄 구독',
                    'keywords': ['뉴스', '분석', '전문가', '시장정보'],
                    'target_events': ['price_change', 'volume_spike'],
                    'risk_level': 'low'
                }
            ],
            'financial_products': [
                {
                    'id': 'prod_001',
                    'title': '고수익 적금 상품',
                    'description': '안전하면서도 높은 수익률을 제공하는 특별 적금 상품입니다.',
                    'cta': '상품 상세보기',
                    'keywords': ['적금', '안전', '수익률', '저축'],
                    'target_events': ['high_volatility'],
                    'risk_level': 'low'
                },
                {
                    'id': 'prod_002',
                    'title': '투자형 보험',
                    'description': '보장과 투자를 동시에! 안정적인 수익과 보험 혜택을 누리세요.',
                    'cta': '무료 설계 상담',
                    'keywords': ['보험', '투자', '보장', '안정'],
                    'target_events': ['price_change'],
                    'risk_level': 'medium'
                }
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """에이전트 능력 반환"""
        return self.capabilities
    
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """광고 추천 처리"""
        
        # 필요한 데이터 수집
        event_data = context.input_data.get('event')
        article = await self.get_shared_data(context, 'article')
        data_analysis = await self.get_shared_data(context, 'data_analysis')
        
        if not event_data or not article:
            raise Exception("광고 추천에 필요한 데이터가 없습니다")
        
        self.logger.info("📢 광고 추천 시작")
        
        try:
            # 1. 컨텍스트 분석
            context_analysis = await self._analyze_context(event_data, article, data_analysis)
            
            # 2. 타겟 오디언스 분석
            audience_profile = await self._analyze_audience(context_analysis)
            
            # 3. 광고 매칭
            matched_ads = await self._match_advertisements(context_analysis, audience_profile)
            
            # 4. 광고 랭킹 및 선택
            recommended_ads = await self._rank_and_select_ads(matched_ads, context_analysis)
            
            # 5. 광고 개인화
            personalized_ads = await self._personalize_ads(recommended_ads, context_analysis)
            
            result = {
                'recommended_ads': personalized_ads,
                'context_analysis': context_analysis,
                'audience_profile': audience_profile,
                'recommendation_timestamp': datetime.now().isoformat(),
                'total_ads': len(personalized_ads)
            }
            
            # 공유 메모리에 저장
            await self.set_shared_data(context, 'advertisements', result)
            
            self.logger.info(f"✅ 광고 추천 완료: {len(personalized_ads)}개")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 광고 추천 실패: {e}")
            raise
    
    async def _analyze_context(self, event_data: Dict[str, Any], article: Dict[str, Any], data_analysis: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """컨텍스트 분석"""
        
        symbol = event_data.get('symbol', 'Unknown')
        event_type = event_data.get('event_type', 'unknown')
        severity = event_data.get('severity', 'low')
        
        # 기사 내용에서 키워드 추출
        article_text = f"{article.get('title', '')} {article.get('body', '')} {article.get('conclusion', '')}"
        keywords = await self._extract_keywords(article_text)
        
        # 시장 상황 분석
        market_condition = 'neutral'
        risk_sentiment = 'medium'
        
        if data_analysis:
            # 변동성 기반 시장 상황 판단
            stats = data_analysis.get('statistics', {})
            if stats.get('volatility_annualized'):
                volatility = stats['volatility_annualized']
                if volatility > 0.3:  # 30% 이상
                    market_condition = 'volatile'
                    risk_sentiment = 'high'
                elif volatility < 0.15:  # 15% 미만
                    market_condition = 'stable'
                    risk_sentiment = 'low'
            
            # 기술적 지표 기반 추가 분석
            technical = data_analysis.get('technical_indicators', {})
            if technical.get('rsi'):
                rsi = technical['rsi']
                if rsi > 70:
                    market_condition = 'overbought'
                elif rsi < 30:
                    market_condition = 'oversold'
        
        return {
            'symbol': symbol,
            'event_type': event_type,
            'severity': severity,
            'keywords': keywords,
            'market_condition': market_condition,
            'risk_sentiment': risk_sentiment,
            'article_length': len(article.get('body', '').split()),
            'has_technical_analysis': bool(data_analysis and data_analysis.get('technical_indicators'))
        }
    
    async def _extract_keywords(self, text: str) -> List[str]:
        """텍스트에서 키워드 추출"""
        
        # 금융 관련 키워드 사전
        financial_keywords = {
            '투자', '거래', '수익', '손실', '리스크', '위험', '안전', '수익률',
            '포트폴리오', '자산', '주식', '채권', '펀드', '적금', '예금', '보험',
            '분석', '예측', '전망', '추천', '상승', '하락', '변동성', '안정성',
            '트레이딩', '매수', '매도', '차트', '지표', '시장', '경제', '금융'
        }
        
        # 텍스트를 소문자로 변환하고 단어 분리
        words = text.lower().split()
        
        # 금융 키워드만 추출
        extracted_keywords = []
        for word in words:
            for keyword in financial_keywords:
                if keyword in word:
                    extracted_keywords.append(keyword)
        
        # 중복 제거 및 빈도순 정렬
        keyword_counts = {}
        for keyword in extracted_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # 상위 10개 키워드 반환
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, count in sorted_keywords[:10]]
    
    async def _analyze_audience(self, context_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """타겟 오디언스 분석"""
        
        event_type = context_analysis.get('event_type', 'unknown')
        risk_sentiment = context_analysis.get('risk_sentiment', 'medium')
        market_condition = context_analysis.get('market_condition', 'neutral')
        
        # 이벤트 유형별 오디언스 프로파일
        audience_profiles = {
            'price_change': {
                'investor_type': 'active_trader',
                'risk_tolerance': 'medium_to_high',
                'interests': ['trading_tools', 'market_analysis', 'investment_platforms'],
                'experience_level': 'intermediate'
            },
            'volume_spike': {
                'investor_type': 'momentum_trader',
                'risk_tolerance': 'high',
                'interests': ['trading_tools', 'real_time_data', 'technical_analysis'],
                'experience_level': 'advanced'
            },
            'high_volatility': {
                'investor_type': 'risk_averse',
                'risk_tolerance': 'low_to_medium',
                'interests': ['stable_products', 'education', 'risk_management'],
                'experience_level': 'beginner_to_intermediate'
            }
        }
        
        base_profile = audience_profiles.get(event_type, audience_profiles['price_change'])
        
        # 시장 상황에 따른 조정
        if market_condition == 'volatile':
            base_profile['risk_tolerance'] = 'low'
            base_profile['interests'].append('education')
        elif market_condition == 'stable':
            base_profile['risk_tolerance'] = 'medium_to_high'
            base_profile['interests'].append('investment_platforms')
        
        return {
            **base_profile,
            'market_awareness': 'high' if context_analysis.get('has_technical_analysis') else 'medium',
            'engagement_level': 'high' if context_analysis.get('article_length', 0) > 100 else 'medium'
        }
    
    async def _match_advertisements(self, context_analysis: Dict[str, Any], audience_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """광고 매칭"""
        
        event_type = context_analysis.get('event_type', 'unknown')
        keywords = context_analysis.get('keywords', [])
        risk_sentiment = context_analysis.get('risk_sentiment', 'medium')
        
        matched_ads = []
        
        # 모든 광고 카테고리 검토
        for category, ads in self.ad_database.items():
            for ad in ads:
                score = 0
                
                # 이벤트 타입 매칭
                if event_type in ad.get('target_events', []):
                    score += 3
                
                # 키워드 매칭
                ad_keywords = ad.get('keywords', [])
                keyword_matches = len(set(keywords) & set(ad_keywords))
                score += keyword_matches * 2
                
                # 리스크 레벨 매칭
                ad_risk = ad.get('risk_level', 'medium')
                audience_risk = audience_profile.get('risk_tolerance', 'medium')
                
                if self._risk_compatibility(ad_risk, audience_risk):
                    score += 2
                
                # 관심사 매칭
                audience_interests = audience_profile.get('interests', [])
                if category.replace('_', ' ') in ' '.join(audience_interests):
                    score += 1
                
                if score > 0:
                    matched_ads.append({
                        **ad,
                        'category': category,
                        'match_score': score,
                        'match_reasons': self._get_match_reasons(ad, context_analysis, audience_profile)
                    })
        
        return matched_ads
    
    def _risk_compatibility(self, ad_risk: str, audience_risk: str) -> bool:
        """리스크 호환성 검사"""
        
        risk_levels = {'low': 1, 'medium': 2, 'high': 3}
        
        ad_level = risk_levels.get(ad_risk, 2)
        
        # 오디언스 리스크 허용도 파싱
        if 'low' in audience_risk:
            audience_max = 1 if 'to' not in audience_risk else 2
        elif 'high' in audience_risk:
            audience_max = 3
        else:
            audience_max = 2
        
        return ad_level <= audience_max
    
    def _get_match_reasons(self, ad: Dict[str, Any], context_analysis: Dict[str, Any], audience_profile: Dict[str, Any]) -> List[str]:
        """매칭 이유 생성"""
        
        reasons = []
        
        # 이벤트 타입 매칭
        if context_analysis.get('event_type') in ad.get('target_events', []):
            reasons.append(f"{context_analysis.get('event_type')} 이벤트에 적합")
        
        # 키워드 매칭
        keywords = context_analysis.get('keywords', [])
        ad_keywords = ad.get('keywords', [])
        matches = set(keywords) & set(ad_keywords)
        if matches:
            reasons.append(f"관련 키워드: {', '.join(list(matches)[:3])}")
        
        # 리스크 레벨
        if self._risk_compatibility(ad.get('risk_level', 'medium'), audience_profile.get('risk_tolerance', 'medium')):
            reasons.append("리스크 수준 적합")
        
        return reasons
    
    async def _rank_and_select_ads(self, matched_ads: List[Dict[str, Any]], context_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """광고 랭킹 및 선택"""
        
        # 매치 스코어로 정렬
        sorted_ads = sorted(matched_ads, key=lambda x: x.get('match_score', 0), reverse=True)
        
        # 다양성을 위해 카테고리별로 최대 1개씩 선택
        selected_ads = []
        used_categories = set()
        
        for ad in sorted_ads:
            category = ad.get('category')
            if category not in used_categories and len(selected_ads) < 3:
                selected_ads.append(ad)
                used_categories.add(category)
        
        # 3개가 안 되면 스코어 순으로 추가
        if len(selected_ads) < 3:
            for ad in sorted_ads:
                if ad not in selected_ads and len(selected_ads) < 3:
                    selected_ads.append(ad)
        
        # 여전히 3개가 안 되면 랜덤으로 추가
        if len(selected_ads) < 3:
            all_ads = []
            for category_ads in self.ad_database.values():
                all_ads.extend(category_ads)
            
            remaining_ads = [ad for ad in all_ads if ad not in selected_ads]
            while len(selected_ads) < 3 and remaining_ads:
                selected_ads.append(remaining_ads.pop(random.randint(0, len(remaining_ads) - 1)))
        
        return selected_ads[:3]  # 최대 3개
    
    async def _personalize_ads(self, ads: List[Dict[str, Any]], context_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """광고 개인화"""
        
        personalized_ads = []
        symbol = context_analysis.get('symbol', 'Unknown')
        event_type = context_analysis.get('event_type', 'unknown')
        
        for i, ad in enumerate(ads):
            personalized_ad = {
                'id': ad.get('id', f'ad_{i+1}'),
                'title': ad.get('title', '투자 상품'),
                'description': ad.get('description', '투자 관련 서비스입니다.'),
                'cta': ad.get('cta', '자세히 보기'),
                'category': ad.get('category', 'general'),
                'match_score': ad.get('match_score', 0),
                'match_reasons': ad.get('match_reasons', []),
                'personalization': {
                    'symbol_context': symbol,
                    'event_context': event_type,
                    'relevance_score': ad.get('match_score', 0) / 10.0
                }
            }
            
            # 컨텍스트 기반 설명 개인화
            if symbol != 'Unknown' and event_type == 'volume_spike':
                personalized_ad['description'] += f" {symbol}과 같은 활발한 거래 상황에서 더욱 유용합니다."
            elif event_type == 'high_volatility':
                personalized_ad['description'] += " 변동성이 높은 시장에서 안정적인 투자를 도와드립니다."
            
            personalized_ads.append(personalized_ad)
        
        return personalized_ads
