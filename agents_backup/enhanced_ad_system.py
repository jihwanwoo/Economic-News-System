#!/usr/bin/env python3
"""
향상된 광고 추천 시스템
기사 내용 기반 맞춤 광고 추천
"""

import logging
from typing import Dict, List, Any
import random

class EnhancedAdRecommendationAgent:
    """향상된 광고 추천 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 광고 데이터베이스
        self.ad_database = {
            'trading_platforms': [
                {
                    'title': '스마트 트레이딩 플랫폼',
                    'description': '실시간 차트 분석과 자동매매 기능을 제공하는 차세대 트레이딩 플랫폼',
                    'target_audience': '액티브 트레이더, 기술적 분석 관심자',
                    'keywords': ['trading', 'chart', 'technical', 'analysis', '거래', '차트', '기술적'],
                    'category': 'trading',
                    'base_relevance': 8.5
                },
                {
                    'title': '프리미엄 투자 도구',
                    'description': '전문가급 투자 분석 도구와 실시간 알림 서비스',
                    'target_audience': '전문 투자자, 기관 투자자',
                    'keywords': ['investment', 'professional', 'analysis', '투자', '전문가', '분석'],
                    'category': 'tools',
                    'base_relevance': 7.8
                },
                {
                    'title': '로보어드바이저 서비스',
                    'description': 'AI 기반 자동 포트폴리오 관리 및 리밸런싱 서비스',
                    'target_audience': '장기 투자자, 초보 투자자',
                    'keywords': ['robo', 'portfolio', 'automatic', '자동', '포트폴리오', '장기'],
                    'category': 'robo_advisor',
                    'base_relevance': 7.2
                }
            ],
            'education': [
                {
                    'title': '투자 교육 아카데미',
                    'description': '기초부터 고급까지 체계적인 투자 교육 프로그램',
                    'target_audience': '투자 초보자, 지식 향상 희망자',
                    'keywords': ['education', 'learning', 'beginner', '교육', '학습', '초보'],
                    'category': 'education',
                    'base_relevance': 6.5
                },
                {
                    'title': '경제 뉴스 프리미엄',
                    'description': '실시간 경제 뉴스와 전문가 분석 리포트 구독 서비스',
                    'target_audience': '정보 중시 투자자, 전문가',
                    'keywords': ['news', 'report', 'analysis', '뉴스', '리포트', '분석'],
                    'category': 'information',
                    'base_relevance': 7.0
                },
                {
                    'title': '투자 심리학 코스',
                    'description': '투자 심리와 행동경제학 기반 투자 전략 교육',
                    'target_audience': '심화 학습자, 투자 전략 개선 희망자',
                    'keywords': ['psychology', 'behavior', 'strategy', '심리', '행동', '전략'],
                    'category': 'advanced_education',
                    'base_relevance': 6.8
                }
            ],
            'financial_services': [
                {
                    'title': '프리미엄 자산관리',
                    'description': '고액 자산가를 위한 맞춤형 자산관리 서비스',
                    'target_audience': '고액 투자자, 자산관리 필요자',
                    'keywords': ['wealth', 'management', 'premium', '자산', '관리', '프리미엄'],
                    'category': 'wealth_management',
                    'base_relevance': 8.0
                },
                {
                    'title': '투자 컨설팅 서비스',
                    'description': '개인 맞춤형 투자 전략 수립 및 컨설팅',
                    'target_audience': '전략 수립 필요자, 컨설팅 희망자',
                    'keywords': ['consulting', 'strategy', 'personal', '컨설팅', '전략', '개인'],
                    'category': 'consulting',
                    'base_relevance': 7.5
                },
                {
                    'title': '리스크 관리 솔루션',
                    'description': '포트폴리오 리스크 분석 및 헤징 전략 제공',
                    'target_audience': '리스크 관리 중시자, 기관 투자자',
                    'keywords': ['risk', 'hedge', 'portfolio', '리스크', '헤징', '포트폴리오'],
                    'category': 'risk_management',
                    'base_relevance': 7.3
                }
            ],
            'fintech': [
                {
                    'title': '블록체인 투자 플랫폼',
                    'description': '암호화폐 및 블록체인 자산 투자 전문 플랫폼',
                    'target_audience': '암호화폐 투자자, 핀테크 관심자',
                    'keywords': ['blockchain', 'crypto', 'fintech', '블록체인', '암호화폐', '핀테크'],
                    'category': 'crypto',
                    'base_relevance': 6.0
                },
                {
                    'title': 'AI 투자 분석 서비스',
                    'description': '인공지능 기반 시장 분석 및 투자 신호 제공',
                    'target_audience': 'AI 기술 관심자, 혁신 투자자',
                    'keywords': ['AI', 'artificial', 'intelligence', 'AI', '인공지능', '혁신'],
                    'category': 'ai_service',
                    'base_relevance': 7.8
                },
                {
                    'title': '모바일 투자 앱',
                    'description': '언제 어디서나 간편한 모바일 투자 서비스',
                    'target_audience': '모바일 사용자, 편의성 중시자',
                    'keywords': ['mobile', 'app', 'convenient', '모바일', '앱', '편리'],
                    'category': 'mobile',
                    'base_relevance': 6.8
                }
            ]
        }
        
        self.logger.info("✅ 향상된 광고 추천 에이전트 초기화 완료")
    
    async def recommend_ads(self, article: Dict[str, Any], event_data: Dict[str, Any], num_ads: int = 3) -> List[Dict[str, Any]]:
        """기사 내용 기반 광고 추천"""
        
        self.logger.info("📢 기사 기반 광고 추천 시작")
        
        try:
            # 기사 내용 분석
            content = article.get('content', '')
            title = article.get('title', '')
            symbol = event_data.get('symbol', '')
            change_percent = event_data.get('change_percent', 0)
            
            # 키워드 추출 및 분석
            keywords = self._extract_keywords(content, title)
            user_profile = self._analyze_user_profile(content, change_percent)
            
            # 광고 점수 계산
            scored_ads = []
            for category, ads in self.ad_database.items():
                for ad in ads:
                    relevance_score = self._calculate_relevance_score(ad, keywords, user_profile)
                    scored_ad = ad.copy()
                    scored_ad['relevance_score'] = relevance_score
                    scored_ad['match_reasons'] = self._get_match_reasons(ad, keywords, user_profile)
                    scored_ads.append(scored_ad)
            
            # 점수순 정렬 및 상위 광고 선택
            scored_ads.sort(key=lambda x: x['relevance_score'], reverse=True)
            recommended_ads = scored_ads[:num_ads]
            
            self.logger.info(f"✅ {len(recommended_ads)}개 광고 추천 완료")
            return recommended_ads
            
        except Exception as e:
            self.logger.error(f"❌ 광고 추천 실패: {e}")
            return self._get_default_ads(num_ads)
    
    def _extract_keywords(self, content: str, title: str) -> List[str]:
        """기사에서 키워드 추출"""
        
        text = (content + ' ' + title).lower()
        
        # 금융/투자 관련 키워드
        financial_keywords = [
            'trading', 'investment', 'portfolio', 'analysis', 'chart', 'technical',
            'fundamental', 'risk', 'return', 'profit', 'loss', 'market', 'stock',
            'bond', 'etf', 'mutual fund', 'hedge', 'derivative', 'option',
            '거래', '투자', '포트폴리오', '분석', '차트', '기술적', '펀더멘털',
            '리스크', '수익', '손실', '시장', '주식', '채권', '펀드', '헤징'
        ]
        
        found_keywords = []
        for keyword in financial_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _analyze_user_profile(self, content: str, change_percent: float) -> Dict[str, Any]:
        """사용자 프로필 분석"""
        
        content_lower = content.lower()
        
        profile = {
            'risk_tolerance': 'medium',
            'experience_level': 'intermediate',
            'investment_style': 'balanced',
            'interest_areas': []
        }
        
        # 리스크 성향 분석
        if abs(change_percent) > 5:
            profile['risk_tolerance'] = 'high'
        elif abs(change_percent) < 2:
            profile['risk_tolerance'] = 'low'
        
        # 경험 수준 분석
        technical_terms = ['rsi', 'macd', 'bollinger', 'fibonacci', '기술적', '지표']
        if any(term in content_lower for term in technical_terms):
            profile['experience_level'] = 'advanced'
        
        # 투자 스타일 분석
        if 'long term' in content_lower or '장기' in content_lower:
            profile['investment_style'] = 'long_term'
        elif 'short term' in content_lower or '단기' in content_lower:
            profile['investment_style'] = 'short_term'
        
        # 관심 영역 분석
        if 'crypto' in content_lower or '암호화폐' in content_lower:
            profile['interest_areas'].append('crypto')
        if 'ai' in content_lower or '인공지능' in content_lower:
            profile['interest_areas'].append('ai')
        if 'mobile' in content_lower or '모바일' in content_lower:
            profile['interest_areas'].append('mobile')
        
        return profile
    
    def _calculate_relevance_score(self, ad: Dict[str, Any], keywords: List[str], user_profile: Dict[str, Any]) -> float:
        """광고 관련성 점수 계산"""
        
        base_score = ad['base_relevance']
        
        # 키워드 매칭 점수
        keyword_score = 0
        for keyword in keywords:
            if any(kw in keyword for kw in ad['keywords']):
                keyword_score += 1
        
        keyword_bonus = min(keyword_score * 0.5, 2.0)
        
        # 사용자 프로필 매칭 점수
        profile_bonus = 0
        
        # 리스크 성향 매칭
        if user_profile['risk_tolerance'] == 'high' and ad['category'] in ['trading', 'crypto']:
            profile_bonus += 0.5
        elif user_profile['risk_tolerance'] == 'low' and ad['category'] in ['robo_advisor', 'education']:
            profile_bonus += 0.5
        
        # 경험 수준 매칭
        if user_profile['experience_level'] == 'advanced' and ad['category'] in ['tools', 'advanced_education']:
            profile_bonus += 0.3
        elif user_profile['experience_level'] == 'beginner' and ad['category'] in ['education', 'robo_advisor']:
            profile_bonus += 0.3
        
        # 관심 영역 매칭
        for interest in user_profile['interest_areas']:
            if interest in ad['category']:
                profile_bonus += 0.4
        
        # 최종 점수 계산
        final_score = base_score + keyword_bonus + profile_bonus
        return min(final_score, 10.0)  # 최대 10점
    
    def _get_match_reasons(self, ad: Dict[str, Any], keywords: List[str], user_profile: Dict[str, Any]) -> List[str]:
        """매칭 이유 생성"""
        
        reasons = []
        
        # 키워드 매칭
        matched_keywords = [kw for kw in keywords if any(ad_kw in kw for ad_kw in ad['keywords'])]
        if matched_keywords:
            reasons.append(f"기사 키워드 매칭: {', '.join(matched_keywords[:3])}")
        
        # 프로필 매칭
        if user_profile['risk_tolerance'] == 'high' and ad['category'] in ['trading', 'crypto']:
            reasons.append("고위험 투자 성향 매칭")
        
        if user_profile['experience_level'] == 'advanced' and ad['category'] in ['tools', 'advanced_education']:
            reasons.append("고급 사용자 대상 서비스")
        
        return reasons[:2]  # 최대 2개 이유
    
    def _get_default_ads(self, num_ads: int) -> List[Dict[str, Any]]:
        """기본 광고 반환"""
        
        default_ads = [
            {
                'title': '스마트 투자 플랫폼',
                'description': '실시간 시장 분석과 투자 도구를 제공하는 종합 투자 플랫폼',
                'target_audience': '모든 투자자',
                'relevance_score': 7.0,
                'match_reasons': ['일반 투자 서비스']
            },
            {
                'title': '투자 교육 서비스',
                'description': '체계적인 투자 교육과 전문가 멘토링 프로그램',
                'target_audience': '투자 학습자',
                'relevance_score': 6.5,
                'match_reasons': ['투자 지식 향상']
            },
            {
                'title': '포트폴리오 관리 도구',
                'description': '개인 맞춤형 포트폴리오 분석 및 관리 서비스',
                'target_audience': '포트폴리오 투자자',
                'relevance_score': 6.8,
                'match_reasons': ['자산 관리 최적화']
            }
        ]
        
        return default_ads[:num_ads]

# 기존 AdRecommendationAgent 업데이트
def update_ad_recommendation_agent():
    """기존 광고 추천 에이전트 업데이트"""
    
    enhanced_method = '''
    async def recommend_ads(self, article: Dict[str, Any], analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """향상된 광고 추천"""
        
        from agents.enhanced_ad_system import EnhancedAdRecommendationAgent
        
        enhanced_agent = EnhancedAdRecommendationAgent()
        event_data = {
            'symbol': analysis_data.get('symbol', 'MARKET'),
            'change_percent': analysis_data.get('raw_data', {}).get('change_percent', 0)
        }
        
        return await enhanced_agent.recommend_ads(article, event_data, num_ads=3)
    '''
    
    return enhanced_method
