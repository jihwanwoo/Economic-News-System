"""
검수 Strand Agent
작성된 기사의 품질을 검토하고 개선사항을 제안
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from .strands_framework import BaseStrandAgent, StrandContext, StrandMessage, MessageType

class ReviewStrand(BaseStrandAgent):
    """검수 Strand Agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="reviewer",
            name="기사 검수 에이전트"
        )
        
        self.capabilities = [
            "content_quality_review",
            "fact_checking",
            "readability_analysis",
            "compliance_check",
            "improvement_suggestions"
        ]
        
        # 검수 기준
        self.review_criteria = {
            'content_accuracy': {
                'weight': 0.3,
                'checks': ['data_consistency', 'factual_accuracy', 'source_reliability']
            },
            'readability': {
                'weight': 0.25,
                'checks': ['sentence_length', 'vocabulary_level', 'structure_clarity']
            },
            'completeness': {
                'weight': 0.2,
                'checks': ['essential_information', 'context_provision', 'conclusion_presence']
            },
            'compliance': {
                'weight': 0.15,
                'checks': ['investment_advice_avoidance', 'disclaimer_presence', 'objective_tone']
            },
            'engagement': {
                'weight': 0.1,
                'checks': ['title_effectiveness', 'lead_strength', 'flow_quality']
            }
        }
    
    def get_capabilities(self) -> List[str]:
        """에이전트 능력 반환"""
        return self.capabilities
    
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """기사 검수 처리"""
        
        # 기사 데이터 가져오기
        article = await self.get_shared_data(context, 'article')
        if not article:
            raise Exception("검수할 기사가 없습니다")
        
        self.logger.info("🔍 기사 검수 시작")
        
        try:
            # 1. 내용 정확성 검토
            accuracy_score = await self._review_content_accuracy(article, context)
            
            # 2. 가독성 분석
            readability_score = await self._analyze_readability(article)
            
            # 3. 완성도 검토
            completeness_score = await self._review_completeness(article)
            
            # 4. 컴플라이언스 검토
            compliance_score = await self._review_compliance(article)
            
            # 5. 참여도 분석
            engagement_score = await self._analyze_engagement(article)
            
            # 6. 종합 점수 계산
            overall_score = await self._calculate_overall_score({
                'accuracy': accuracy_score,
                'readability': readability_score,
                'completeness': completeness_score,
                'compliance': compliance_score,
                'engagement': engagement_score
            })
            
            # 7. 개선사항 제안
            improvements = await self._suggest_improvements(article, {
                'accuracy': accuracy_score,
                'readability': readability_score,
                'completeness': completeness_score,
                'compliance': compliance_score,
                'engagement': engagement_score
            })
            
            # 검수 결과 패키지
            review_result = {
                'overall_score': overall_score,
                'detailed_scores': {
                    'content_accuracy': accuracy_score,
                    'readability': readability_score,
                    'completeness': completeness_score,
                    'compliance': compliance_score,
                    'engagement': engagement_score
                },
                'improvements': improvements,
                'review_timestamp': datetime.now().isoformat(),
                'reviewer': self.name,
                'status': 'approved' if overall_score >= 7.0 else 'needs_revision'
            }
            
            # 공유 메모리에 저장
            await self.set_shared_data(context, 'review_result', review_result)
            
            self.logger.info(f"✅ 기사 검수 완료 (점수: {overall_score:.1f}/10)")
            return review_result
            
        except Exception as e:
            self.logger.error(f"❌ 기사 검수 실패: {e}")
            raise
    
    async def _review_content_accuracy(self, article: Dict[str, Any], context: StrandContext) -> float:
        """내용 정확성 검토"""
        
        score = 8.0  # 기본 점수
        
        try:
            # 데이터 일관성 검토
            data_analysis = await self.get_shared_data(context, 'data_analysis')
            if data_analysis:
                # 기사에서 언급된 수치와 데이터 분석 결과 비교
                body = article.get('body', '')
                
                # 가격 정보 일관성
                raw_data = data_analysis.get('raw_data', {})
                current_price = raw_data.get('current_price')
                if current_price and str(current_price) not in body:
                    score -= 0.5
                
                # 기술적 지표 일관성
                technical = data_analysis.get('technical_indicators', {})
                if technical.get('rsi'):
                    rsi = technical['rsi']
                    if 'RSI' in body:
                        # RSI 값이 기사에 정확히 반영되었는지 확인
                        if abs(rsi - 50) > 20:  # 극단적인 값인 경우
                            if ('과매수' in body and rsi < 70) or ('과매도' in body and rsi > 30):
                                score -= 1.0
            
            # 사실 정확성 기본 검토
            body = article.get('body', '').lower()
            
            # 부정확한 표현 검출
            inaccurate_phrases = [
                '확실히', '반드시', '100%', '절대적으로',
                '투자하세요', '매수하세요', '매도하세요'
            ]
            
            for phrase in inaccurate_phrases:
                if phrase in body:
                    score -= 0.3
            
            return max(0.0, min(10.0, score))
            
        except Exception as e:
            self.logger.error(f"내용 정확성 검토 실패: {e}")
            return 7.0
    
    async def _analyze_readability(self, article: Dict[str, Any]) -> float:
        """가독성 분석"""
        
        score = 8.0
        
        try:
            body = article.get('body', '')
            if not body:
                return 5.0
            
            # 문장 길이 분석
            sentences = re.split(r'[.!?]', body)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if sentences:
                avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
                
                # 적정 문장 길이: 15-25단어
                if avg_sentence_length > 30:
                    score -= 1.0
                elif avg_sentence_length > 25:
                    score -= 0.5
                elif avg_sentence_length < 10:
                    score -= 0.5
            
            # 단락 구조 분석
            paragraphs = body.split('\n\n')
            if len(paragraphs) < 2:
                score -= 0.5
            
            # 전문용어 밀도 검토
            technical_terms = [
                'RSI', 'MACD', '볼린저', '이동평균', '변동성',
                '베타', '상관관계', '과매수', '과매도'
            ]
            
            term_count = sum(1 for term in technical_terms if term in body)
            word_count = len(body.split())
            
            if word_count > 0:
                term_density = term_count / word_count
                if term_density > 0.1:  # 10% 이상이면 너무 전문적
                    score -= 0.5
            
            return max(0.0, min(10.0, score))
            
        except Exception as e:
            self.logger.error(f"가독성 분석 실패: {e}")
            return 7.0
    
    async def _review_completeness(self, article: Dict[str, Any]) -> float:
        """완성도 검토"""
        
        score = 8.0
        
        try:
            # 필수 요소 확인
            title = article.get('title', '')
            lead = article.get('lead', '')
            body = article.get('body', '')
            conclusion = article.get('conclusion', '')
            
            # 제목 검토
            if not title or len(title) < 10:
                score -= 1.0
            
            # 리드 검토
            if not lead or len(lead) < 20:
                score -= 1.0
            
            # 본문 검토
            if not body or len(body.split()) < 50:
                score -= 2.0
            
            # 결론 검토
            if not conclusion or len(conclusion) < 20:
                score -= 0.5
            
            # 핵심 정보 포함 여부
            essential_elements = [
                '가격', '거래량', '변동성', '분석', '시장'
            ]
            
            missing_elements = 0
            for element in essential_elements:
                if element not in body:
                    missing_elements += 1
            
            score -= missing_elements * 0.2
            
            return max(0.0, min(10.0, score))
            
        except Exception as e:
            self.logger.error(f"완성도 검토 실패: {e}")
            return 7.0
    
    async def _review_compliance(self, article: Dict[str, Any]) -> float:
        """컴플라이언스 검토"""
        
        score = 9.0
        
        try:
            body = article.get('body', '').lower()
            title = article.get('title', '').lower()
            conclusion = article.get('conclusion', '').lower()
            
            full_text = f"{title} {body} {conclusion}"
            
            # 투자 조언 금지 표현 검출
            investment_advice_phrases = [
                '투자하세요', '매수하세요', '매도하세요', '추천합니다',
                '사세요', '파세요', '투자 기회', '수익을 보장'
            ]
            
            for phrase in investment_advice_phrases:
                if phrase in full_text:
                    score -= 2.0
            
            # 객관적 톤 검토
            subjective_phrases = [
                '확실히', '분명히', '틀림없이', '반드시',
                '최고의', '최악의', '완벽한'
            ]
            
            for phrase in subjective_phrases:
                if phrase in full_text:
                    score -= 0.5
            
            # 면책 조항 확인
            disclaimer_keywords = [
                '투자 결정', '전문가 상담', '리스크', '신중한'
            ]
            
            disclaimer_present = any(keyword in full_text for keyword in disclaimer_keywords)
            if not disclaimer_present:
                score -= 1.0
            
            return max(0.0, min(10.0, score))
            
        except Exception as e:
            self.logger.error(f"컴플라이언스 검토 실패: {e}")
            return 8.0
    
    async def _analyze_engagement(self, article: Dict[str, Any]) -> float:
        """참여도 분석"""
        
        score = 7.0
        
        try:
            title = article.get('title', '')
            lead = article.get('lead', '')
            body = article.get('body', '')
            
            # 제목 효과성
            if title:
                # 숫자나 구체적 정보 포함
                if any(char.isdigit() for char in title):
                    score += 0.5
                
                # 적절한 길이 (20-60자)
                if 20 <= len(title) <= 60:
                    score += 0.5
                
                # 감정적 단어 포함
                emotional_words = ['급증', '급락', '주목', '관심', '충격', '놀라운']
                if any(word in title for word in emotional_words):
                    score += 0.3
            
            # 리드 강도
            if lead:
                # 핵심 정보 포함
                key_info = ['%', '배', '달러', '원']
                if any(info in lead for info in key_info):
                    score += 0.5
                
                # 적절한 길이
                if 50 <= len(lead) <= 150:
                    score += 0.3
            
            # 본문 흐름
            if body:
                # 단락 구분
                paragraphs = body.split('\n')
                if len(paragraphs) >= 3:
                    score += 0.5
                
                # 연결어 사용
                connectors = ['그러나', '또한', '따라서', '한편', '결과적으로']
                connector_count = sum(1 for conn in connectors if conn in body)
                score += min(1.0, connector_count * 0.2)
            
            return max(0.0, min(10.0, score))
            
        except Exception as e:
            self.logger.error(f"참여도 분석 실패: {e}")
            return 7.0
    
    async def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """종합 점수 계산"""
        
        try:
            weighted_score = 0.0
            
            for criterion, weight_info in self.review_criteria.items():
                weight = weight_info['weight']
                score_key = {
                    'content_accuracy': 'accuracy',
                    'readability': 'readability',
                    'completeness': 'completeness',
                    'compliance': 'compliance',
                    'engagement': 'engagement'
                }.get(criterion, criterion)
                
                score = scores.get(score_key, 7.0)
                weighted_score += score * weight
            
            return round(weighted_score, 1)
            
        except Exception as e:
            self.logger.error(f"종합 점수 계산 실패: {e}")
            return 7.0
    
    async def _suggest_improvements(self, article: Dict[str, Any], scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """개선사항 제안"""
        
        improvements = []
        
        try:
            # 각 영역별 개선사항 제안
            if scores.get('accuracy', 8.0) < 7.0:
                improvements.append({
                    'category': 'content_accuracy',
                    'priority': 'high',
                    'suggestion': '데이터 일관성을 확인하고 부정확한 표현을 수정하세요.',
                    'details': '수치 정보와 분석 결과의 일치성을 검토해주세요.'
                })
            
            if scores.get('readability', 8.0) < 7.0:
                improvements.append({
                    'category': 'readability',
                    'priority': 'medium',
                    'suggestion': '문장 길이를 조정하고 전문용어 사용을 줄이세요.',
                    'details': '평균 문장 길이를 15-25단어로 유지하고 일반인도 이해할 수 있는 표현을 사용하세요.'
                })
            
            if scores.get('completeness', 8.0) < 7.0:
                improvements.append({
                    'category': 'completeness',
                    'priority': 'high',
                    'suggestion': '필수 정보를 추가하고 구조를 완성하세요.',
                    'details': '제목, 리드, 본문, 결론의 완성도를 높이고 핵심 정보를 포함하세요.'
                })
            
            if scores.get('compliance', 8.0) < 8.0:
                improvements.append({
                    'category': 'compliance',
                    'priority': 'critical',
                    'suggestion': '투자 조언 표현을 제거하고 객관적 톤을 유지하세요.',
                    'details': '투자 권유 표현을 피하고 면책 조항을 포함하세요.'
                })
            
            if scores.get('engagement', 8.0) < 6.0:
                improvements.append({
                    'category': 'engagement',
                    'priority': 'low',
                    'suggestion': '제목과 리드의 매력도를 높이세요.',
                    'details': '구체적 수치를 포함하고 독자의 관심을 끌 수 있는 표현을 사용하세요.'
                })
            
            return improvements
            
        except Exception as e:
            self.logger.error(f"개선사항 제안 실패: {e}")
            return [{
                'category': 'general',
                'priority': 'medium',
                'suggestion': '전반적인 기사 품질을 검토하세요.',
                'details': '내용의 정확성과 완성도를 확인해주세요.'
            }]
