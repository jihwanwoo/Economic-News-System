#!/usr/bin/env python3
"""
경제 데이터 모니터링 시스템 테스트
"""

import asyncio
import sys
import os

# 프로젝트 경로 추가
sys.path.append('/home/ec2-user/projects/ABP/economic_news_system')

from data_monitoring.data_collector import EconomicDataCollector
from data_monitoring.event_detector import EventDetector
from data_monitoring.monitor import EconomicMonitor

async def test_data_collection():
    """데이터 수집 테스트"""
    print("=== 데이터 수집 테스트 ===")
    
    async with EconomicDataCollector() as collector:
        # 주요 지표 테스트
        test_symbols = ["^KS11", "^GSPC", "USDKRW=X", "CL=F"]
        
        print(f"테스트 대상: {test_symbols}")
        
        market_data = await collector.collect_multiple_symbols(test_symbols)
        
        if market_data:
            print(f"✅ 성공적으로 {len(market_data)}개 지표 데이터 수집")
            
            for symbol, data in market_data.items():
                print(f"  📊 {data.name} ({symbol})")
                print(f"     현재가: {data.current_price:,.2f}")
                print(f"     변화율: {data.change_percent:+.2f}%")
                print(f"     거래량: {data.volume:,}")
                print()
        else:
            print("❌ 데이터 수집 실패")
    
    return market_data

async def test_event_detection(market_data):
    """이벤트 탐지 테스트"""
    print("=== 이벤트 탐지 테스트 ===")
    
    if not market_data:
        print("❌ 시장 데이터가 없어 이벤트 탐지를 건너뜁니다.")
        return
    
    detector = EventDetector()
    events = detector.detect_events(market_data)
    
    if events:
        print(f"✅ {len(events)}개 이벤트 탐지됨")
        
        for event in events:
            print(f"  🚨 {event.event_type.value.upper()}: {event.name}")
            print(f"     심각도: {event.severity:.2f}/1.0")
            print(f"     설명: {event.description}")
            print()
    else:
        print("ℹ️  현재 탐지된 이벤트가 없습니다.")
    
    return events

async def test_monitoring_cycle():
    """모니터링 사이클 테스트"""
    print("=== 모니터링 사이클 테스트 ===")
    
    monitor = EconomicMonitor()
    
    print("한 번의 모니터링 사이클을 실행합니다...")
    
    try:
        await monitor._monitoring_cycle()
        print("✅ 모니터링 사이클 완료")
    except Exception as e:
        print(f"❌ 모니터링 사이클 실패: {str(e)}")

async def test_technical_indicators():
    """기술적 지표 계산 테스트"""
    print("=== 기술적 지표 테스트 ===")
    
    collector = EconomicDataCollector()
    
    # KOSPI 기술적 지표 테스트
    symbol = "^KS11"
    historical_data = collector.get_historical_data(symbol, "3mo")
    
    if not historical_data.empty:
        indicators = collector.calculate_technical_indicators(historical_data)
        
        if indicators:
            print(f"✅ {symbol} 기술적 지표 계산 완료")
            for key, value in indicators.items():
                if value is not None:
                    print(f"  {key}: {value:.2f}")
        else:
            print("❌ 기술적 지표 계산 실패")
    else:
        print("❌ 과거 데이터 조회 실패")

async def main():
    """메인 테스트 함수"""
    print("🚀 경제 데이터 모니터링 시스템 테스트 시작\n")
    
    try:
        # 1. 데이터 수집 테스트
        market_data = await test_data_collection()
        print()
        
        # 2. 이벤트 탐지 테스트
        await test_event_detection(market_data)
        print()
        
        # 3. 기술적 지표 테스트
        await test_technical_indicators()
        print()
        
        # 4. 모니터링 사이클 테스트
        await test_monitoring_cycle()
        print()
        
        print("✅ 모든 테스트 완료!")
        
        # 실제 모니터링 시작 여부 확인
        response = input("\n실제 모니터링을 시작하시겠습니까? (y/N): ")
        if response.lower() == 'y':
            print("\n모니터링을 시작합니다. Ctrl+C로 중단할 수 있습니다.")
            monitor = EconomicMonitor()
            await monitor.start_monitoring()
        
    except KeyboardInterrupt:
        print("\n테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
