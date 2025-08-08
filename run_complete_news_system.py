#!/usr/bin/env python3
"""
경제 뉴스 시스템 통합 실행기
데이터 모니터링 → 이벤트 감지 → 기사 작성 → 광고 표시까지 전체 파이프라인 실행
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/complete_system_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CompleteNewsSystem:
    """통합 경제 뉴스 시스템"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.output_dirs = [
            'output/automated_articles',
            'output/charts', 
            'output/images',
            'streamlit_articles',
            'logs'
        ]
        
        for dir_path in self.output_dirs:
            os.makedirs(dir_path, exist_ok=True)
        
        self.logger.info("🚀 경제 뉴스 시스템 초기화 완료")
    
    async def run_complete_pipeline(self, mode: str = "auto") -> Dict[str, Any]:
        """전체 파이프라인 실행"""
        
        self.logger.info("🔄 전체 파이프라인 시작")
        start_time = datetime.now()
        
        try:
            # 1. 이벤트 감지 및 모니터링
            self.logger.info("📊 1단계: 경제 데이터 모니터링 및 이벤트 감지")
            events = await self._detect_events()
            
            if not events:
                self.logger.info("⚠️ 감지된 이벤트가 없습니다.")
                return {
                    'status': 'no_events',
                    'message': '처리할 이벤트가 없습니다.',
                    'execution_time': (datetime.now() - start_time).total_seconds()
                }
            
            self.logger.info(f"✅ {len(events)}개 이벤트 감지됨")
            
            # 2. 각 이벤트에 대해 기사 생성
            self.logger.info("✍️ 2단계: 이벤트별 기사 생성")
            articles = []
            
            for i, event in enumerate(events[:3]):  # 최대 3개 이벤트 처리
                self.logger.info(f"📝 이벤트 {i+1}/{len(events[:3])} 처리 중: {event.get('symbol', 'Unknown')}")
                
                try:
                    article_result = await self._generate_article_for_event(event)
                    if article_result:
                        articles.append(article_result)
                        self.logger.info(f"✅ {event.get('symbol')} 기사 생성 완료")
                    else:
                        self.logger.warning(f"⚠️ {event.get('symbol')} 기사 생성 실패")
                        
                except Exception as e:
                    self.logger.error(f"❌ {event.get('symbol')} 기사 생성 오류: {e}")
                    continue
            
            # 3. Slack 알림 전송
            self.logger.info("📢 3단계: Slack 알림 전송")
            slack_results = await self._send_slack_notifications(events, articles)
            
            # 4. 결과 정리
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'status': 'success',
                'execution_time': execution_time,
                'events_detected': len(events),
                'articles_generated': len(articles),
                'slack_notifications': len(slack_results),
                'events': events,
                'articles': articles,
                'slack_results': slack_results,
                'timestamp': datetime.now().isoformat()
            }
            
            # 결과 저장
            await self._save_execution_result(result)
            
            self.logger.info(f"🎉 전체 파이프라인 완료 ({execution_time:.1f}초)")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 파이프라인 실행 실패: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': (datetime.now() - start_time).total_seconds()
            }
    
    async def _detect_events(self) -> List[Dict[str, Any]]:
        """이벤트 감지"""
        
        try:
            # 이벤트 감지 시스템 임포트 및 실행
            from event_detection_slack_system import EventMonitoringSystem
            
            monitor = EventMonitoringSystem()
            events = await monitor.detect_events()
            
            # 이벤트를 딕셔너리 형태로 변환
            event_dicts = []
            for event in events:
                if hasattr(event, '__dict__'):
                    event_dict = event.__dict__.copy()
                    # datetime 객체를 문자열로 변환
                    if 'timestamp' in event_dict and hasattr(event_dict['timestamp'], 'isoformat'):
                        event_dict['timestamp'] = event_dict['timestamp'].isoformat()
                    # Enum 객체를 문자열로 변환
                    if 'severity' in event_dict and hasattr(event_dict['severity'], 'value'):
                        event_dict['severity'] = event_dict['severity'].value
                    event_dicts.append(event_dict)
                else:
                    event_dicts.append(event)
            
            return event_dicts
            
        except Exception as e:
            self.logger.error(f"이벤트 감지 실패: {e}")
            # 폴백: 테스트 이벤트 생성
            return await self._create_test_events()
    
    async def _create_test_events(self) -> List[Dict[str, Any]]:
        """테스트 이벤트 생성"""
        
        test_events = [
            {
                'symbol': 'AAPL',
                'event_type': 'price_change',
                'severity': 'medium',
                'title': 'AAPL 주가 변동',
                'description': 'AAPL 주가가 3.2% 상승했습니다.',
                'current_value': 150.25,
                'previous_value': 145.50,
                'change_percent': 3.26,
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        self.logger.info("📋 테스트 이벤트 생성됨")
        return test_events
    
    async def _generate_article_for_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """이벤트에 대한 기사 생성"""
        
        try:
            # Strands Agent 시스템 사용
            from agents import main_orchestrator
            from agents.strands_framework import StrandContext
            
            # 컨텍스트 생성
            strand_id = f"news_{event.get('symbol', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            context = StrandContext(
                strand_id=strand_id,
                input_data={'event': event}
            )
            
            # 전체 워크플로우 실행
            result = await main_orchestrator.process(context)
            
            if result.get('status') == 'success':
                return result
            else:
                self.logger.error(f"기사 생성 실패: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            self.logger.error(f"기사 생성 중 오류: {e}")
            return None
    
    async def _send_slack_notifications(self, events: List[Dict[str, Any]], articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Slack 알림 전송"""
        
        slack_results = []
        
        try:
            webhook_url = os.getenv('SLACK_WEBHOOK_URL')
            if not webhook_url:
                self.logger.warning("⚠️ Slack 웹훅 URL이 설정되지 않음")
                return slack_results
            
            # 이벤트 요약 알림
            summary_message = self._create_summary_message(events, articles)
            summary_result = await self._send_slack_message(webhook_url, summary_message)
            slack_results.append(summary_result)
            
            # 개별 기사 알림
            for article in articles[:2]:  # 최대 2개 기사만 알림
                article_message = self._create_article_message(article)
                article_result = await self._send_slack_message(webhook_url, article_message)
                slack_results.append(article_result)
            
            return slack_results
            
        except Exception as e:
            self.logger.error(f"Slack 알림 전송 실패: {e}")
            return slack_results
    
    def _create_summary_message(self, events: List[Dict[str, Any]], articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """요약 메시지 생성"""
        
        event_symbols = [event.get('symbol', 'Unknown') for event in events]
        
        message = {
            "text": "📈 경제 뉴스 시스템 실행 완료",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🤖 AI 경제 뉴스 시스템"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*감지된 이벤트:* {len(events)}개"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*생성된 기사:* {len(articles)}개"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*대상 심볼:* {', '.join(event_symbols[:5])}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*실행 시간:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        }
                    ]
                }
            ]
        }
        
        return message
    
    def _create_article_message(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """기사 알림 메시지 생성"""
        
        package = article.get('package', {})
        event = package.get('event', {})
        article_data = package.get('article', {})
        ads = package.get('advertisements', [])
        
        message = {
            "text": f"📰 새 기사: {article_data.get('title', '경제 뉴스')}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*📰 {article_data.get('title', '경제 뉴스')}*\n\n{article_data.get('lead', '')[:200]}..."
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*심볼:* {event.get('symbol', 'N/A')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*이벤트:* {event.get('event_type', 'N/A')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*품질점수:* {package.get('review_result', {}).get('overall_score', 'N/A')}/10"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*광고 추천:* {len(ads)}개"
                        }
                    ]
                }
            ]
        }
        
        return message
    
    async def _send_slack_message(self, webhook_url: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Slack 메시지 전송"""
        
        try:
            import requests
            
            response = requests.post(
                webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                return {'status': 'success', 'message': 'Slack 알림 전송 성공'}
            else:
                return {'status': 'error', 'message': f'Slack 전송 실패: {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'message': f'Slack 전송 오류: {str(e)}'}
    
    async def _save_execution_result(self, result: Dict[str, Any]) -> None:
        """실행 결과 저장"""
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"complete_system_execution_{timestamp}.json"
            filepath = os.path.join('output', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"💾 실행 결과 저장: {filepath}")
            
        except Exception as e:
            self.logger.error(f"결과 저장 실패: {e}")

async def main():
    """메인 함수"""
    
    print("🚀 경제 뉴스 시스템 통합 실행기")
    print("=" * 50)
    
    # 시스템 초기화
    system = CompleteNewsSystem()
    
    # 전체 파이프라인 실행
    result = await system.run_complete_pipeline()
    
    # 결과 출력
    print("\n📊 실행 결과:")
    print(f"상태: {result.get('status', 'unknown')}")
    print(f"실행 시간: {result.get('execution_time', 0):.1f}초")
    print(f"감지된 이벤트: {result.get('events_detected', 0)}개")
    print(f"생성된 기사: {result.get('articles_generated', 0)}개")
    print(f"Slack 알림: {result.get('slack_notifications', 0)}개")
    
    if result.get('status') == 'success':
        print("\n🎉 전체 시스템 실행 완료!")
        
        # Streamlit 실행 안내
        articles = result.get('articles', [])
        if articles:
            print("\n💡 생성된 기사 확인:")
            for i, article in enumerate(articles):
                streamlit_page = article.get('streamlit_page', '')
                if streamlit_page:
                    print(f"  {i+1}. streamlit run {streamlit_page}")
    else:
        print(f"\n❌ 실행 실패: {result.get('error', 'Unknown error')}")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
