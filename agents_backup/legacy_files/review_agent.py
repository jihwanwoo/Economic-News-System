#!/usr/bin/env python3
"""
검수 에이전트
생성된 기사의 품질과 정확성을 검수
"""

import os
import sys
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

class ReviewAgent:
    """검수 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 검수 기준 설정
        self.review_criteria = {
            'content_quality': {
                'min_word_count': 200,
                'max_word_count': 1500,
                'required_sections': ['분석', '전망'],
                'forbidden_words': ['투자 조언', '매수 추천', '매도 추천']
            },
            'data_accuracy': {
                'required_data_points': ['current_price', 'change_percent'],
                'acceptable_variance': 0.1  # 10% 오차 허용
            },
            'style_guidelines': {
                'tone': 'professional',
                'objectivity_required': True,
                'speculation_limit': 0.2  # 추측성 표현 20% 이하
            },
            'compliance': {
                'disclaimer_required': True,
                'source_attribution': True,
                'risk_warning': True
            }
        }
        
        self.logger.info("✅ 검수 에이전트 초기화 완료")
    
    async def review_article(self, article: Dict[str, Any], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """기사 검수"""
        
        self.logger.info("🔍 기사 검수 시작")
        
        try:
            # 1. 내용 품질 검수
            content_review = self._review_content_quality(article)
            
            # 2. 데이터 정확성 검수
            data_review = self._review_data_accuracy(article, analysis_data)
            
            # 3. 스타일 가이드라인 검수
            style_review = self._review_style_guidelines(article)
            
            # 4. 컴플라이언스 검수
            compliance_review = self._review_compliance(article)
            
            # 5. 전체 점수 계산
            overall_score = self._calculate_overall_score(
                content_review, data_review, style_review, compliance_review
            )
            
            # 6. 개선 제안 생성
            suggestions = self._generate_suggestions(
                content_review, data_review, style_review, compliance_review
            )
            
            # 7. 최종 승인 여부 결정
            approval_status = self._determine_approval_status(overall_score, suggestions)
            
            review_result = {
                'review_timestamp': datetime.now().isoformat(),
                'overall_score': overall_score,
                'quality_score': content_review['score'],
                'accuracy_score': data_review['score'],
                'style_score': style_review['score'],
                'compliance_score': compliance_review['score'],
                'approval_status': approval_status,
                'suggestions': suggestions,
                'detailed_review': {
                    'content_quality': content_review,
                    'data_accuracy': data_review,
                    'style_guidelines': style_review,
                    'compliance': compliance_review
                },
                'reviewer': 'AI 검수 시스템'
            }
            
            self.logger.info(f"✅ 기사 검수 완료 (점수: {overall_score:.1f}/10)")
            return review_result
            
        except Exception as e:
            self.logger.error(f"❌ 기사 검수 실패: {e}")
            return {
                'error': str(e),
                'review_timestamp': datetime.now().isoformat(),
                'overall_score': 0
            }
    
    def _review_content_quality(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """내용 품질 검수"""
        
        try:
            content = article.get('content', '')
            word_count = article.get('word_count', len(content.split()))
            
            issues = []
            score = 10.0
            
            # 1. 단어 수 검사
            min_words = self.review_criteria['content_quality']['min_word_count']
            max_words = self.review_criteria['content_quality']['max_word_count']
            
            if word_count < min_words:
                issues.append(f"내용이 너무 짧습니다 ({word_count}단어 < {min_words}단어)")
                score -= 2.0
            elif word_count > max_words:
                issues.append(f"내용이 너무 깁니다 ({word_count}단어 > {max_words}단어)")
                score -= 1.0
            
            # 2. 필수 섹션 검사
            required_sections = self.review_criteria['content_quality']['required_sections']
            for section in required_sections:
                if section not in content:
                    issues.append(f"필수 섹션 누락: {section}")
                    score -= 1.5
            
            # 3. 금지 단어 검사
            forbidden_words = self.review_criteria['content_quality']['forbidden_words']
            for word in forbidden_words:
                if word in content:
                    issues.append(f"부적절한 표현 사용: {word}")
                    score -= 2.0
            
            # 4. 구조적 완성도 검사
            if not article.get('title'):
                issues.append("제목이 없습니다")
                score -= 1.0
            
            if not article.get('lead_paragraph'):
                issues.append("리드 문단이 없습니다")
                score -= 1.0
            
            if not article.get('conclusion'):
                issues.append("결론이 없습니다")
                score -= 1.0
            
            return {
                'score': max(0, score),
                'issues': issues,
                'word_count': word_count,
                'structure_complete': len(issues) == 0
            }
            
        except Exception as e:
            self.logger.error(f"내용 품질 검수 실패: {e}")
            return {'score': 0, 'issues': [f"검수 오류: {e}"]}
    
    def _review_data_accuracy(self, article: Dict[str, Any], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 정확성 검수"""
        
        try:
            issues = []
            score = 10.0
            
            # 메타데이터에서 데이터 추출
            metadata = article.get('metadata', {})
            raw_data = analysis_data.get('raw_data', {})
            
            # 1. 필수 데이터 포인트 검사
            required_points = self.review_criteria['data_accuracy']['required_data_points']
            for point in required_points:
                if point not in metadata and point not in raw_data:
                    issues.append(f"필수 데이터 누락: {point}")
                    score -= 2.0
            
            # 2. 데이터 일관성 검사
            article_change = metadata.get('change_percent')
            data_change = raw_data.get('change_percent')
            
            if article_change is not None and data_change is not None:
                variance = abs(article_change - data_change) / max(abs(data_change), 1)
                acceptable_variance = self.review_criteria['data_accuracy']['acceptable_variance']
                
                if variance > acceptable_variance:
                    issues.append(f"데이터 불일치: 변화율 차이 {variance:.2%}")
                    score -= 3.0
            
            # 3. 데이터 품질 검사
            data_quality = analysis_data.get('data_quality', {})
            completeness = data_quality.get('data_completeness', 100)
            
            if completeness < 90:
                issues.append(f"데이터 품질 부족: 완성도 {completeness:.1f}%")
                score -= 1.0
            
            # 4. 시간 정확성 검사
            analysis_timestamp = analysis_data.get('analysis_timestamp')
            if analysis_timestamp:
                try:
                    analysis_time = datetime.fromisoformat(analysis_timestamp.replace('Z', '+00:00'))
                    time_diff = (datetime.now() - analysis_time).total_seconds() / 3600
                    
                    if time_diff > 24:  # 24시간 이상 된 데이터
                        issues.append(f"데이터가 오래됨: {time_diff:.1f}시간 전")
                        score -= 1.0
                except:
                    issues.append("분석 시간 정보 오류")
                    score -= 0.5
            
            return {
                'score': max(0, score),
                'issues': issues,
                'data_freshness': time_diff if 'time_diff' in locals() else 0,
                'data_completeness': completeness
            }
            
        except Exception as e:
            self.logger.error(f"데이터 정확성 검수 실패: {e}")
            return {'score': 0, 'issues': [f"검수 오류: {e}"]}
    
    def _review_style_guidelines(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """스타일 가이드라인 검수"""
        
        try:
            content = article.get('content', '')
            issues = []
            score = 10.0
            
            # 1. 객관성 검사
            subjective_words = ['확실히', '틀림없이', '반드시', '절대', '무조건']
            subjective_count = sum(content.count(word) for word in subjective_words)
            
            if subjective_count > 3:
                issues.append(f"주관적 표현 과다: {subjective_count}개")
                score -= 1.5
            
            # 2. 추측성 표현 검사
            speculative_words = ['아마도', '추정', '예상', '것으로 보인다', '가능성']
            speculative_count = sum(content.count(word) for word in speculative_words)
            total_words = len(content.split())
            
            if total_words > 0:
                speculation_ratio = speculative_count / total_words
                limit = self.review_criteria['style_guidelines']['speculation_limit']
                
                if speculation_ratio > limit:
                    issues.append(f"추측성 표현 과다: {speculation_ratio:.1%}")
                    score -= 2.0
            
            # 3. 전문성 검사
            technical_terms = ['기술적 분석', '이동평균', 'RSI', 'MACD', '볼린저 밴드', '지지선', '저항선']
            technical_count = sum(content.count(term) for term in technical_terms)
            
            if technical_count == 0:
                issues.append("전문 용어 부족")
                score -= 1.0
            
            # 4. 문장 구조 검사
            sentences = content.split('.')
            long_sentences = [s for s in sentences if len(s.split()) > 30]
            
            if len(long_sentences) > len(sentences) * 0.3:
                issues.append("긴 문장 과다")
                score -= 1.0
            
            return {
                'score': max(0, score),
                'issues': issues,
                'objectivity_score': max(0, 10 - subjective_count),
                'speculation_ratio': speculation_ratio if 'speculation_ratio' in locals() else 0,
                'technical_depth': technical_count
            }
            
        except Exception as e:
            self.logger.error(f"스타일 가이드라인 검수 실패: {e}")
            return {'score': 0, 'issues': [f"검수 오류: {e}"]}
    
    def _review_compliance(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """컴플라이언스 검수"""
        
        try:
            content = article.get('content', '')
            metadata = article.get('metadata', {})
            issues = []
            score = 10.0
            
            # 1. 면책 조항 검사
            disclaimer_keywords = ['투자 조언이 아닙니다', '신중한 투자', '리스크']
            has_disclaimer = any(keyword in content for keyword in disclaimer_keywords)
            
            if not has_disclaimer:
                issues.append("면책 조항 누락")
                score -= 3.0
            
            # 2. 출처 표시 검사
            sources = metadata.get('sources', [])
            if not sources:
                issues.append("데이터 출처 누락")
                score -= 2.0
            
            # 3. 리스크 경고 검사
            risk_keywords = ['위험', '리스크', '주의', '신중']
            risk_mentions = sum(content.count(keyword) for keyword in risk_keywords)
            
            if risk_mentions == 0:
                issues.append("리스크 경고 부족")
                score -= 2.0
            
            # 4. 투자 조언 금지 검사
            advice_keywords = ['매수하세요', '매도하세요', '추천합니다', '사야 합니다']
            has_advice = any(keyword in content for keyword in advice_keywords)
            
            if has_advice:
                issues.append("투자 조언 포함 (금지)")
                score -= 5.0
            
            # 5. 작성자 정보 검사
            author = article.get('author')
            if not author:
                issues.append("작성자 정보 누락")
                score -= 1.0
            
            return {
                'score': max(0, score),
                'issues': issues,
                'has_disclaimer': has_disclaimer,
                'has_sources': len(sources) > 0,
                'risk_warnings': risk_mentions,
                'compliance_level': 'high' if score >= 8 else 'medium' if score >= 5 else 'low'
            }
            
        except Exception as e:
            self.logger.error(f"컴플라이언스 검수 실패: {e}")
            return {'score': 0, 'issues': [f"검수 오류: {e}"]}
    
    def _calculate_overall_score(self, content_review: Dict, data_review: Dict, 
                                style_review: Dict, compliance_review: Dict) -> float:
        """전체 점수 계산"""
        
        # 가중 평균 계산
        weights = {
            'content': 0.3,
            'data': 0.3,
            'style': 0.2,
            'compliance': 0.2
        }
        
        overall_score = (
            content_review['score'] * weights['content'] +
            data_review['score'] * weights['data'] +
            style_review['score'] * weights['style'] +
            compliance_review['score'] * weights['compliance']
        )
        
        return round(overall_score, 1)
    
    def _generate_suggestions(self, content_review: Dict, data_review: Dict,
                            style_review: Dict, compliance_review: Dict) -> List[str]:
        """개선 제안 생성"""
        
        suggestions = []
        
        # 내용 품질 개선 제안
        if content_review['score'] < 7:
            suggestions.extend([
                "기사 내용을 더 상세히 작성하세요",
                "필수 섹션(분석, 전망)을 포함하세요",
                "적절한 분량을 유지하세요"
            ])
        
        # 데이터 정확성 개선 제안
        if data_review['score'] < 7:
            suggestions.extend([
                "최신 데이터를 사용하세요",
                "데이터 일관성을 확인하세요",
                "필수 데이터 포인트를 포함하세요"
            ])
        
        # 스타일 개선 제안
        if style_review['score'] < 7:
            suggestions.extend([
                "객관적인 표현을 사용하세요",
                "추측성 표현을 줄이세요",
                "전문 용어를 적절히 사용하세요"
            ])
        
        # 컴플라이언스 개선 제안
        if compliance_review['score'] < 7:
            suggestions.extend([
                "면책 조항을 추가하세요",
                "데이터 출처를 명시하세요",
                "리스크 경고를 포함하세요",
                "투자 조언 표현을 제거하세요"
            ])
        
        return suggestions[:5]  # 최대 5개 제안
    
    def _determine_approval_status(self, overall_score: float, suggestions: List[str]) -> str:
        """승인 상태 결정"""
        
        if overall_score >= 8.0 and len(suggestions) <= 2:
            return "approved"
        elif overall_score >= 6.0:
            return "conditional_approval"
        else:
            return "revision_required"
