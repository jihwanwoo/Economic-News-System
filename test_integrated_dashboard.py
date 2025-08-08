#!/usr/bin/env python3
"""
통합 대시보드 테스트 스크립트
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_imports():
    """필수 모듈 import 테스트"""
    print("📦 모듈 import 테스트 중...")
    
    try:
        import streamlit as st
        print("✅ Streamlit 로드 성공")
    except ImportError as e:
        print(f"❌ Streamlit 로드 실패: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas 로드 성공")
    except ImportError as e:
        print(f"❌ Pandas 로드 실패: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly 로드 성공")
    except ImportError as e:
        print(f"❌ Plotly 로드 실패: {e}")
        return False
    
    try:
        import yfinance as yf
        print("✅ yfinance 로드 성공")
    except ImportError as e:
        print(f"❌ yfinance 로드 실패: {e}")
        return False
    
    try:
        import requests
        print("✅ requests 로드 성공")
    except ImportError as e:
        print(f"❌ requests 로드 실패: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 로드 성공")
    except ImportError as e:
        print(f"❌ python-dotenv 로드 실패: {e}")
        return False
    
    return True

def test_env_variables():
    """환경 변수 테스트"""
    print("\n⚙️ 환경 변수 테스트 중...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'SLACK_WEBHOOK_URL',
        'ALPHA_VANTAGE_API_KEY',
        'AWS_DEFAULT_REGION'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: 설정됨")
        else:
            print(f"❌ {var}: 설정되지 않음")
            all_set = False
    
    return all_set

def test_data_collection():
    """데이터 수집 테스트"""
    print("\n📊 데이터 수집 테스트 중...")
    
    try:
        import yfinance as yf
        
        # 간단한 데이터 수집 테스트
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="1d", interval="5m")
        
        if len(hist) > 0:
            print(f"✅ AAPL 데이터 수집 성공: {len(hist)}개 데이터포인트")
            print(f"   최신 가격: ${hist['Close'].iloc[-1]:.2f}")
            return True
        else:
            print("❌ 데이터 수집 실패: 빈 데이터")
            return False
            
    except Exception as e:
        print(f"❌ 데이터 수집 오류: {e}")
        return False

def test_slack_webhook():
    """Slack 웹훅 테스트"""
    print("\n📱 Slack 웹훅 테스트 중...")
    
    from dotenv import load_dotenv
    import requests
    
    load_dotenv()
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL이 설정되지 않음")
        return False
    
    try:
        test_message = {
            "text": "🧪 통합 대시보드 테스트 메시지",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "통합 경제 뉴스 시스템 테스트가 성공적으로 완료되었습니다! 🎉"
                    }
                }
            ]
        }
        
        response = requests.post(webhook_url, json=test_message, timeout=10)
        
        if response.status_code == 200:
            print("✅ Slack 웹훅 테스트 성공")
            return True
        else:
            print(f"❌ Slack 웹훅 테스트 실패: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Slack 웹훅 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🤖 통합 대시보드 테스트 시작")
    print("=" * 50)
    
    # 테스트 실행
    tests = [
        ("모듈 Import", test_imports),
        ("환경 변수", test_env_variables),
        ("데이터 수집", test_data_collection),
        ("Slack 웹훅", test_slack_webhook)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 오류: {e}")
            results.append((test_name, False))
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📋 테스트 결과 요약")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n총 {len(results)}개 테스트 중 {passed}개 통과")
    
    if passed == len(results):
        print("\n🎉 모든 테스트가 통과했습니다!")
        print("💡 다음 명령어로 통합 대시보드를 실행하세요:")
        print("   ./start_integrated_system.sh")
        print("   또는")
        print("   python run_integrated_dashboard.py")
    else:
        print(f"\n⚠️ {len(results) - passed}개 테스트가 실패했습니다.")
        print("💡 실패한 테스트를 확인하고 문제를 해결한 후 다시 시도하세요.")

if __name__ == "__main__":
    main()
