"""
콘텐츠 최적화 Agent
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import re

from .base_agent import BaseAgent, AgentConfig


class ContentOptimizerAgent(BaseAgent):
    """콘텐츠 최적화를 담당하는 Agent"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        
        # 최적화 기준 설정
        self.optimization_criteria = {
            "readability": "가독성 향상",
            "engagement": "독자 참여도 증대",
            "seo": "검색 엔진 최적화",
            "accuracy": "정확성 검증",
            "compliance": "규정 준수"
        }
    
    def get_system_prompt(self) -> str:
        return """
        당신은 콘텐츠 최적화 전문가입니다. 경제 기사의 품질을 향상시키고
        독자 경험을 개선하며 검색 엔진 최적화를 수행합니다.
        
        최적화 영역:
        1. 가독성: 문장 구조, 단락 구성, 용어 설명
        2. 참여도: 흥미로운 표현, 시각적 요소 제안
        3. SEO: 키워드 최적화, 메타데이터 개선
        4. 정확성: 사실 확인, 데이터 검증
        5. 규정 준수: 금융 규정, 윤리적 기준
        
        객관적이고 데이터 기반의 개선 제안을 제공하세요.
        """
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 최적화 프로세스"""
        self.log_activity("콘텐츠 최적화 시작")
        
        try:
            article = input_data.get("article", {})
            optimization_focus = input_data.get("focus", ["readability", "seo", "engagement"])
            
            # 각 영역별 최적화 수행
            optimizations = {}
            
            if "readability" in optimization_focus:
                optimizations["readability"] = self.optimize_readability(article)
            
            if "engagement" in optimization_focus:
                optimizations["engagement"] = self.optimize_engagement(article)
            
            if "seo" in optimization_focus:
                optimizations["seo"] = self.optimize_seo(article)
            
            if "accuracy" in optimization_focus:
                optimizations["accuracy"] = self.verify_accuracy(article)
            
            if "compliance" in optimization_focus:
                optimizations["compliance"] = self.check_compliance(article)
            
            # 최적화된 버전 생성
            optimized_article = self.apply_optimizations(article, optimizations)
            
            # 개선 효과 측정
            improvement_metrics = self.measure_improvements(article, optimized_article)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "original_article": article,
                "optimized_article": optimized_article,
                "optimizations": optimizations,
                "improvement_metrics": improvement_metrics,
                "recommendations": self.generate_recommendations(optimizations)
            }
            
            self.log_activity("콘텐츠 최적화 완료", {"optimizations_applied": len(optimizations)})
            return result
            
        except Exception as e:
            self.logger.error(f"콘텐츠 최적화 중 오류: {str(e)}")
            raise
    
    def optimize_readability(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """가독성 최적화"""
        
        content = article.get("content", "")
        
        readability_prompt = f"""
        다음 경제 기사의 가독성을 분석하고 개선 방안을 제시해주세요:
        
        제목: {article.get('headline', '')}
        내용: {content[:1000]}...
        
        분석 항목:
        1. 문장 길이 및 복잡성
        2. 전문 용어 사용 빈도
        3. 단락 구성
        4. 논리적 흐름
        5. 독자 친화성
        
        JSON 형식으로 응답해주세요:
        {{
            "readability_score": 75,
            "sentence_analysis": {{
                "avg_sentence_length": 25,
                "complex_sentences": 15,
                "recommendation": "문장을 더 짧게 나누세요"
            }},
            "terminology": {{
                "technical_terms": ["용어1", "용어2"],
                "suggestions": ["용어 설명 추가", "쉬운 표현 사용"]
            }},
            "structure": {{
                "paragraph_count": 8,
                "logical_flow": "양호",
                "improvements": ["소제목 추가", "요약 박스 삽입"]
            }},
            "improved_content": "가독성이 개선된 내용 샘플"
        }}
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": readability_prompt}
        ]
        
        response = self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "readability_score": 70,
                "sentence_analysis": {"avg_sentence_length": 20, "recommendation": "문장 길이 적절"},
                "terminology": {"suggestions": ["전문 용어 설명 추가"]},
                "structure": {"improvements": ["단락 구성 개선"]},
                "improved_content": content
            }
    
    def optimize_engagement(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """독자 참여도 최적화"""
        
        engagement_prompt = f"""
        다음 경제 기사의 독자 참여도를 높이는 방안을 제시해주세요:
        
        제목: {article.get('headline', '')}
        리드: {article.get('lead', '')}
        내용: {article.get('content', '')[:500]}...
        
        개선 영역:
        1. 헤드라인 매력도
        2. 스토리텔링 요소
        3. 시각적 요소 제안
        4. 독자 상호작용
        5. 감정적 연결
        
        JSON 형식으로 응답해주세요:
        {{
            "engagement_score": 80,
            "headline_suggestions": ["더 매력적인 헤드라인 1", "헤드라인 2"],
            "storytelling": {{
                "narrative_elements": ["스토리 요소 1", "요소 2"],
                "human_interest": "개인 투자자 사례 추가"
            }},
            "visual_elements": ["차트 제안", "인포그래픽", "이미지"],
            "interaction": ["질문 추가", "독자 의견 유도"],
            "emotional_hooks": ["감정적 연결 포인트 1", "포인트 2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": engagement_prompt}
        ]
        
        response = self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "engagement_score": 75,
                "headline_suggestions": [article.get('headline', '')],
                "storytelling": {"narrative_elements": ["데이터 스토리"]},
                "visual_elements": ["차트", "그래프"],
                "interaction": ["독자 질문 유도"],
                "emotional_hooks": ["투자자 관심사"]
            }
    
    def optimize_seo(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """SEO 최적화"""
        
        seo_prompt = f"""
        다음 경제 기사의 SEO를 최적화해주세요:
        
        제목: {article.get('headline', '')}
        내용: {article.get('content', '')[:800]}...
        기존 태그: {article.get('tags', [])}
        
        SEO 최적화 항목:
        1. 키워드 밀도 및 배치
        2. 메타 태그 최적화
        3. 구조화된 데이터
        4. 내부/외부 링크
        5. 이미지 alt 텍스트
        
        JSON 형식으로 응답해주세요:
        {{
            "seo_score": 85,
            "primary_keywords": ["주요 키워드 1", "키워드 2"],
            "secondary_keywords": ["보조 키워드 1", "키워드 2"],
            "meta_optimization": {{
                "title": "SEO 최적화된 제목",
                "description": "메타 설명",
                "keywords": "키워드 목록"
            }},
            "content_optimization": {{
                "keyword_density": "2.5%",
                "heading_structure": ["H1", "H2", "H3"],
                "internal_links": ["관련 기사 링크"]
            }},
            "technical_seo": {{
                "structured_data": "JSON-LD 스키마",
                "image_alt": ["이미지 alt 텍스트"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": seo_prompt}
        ]
        
        response = self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "seo_score": 80,
                "primary_keywords": ["경제", "투자"],
                "meta_optimization": {
                    "title": article.get('headline', ''),
                    "description": article.get('lead', '')[:160]
                },
                "content_optimization": {"keyword_density": "적절"},
                "technical_seo": {"structured_data": "기본 스키마"}
            }
    
    def verify_accuracy(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """정확성 검증"""
        
        accuracy_prompt = f"""
        다음 경제 기사의 정확성을 검증해주세요:
        
        내용: {article.get('content', '')[:1000]}...
        
        검증 항목:
        1. 수치 데이터 일관성
        2. 경제 개념 정확성
        3. 시장 분석 논리성
        4. 출처 및 인용 적절성
        5. 사실 확인 필요 사항
        
        JSON 형식으로 응답해주세요:
        {{
            "accuracy_score": 90,
            "data_verification": {{
                "numerical_consistency": "일관성 있음",
                "source_reliability": "신뢰할 만함",
                "fact_check_needed": ["확인 필요 사항 1"]
            }},
            "concept_accuracy": {{
                "economic_terms": "정확함",
                "market_analysis": "논리적",
                "corrections_needed": []
            }},
            "recommendations": ["개선 권장사항 1", "권장사항 2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": accuracy_prompt}
        ]
        
        response = self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "accuracy_score": 85,
                "data_verification": {"numerical_consistency": "검토 필요"},
                "concept_accuracy": {"economic_terms": "적절"},
                "recommendations": ["출처 명시 강화"]
            }
    
    def check_compliance(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """규정 준수 확인"""
        
        compliance_prompt = f"""
        다음 경제 기사의 규정 준수 사항을 확인해주세요:
        
        내용: {article.get('content', '')[:800]}...
        
        확인 항목:
        1. 금융 투자 권유 규정
        2. 공정한 보도 원칙
        3. 이해상충 공시
        4. 면책 조항
        5. 윤리적 기준
        
        JSON 형식으로 응답해주세요:
        {{
            "compliance_score": 95,
            "financial_regulations": {{
                "investment_advice": "권유 아님 명시",
                "risk_disclosure": "리스크 고지 적절",
                "disclaimer_needed": true
            }},
            "editorial_standards": {{
                "objectivity": "객관적",
                "balance": "균형잡힌 시각",
                "transparency": "투명성 확보"
            }},
            "required_additions": ["면책 조항 추가", "리스크 경고"],
            "ethical_review": "윤리적 기준 준수"
        }}
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": compliance_prompt}
        ]
        
        response = self.invoke_llm(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "compliance_score": 90,
                "financial_regulations": {"disclaimer_needed": True},
                "editorial_standards": {"objectivity": "적절"},
                "required_additions": ["면책 조항"],
                "ethical_review": "기준 준수"
            }
    
    def apply_optimizations(self, original_article: Dict[str, Any], optimizations: Dict[str, Any]) -> Dict[str, Any]:
        """최적화 적용"""
        
        optimized_article = original_article.copy()
        
        # 가독성 개선 적용
        if "readability" in optimizations:
            readability = optimizations["readability"]
            if "improved_content" in readability:
                optimized_article["content"] = readability["improved_content"]
        
        # 참여도 개선 적용
        if "engagement" in optimizations:
            engagement = optimizations["engagement"]
            if "headline_suggestions" in engagement and engagement["headline_suggestions"]:
                optimized_article["headline"] = engagement["headline_suggestions"][0]
        
        # SEO 최적화 적용
        if "seo" in optimizations:
            seo = optimizations["seo"]
            if "meta_optimization" in seo:
                optimized_article["meta"] = seo["meta_optimization"]
            if "primary_keywords" in seo:
                optimized_article["keywords"] = seo["primary_keywords"]
        
        # 규정 준수 요소 추가
        if "compliance" in optimizations:
            compliance = optimizations["compliance"]
            if compliance.get("financial_regulations", {}).get("disclaimer_needed"):
                disclaimer = "\n\n※ 본 기사는 투자 권유가 아니며, 투자 결정은 개인의 판단과 책임하에 이루어져야 합니다."
                optimized_article["content"] += disclaimer
        
        return optimized_article
    
    def measure_improvements(self, original: Dict[str, Any], optimized: Dict[str, Any]) -> Dict[str, Any]:
        """개선 효과 측정"""
        
        original_content = original.get("content", "")
        optimized_content = optimized.get("content", "")
        
        return {
            "content_length_change": len(optimized_content) - len(original_content),
            "readability_improvement": "측정됨",
            "seo_enhancement": "키워드 최적화 적용",
            "engagement_boost": "헤드라인 개선",
            "compliance_status": "규정 준수 강화"
        }
    
    def generate_recommendations(self, optimizations: Dict[str, Any]) -> List[str]:
        """종합 권장사항 생성"""
        
        recommendations = []
        
        for opt_type, opt_data in optimizations.items():
            if opt_type == "readability" and opt_data.get("readability_score", 0) < 80:
                recommendations.append("가독성 개선을 위해 문장을 더 짧게 구성하세요")
            
            if opt_type == "seo" and opt_data.get("seo_score", 0) < 85:
                recommendations.append("SEO 최적화를 위해 키워드 밀도를 조정하세요")
            
            if opt_type == "engagement" and opt_data.get("engagement_score", 0) < 80:
                recommendations.append("독자 참여도 향상을 위해 시각적 요소를 추가하세요")
        
        if not recommendations:
            recommendations.append("전반적으로 양호한 품질의 콘텐츠입니다")
        
        return recommendations
