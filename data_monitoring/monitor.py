"""
경제 데이터 모니터링 메인 시스템
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from dataclasses import asdict

from .data_collector import EconomicDataCollector, MarketData
from .event_detector import EventDetector, EconomicEvent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.monitoring_config import ECONOMIC_INDICATORS, MONITORING_CONFIG

class EconomicMonitor:
    def __init__(self):
        self.logger = self._setup_logging()
        self.data_collector = EconomicDataCollector()
        self.event_detector = EventDetector()
        self.is_running = False
        self.monitoring_symbols = self._get_monitoring_symbols()
        
    def _setup_logging(self) -> logging.Logger:
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/home/ec2-user/projects/ABP/economic_news_system/logs/monitor.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _get_monitoring_symbols(self) -> List[str]:
        """모니터링할 심볼 목록 생성"""
        symbols = []
        for category, indicators in ECONOMIC_INDICATORS.items():
            for key, config in indicators.items():
                symbols.append(config['symbol'])
        return symbols
    
    async def start_monitoring(self):
        """모니터링 시작"""
        self.is_running = True
        self.logger.info("경제 데이터 모니터링을 시작합니다.")
        self.logger.info(f"모니터링 대상: {len(self.monitoring_symbols)}개 지표")
        
        while self.is_running:
            try:
                await self._monitoring_cycle()
                await asyncio.sleep(MONITORING_CONFIG['check_interval'])
                
            except KeyboardInterrupt:
                self.logger.info("사용자에 의해 모니터링이 중단되었습니다.")
                break
            except Exception as e:
                self.logger.error(f"모니터링 중 오류 발생: {str(e)}")
                await asyncio.sleep(30)  # 오류 시 30초 대기
    
    async def _monitoring_cycle(self):
        """한 번의 모니터링 사이클"""
        cycle_start = datetime.now()
        self.logger.info(f"모니터링 사이클 시작: {cycle_start}")
        
        # 1. 데이터 수집
        market_data = await self._collect_market_data()
        if not market_data:
            self.logger.warning("수집된 시장 데이터가 없습니다.")
            return
        
        self.logger.info(f"수집된 데이터: {len(market_data)}개 지표")
        
        # 2. 이벤트 탐지
        events = self.event_detector.detect_events(market_data)
        
        if events:
            self.logger.info(f"탐지된 이벤트: {len(events)}개")
            await self._process_events(events)
        else:
            self.logger.info("탐지된 이벤트가 없습니다.")
        
        # 3. 시장 상황 요약
        await self._log_market_summary(market_data)
        
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        self.logger.info(f"모니터링 사이클 완료: {cycle_duration:.2f}초 소요")
    
    async def _collect_market_data(self) -> Dict[str, MarketData]:
        """시장 데이터 수집"""
        try:
            async with EconomicDataCollector() as collector:
                market_data = await collector.collect_multiple_symbols(self.monitoring_symbols)
                return market_data
        except Exception as e:
            self.logger.error(f"데이터 수집 중 오류: {str(e)}")
            return {}
    
    async def _process_events(self, events: List[EconomicEvent]):
        """탐지된 이벤트 처리"""
        for event in events:
            # 이벤트 로깅
            self.logger.warning(f"🚨 {event.event_type.value.upper()} 이벤트 탐지!")
            self.logger.warning(f"   대상: {event.name} ({event.symbol})")
            self.logger.warning(f"   심각도: {event.severity:.2f}")
            self.logger.warning(f"   설명: {event.description}")
            
            # 이벤트 저장
            await self._save_event(event)
            
            # 높은 심각도 이벤트는 즉시 알림
            if event.severity >= 0.7:
                await self._send_high_priority_alert(event)
    
    async def _save_event(self, event: EconomicEvent):
        """이벤트를 파일에 저장"""
        try:
            event_data = {
                'event_id': event.event_id,
                'symbol': event.symbol,
                'name': event.name,
                'event_type': event.event_type.value,
                'severity': event.severity,
                'timestamp': event.timestamp.isoformat(),
                'current_price': event.current_price,
                'change_percent': event.change_percent,
                'volume': event.volume,
                'description': event.description,
                'technical_indicators': event.technical_indicators,
                'market_context': event.market_context
            }
            
            # 날짜별 파일에 저장
            date_str = event.timestamp.strftime('%Y-%m-%d')
            filename = f"/home/ec2-user/projects/ABP/economic_news_system/logs/events_{date_str}.json"
            
            # 파일에 추가
            try:
                with open(filename, 'r') as f:
                    events_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                events_data = []
            
            events_data.append(event_data)
            
            with open(filename, 'w') as f:
                json.dump(events_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"이벤트 저장 중 오류: {str(e)}")
    
    async def _send_high_priority_alert(self, event: EconomicEvent):
        """고우선순위 이벤트 알림"""
        # 여기서 실제 알림 시스템 연동 (이메일, 슬랙, AWS SNS 등)
        alert_message = f"""
