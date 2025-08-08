#!/usr/bin/env python3
"""
종합 경제 모니터링 시스템 테스트
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_economic_monitor import ComprehensiveEconomicMonitor

async def test_comprehensive_monitoring():
    """종합 모니터링 시스템 테스트"""
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 종합 경제 모니터링 시스템 테스트 시작")
    print("=" * 60)
    
    try:
        # 모니터링 시스템 초기화
        print("📋 1. 시스템 초기화 중...")
        monitor = ComprehensiveEconomicMonitor()
        print("✅ 시스템 초기화 완료")
        
        # API 키 상태 확인
        print("\n🔌 2. API 연결 상태 확인")
        print("-" * 30)
        
        # FRED API
        fred_key = os.getenv('FRED_API_KEY')
        if fred_key and fred_key != "demo":
            print("✅ FRED API: 연결됨")
        else:
            print("🟡 FRED API: Demo 모드")
        
        # Reddit API
        reddit_id = os.getenv('REDDIT_CLIENT_ID')
        reddit_secret = os.getenv('REDDIT_CLIENT_SECRET')
        if reddit_id and reddit_secret:
            print("✅ Reddit API: 연결됨")
        else:
            print("❌ Reddit API: 미연결")
        
        # Alpha Vantage API
        alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if alpha_key:
            print("✅ Alpha Vantage API: 연결됨")
        else:
            print("❌ Alpha Vantage API: 미연결")
        
        # Slack 웹훅
        slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        if slack_webhook:
            print("✅ Slack 웹훅: 설정됨")
        else:
            print("❌ Slack 웹훅: 미설정")
        
        # 종합 모니터링 실행
        print("\n📊 3. 종합 모니터링 실행 중...")
        print("-" * 30)
        
        start_time = datetime.now()
        result = await monitor.run_comprehensive_monitoring()
        end_time = datetime.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        # 결과 분석
        print("\n📋 4. 수집 결과 분석")
        print("-" * 30)
        
        market_data = result.get('market_data', {})
        economic_data = result.get('economic_indicators', {})
        social_data = result.get('social_sentiment', {})
        events = result.get('detected_events', [])
        
        print(f"📊 시장 데이터:")
        us_stocks = market_data.get('us_stocks', {})
        print(f"   - 미국 주식: {len(us_stocks)}개")
        
        currencies = market_data.get('currencies', {})
        print(f"   - 통화: {len(currencies)}개")
        
        commodities = market_data.get('commodities', {})
        print(f"   - 원자재: {len(commodities)}개")
        
        print(f"📈 경제 지표: {len(economic_data)}개")
        for indicator in economic_data.keys():
            print(f"   - {indicator}")
        
        print(f"💬 소셜 데이터: {len(social_data)}개 플랫폼")
        for platform, data in social_data.items():
            sentiment = data.get('sentiment_score', 0)
            posts = data.get('post_count', 0)
            print(f"   - r/{platform}: {sentiment:.2f} ({posts}개 게시물)")
        
        print(f"🚨 감지된 이벤트: {len(events)}개")
        for event in events[:5]:  # 최대 5개만 표시
            symbol = event.get('symbol', 'Unknown')
            event_type = event.get('event_type', 'Unknown')
            severity = event.get('severity', 0)
            print(f"   - {symbol}: {event_type} (심각도: {severity:.2f})")
        
        print(f"\n⏱️ 총 처리 시간: {processing_time:.2f}초")
        
        # 성공 여부 판단
        success_criteria = {
            'market_data_collected': len(us_stocks) > 0,
            'processing_completed': 'error' not in result,
            'reasonable_time': processing_time < 300  # 5분 이내
        }
        
        print("\n🎯 5. 테스트 결과")
        print("-" * 30)
        
        all_passed = True
        for criterion, passed in success_criteria.items():
            status = "✅ 통과" if passed else "❌ 실패"
            print(f"{criterion}: {status}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 종합 모니터링 시스템 테스트 성공!")
            print("✅ 모든 기능이 정상적으로 작동합니다.")
        else:
            print("\n⚠️ 일부 기능에 문제가 있습니다.")
            print("🔧 설정을 확인하고 다시 시도해주세요.")
        
        return result
        
    except Exception as e:
        print(f"\n❌ 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_individual_components():
    """개별 컴포넌트 테스트"""
    print("\n🔧 개별 컴포넌트 테스트")
    print("=" * 40)
    
    # 환경 변수 테스트
    print("1. 환경 변수 확인:")
    env_vars = [
        'FRED_API_KEY',
        'REDDIT_CLIENT_ID', 
        'REDDIT_CLIENT_SECRET',
        'ALPHA_VANTAGE_API_KEY',
        'SLACK_WEBHOOK_URL'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: 설정됨")
        else:
            print(f"   ❌ {var}: 미설정")
    
    # 모듈 import 테스트
    print("\n2. 모듈 import 테스트:")
    modules = [
        'yfinance',
        'pandas',
        'numpy',
        'requests',
        'plotly',
        'streamlit'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}: 로드 성공")
        except ImportError as e:
            print(f"   ❌ {module}: 로드 실패 - {e}")

async def main():
    """메인 실행 함수"""
    print("🤖 종합 경제 모니터링 시스템 테스트")
    print("=" * 60)
    
    # 개별 컴포넌트 테스트
    test_individual_components()
    
    # 종합 모니터링 테스트
    result = await test_comprehensive_monitoring()
    
    if result:
        print(f"\n💾 결과가 output/ 폴더에 저장되었습니다.")
        print("🌐 enhanced_integrated_dashboard.py를 실행하여 웹 대시보드에서 확인하세요.")
    
    print("\n" + "=" * 60)
    print("테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())
