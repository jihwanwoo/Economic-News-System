#!/usr/bin/env python3
"""
Slack 연속 모니터링 시작 스크립트
"""

import asyncio
import os
import sys
import logging
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notifications.integrated_slack_monitor import SlackIntegratedMonitor

def setup_logging():
    """로깅 설정"""
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/slack_monitoring.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

async def start_monitoring():
    """모니터링 시작"""
    # 웹훅 URL 로드
    webhook_url = None
    
    # 1. 환경변수에서 확인
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    # 2. 파일에서 확인
    if not webhook_url:
        try:
            with open('config/slack_webhook.txt', 'r') as f:
                webhook_url = f.read().strip()
        except FileNotFoundError:
            pass
    
    if not webhook_url:
        print("❌ Slack 웹훅 URL을 찾을 수 없습니다.")
        print("다음 중 하나를 설정해주세요:")
        print("1. 환경변수: export SLACK_WEBHOOK_URL='your_url'")
        print("2. 파일: config/slack_webhook.txt에 URL 저장")
        return
    
    print("🚀 Slack 연속 모니터링 시스템 시작")
    print("=" * 50)
    print(f"📱 웹훅 URL: {webhook_url[:50]}...")
    print(f"⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔄 모니터링 간격: 30분")
    print("⚠️  Ctrl+C로 중지할 수 있습니다.")
    print("=" * 50)
    
    # 모니터링 시스템 초기화
    monitor = SlackIntegratedMonitor(webhook_url)
    
    # 알림 설정 최적화
    monitor.update_notification_settings({
        "send_summary": True,
        "send_critical_alerts": True,
        "send_news_updates": True,
        "summary_interval_minutes": 60,  # 1시간마다 요약
        "min_alert_severity": 0.6,       # 심각도 0.6 이상
        "max_alerts_per_hour": 15,       # 시간당 최대 15개
        "cooldown_minutes": 15           # 15분 쿨다운
    })
    
    try:
        # 연속 모니터링 시작 (30분 간격)
        await monitor.start_monitoring_with_alerts(interval_minutes=30)
    except KeyboardInterrupt:
        print("\n👋 사용자에 의한 모니터링 중지")
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        logging.error(f"모니터링 중 오류: {str(e)}")
    finally:
        print("🔚 모니터링 종료")

def main():
    """메인 함수"""
    setup_logging()
    
    print("📱 Slack 경제 알림 모니터링 시스템")
    print("=" * 40)
    
    # 웹훅 URL 설정
    webhook_url = "https://hooks.slack.com/services/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"
    os.environ["SLACK_WEBHOOK_URL"] = webhook_url
    
    # 모니터링 시작
    asyncio.run(start_monitoring())

if __name__ == "__main__":
    main()