🚨 긴급 경제 이벤트 알림 🚨

대상: {event.name} ({event.symbol})
이벤트: {event.event_type.value.upper()}
심각도: {event.severity:.2f}/1.0
시간: {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

현재가: {event.current_price:,.2f}
변화율: {event.change_percent:+.2f}%
거래량: {event.volume:,}

설명: {event.description}
        """
        
        self.logger.critical(alert_message)
        
        # TODO: 실제 알림 시스템 연동
        # await self._send_slack_notification(alert_message)
        # await self._send_email_notification(alert_message)
    
    async def _log_market_summary(self, market_data: Dict[str, MarketData]):
        """시장 상황 요약 로깅"""
        summary_lines = ["📊 시장 상황 요약:"]
        
        # 카테고리별 요약
        categories = {
            'stock_indices': '주식 지수',
            'currencies': '환율',
            'commodities': '원자재'
        }
        
        for category, category_name in categories.items():
            category_data = []
            
            if category in ECONOMIC_INDICATORS:
                for key, config in ECONOMIC_INDICATORS[category].items():
                    symbol = config['symbol']
                    if symbol in market_data:
                        data = market_data[symbol]
                        category_data.append(f"  {config['name']}: {data.change_percent:+.2f}%")
            
            if category_data:
                summary_lines.append(f"{category_name}:")
                summary_lines.extend(category_data)
        
        self.logger.info('\n'.join(summary_lines))
    
    def stop_monitoring(self):
        """모니터링 중단"""
        self.is_running = False
        self.logger.info("모니터링 중단 요청됨")
    
    async def get_recent_events(self, hours: int = 24) -> List[Dict]:
        """최근 이벤트 조회"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_events = []
            
            # 최근 며칠간의 이벤트 파일 확인
            for i in range(3):  # 최근 3일
                date = datetime.now() - timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                filename = f"/home/ec2-user/projects/ABP/economic_news_system/logs/events_{date_str}.json"
                
                try:
                    with open(filename, 'r') as f:
                        events_data = json.load(f)
                        
                    for event_data in events_data:
                        event_time = datetime.fromisoformat(event_data['timestamp'])
                        if event_time >= cutoff_time:
                            recent_events.append(event_data)
                            
                except (FileNotFoundError, json.JSONDecodeError):
                    continue
            
            # 시간순 정렬
            recent_events.sort(key=lambda x: x['timestamp'], reverse=True)
            return recent_events
            
        except Exception as e:
            self.logger.error(f"최근 이벤트 조회 중 오류: {str(e)}")
            return []

# CLI 인터페이스
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='경제 데이터 모니터링 시스템')
    parser.add_argument('--mode', choices=['monitor', 'events'], default='monitor',
                       help='실행 모드: monitor(모니터링), events(최근 이벤트 조회)')
    parser.add_argument('--hours', type=int, default=24,
                       help='최근 이벤트 조회 시간 (시간 단위)')
    
    args = parser.parse_args()
    
    monitor = EconomicMonitor()
    
    if args.mode == 'monitor':
        try:
            await monitor.start_monitoring()
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            print("\n모니터링이 중단되었습니다.")
    
    elif args.mode == 'events':
        events = await monitor.get_recent_events(args.hours)
        print(f"\n최근 {args.hours}시간 동안의 이벤트: {len(events)}개")
        
        for event in events[:10]:  # 최근 10개만 표시
            print(f"- {event['timestamp']}: {event['name']} ({event['event_type']}) - {event['description']}")

if __name__ == "__main__":
    asyncio.run(main())
