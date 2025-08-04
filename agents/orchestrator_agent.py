"""
오케스트레이터 Agent - 전체 시스템 조율
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import os

from .base_agent import BaseAgent, AgentConfig
from .data_collector_agent import DataCollectorAgent
from .news_writer_agent import NewsWriterAgent
from .content_optimizer_agent import ContentOptimizerAgent


class OrchestratorAgent(BaseAgent):
    """전체 경제 뉴스 시스템을 조율하는 마스터 Agent"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        
        # 하위 Agent들 초기화
        self.data_collector = DataCollectorAgent(
            AgentConfig(name="DataCollector", **config.dict(exclude={"name"}))
        )
        
        self.news_writer = NewsWriterAgent(
            AgentConfig(name="NewsWriter", **config.dict(exclude={"name"}))
        )
        
        self.content_optimizer = ContentOptimizerAgent(
            AgentConfig(name="ContentOptimizer", **config.dict(exclude={"name"}))
        )
        
        # 작업 스케줄 설정
        self.schedule_config = {
            "data_collection_interval": 30,  # 30분마다
            "article_generation_interval": 60,  # 1시간마다
            "optimization_interval": 120,  # 2시간마다
        }
        
        # 출력 디렉토리 설정
        self.output_dir = "/home/ec2-user/projects/ABP/economic_news_system/output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_system_prompt(self) -> str:
        return """
        당신은 경제 뉴스 시스템의 마스터 오케스트레이터입니다.
        여러 전문 Agent들을 조율하여 고품질의 경제 기사를 자동으로 생성합니다.
        
        주요 역할:
        1. 데이터 수집 Agent 관리
        2. 기사 작성 Agent 조율
        3. 콘텐츠 최적화 Agent 운영
        4. 전체 워크플로우 모니터링
        5. 품질 관리 및 성능 최적화
        
        효율적이고 안정적인 시스템 운영을 보장하세요.
        """
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """전체 뉴스 생성 프로세스 실행"""
        self.log_activity("경제 뉴스 생성 프로세스 시작")
        
        try:
            workflow_type = input_data.get("workflow_type", "full_pipeline")
            
            if workflow_type == "full_pipeline":
                return self.run_full_pipeline(input_data)
            elif workflow_type == "data_only":
                return self.run_data_collection_only(input_data)
            elif workflow_type == "article_only":
                return self.run_article_generation_only(input_data)
            elif workflow_type == "optimize_only":
                return self.run_optimization_only(input_data)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
                
        except Exception as e:
            self.logger.error(f"프로세스 실행 중 오류: {str(e)}")
            raise
    
    def run_full_pipeline(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """전체 파이프라인 실행"""
        pipeline_start = datetime.now()
        
        # 1단계: 데이터 수집
        self.log_activity("1단계: 데이터 수집 시작")
        collected_data = self.data_collector.process({})
        
        # 2단계: 기사 작성
        self.log_activity("2단계: 기사 작성 시작")
        article_configs = input_data.get("article_configs", [
            {"article_type": "market_summary", "target_length": "medium"},
            {"article_type": "stock_focus", "target_length": "short"},
            {"article_type": "economic_outlook", "target_length": "long"}
        ])
        
        articles = []
        for config in article_configs:
            article_input = {
                "collected_data": collected_data,
                **config
            }
            article_result = self.news_writer.process(article_input)
            articles.append(article_result)
        
        # 3단계: 콘텐츠 최적화
        self.log_activity("3단계: 콘텐츠 최적화 시작")
        optimized_articles = []
        for article_result in articles:
            optimization_input = {
                "article": article_result["article"],
                "focus": ["readability", "seo", "engagement", "compliance"]
            }
            optimized_result = self.content_optimizer.process(optimization_input)
            optimized_articles.append(optimized_result)
        
        # 4단계: 결과 통합 및 저장
        pipeline_result = {
            "timestamp": datetime.now().isoformat(),
            "pipeline_duration": (datetime.now() - pipeline_start).total_seconds(),
            "collected_data": collected_data,
            "articles": articles,
            "optimized_articles": optimized_articles,
            "summary": self.generate_pipeline_summary(collected_data, articles, optimized_articles)
        }
        
        # 결과 저장
        self.save_pipeline_result(pipeline_result)
        
        self.log_activity("전체 파이프라인 완료", {
            "articles_generated": len(articles),
            "duration_seconds": pipeline_result["pipeline_duration"]
        })
        
        return pipeline_result
    
    def run_data_collection_only(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 수집만 실행"""
        self.log_activity("데이터 수집 전용 모드 시작")
        
        collected_data = self.data_collector.process(input_data)
        
        # 데이터 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_file = os.path.join(self.output_dir, f"collected_data_{timestamp}.json")
        self.save_result(collected_data, data_file)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": "data_collection_only",
            "collected_data": collected_data,
            "saved_to": data_file
        }
    
    def run_article_generation_only(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """기사 생성만 실행 (기존 데이터 사용)"""
        self.log_activity("기사 생성 전용 모드 시작")
        
        # 기존 데이터 로드 또는 새로 수집
        collected_data = input_data.get("collected_data")
        if not collected_data:
            collected_data = self.data_collector.process({})
        
        # 기사 생성
        article_config = input_data.get("article_config", {
            "article_type": "market_summary",
            "target_length": "medium"
        })
        
        article_input = {
            "collected_data": collected_data,
            **article_config
        }
        
        article_result = self.news_writer.process(article_input)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        article_file = os.path.join(self.output_dir, f"article_{timestamp}.json")
        self.save_result(article_result, article_file)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": "article_generation_only",
            "article_result": article_result,
            "saved_to": article_file
        }
    
    def run_optimization_only(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 최적화만 실행"""
        self.log_activity("콘텐츠 최적화 전용 모드 시작")
        
        article = input_data.get("article")
        if not article:
            raise ValueError("최적화할 기사가 제공되지 않았습니다")
        
        optimization_input = {
            "article": article,
            "focus": input_data.get("focus", ["readability", "seo", "engagement"])
        }
        
        optimized_result = self.content_optimizer.process(optimization_input)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        optimized_file = os.path.join(self.output_dir, f"optimized_{timestamp}.json")
        self.save_result(optimized_result, optimized_file)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": "optimization_only",
            "optimized_result": optimized_result,
            "saved_to": optimized_file
        }
    
    def generate_pipeline_summary(self, collected_data: Dict, articles: List, optimized_articles: List) -> Dict[str, Any]:
        """파이프라인 실행 요약 생성"""
        
        summary_prompt = f"""
        다음 경제 뉴스 생성 파이프라인 실행 결과를 요약해주세요:
        
        수집된 데이터:
        - 주식 데이터: {len(collected_data.get('stock_data', {}))}개 종목
        - 경제 지표: {len(collected_data.get('economic_data', {}))}개 지표
        - 뉴스 항목: {len(collected_data.get('news_data', []))}개 기사
        
        생성된 기사:
        - 총 {len(articles)}개 기사 생성
        - 기사 유형: {[article.get('metadata', {}).get('article_type', 'unknown') for article in articles]}
        
        최적화 결과:
        - {len(optimized_articles)}개 기사 최적화 완료
        
        다음 JSON 형식으로 요약해주세요:
        {{
            "execution_summary": "전체 실행 요약",
            "data_quality": "수집된 데이터 품질 평가",
            "article_quality": "생성된 기사 품질 평가",
            "optimization_impact": "최적화 효과 평가",
            "recommendations": ["개선 권장사항 1", "권장사항 2"],
            "next_actions": ["다음 실행 시 고려사항"]
        }}
        """
        
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": summary_prompt}
        ]
        
        summary_response = self.invoke_llm(messages)
        
        try:
            return json.loads(summary_response)
        except json.JSONDecodeError:
            return {
                "execution_summary": f"{len(articles)}개 기사 생성 완료",
                "data_quality": "양호",
                "article_quality": "표준",
                "optimization_impact": "개선됨",
                "recommendations": ["정기적 모니터링"],
                "next_actions": ["다음 스케줄 실행"]
            }
    
    def save_pipeline_result(self, result: Dict[str, Any]) -> None:
        """파이프라인 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 전체 결과 저장
        full_result_file = os.path.join(self.output_dir, f"pipeline_result_{timestamp}.json")
        self.save_result(result, full_result_file)
        
        # 개별 기사들을 HTML 형식으로 저장
        for i, article_result in enumerate(result.get("optimized_articles", [])):
            article = article_result.get("optimized_article", {})
            html_content = self.generate_html_article(article)
            
            html_file = os.path.join(self.output_dir, f"article_{timestamp}_{i+1}.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        self.logger.info(f"파이프라인 결과 저장 완료: {full_result_file}")
    
    def generate_html_article(self, article: Dict[str, Any]) -> str:
        """기사를 HTML 형식으로 변환"""
        
        # HTML 템플릿 생성 (f-string 백슬래시 문제 해결)
        content_with_br = article.get('content', '').replace('\n', '<br>')
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in article.get('tags', [])])
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.get('headline', '경제 뉴스')}</title>
    <meta name="description" content="{article.get('lead', '')[:160]}">
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .headline {{ font-size: 2em; font-weight: bold; margin-bottom: 10px; }}
        .lead {{ font-size: 1.2em; color: #666; margin-bottom: 20px; }}
        .content {{ line-height: 1.6; margin-bottom: 20px; }}
        .conclusion {{ background-color: #f5f5f5; padding: 15px; border-left: 4px solid #007cba; }}
        .tags {{ margin-top: 20px; }}
        .tag {{ background-color: #e0e0e0; padding: 5px 10px; margin: 2px; display: inline-block; border-radius: 3px; }}
        .timestamp {{ color: #999; font-size: 0.9em; margin-top: 20px; }}
    </style>
</head>
<body>
    <article>
        <h1 class="headline">{article.get('headline', '')}</h1>
        <p class="lead">{article.get('lead', '')}</p>
        <div class="content">
            {content_with_br}
        </div>
        <div class="conclusion">
            <strong>결론:</strong> {article.get('conclusion', '')}
        </div>
        <div class="tags">
            {tags_html}
        </div>
        <div class="timestamp">
            생성 시간: {current_time}
        </div>
    </article>
</body>
</html>"""
        
        return html_template
    
    def schedule_automated_runs(self) -> None:
        """자동화된 실행 스케줄링"""
        import schedule
        import time
        
        # 정기적 데이터 수집
        schedule.every(self.schedule_config["data_collection_interval"]).minutes.do(
            self.run_scheduled_data_collection
        )
        
        # 정기적 기사 생성
        schedule.every(self.schedule_config["article_generation_interval"]).minutes.do(
            self.run_scheduled_article_generation
        )
        
        self.log_activity("자동화 스케줄 설정 완료")
        
        # 스케줄 실행 루프
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    
    def run_scheduled_data_collection(self) -> None:
        """스케줄된 데이터 수집 실행"""
        try:
            self.log_activity("스케줄된 데이터 수집 시작")
            result = self.run_data_collection_only({})
            self.log_activity("스케줄된 데이터 수집 완료")
        except Exception as e:
            self.logger.error(f"스케줄된 데이터 수집 오류: {str(e)}")
    
    def run_scheduled_article_generation(self) -> None:
        """스케줄된 기사 생성 실행"""
        try:
            self.log_activity("스케줄된 기사 생성 시작")
            result = self.run_full_pipeline({
                "article_configs": [
                    {"article_type": "market_summary", "target_length": "medium"}
                ]
            })
            self.log_activity("스케줄된 기사 생성 완료")
        except Exception as e:
            self.logger.error(f"스케줄된 기사 생성 오류: {str(e)}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 조회"""
        return {
            "timestamp": datetime.now().isoformat(),
            "agents_status": {
                "data_collector": "active",
                "news_writer": "active", 
                "content_optimizer": "active"
            },
            "last_execution": "정보 없음",
            "output_directory": self.output_dir,
            "schedule_config": self.schedule_config
        }
