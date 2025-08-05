#!/usr/bin/env python3
"""
Slack 알림 시스템 데모
실제 경제 데이터 분석 결과를 Slack으로 전송하는 데모
"""

import asyncio
import os
import json
import logging
from datetime import datetime
from typing import Dict

from notifications.integrated_slack_monitor import SlackIntegratedMonitor
from data_monitoring.enhanced_monitor import EnhancedEconomicMonitor

class SlackAlertDemo:
    """Slack 알림 데모 클래스"""
    
    def __init__(self, webhook_url: str = None):
        self.logger = logging.getLogger(__name__)
        
        # 웹훅 URL 설정
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        
        if not self.webhook_url or self.webhook_url == "YOUR_SLACK_WEBHOOK_URL_HERE":
            self.demo_mode = True
            self.webhook_url = "https://dummy.webhook.url"
            print("⚠️  데모 모드: 실제 Slack 전송 없이 시뮬레이션만 실행됩니다.")
        else:
            self.demo_mode = False
            print("🔗 실제 Slack 연동 모드로 실행됩니다.")
        
        # 시스템 초기화
        self.slack_monitor = SlackIntegratedMonitor(self.webhook_url)
        self.enhanced_monitor = EnhancedEconomicMonitor()
    
    async def run_demo(self):
        """데모 실행"""
        print("📱 Slack 알림 시스템 데모 시작")
        print("=" * 50)
        
        try:
            # 1. 시스템 상태 확인
            await self._demo_system_status()
            
            # 2. 경제 데이터 분석 실행
            print("\n📊 경제 데이터 분석 실행 중...")
            monitoring_result = await self.enhanced_monitor.run_enhanced_monitoring_cycle()
            
            if "error" in monitoring_result:
                print(f"❌ 분석 실패: {monitoring_result['error']}")
                return
            
            # 3. 분석 결과 요약 출력
            self._print_analysis_summary(monitoring_result)
            
            # 4. Slack 알림 시뮬레이션
            await self._demo_slack_notifications(monitoring_result)
            
            # 5. 결과 저장
            self._save_demo_results(monitoring_result)
            
        except Exception as e:
            self.logger.error(f"데모 실행 중 오류: {str(e)}")
            print(f"❌ 오류 발생: {str(e)}")
    
    async def _demo_system_status(self):
        """시스템 상태 데모"""
        print("🔧 1단계: 시스템 상태 확인")
        print("-" * 30)
        
        status = self.enhanced_monitor.get_monitoring_status()
        
        print(f"모니터링 상태: {'🟢 활성' if status.get('is_running', False) else '🔴 비활성'}")
        print(f"모니터링 심볼: {status.get('monitoring_symbols_count', 0)}개")
        print(f"최근 위험도: {status.get('latest_risk_level', 'unknown').upper()}")
        
        if not self.demo_mode:
            print("📤 시스템 상태를 Slack으로 전송 중...")
            await self.slack_monitor.slack_notifier.send_system_status(status)
            print("✅ 시스템 상태 알림 전송 완료")
        else:
            print("💭 [시뮬레이션] 시스템 상태 알림 전송됨")
    
    def _print_analysis_summary(self, result: Dict):
        """분석 결과 요약 출력"""
        print("\n📈 2단계: 분석 결과 요약")
        print("-" * 30)
        
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
        
        if result['priority_alerts']:
            print(f"\n🚨 우선순위 알림 {len(result['priority_alerts'])}개:")
            for i, alert in enumerate(result['priority_alerts'][:3], 1):
                print(f"  {i}. [{alert['symbol']}] {alert['message']}")
                print(f"     심각도: {alert['severity']:.2f}")
    
    async def _demo_slack_notifications(self, monitoring_result: Dict):
        """Slack 알림 데모"""
        print("\n📱 3단계: Slack 알림 시뮬레이션")
        print("-" * 30)
        
        # 시장 요약 알림
        print("📊 시장 요약 알림 생성 중...")
        if not self.demo_mode:
            success = await self.slack_monitor.slack_notifier.send_market_summary(monitoring_result)
            print(f"{'✅ 성공' if success else '❌ 실패'}: 시장 요약 알림")
        else:
            print("💭 [시뮬레이션] 시장 요약 알림 전송됨")
            self._simulate_market_summary_message(monitoring_result)
        
        # 긴급 알림
        priority_alerts = monitoring_result.get('priority_alerts', [])
        high_severity_alerts = [alert for alert in priority_alerts if alert['severity'] > 0.7]
        
        if high_severity_alerts:
            print(f"\n🚨 긴급 알림 {len(high_severity_alerts)}개 전송 중...")
            
            for alert in high_severity_alerts[:3]:  # 최대 3개만
                if not self.demo_mode:
                    from notifications.slack_notifier import create_alert_from_event
                    slack_alert = create_alert_from_event(alert)
                    success = await self.slack_monitor.slack_notifier.send_critical_alert(slack_alert)
                    print(f"{'✅ 성공' if success else '❌ 실패'}: {alert['symbol']} 긴급 알림")
                else:
                    print(f"💭 [시뮬레이션] {alert['symbol']} 긴급 알림 전송됨")
                    self._simulate_critical_alert_message(alert)
        else:
            print("ℹ️  긴급 알림 대상 없음 (심각도 0.7 미만)")
        
        # 뉴스 업데이트 알림 (시뮬레이션)
        print(f"\n📰 뉴스 업데이트 알림...")
        if not self.demo_mode:
            news_data = {"article": {"headline": "AI 생성 경제 뉴스 업데이트"}}
            success = await self.slack_monitor.slack_notifier.send_news_notification(news_data)
            print(f"{'✅ 성공' if success else '❌ 실패'}: 뉴스 업데이트 알림")
        else:
            print("💭 [시뮬레이션] 뉴스 업데이트 알림 전송됨")
            self._simulate_news_update_message()
    
    def _simulate_market_summary_message(self, monitoring_result: Dict):
        """시장 요약 메시지 시뮬레이션"""
        risk_level = monitoring_result['risk_assessment']['overall_risk_level']
        total_events = monitoring_result['total_events']
        
        print("📋 [Slack 메시지 미리보기]")
        print("┌─────────────────────────────────────┐")
        print("│ 📊 Market Analysis Summary          │")
        print("├─────────────────────────────────────┤")
        print(f"│ 위험도: {risk_level.upper().replace('_', ' '):<25} │")
        print(f"│ 감지 이벤트: {total_events}개{' ' * (21 - len(str(total_events)))}│")
        print(f"│ 위험 점수: {monitoring_result['risk_assessment']['risk_score']:.2f}/1.00{' ' * 16}│")
        print("└─────────────────────────────────────┘")
    
    def _simulate_critical_alert_message(self, alert: Dict):
        """긴급 알림 메시지 시뮬레이션"""
        print("🚨 [긴급 알림 미리보기]")
        print("┌─────────────────────────────────────┐")
        print("│ 🔴 CRITICAL ALERT                   │")
        print("├─────────────────────────────────────┤")
        print(f"│ 심볼: {alert['symbol']:<29} │")
        print(f"│ 메시지: {alert['message'][:25]:<25} │")
        print(f"│ 심각도: {alert['severity']:.2f}{' ' * 25} │")
        print("└─────────────────────────────────────┘")
    
    def _simulate_news_update_message(self):
        """뉴스 업데이트 메시지 시뮬레이션"""
        print("📰 [뉴스 알림 미리보기]")
        print("┌─────────────────────────────────────┐")
        print("│ 📰 새로운 AI 경제 뉴스 생성         │")
        print("├─────────────────────────────────────┤")
        print("│ • 시장 동향 분석                    │")
        print("│ • 투자 포인트 정리                  │")
        print("│ • 리스크 요인 평가                  │")
        print("└─────────────────────────────────────┘")
    
    def _save_demo_results(self, monitoring_result: Dict):
        """데모 결과 저장"""
        print("\n💾 4단계: 결과 저장")
        print("-" * 30)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        demo_result = {
            "demo_info": {
                "timestamp": timestamp,
                "demo_mode": self.demo_mode,
                "webhook_configured": bool(self.webhook_url and self.webhook_url != "https://dummy.webhook.url")
            },
            "monitoring_result": monitoring_result,
            "slack_simulation": {
                "market_summary_sent": True,
                "critical_alerts_count": len([a for a in monitoring_result.get('priority_alerts', []) if a['severity'] > 0.7]),
                "news_update_sent": True
            }
        }
        
        filename = f"output/slack_demo_{timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(demo_result, f, ensure_ascii=False, indent=2)
            print(f"✅ 데모 결과 저장: {filename}")
        except Exception as e:
            print(f"❌ 저장 실패: {str(e)}")
        
        print("\n🎉 Slack 알림 시스템 데모 완료!")
        
        if self.demo_mode:
            print("\n💡 실제 Slack 연동을 위한 다음 단계:")
            print("1. Slack 웹훅 URL 생성 (SLACK_SETUP_GUIDE.md 참조)")
            print("2. 환경변수 설정: export SLACK_WEBHOOK_URL='your_webhook_url'")
            print("3. 다시 데모 실행: python demo_slack_alerts.py")

def setup_logging():
    """로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/slack_demo.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

async def main():
    """메인 함수"""
    setup_logging()
    
    print("🚀 Slack 알림 시스템 데모")
    print("=" * 40)
    
    # 웹훅 URL 확인
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    if webhook_url:
        print(f"✅ 웹훅 URL 감지됨: {webhook_url[:50]}...")
        confirm = input("실제 Slack으로 알림을 전송하시겠습니까? (y/N): ").strip().lower()
        if confirm != 'y':
            webhook_url = None
            print("📝 시뮬레이션 모드로 실행합니다.")
    else:
        print("ℹ️  웹훅 URL이 설정되지 않았습니다. 시뮬레이션 모드로 실행합니다.")
    
    # 데모 실행
    demo = SlackAlertDemo(webhook_url)
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
