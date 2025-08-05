#!/usr/bin/env python3
"""
고도화된 이벤트 감지 시스템 데모
기술적 분석, 감정 분석, 상관관계 분석을 통합한 종합 이벤트 감지 및 뉴스 생성
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List

from data_monitoring.enhanced_monitor import EnhancedEconomicMonitor
from agents.base_agent import AgentConfig
from agents.news_writer_agent import NewsWriterAgent

class AdvancedEventNewsDemo:
    """고도화된 이벤트 기반 뉴스 생성 데모"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.enhanced_monitor = EnhancedEconomicMonitor()
        
        # 뉴스 작성 Agent 초기화
        self.news_writer = NewsWriterAgent(
            AgentConfig(
                name="AdvancedNewsWriter",
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                region="us-east-1",
                temperature=0.7,
                max_tokens=2000
            )
        )
    
    async def run_demo(self):
        """데모 실행"""
        print("🚀 고도화된 이벤트 감지 및 뉴스 생성 데모 시작")
        print("=" * 60)
        
        try:
            # 1. 고도화된 모니터링 실행
            print("📊 1단계: 고도화된 시장 분석 실행 중...")
            monitoring_result = await self.enhanced_monitor.run_enhanced_monitoring_cycle()
            
            if "error" in monitoring_result:
                print(f"❌ 모니터링 오류: {monitoring_result['error']}")
                return
            
            # 2. 분석 결과 요약 출력
            self._print_analysis_summary(monitoring_result)
            
            # 3. 고도화된 분석 기반 뉴스 생성
            print("\n📝 3단계: AI 뉴스 생성 중...")
            news_article = await self._generate_advanced_news(monitoring_result)
            
            # 4. 결과 출력 및 저장
            self._display_results(monitoring_result, news_article)
            
        except Exception as e:
            self.logger.error(f"데모 실행 중 오류: {str(e)}")
            print(f"❌ 오류 발생: {str(e)}")
    
    def _print_analysis_summary(self, result: Dict):
        """분석 결과 요약 출력"""
        print("\n📈 2단계: 시장 분석 결과")
        print("-" * 40)
        
        print(f"총 감지 이벤트: {result['total_events']}개")
        print(f"  • 기본 이벤트: {result['basic_events_count']}개")
        print(f"  • 고급 이벤트: {result['advanced_events_count']}개")
        
        risk_assessment = result['risk_assessment']
        risk_emoji = {
            "low": "🟢",
            "medium": "🟡", 
            "high": "🟠",
            "very_high": "🔴"
        }
        
        print(f"\n위험도 평가: {risk_emoji.get(risk_assessment['overall_risk_level'], '⚪')} {risk_assessment['overall_risk_level'].upper()}")
        print(f"위험 점수: {risk_assessment['risk_score']:.2f}/1.00")
        
        if risk_assessment['risk_factors']:
            print("주요 위험 요소:")
            for factor in risk_assessment['risk_factors']:
                print(f"  • {factor}")
        
        # 우선순위 알림
        if result['priority_alerts']:
            print("\n🚨 우선순위 알림:")
            for i, alert in enumerate(result['priority_alerts'][:3], 1):
                print(f"  {i}. [{alert['symbol']}] {alert['message']}")
                print(f"     심각도: {alert['severity']:.2f}")
        
        # 고급 분석 인사이트
        advanced_summary = result['advanced_analysis'].get('analysis_summary', {})
        if advanced_summary.get('key_insights'):
            print("\n💡 주요 인사이트:")
            for insight in advanced_summary['key_insights']:
                print(f"  • {insight}")
    
    async def _generate_advanced_news(self, monitoring_result: Dict) -> str:
        """고도화된 분석 기반 뉴스 생성"""
        try:
            # 뉴스 생성용 데이터 준비
            news_data = {
                "market_analysis": monitoring_result['news_summary'],
                "risk_assessment": monitoring_result['risk_assessment'],
                "priority_events": monitoring_result['priority_alerts'][:5],
                "advanced_insights": monitoring_result['advanced_analysis'].get('analysis_summary', {}),
                "timestamp": monitoring_result['timestamp']
            }
            
            # 뉴스 작성 Agent 실행
            article_result = self.news_writer.process({
                "article_type": "advanced_market_analysis",
                "market_data": news_data,
                "length": "medium",
                "focus": ["technical_analysis", "sentiment_analysis", "risk_assessment"]
            })
            
            return article_result.get('article', '뉴스 생성에 실패했습니다.')
            
        except Exception as e:
            self.logger.error(f"뉴스 생성 중 오류: {str(e)}")
            return f"뉴스 생성 중 오류가 발생했습니다: {str(e)}"
    
    def _display_results(self, monitoring_result: Dict, news_article: str):
        """결과 출력 및 저장"""
        print("\n" + "=" * 60)
        print("📰 생성된 AI 뉴스 기사")
        print("=" * 60)
        print(news_article)
        
        # 결과 파일 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON 결과 저장
        result_data = {
            "timestamp": timestamp,
            "monitoring_result": monitoring_result,
            "generated_article": news_article
        }
        
        json_filename = f"output/advanced_demo_{timestamp}.json"
        try:
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 결과 저장: {json_filename}")
        except Exception as e:
            print(f"❌ 파일 저장 실패: {str(e)}")
        
        print("\n✅ 고도화된 이벤트 감지 및 뉴스 생성 데모 완료!")

def setup_logging():
    """로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/advanced_demo.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

async def main():
    """메인 함수"""
    setup_logging()
    
    demo = AdvancedEventNewsDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
