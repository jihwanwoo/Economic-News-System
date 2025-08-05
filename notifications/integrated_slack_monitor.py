"""
Slack 통합 모니터링 시스템
고도화된 이벤트 감지 결과를 Slack으로 실시간 알림
"""

import asyncio
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notifications.slack_notifier import SlackNotifier, SlackAlert, AlertPriority, create_alert_from_event
from data_monitoring.enhanced_monitor import EnhancedEconomicMonitor

class SlackIntegratedMonitor:
    """Slack 통합 모니터링 시스템"""
    
    def __init__(self, webhook_url: str, channel: str = "#economic-alerts"):
        self.logger = logging.getLogger(__name__)
        
        # 모니터링 시스템 초기화
        self.enhanced_monitor = EnhancedEconomicMonitor()
        
        # Slack 알림 시스템 초기화
        self.slack_notifier = SlackNotifier(webhook_url, channel)
        
        # 알림 설정
        self.notification_settings = {
            "send_summary": True,           # 요약 알림 전송
            "send_critical_alerts": True,   # 긴급 알림 전송
            "send_news_updates": True,      # 뉴스 업데이트 알림
            "send_system_status": True,     # 시스템 상태 알림
            "summary_interval_minutes": 60, # 요약 알림 간격
            "min_alert_severity": 0.6,      # 최소 알림 심각도
        }
        
        # 상태 관리
        self.last_summary_time = None
        self.monitoring_active = False
        self.alert_history = []
    
    async def start_monitoring_with_alerts(self, interval_minutes: int = 30):
        """알림 기능이 포함된 모니터링 시작"""
        self.monitoring_active = True
        self.logger.info("🚀 Slack 통합 모니터링 시작")
        
        # 시작 알림 전송
        await self._send_startup_notification()
        
        try:
            while self.monitoring_active:
                # 모니터링 사이클 실행
                monitoring_result = await self.enhanced_monitor.run_enhanced_monitoring_cycle()
                
                if "error" not in monitoring_result:
                    # 알림 처리
                    await self._process_monitoring_result(monitoring_result)
                else:
                    # 오류 알림
                    await self._send_error_notification(monitoring_result["error"])
                
                # 대기
                await asyncio.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            self.logger.info("사용자에 의한 모니터링 중지")
        except Exception as e:
            self.logger.error(f"모니터링 중 오류: {str(e)}")
            await self._send_error_notification(str(e))
        finally:
            self.monitoring_active = False
            await self._send_shutdown_notification()
    
    async def run_single_analysis_with_alerts(self):
        """단일 분석 실행 및 알림"""
        self.logger.info("📊 단일 분석 및 알림 실행")
        
        try:
            # 모니터링 실행
            monitoring_result = await self.enhanced_monitor.run_enhanced_monitoring_cycle()
            
            if "error" not in monitoring_result:
                # 알림 처리
                await self._process_monitoring_result(monitoring_result)
                return monitoring_result
            else:
                await self._send_error_notification(monitoring_result["error"])
                return monitoring_result
                
        except Exception as e:
            self.logger.error(f"단일 분석 중 오류: {str(e)}")
            await self._send_error_notification(str(e))
            return {"error": str(e)}
    
    async def _process_monitoring_result(self, monitoring_result: Dict):
        """모니터링 결과 처리 및 알림 전송"""
        try:
            # 1. 긴급 알림 처리
            if self.notification_settings["send_critical_alerts"]:
                await self._send_critical_alerts(monitoring_result)
            
            # 2. 요약 알림 처리
            if self.notification_settings["send_summary"]:
                await self._send_summary_if_needed(monitoring_result)
            
            # 3. 뉴스 업데이트 알림 (뉴스가 생성된 경우)
            if (self.notification_settings["send_news_updates"] and 
                monitoring_result.get('news_generated')):
                await self.slack_notifier.send_news_notification(monitoring_result)
            
            # 4. 알림 히스토리 업데이트
            self._update_alert_history(monitoring_result)
            
        except Exception as e:
            self.logger.error(f"알림 처리 중 오류: {str(e)}")
    
    async def _send_critical_alerts(self, monitoring_result: Dict):
        """긴급 알림 전송"""
        try:
            # 우선순위 알림에서 긴급 알림 추출
            priority_alerts = monitoring_result.get('priority_alerts', [])
            
            for alert_data in priority_alerts:
                severity = alert_data.get('severity', 0.5)
                
                # 최소 심각도 체크
                if severity < self.notification_settings["min_alert_severity"]:
                    continue
                
                # SlackAlert 생성
                slack_alert = create_alert_from_event(alert_data)
                
                # 알림 전송
                success = await self.slack_notifier.send_critical_alert(slack_alert)
                
                if success:
                    self.logger.info(f"긴급 알림 전송 완료: {alert_data['symbol']}")
                else:
                    self.logger.warning(f"긴급 알림 전송 실패: {alert_data['symbol']}")
            
            # 고위험 상황 특별 알림
            risk_level = monitoring_result['risk_assessment']['overall_risk_level']
            if risk_level == "very_high":
                await self._send_high_risk_alert(monitoring_result)
                
        except Exception as e:
            self.logger.error(f"긴급 알림 전송 중 오류: {str(e)}")
    
    async def _send_high_risk_alert(self, monitoring_result: Dict):
        """고위험 상황 특별 알림"""
        try:
            risk_assessment = monitoring_result['risk_assessment']
            
            special_alert = SlackAlert(
                title="🚨 HIGH RISK MARKET CONDITION",
                message=f"시장 위험도가 매우 높은 수준에 도달했습니다.\n"
                       f"위험 점수: {risk_assessment['risk_score']:.2f}/1.00\n"
                       f"총 이벤트: {monitoring_result['total_events']}개",
                priority=AlertPriority.CRITICAL,
                symbol="MARKET",
                severity=risk_assessment['risk_score'],
                timestamp=datetime.now(),
                details={
                    "risk_factors": risk_assessment.get('risk_factors', []),
                    "high_severity_events": monitoring_result.get('advanced_events_count', 0)
                }
            )
            
            await self.slack_notifier.send_critical_alert(special_alert)
            
        except Exception as e:
            self.logger.error(f"고위험 알림 전송 중 오류: {str(e)}")
    
    async def _send_summary_if_needed(self, monitoring_result: Dict):
        """필요시 요약 알림 전송"""
        try:
            now = datetime.now()
            
            # 첫 실행이거나 설정된 간격이 지난 경우
            if (self.last_summary_time is None or 
                (now - self.last_summary_time).total_seconds() >= 
                self.notification_settings["summary_interval_minutes"] * 60):
                
                success = await self.slack_notifier.send_market_summary(monitoring_result)
                
                if success:
                    self.last_summary_time = now
                    self.logger.info("시장 요약 알림 전송 완료")
                
        except Exception as e:
            self.logger.error(f"요약 알림 전송 중 오류: {str(e)}")
    
    async def _send_startup_notification(self):
        """시작 알림"""
        try:
            status = self.enhanced_monitor.get_monitoring_status()
            status['is_running'] = True
            status['startup_time'] = datetime.now().isoformat()
            
            await self.slack_notifier.send_system_status(status)
            self.logger.info("시작 알림 전송 완료")
            
        except Exception as e:
            self.logger.error(f"시작 알림 전송 실패: {str(e)}")
    
    async def _send_shutdown_notification(self):
        """종료 알림"""
        try:
            status = {
                'is_running': False,
                'shutdown_time': datetime.now().isoformat(),
                'total_alerts_sent': len(self.alert_history)
            }
            
            await self.slack_notifier.send_system_status(status)
            self.logger.info("종료 알림 전송 완료")
            
        except Exception as e:
            self.logger.error(f"종료 알림 전송 실패: {str(e)}")
    
    async def _send_error_notification(self, error_message: str):
        """오류 알림"""
        try:
            error_alert = SlackAlert(
                title="⚠️ 시스템 오류 발생",
                message=f"모니터링 시스템에서 오류가 발생했습니다:\n```{error_message}```",
                priority=AlertPriority.HIGH,
                symbol="SYSTEM",
                severity=0.8,
                timestamp=datetime.now()
            )
            
            await self.slack_notifier.send_critical_alert(error_alert)
            
        except Exception as e:
            self.logger.error(f"오류 알림 전송 실패: {str(e)}")
    
    def _update_alert_history(self, monitoring_result: Dict):
        """알림 히스토리 업데이트"""
        try:
            history_entry = {
                "timestamp": monitoring_result["timestamp"],
                "total_events": monitoring_result["total_events"],
                "risk_level": monitoring_result["risk_assessment"]["overall_risk_level"],
                "alerts_sent": len(monitoring_result.get("priority_alerts", []))
            }
            
            self.alert_history.append(history_entry)
            
            # 24시간 이전 히스토리 제거
            cutoff_time = datetime.now() - timedelta(hours=24)
            self.alert_history = [
                entry for entry in self.alert_history
                if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
            ]
            
        except Exception as e:
            self.logger.error(f"히스토리 업데이트 중 오류: {str(e)}")
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring_active = False
        self.logger.info("모니터링 중지 요청")
    
    def update_notification_settings(self, settings: Dict):
        """알림 설정 업데이트"""
        self.notification_settings.update(settings)
        self.slack_notifier.update_settings(settings)
        self.logger.info(f"알림 설정 업데이트: {settings}")
    
    def get_alert_statistics(self) -> Dict:
        """알림 통계 조회"""
        if not self.alert_history:
            return {"message": "알림 히스토리가 없습니다."}
        
        total_alerts = sum(entry["alerts_sent"] for entry in self.alert_history)
        avg_events = sum(entry["total_events"] for entry in self.alert_history) / len(self.alert_history)
        
        risk_levels = [entry["risk_level"] for entry in self.alert_history]
        high_risk_count = sum(1 for level in risk_levels if level in ["high", "very_high"])
        
        return {
            "total_monitoring_cycles": len(self.alert_history),
            "total_alerts_sent": total_alerts,
            "average_events_per_cycle": round(avg_events, 2),
            "high_risk_cycles": high_risk_count,
            "high_risk_percentage": round(high_risk_count / len(self.alert_history) * 100, 1)
        }

