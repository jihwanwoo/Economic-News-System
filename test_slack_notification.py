#!/usr/bin/env python3
"""
Slack 알림 테스트 스크립트
.env 파일의 웹훅 URL을 사용하여 Slack 알림 테스트
"""

import os
import sys
import json
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_slack_webhook():
    """Slack 웹훅 테스트"""
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        logger.error("❌ SLACK_WEBHOOK_URL이 .env 파일에 설정되지 않았습니다.")
        return False
    
    logger.info(f"🔗 Slack 웹훅 URL: {webhook_url[:50]}...")
    
    # 테스트 메시지 생성
    test_message = {
        "text": "🤖 경제 뉴스 시스템 Slack 알림 테스트",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🤖 AI 경제 뉴스 시스템 테스트"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*테스트 시간:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*상태:* ✅ 연결 성공"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*시스템:* 경제 뉴스 자동 생성"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*환경:* AWS EC2"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "📊 시스템이 정상적으로 작동하고 있습니다. 경제 이벤트 감지 시 자동으로 알림을 받게 됩니다."
                }
            }
        ]
    }
    
    try:
        # Slack으로 메시지 전송
        response = requests.post(
            webhook_url,
            json=test_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("✅ Slack 알림 전송 성공!")
            logger.info("📱 Slack 채널을 확인해보세요.")
            return True
        else:
            logger.error(f"❌ Slack 알림 전송 실패: {response.status_code}")
            logger.error(f"응답: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 네트워크 오류: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ 예상치 못한 오류: {e}")
        return False

def test_economic_event_notification():
    """경제 이벤트 알림 테스트"""
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        logger.error("❌ SLACK_WEBHOOK_URL이 설정되지 않았습니다.")
        return False
    
    # 경제 이벤트 알림 메시지
    event_message = {
        "text": "🚨 경제 이벤트 감지: AAPL 주가 급등",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 경제 이벤트 알림"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*📈 AAPL 주가 3.2% 급등*\n\n애플 주가가 150.25달러로 상승하며 투자자들의 관심이 집중되고 있습니다."
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*심볼:* AAPL"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*변동률:* +3.2%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*현재가:* $150.25"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*심각도:* 🟡 중간"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🤖 *AI 기사 생성 중...*\n데이터 분석 및 기사 작성이 진행 중입니다."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 🤖 경제 뉴스 자동 생성 시스템"
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=event_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("✅ 경제 이벤트 알림 전송 성공!")
            return True
        else:
            logger.error(f"❌ 경제 이벤트 알림 전송 실패: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 경제 이벤트 알림 전송 오류: {e}")
        return False

def test_article_completion_notification():
    """기사 완성 알림 테스트"""
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        return False
    
    # 기사 완성 알림 메시지
    article_message = {
        "text": "📰 AI 기사 생성 완료: AAPL 분석 리포트",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📰 AI 기사 생성 완료"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*애플 주가 상승, 신제품 출시 기대감 반영*\n\n애플이 올해 한 달러를 기록했다. 이는 올해 새로운 아이폰 모델 출시에 대한 기대감이 반영된 것으로 보인다..."
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*기사 길이:* 143단어"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*품질 점수:* 7.8/10"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*생성 시간:* 18초"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*이미지:* 3개 생성"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🌐 *웹에서 보기:*\n`streamlit run streamlit_articles/article_AAPL_20250807.py`"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📊 차트 보기"
                        },
                        "style": "primary",
                        "url": "http://localhost:8501"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "📰 기사 전문"
                        },
                        "url": "http://localhost:8501"
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=article_message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("✅ 기사 완성 알림 전송 성공!")
            return True
        else:
            logger.error(f"❌ 기사 완성 알림 전송 실패: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 기사 완성 알림 전송 오류: {e}")
        return False

def main():
    """메인 함수"""
    
    print("🚀 Slack 알림 시스템 테스트")
    print("=" * 50)
    
    # 환경 변수 확인
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if webhook_url:
        print(f"✅ Slack 웹훅 URL 설정됨: {webhook_url[:50]}...")
    else:
        print("❌ Slack 웹훅 URL이 설정되지 않았습니다.")
        print("💡 .env 파일에 SLACK_WEBHOOK_URL을 설정해주세요.")
        return
    
    print("\n1️⃣ 기본 연결 테스트...")
    test1_result = test_slack_webhook()
    
    print("\n2️⃣ 경제 이벤트 알림 테스트...")
    test2_result = test_economic_event_notification()
    
    print("\n3️⃣ 기사 완성 알림 테스트...")
    test3_result = test_article_completion_notification()
    
    print("\n" + "=" * 50)
    print("📊 테스트 결과:")
    print(f"  기본 연결: {'✅ 성공' if test1_result else '❌ 실패'}")
    print(f"  이벤트 알림: {'✅ 성공' if test2_result else '❌ 실패'}")
    print(f"  기사 완성 알림: {'✅ 성공' if test3_result else '❌ 실패'}")
    
    if all([test1_result, test2_result, test3_result]):
        print("\n🎉 모든 Slack 알림 테스트 성공!")
        print("📱 Slack 채널에서 3개의 테스트 메시지를 확인하세요.")
        print("\n💡 이제 통합 시스템을 실행하면 자동으로 Slack 알림이 전송됩니다:")
        print("   ./run_news_system.sh")
    else:
        print("\n⚠️ 일부 테스트가 실패했습니다.")
        print("🔧 문제 해결:")
        print("  1. Slack 웹훅 URL 확인")
        print("  2. 네트워크 연결 확인")
        print("  3. Slack 채널 권한 확인")

if __name__ == "__main__":
    main()
