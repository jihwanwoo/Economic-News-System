#!/usr/bin/env python3
"""
광고 추천 에이전트
기사 내용에 맞는 광고 3개 추천
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import random


from agents.enhanced_ad_system import EnhancedAdRecommendationAgent

class AdRecommendationAgent:
    """광고 추천 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 광고 데이터베이스
        self.ad_database = {
            # 투자 플랫폼
            'investment_platforms': [
                {
                    'title': '스마트 투자 플랫폼 - InvestSmart',
                    'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.',
                    'target_audience': '개인 투자자',
                    'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'],
                    'cta': '무료 체험 시작하기',
                    'advertiser': 'InvestSmart Inc.',
                    'category': 'investment_platform'
                },
                {
                    'title': '로보어드바이저 - WealthBot',
                    'description': '전문가 수준의 자산 관리를 자동화된 시스템으로 경험하세요. 최소 투자금 10만원.',
                    'target_audience': '초보 투자자',
                    'relevance_keywords': ['자산관리', '로보어드바이저', '자동투자'],
                    'cta': '포트폴리오 진단받기',
                    'advertiser': 'WealthBot Co.',
                    'category': 'robo_advisor'
                }
            ],
            
            # 트레이딩 도구
            'trading_tools': [
                {
                    'title': '프로 트레이딩 플랫폼 - TradeMax',
                    'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.',
                    'target_audience': '전문 트레이더',
                    'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'],
                    'cta': '30일 무료 체험',
                    'advertiser': 'TradeMax Ltd.',
                    'category': 'trading_platform'
                },
                {
                    'title': '모바일 트레이딩 앱 - QuickTrade',
                    'description': '언제 어디서나 빠른 매매. 실시간 알림과 간편한 주문으로 기회를 놓치지 마세요.',
                    'target_audience': '모바일 트레이더',
                    'relevance_keywords': ['모바일', '실시간', '알림', '빠른매매'],
                    'cta': '앱 다운로드',
                    'advertiser': 'QuickTrade App',
                    'category': 'mobile_trading'
                }
            ],
            
            # 금융 교육
            'financial_education': [
                {
                    'title': '투자 마스터 클래스 - InvestEdu',
                    'description': '기초부터 고급까지, 체계적인 투자 교육으로 성공적인 투자자가 되세요.',
                    'target_audience': '투자 학습자',
                    'relevance_keywords': ['교육', '학습', '투자기초', '전략'],
                    'cta': '무료 강의 수강',
                    'advertiser': 'InvestEdu Academy',
                    'category': 'education'
                },
                {
                    'title': '경제 뉴스 프리미엄 - EcoNews+',
                    'description': '전문가 분석과 독점 리포트로 시장을 앞서가세요. 실시간 알림 서비스 포함.',
                    'target_audience': '정보 추구자',
                    'relevance_keywords': ['뉴스', '분석', '리포트', '정보'],
                    'cta': '프리미엄 구독',
                    'advertiser': 'EcoNews Media',
                    'category': 'news_service'
                }
            ],
            
            # 금융 서비스
            'financial_services': [
                {
                    'title': '투자자 대출 - InvestLoan',
                    'description': '주식 담보 대출로 투자 기회를 확대하세요. 경쟁력 있는 금리와 빠른 승인.',
                    'target_audience': '레버리지 투자자',
                    'relevance_keywords': ['대출', '담보', '레버리지', '자금'],
                    'cta': '대출 상담 신청',
                    'advertiser': 'InvestLoan Bank',
                    'category': 'lending'
                },
                {
                    'title': '세금 최적화 서비스 - TaxSmart',
                    'description': '투자 수익의 세금 부담을 줄이는 전문 컨설팅. 절세 전략으로 수익률을 높이세요.',
                    'target_audience': '고수익 투자자',
                    'relevance_keywords': ['세금', '절세', '최적화', '컨설팅'],
                    'cta': '무료 세무 상담',
                    'advertiser': 'TaxSmart Consulting',
                    'category': 'tax_service'
                }
            ],
            
            # 암호화폐
            'cryptocurrency': [
                {
                    'title': '암호화폐 거래소 - CryptoMax',
                    'description': '안전하고 빠른 암호화폐 거래. 다양한 코인과 낮은 수수료로 디지털 자산 투자를 시작하세요.',
                    'target_audience': '암호화폐 투자자',
                    'relevance_keywords': ['암호화폐', '비트코인', '블록체인', '디지털자산'],
                    'cta': '거래소 가입',
                    'advertiser': 'CryptoMax Exchange',
                    'category': 'crypto_exchange'
                }
            ],
            
            # 부동산
            'real_estate': [
                {
                    'title': '부동산 투자 플랫폼 - RealtyInvest',
                    'description': '소액으로 시작하는 부동산 투자. 전문가가 선별한 수익형 부동산에 투자하세요.',
                    'target_audience': '부동산 투자자',
                    'relevance_keywords': ['부동산', '투자', '수익형', '소액투자'],
                    'cta': '투자 상품 보기',
                    'advertiser': 'RealtyInvest Co.',
                    'category': 'real_estate'
                }
            ]
        }
        
        self.logger.info("✅ 광고 추천 에이전트 초기화 완료")
    
    async def recommend_ads(self, article: Dict[str, Any], event) -> List[Dict[str, Any]]:
        """기사에 맞는 광고 3개 추천"""
        
        self.logger.info("📢 광고 추천 시작")
        
        try:
            # 1. 기사 내용 분석
            content_analysis = self._analyze_article_content(article, event)
            
            # 2. 관련성 점수 계산
            ad_scores = self._calculate_relevance_scores(content_analysis)
            
            # 3. 상위 3개 광고 선택
            top_ads = self._select_top_ads(ad_scores, 3)
            
            # 4. 광고 정보 보강
            recommended_ads = self._enrich_ad_information(top_ads, content_analysis)
            
            self.logger.info(f"✅ 광고 추천 완료: {len(recommended_ads)}개")
            return recommended_ads
            
        except Exception as e:
            self.logger.error(f"❌ 광고 추천 실패: {e}")
            return self._get_default_ads()
    
    def _analyze_article_content(self, article: Dict[str, Any], event) -> Dict[str, Any]:
        """기사 내용 분석"""
        
        content = article.get('content', '').lower()
        title = article.get('title', '').lower()
        tags = article.get('tags', [])
        
        # 키워드 추출
        keywords = []
        
        # 이벤트 기반 키워드
        keywords.append(event.symbol.lower())
        keywords.append(event.event_type)
        
        # 태그 기반 키워드
        keywords.extend([tag.lower() for tag in tags])
        
        # 내용 기반 키워드 추출
        financial_terms = [
            '투자', '주식', '거래', '매매', '포트폴리오', '수익', '손실',
            '분석', '차트', '기술적', '펀더멘털', '시장', '경제',
            '암호화폐', '비트코인', '부동산', '채권', '파생상품',
            '리스크', '변동성', '수익률', '배당', '성장주', '가치주'
        ]
        
        found_terms = [term for term in financial_terms if term in content or term in title]
        keywords.extend(found_terms)
        
        # 투자자 유형 추정
        investor_type = self._estimate_investor_type(content, event)
        
        # 관심 분야 추정
        interest_areas = self._estimate_interest_areas(content, keywords, event)
        
        return {
            'keywords': list(set(keywords)),
            'investor_type': investor_type,
            'interest_areas': interest_areas,
            'event_type': event.event_type,
            'symbol': event.symbol,
            'severity': event.severity.value,
            'content_length': len(content.split())
        }
    
    def _estimate_investor_type(self, content: str, event) -> str:
        """투자자 유형 추정"""
        
        # 기술적 분석 용어 빈도
        technical_terms = ['rsi', 'macd', '이동평균', '볼린저밴드', '지지선', '저항선']
        technical_count = sum(content.count(term) for term in technical_terms)
        
        # 기본 분석 용어 빈도
        fundamental_terms = ['실적', '매출', '순이익', 'eps', '배당', '성장률']
        fundamental_count = sum(content.count(term) for term in fundamental_terms)
        
        # 이벤트 심각도 고려
        if event.severity.value in ['high', 'critical']:
            if technical_count > fundamental_count:
                return '전문 트레이더'
            else:
                return '적극적 투자자'
        else:
            if technical_count > 2:
                return '기술적 분석 투자자'
            elif fundamental_count > 2:
                return '가치 투자자'
            else:
                return '일반 투자자'
    
    def _estimate_interest_areas(self, content: str, keywords: List[str], event) -> List[str]:
        """관심 분야 추정"""
        
        interest_areas = []
        
        # 키워드 기반 관심 분야 매핑
        area_keywords = {
            'trading': ['거래', '매매', '트레이딩', '단타', '스윙'],
            'investment': ['투자', '포트폴리오', '자산배분', '장기투자'],
            'analysis': ['분석', '차트', '지표', '전망', '예측'],
            'education': ['학습', '교육', '기초', '전략', '방법'],
            'news': ['뉴스', '정보', '리포트', '분석', '전망'],
            'crypto': ['암호화폐', '비트코인', '블록체인', '디지털자산'],
            'real_estate': ['부동산', '리츠', 'reit'],
            'tax': ['세금', '절세', '세무', '최적화']
        }
        
        for area, area_keywords_list in area_keywords.items():
            if any(keyword in keywords or keyword in content for keyword in area_keywords_list):
                interest_areas.append(area)
        
        # 이벤트 유형 기반 추가
        if event.event_type == 'volume_spike':
            interest_areas.append('trading')
        elif event.event_type == 'high_volatility':
            interest_areas.extend(['trading', 'analysis'])
        
        return list(set(interest_areas))
    
    def _calculate_relevance_scores(self, content_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """관련성 점수 계산"""
        
        ad_scores = []
        keywords = content_analysis['keywords']
        investor_type = content_analysis['investor_type']
        interest_areas = content_analysis['interest_areas']
        
        # 모든 광고에 대해 점수 계산
        for category, ads in self.ad_database.items():
            for ad in ads:
                score = 0
                
                # 1. 키워드 매칭 점수 (40%)
                keyword_matches = sum(1 for keyword in ad['relevance_keywords'] 
                                    if any(k in keyword.lower() for k in keywords))
                keyword_score = (keyword_matches / len(ad['relevance_keywords'])) * 40
                
                # 2. 투자자 유형 매칭 점수 (30%)
                target_score = 30 if investor_type in ad['target_audience'] else 0
                
                # 3. 관심 분야 매칭 점수 (20%)
                interest_score = 0
                if category.replace('_', '') in [area.replace('_', '') for area in interest_areas]:
                    interest_score = 20
                elif any(area in ad['category'] for area in interest_areas):
                    interest_score = 15
                
                # 4. 이벤트 심각도 보너스 (10%)
                severity_bonus = 0
                if content_analysis['severity'] in ['high', 'critical']:
                    if 'trading' in ad['category'] or 'platform' in ad['category']:
                        severity_bonus = 10
                
                total_score = keyword_score + target_score + interest_score + severity_bonus
                
                ad_scores.append({
                    'ad': ad,
                    'score': total_score,
                    'keyword_score': keyword_score,
                    'target_score': target_score,
                    'interest_score': interest_score,
                    'severity_bonus': severity_bonus
                })
        
        return sorted(ad_scores, key=lambda x: x['score'], reverse=True)
    
    def _select_top_ads(self, ad_scores: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """상위 광고 선택"""
        
        # 다양성을 위해 같은 카테고리에서 최대 2개까지만 선택
        selected_ads = []
        category_counts = {}
        
        for ad_score in ad_scores:
            if len(selected_ads) >= count:
                break
            
            category = ad_score['ad']['category']
            current_count = category_counts.get(category, 0)
            
            if current_count < 2:  # 같은 카테고리 최대 2개
                selected_ads.append(ad_score)
                category_counts[category] = current_count + 1
        
        # 부족한 경우 나머지 채우기
        if len(selected_ads) < count:
            remaining = [ad for ad in ad_scores if ad not in selected_ads]
            selected_ads.extend(remaining[:count - len(selected_ads)])
        
        return selected_ads[:count]
    
    def _enrich_ad_information(self, top_ads: List[Dict[str, Any]], 
                              content_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """광고 정보 보강"""
        
        enriched_ads = []
        
        for i, ad_score in enumerate(top_ads, 1):
            ad = ad_score['ad'].copy()
            
            # 관련성 점수 추가
            ad['relevance_score'] = round(ad_score['score'] / 10, 1)  # 10점 만점으로 정규화
            
            # 추천 순위 추가
            ad['rank'] = i
            
            # 맞춤 메시지 생성
            ad['personalized_message'] = self._generate_personalized_message(
                ad, content_analysis
            )
            
            # 클릭 추적 URL (실제로는 광고 플랫폼 연동)
            ad['tracking_url'] = f"https://ads.example.com/click?ad_id={ad.get('title', '').replace(' ', '_')}&article_symbol={content_analysis['symbol']}"
            
            # 광고 메트릭
            ad['metrics'] = {
                'keyword_relevance': round(ad_score['keyword_score'] / 4, 1),
                'audience_match': round(ad_score['target_score'] / 3, 1),
                'interest_alignment': round(ad_score['interest_score'] / 2, 1)
            }
            
            enriched_ads.append(ad)
        
        return enriched_ads
    
    def _generate_personalized_message(self, ad: Dict[str, Any], 
                                     content_analysis: Dict[str, Any]) -> str:
        """개인화된 메시지 생성"""
        
        symbol = content_analysis['symbol']
        investor_type = content_analysis['investor_type']
        
        # 투자자 유형별 맞춤 메시지
        if investor_type == '전문 트레이더':
            return f"{symbol} 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요."
        elif investor_type == '기술적 분석 투자자':
            return f"{symbol}의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?"
        elif investor_type == '가치 투자자':
            return f"{symbol}의 펀더멘털 분석에 도움이 될 전문 정보를 제공합니다."
        else:
            return f"{symbol} 투자에 관심이 있으시군요! 초보자도 쉽게 시작할 수 있는 서비스입니다."
    
    def _get_default_ads(self) -> List[Dict[str, Any]]:
        """기본 광고 반환 (오류 시)"""
        
        default_ads = []
        
        # 각 카테고리에서 첫 번째 광고 선택
        categories = ['investment_platforms', 'trading_tools', 'financial_education']
        
        for category in categories:
            if category in self.ad_database and self.ad_database[category]:
                ad = self.ad_database[category][0].copy()
                ad['relevance_score'] = 5.0
                ad['rank'] = len(default_ads) + 1
                ad['personalized_message'] = "투자에 관심이 있으시군요! 이 서비스를 확인해보세요."
                default_ads.append(ad)
        
        return default_ads