# 설정 파일 로드 함수
def load_slack_config(config_file: str = "config/slack_config.json") -> Dict:
    """Slack 설정 파일 로드"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 기본 설정 반환
        return {
            "webhook_url": os.getenv("SLACK_WEBHOOK_URL", ""),
            "channel": "#economic-alerts",
            "notification_settings": {
                "send_summary": True,
                "send_critical_alerts": True,
                "send_news_updates": True,
                "summary_interval_minutes": 60,
                "min_alert_severity": 0.6
            }
        }

# 메인 실행 함수
async def main():
    """메인 실행 함수"""
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/slack_monitor.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # 설정 로드
    config = load_slack_config()
    
    if not config["webhook_url"]:
        print("❌ Slack 웹훅 URL이 설정되지 않았습니다.")
        print("환경변수 SLACK_WEBHOOK_URL을 설정하거나 config/slack_config.json 파일을 생성해주세요.")
        return
    
    # 모니터링 시스템 초기화
    monitor = SlackIntegratedMonitor(
        webhook_url=config["webhook_url"],
        channel=config.get("channel", "#economic-alerts")
    )
    
    # 알림 설정 적용
    if "notification_settings" in config:
        monitor.update_notification_settings(config["notification_settings"])
    
    print("🚀 Slack 통합 모니터링 시스템")
    print("=" * 50)
    print("1. 연속 모니터링 시작")
    print("2. 단일 분석 실행")
    print("3. 알림 통계 조회")
    print("4. 종료")
    
    while True:
        try:
            choice = input("\n선택하세요 (1-4): ").strip()
            
            if choice == "1":
                interval = input("모니터링 간격(분, 기본값 30): ").strip()
                interval = int(interval) if interval.isdigit() else 30
                
                print(f"📊 {interval}분 간격으로 연속 모니터링을 시작합니다...")
                print("Ctrl+C로 중지할 수 있습니다.")
                
                await monitor.start_monitoring_with_alerts(interval)
                break
                
            elif choice == "2":
                print("📊 단일 분석을 실행합니다...")
                result = await monitor.run_single_analysis_with_alerts()
                
                if "error" not in result:
                    print(f"✅ 분석 완료: {result['total_events']}개 이벤트 감지")
                    print(f"위험도: {result['risk_assessment']['overall_risk_level']}")
                else:
                    print(f"❌ 분석 실패: {result['error']}")
                
            elif choice == "3":
                stats = monitor.get_alert_statistics()
                print("\n📈 알림 통계:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                
            elif choice == "4":
                print("👋 시스템을 종료합니다.")
                break
                
            else:
                print("❌ 잘못된 선택입니다.")
                
        except KeyboardInterrupt:
            print("\n👋 사용자에 의한 종료")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
