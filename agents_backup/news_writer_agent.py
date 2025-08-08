"""
경제 기사 작성 Agent
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .base_agent import BaseAgent, AgentConfig


class NewsWriterAgent(BaseAgent):
    """경제 기사 작성을 담당하는 Agent"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        
        # 기사 템플릿 설정
        self.article_templates = {
            "market_summary": "시장 종합 분석",
            "stock_focus": "개별 종목 분석",
            "economic_outlook": "경제 전망",
            "sector_analysis": "섹터별 분석"
        }
    
    def get_system_prompt(self) -> str:
        return """
        당신은 전문 경제 기자입니다. 복잡한 경제 데이터와 시장 정보를 
        일반 투자자들이 이해하기 쉽게 설명하는 고품질 기사를 작성합니다.
        
        기사 작성 원칙:
        1. 객관적이고 균형잡힌 시각 유지
        2. 데이터 기반의 분석 제공
        3. 투자자에게 실용적인 정보 전달
        4. 명확하고 이해하기 쉬운 문체 사용
        5. 리스크와 기회를 균형있게 제시
        
        기사 구조:
        - 헤드라인: 핵심 내용을 담은 매력적인 제목
        - 리드: 주요 내용 요약 (2-3문장)
        - 본문: 상세 분석과 데이터 해석
        - 결론: 투자자를 위한 시사점
        
        전문적이면서도 접근하기 쉬운 기사를 작성하세요.
        """
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """기사 작성 프로세스"""
        self.log_activity("기사 작성 시작")
        
        try:
            # 입력 데이터에서 정보 추출
            collected_data = input_data.get("collected_data", {})
            article_type = input_data.get("article_type", "market_summary")
            target_length = input_data.get("target_length", "medium")  # short, medium, long
            
            # 기사 작성
            article = self.write_article(collected_data, article_type, target_length)
            
            # 기사 품질 검증
            quality_check = self.validate_article_quality(article)
            
            # SEO 최적화 제안
            seo_suggestions = self.generate_seo_suggestions(article)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "article": article,
                "quality_check": quality_check,
                "seo_suggestions": seo_suggestions,
                "metadata": {
                    "article_type": article_type,
                    "target_length": target_length,
                    "word_count": len(article.get("content", "").split())
                }
            }
            
            self.log_activity("기사 작성 완료", {"word_count": result["metadata"]["word_count"]})
            return result
            
        except Exception as e:
            self.logger.error(f"기사 작성 중 오류: {str(e)}")
            raise
    
    def write_article(self, data: Dict[str, Any], article_type: str, target_length: str) -> Dict[str, Any]:
        """기사 작성"""
        
        # 길이별 단어 수 목표
        length_targets = {
            "short": "300-500단어",
            "medium": "500-800단어", 
            "long": "800-1200단어"
        }
        
        # 데이터 요약
        stock_data = data.get("stock_data", {})
        economic_data = data.get("economic_data", {})
        news_data = data.get("news_data", [])
        analysis = data.get("analysis", {})
        
        writing_prompt = f"""
        다음 경제 데이터를 바탕으로 {self.article_templates.get(article_type, article_type)} 기사를 작성해주세요.
        
        목표 길이: {length_targets.get(target_length, "500-800단어")}
        
        수집된 데이터:
        
        주식 시장 데이터:
        {json.dumps(stock_data, ensure_ascii=False, indent=2)}
        
        경제 지표:
        {json.dumps(economic_data, ensure_ascii=False, indent=2)}
        
        관련 뉴스:
        {[item.get('title', '') for item in news_data[:5]]}
        
        데이터 분석:
        {analysis.get('llm_analysis', '')}
        
        다음 JSON 형식으로 기사를 작성해주세요:
        {{
            "headline": "매력적이고 정확한 헤드라인",
            "lead": "주요 내용을 요약한 리드 문단 (2-3문장)",
            "content": "상세한 기사 본문",
            "conclusion": "투자자를 위한 결론 및 시사점",
            "key_points": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"],
            "tags": ["관련", "태그", "목록"]
        }}
        
        기사는 객관적이고 균형잡힌 시각을 유지하며, 데이터에 기반한 분석을 제공해야 합니다.
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": writing_prompt}
        ]
        
        article_response = self.invoke_llm(messages)
        
        try:
            # JSON 응답 파싱
            article_json = json.loads(article_response)
            return article_json
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트 그대로 반환
            return {
                "headline": "경제 시장 분석",
                "lead": "최신 경제 데이터 분석 결과입니다.",
                "content": article_response,
                "conclusion": "투자 결정 시 신중한 검토가 필요합니다.",
                "key_points": ["시장 동향 분석", "투자 포인트", "리스크 요인"],
                "tags": ["경제", "투자", "시장분석"]
            }
    
    def validate_article_quality(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """기사 품질 검증"""
        
        validation_prompt = f"""
        다음 경제 기사의 품질을 평가해주세요:
        
        헤드라인: {article.get('headline', '')}
        리드: {article.get('lead', '')}
        본문: {article.get('content', '')[:500]}...
        
        다음 기준으로 평가하고 개선 제안을 해주세요:
        1. 정확성 (데이터 해석의 정확성)
        2. 명확성 (이해하기 쉬운 설명)
        3. 완성도 (구조적 완성도)
        4. 객관성 (균형잡힌 시각)
        5. 실용성 (투자자에게 유용한 정보)
        
        JSON 형식으로 응답해주세요:
        {{
            "overall_score": 85,
            "scores": {{
                "accuracy": 90,
                "clarity": 85,
                "completeness": 80,
                "objectivity": 90,
                "usefulness": 85
            }},
            "strengths": ["강점 1", "강점 2"],
            "improvements": ["개선점 1", "개선점 2"],
            "recommendation": "전체적인 평가 및 권장사항"
        }}
        """
        
        messages = [
            {"role": "system", "content": "당신은 경제 기사 품질 평가 전문가입니다."},
            {"role": "user", "content": validation_prompt}
        ]
        
        quality_response = self.invoke_llm(messages)
        
        try:
            return json.loads(quality_response)
        except json.JSONDecodeError:
            return {
                "overall_score": 75,
                "scores": {"accuracy": 75, "clarity": 75, "completeness": 75, "objectivity": 75, "usefulness": 75},
                "strengths": ["데이터 기반 분석"],
                "improvements": ["구체적 수치 보완"],
                "recommendation": "전반적으로 양호한 품질의 기사입니다."
            }
    
    def generate_seo_suggestions(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """SEO 최적화 제안"""
        
        seo_prompt = f"""
        다음 경제 기사에 대한 SEO 최적화 제안을 해주세요:
        
        헤드라인: {article.get('headline', '')}
        내용: {article.get('content', '')[:300]}...
        태그: {article.get('tags', [])}
        
        다음 항목에 대한 제안을 JSON 형식으로 제공해주세요:
        {{
            "meta_title": "검색 엔진 최적화된 제목 (60자 이내)",
            "meta_description": "검색 결과에 표시될 설명 (160자 이내)",
            "keywords": ["주요", "키워드", "목록"],
            "suggested_tags": ["추가", "태그", "제안"],
            "internal_links": ["관련 기사 링크 제안"],
            "readability_score": 85,
            "seo_tips": ["SEO 개선 팁 1", "SEO 개선 팁 2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "당신은 SEO 최적화 전문가입니다."},
            {"role": "user", "content": seo_prompt}
        ]
        
        seo_response = self.invoke_llm(messages)
        
        try:
            return json.loads(seo_response)
        except json.JSONDecodeError:
            return {
                "meta_title": article.get('headline', '')[:60],
                "meta_description": article.get('lead', '')[:160],
                "keywords": article.get('tags', []),
                "suggested_tags": ["경제뉴스", "투자정보"],
                "internal_links": [],
                "readability_score": 80,
                "seo_tips": ["키워드 밀도 최적화", "내부 링크 추가"]
            }
    
    def generate_multiple_versions(self, data: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
        """여러 버전의 기사 생성"""
        versions = []
        
        article_types = ["market_summary", "stock_focus", "economic_outlook"]
        
        for i in range(min(count, len(article_types))):
            version_data = {
                "collected_data": data,
                "article_type": article_types[i],
                "target_length": "medium"
            }
            
            version = self.process(version_data)
            versions.append(version)
        
        return versions
