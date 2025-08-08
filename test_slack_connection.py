#!/usr/bin/env python3
"""
Slack 연결 테스트 스크립트
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def test_slack_connection():
    """Slack 연결 테스트"""
    
    print("🧪 Slack 연결 테스트")
    print("=" * 40)
    
    # 1. Webhook URL 확인
    print("1️⃣ Webhook URL 확인:")
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        # config 파일에서 백업 로드
        try:
            with open('config/slack_webhook.txt', 'r') as f:
                webhook_url = f.read().strip()
            print("   ✅ config/slack_webhook.txt에서 URL 로드")
        except:
            print("   ❌ Webhook URL을 찾을 수 없습니다")
            return False
    else:
        print("   ✅ .env 파일에서 URL 로드")
    
    print(f"   📍 URL: {webhook_url[:50]}...")
    
    # 2. 기본 연결 테스트
    print("\n2️⃣ 기본 연결 테스트:")
    
    try:
        test_message = {
            "text": "🧪 Slack 연결 테스트",
            "attachments": [
                {
                    "color": "#36a64f",
                    "title": "✅ 연결 테스트 성공",
                    "text": "경제 이벤트 모니터링 시스템이 정상적으로 연결되었습니다.",
                    "fields": [
                        {
                            "title": "테스트 시간",
                            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "short": True
                        },
                        {
                            "title": "시스템 상태",
                            "value": "정상",
                            "short": True
                        }
                    ],
                    "footer": "경제 이벤트 모니터링 시스템",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        response = requests.post(
            webhook_url,
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ 기본 연결 테스트 성공")
        else:
            print(f"   ❌ 연결 실패: HTTP {response.status_code}")
            print(f"   응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 연결 오류: {e}")
        return False
    
    # 3. 경제 이벤트 알림 형식 테스트
    print("\n3️⃣ 경제 이벤트 알림 형식 테스트:")
    
    try:
        event_message = {
            "text": "🚨 경제 이벤트 감지: AAPL 급등",
            "attachments": [
                {
                    "color": "#ff9500",
                    "title": "⚠️ AAPL 급등 감지",
                    "text": "AAPL이(가) +3.45% 급등했습니다.",
                    "fields": [
                        {
                            "title": "심볼",
                            "value": "AAPL",
                            "short": True
                        },
                        {
                            "title": "심각도",
                            "value": "HIGH",
                            "short": True
                        },
                        {
                            "title": "현재값",
                            "value": "$175.23",
                            "short": True
                        },
                        {
                            "title": "변화율",
                            "value": "+3.45%",
                            "short": True
                        },
                        {
                            "title": "거래량 비율",
                            "value": "2.1x",
                            "short": True
                        },
                        {
                            "title": "변동성",
                            "value": "18.5%",
                            "short": True
                        }
                    ],
                    "footer": "경제 이벤트 모니터링 시스템",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        response = requests.post(
            webhook_url,
            json=event_message,
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ 이벤트 알림 형식 테스트 성공")
        else:
            print(f"   ❌ 이벤트 알림 실패: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 이벤트 알림 오류: {e}")
        return False
    
    # 4. 요약 알림 형식 테스트
    print("\n4️⃣ 요약 알림 형식 테스트:")
    
    try:
        summary_message = {
            "text": "📊 경제 이벤트 요약 보고서",
            "attachments": [
                {
                    "color": "#36a64f",
                    "title": f"📊 경제 이벤트 요약 ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
                    "text": "📊 경제 이벤트 요약 (5개 이벤트)\n🚨 높음: 2개\n⚠️ 보통: 3개\n",
                    "fields": [
                        {
                            "title": "주요 이벤트",
                            "value": "• AAPL: 급등 감지 (+3.4%)\n• TSLA: 거래량 급증 (+2.1%)\n• ^GSPC: 높은 변동성 (+1.8%)",
                            "short": False
                        }
                    ],
                    "footer": "경제 이벤트 모니터링 시스템",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        response = requests.post(
            webhook_url,
            json=summary_message,
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ 요약 알림 형식 테스트 성공")
        else:
            print(f"   ❌ 요약 알림 실패: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ 요약 알림 오류: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("✅ 모든 Slack 연결 테스트 통과!")
    print("📱 Slack 채널에서 테스트 메시지들을 확인하세요.")
    
    return True

if __name__ == "__main__":
    success = test_slack_connection()
    
    if success:
        print("\n🎉 Slack 연결이 정상적으로 작동합니다!")
        print("이제 경제 이벤트 감지 시스템을 실행할 수 있습니다.")
    else:
        print("\n❌ Slack 연결에 문제가 있습니다.")
        print("\n🔧 해결 방법:")
        print("1. .env 파일 또는 config/slack_webhook.txt 파일의 Webhook URL 확인")
        print("2. Slack 워크스페이스에서 Webhook 설정 확인")
        print("3. 인터넷 연결 상태 확인")
        print("4. Webhook URL 권한 확인")
