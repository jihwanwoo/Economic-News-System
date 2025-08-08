#!/usr/bin/env python3
"""
Slack 웹훅 테스트 스크립트
"""

import os
import json
import requests
from pathlib import Path

def load_webhook_url():
    """웹훅 URL 로드"""
    
    # 1. 환경변수에서 확인
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if webhook_url:
        print("✅ 환경변수에서 웹훅 URL 로드")
        return webhook_url
    
    # 2. 설정 파일에서 확인
    webhook_file = Path("config/slack_webhook.txt")
    if webhook_file.exists():
        try:
            webhook_url = webhook_file.read_text().strip()
            if webhook_url:
                print("✅ 설정 파일에서 웹훅 URL 로드")
                return webhook_url
        except Exception as e:
            print(f"❌ 설정 파일 읽기 오류: {e}")
    
    print("❌ 웹훅 URL을 찾을 수 없습니다")
    return None

def test_webhook(webhook_url):
    """웹훅 테스트"""
    
    test_messages = [
        {
            "text": "🧪 Slack 웹훅 연결 테스트",
            "description": "기본 연결 테스트"
        },
        {
            "text": "📊 경제 뉴스 시스템 알림 테스트",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*경제 뉴스 시스템* 🤖\n\n✅ 시스템이 정상적으로 작동 중입니다."
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*상태:* 정상"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*시간:* 방금 전"
                        }
                    ]
                }
            ],
            "description": "고급 블록 형식 테스트"
        }
    ]
    
    success_count = 0
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔍 테스트 {i}: {message['description']}")
        
        try:
            # 메시지 데이터 준비
            data = {key: value for key, value in message.items() if key != 'description'}
            
            # POST 요청 전송
            response = requests.post(
                webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200 and response.text == 'ok':
                print(f"✅ 테스트 {i} 성공!")
                success_count += 1
            else:
                print(f"❌ 테스트 {i} 실패:")
                print(f"   상태 코드: {response.status_code}")
                print(f"   응답: {response.text}")
                
                # 일반적인 오류 해석
                if response.text == 'no_service':
                    print("   → 웹훅이 비활성화되었거나 삭제됨")
                elif response.text == 'channel_not_found':
                    print("   → 채널을 찾을 수 없음")
                elif response.text == 'invalid_payload':
                    print("   → 잘못된 메시지 형식")
                
        except requests.exceptions.Timeout:
            print(f"❌ 테스트 {i} 시간 초과")
        except requests.exceptions.RequestException as e:
            print(f"❌ 테스트 {i} 네트워크 오류: {e}")
        except Exception as e:
            print(f"❌ 테스트 {i} 예상치 못한 오류: {e}")
    
    return success_count, len(test_messages)

def validate_webhook_url(webhook_url):
    """웹훅 URL 유효성 검증"""
    
    if not webhook_url:
        return False, "웹훅 URL이 없습니다"
    
    if not webhook_url.startswith('https://hooks.slack.com/services/'):
        return False, "올바른 Slack 웹훅 URL 형식이 아닙니다"
    
    # URL 구조 확인
    parts = webhook_url.replace('https://hooks.slack.com/services/', '').split('/')
    if len(parts) != 3:
        return False, "웹훅 URL 구조가 올바르지 않습니다"
    
    return True, "웹훅 URL 형식이 올바릅니다"

def main():
    print("🔍 Slack 웹훅 테스트")
    print("=" * 40)
    
    # 웹훅 URL 로드
    webhook_url = load_webhook_url()
    if not webhook_url:
        print("\n❌ 웹훅 URL 설정이 필요합니다:")
        print("1. 환경변수: export SLACK_WEBHOOK_URL='your_webhook_url'")
        print("2. 설정파일: echo 'your_webhook_url' > config/slack_webhook.txt")
        print("3. 새 웹훅 생성: setup_slack_webhook.md 참조")
        return
    
    # URL 유효성 검증
    is_valid, message = validate_webhook_url(webhook_url)
    print(f"\n🔍 웹훅 URL 검증: {message}")
    
    if not is_valid:
        print("❌ 올바른 웹훅 URL을 설정해주세요")
        return
    
    # 웹훅 테스트 실행
    print(f"\n🔍 웹훅 테스트 시작...")
    print(f"URL: {webhook_url[:50]}...")
    
    success_count, total_count = test_webhook(webhook_url)
    
    # 결과 요약
    print(f"\n📊 테스트 결과:")
    print(f"   성공: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 모든 테스트 성공! Slack 알림이 정상 작동합니다.")
    elif success_count > 0:
        print("⚠️  일부 테스트 성공. 기본 알림은 작동하지만 고급 기능에 문제가 있을 수 있습니다.")
    else:
        print("❌ 모든 테스트 실패. 웹훅 설정을 확인해주세요.")
        print("\n🔧 해결 방법:")
        print("1. setup_slack_webhook.md 가이드 참조")
        print("2. 새로운 Slack 앱 및 웹훅 생성")
        print("3. 워크스페이스 권한 확인")

if __name__ == "__main__":
    main()
