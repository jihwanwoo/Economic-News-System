#!/usr/bin/env python3
"""
Slack 기사 게시 테스트
"""

import os
import sys
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_slack_webhook_basic():
    """기본 Slack 웹훅 테스트"""
    
    print("🔧 기본 Slack 웹훅 테스트...")
    
    try:
        # 환경 변수 로드
        load_dotenv()
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not webhook_url:
            print("❌ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다")
            return False
        
        print(f"📡 웹훅 URL: {webhook_url[:50]}...")
        
        # 간단한 테스트 메시지
        test_message = {
            "text": "🧪 Slack 웹훅 연결 테스트 성공!"
        }
        
        response = requests.post(webhook_url, json=test_message, timeout=10)
        
        if response.status_code == 200:
            print("✅ 기본 웹훅 테스트 성공!")
            return True
        else:
            print(f"❌ 웹훅 테스트 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 기본 테스트 실패: {e}")
        return False

def test_slack_article_with_attachments():
    """첨부파일이 포함된 기사 게시 테스트"""
    
    print("\n🔧 첨부파일 포함 기사 게시 테스트...")
    
    try:
        load_dotenv()
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not webhook_url:
            print("❌ SLACK_WEBHOOK_URL이 설정되지 않았습니다")
            return False
        
        # 샘플 기사 데이터
        article_data = {
            "symbol": "AAPL",
            "title": "애플(AAPL) 주가 급등 - AI 발표 효과",
            "content": """
애플이 새로운 AI 기능을 발표하면서 주가가 5.2% 급등했습니다.

주요 내용:
• 새로운 AI 칩셋 발표
• 시리 기능 대폭 개선
• 개발자 도구 확장

시장 반응:
• 거래량 평소 대비 250% 증가
• 기관 투자자들의 매수세 집중
• 목표주가 상향 조정 전망
            """,
            "change_percent": 5.2,
            "quality_score": 9.5,
            "streamlit_url": "http://localhost:8501/article_AAPL_20250806"
        }
        
        # Slack 메시지 구성
        message = {
            "text": f"📰 새로운 경제 기사: {article_data['title']}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📈 {article_data['title']}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*심볼:* {article_data['symbol']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*변화율:* {article_data['change_percent']:+.2f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*품질 점수:* {article_data['quality_score']}/10"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*생성 시간:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{article_data['content']}```"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📊 전체 기사 보기"
                            },
                            "url": article_data['streamlit_url'],
                            "style": "primary"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "🤖 자동화된 경제 뉴스 생성 시스템"
                        }
                    ]
                }
            ]
        }
        
        # Slack 전송
        print("📤 기사 메시지 전송 중...")
        response = requests.post(webhook_url, json=message, timeout=10)
        
        if response.status_code == 200:
            print("✅ 기사 게시 성공!")
            return True
        else:
            print(f"❌ 기사 게시 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 기사 게시 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_image_upload_capability():
    """이미지 업로드 가능성 확인"""
    
    print("\n🔧 이미지 업로드 기능 확인...")
    
    print("📋 Slack 웹훅의 이미지 업로드 제한사항:")
    print("   • 웹훅은 직접적인 파일 업로드를 지원하지 않음")
    print("   • 이미지는 공개 URL을 통해서만 표시 가능")
    print("   • 대안: AWS S3, GitHub, 또는 다른 호스팅 서비스 필요")
    
    print("\n💡 권장 해결책:")
    print("   1. 생성된 이미지를 AWS S3에 업로드")
    print("   2. 공개 URL을 Slack 메시지에 포함")
    print("   3. 또는 Streamlit 대시보드 링크로 이미지 제공")
    
    return False  # 웹훅으로는 직접 이미지 업로드 불가

def test_slack_with_image_url():
    """이미지 URL을 포함한 Slack 메시지 테스트"""
    
    print("\n🔧 이미지 URL 포함 메시지 테스트...")
    
    try:
        load_dotenv()
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not webhook_url:
            print("❌ SLACK_WEBHOOK_URL이 설정되지 않았습니다")
            return False
        
        # 샘플 이미지 URL (실제로는 S3나 다른 호스팅 서비스 URL)
        sample_image_url = "https://via.placeholder.com/800x400/36a64f/ffffff?text=Sample+Chart"
        
        message = {
            "text": "📊 차트가 포함된 기사 테스트",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📈 AAPL 주가 분석 차트"
                    }
                },
                {
                    "type": "image",
                    "image_url": sample_image_url,
                    "alt_text": "AAPL 주가 차트"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*차트 설명:* 애플 주가의 최근 1개월 추세를 보여주는 차트입니다."
                    }
                }
            ]
        }
        
        response = requests.post(webhook_url, json=message, timeout=10)
        
        if response.status_code == 200:
            print("✅ 이미지 URL 포함 메시지 전송 성공!")
            return True
        else:
            print(f"❌ 이미지 메시지 전송 실패: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 이미지 메시지 테스트 실패: {e}")
        return False

def get_latest_article_data():
    """최근 생성된 기사 데이터 가져오기"""
    
    try:
        output_dir = "output/automated_articles"
        if not os.path.exists(output_dir):
            return None
        
        # 가장 최근 파일 찾기
        files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
        if not files:
            return None
        
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        
        with open(os.path.join(output_dir, latest_file), 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        print(f"기사 데이터 로드 실패: {e}")
        return None

def test_real_article_posting():
    """실제 생성된 기사로 Slack 게시 테스트"""
    
    print("\n🔧 실제 기사 데이터로 Slack 게시 테스트...")
    
    try:
        # 최근 기사 데이터 가져오기
        article_data = get_latest_article_data()
        
        if not article_data:
            print("❌ 게시할 기사 데이터를 찾을 수 없습니다")
            return False
        
        load_dotenv()
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        
        if not webhook_url:
            print("❌ SLACK_WEBHOOK_URL이 설정되지 않았습니다")
            return False
        
        # 기사 정보 추출
        event = article_data.get('event', {})
        article = article_data.get('article', {})
        review = article_data.get('review_result', {})
        
        # Slack 메시지 구성
        message = {
            "text": f"📰 새로운 기사: {event.get('title', '제목 없음')}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📈 {event.get('title', '제목 없음')}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*심볼:* {event.get('symbol', 'N/A')}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*변화율:* {event.get('change_percent', 0):+.2f}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*품질 점수:* {review.get('quality_score', 0):.1f}/10"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*생성 시간:* {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*기사 내용:*\n```{article.get('content', '내용 없음')[:500]}...```"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📊 전체 기사 보기"
                            },
                            "url": article_data.get('streamlit_url', 'http://localhost:8501'),
                            "style": "primary"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=message, timeout=10)
        
        if response.status_code == 200:
            print("✅ 실제 기사 게시 성공!")
            print(f"📰 게시된 기사: {event.get('title', '제목 없음')}")
            return True
        else:
            print(f"❌ 실제 기사 게시 실패: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 실제 기사 게시 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Slack 기사 게시 시스템 테스트")
    print("=" * 60)
    
    # 1. 기본 웹훅 테스트
    success1 = test_slack_webhook_basic()
    
    # 2. 첨부파일 포함 기사 테스트
    success2 = test_slack_article_with_attachments()
    
    # 3. 이미지 업로드 기능 확인
    success3 = check_image_upload_capability()
    
    # 4. 이미지 URL 포함 테스트
    success4 = test_slack_with_image_url()
    
    # 5. 실제 기사 데이터로 테스트
    success5 = test_real_article_posting()
    
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약:")
    print(f"   ✅ 기본 웹훅: {'성공' if success1 else '실패'}")
    print(f"   ✅ 기사 게시: {'성공' if success2 else '실패'}")
    print(f"   ⚠️  이미지 직접 업로드: 웹훅 제한으로 불가")
    print(f"   ✅ 이미지 URL 표시: {'성공' if success4 else '실패'}")
    print(f"   ✅ 실제 기사 게시: {'성공' if success5 else '실패'}")
    
    if success1 and success2:
        print("\n🎉 Slack 기사 게시 기능이 정상 작동합니다!")
        print("💡 이미지는 S3 등 외부 호스팅을 통해 URL로 제공 가능합니다.")
    else:
        print("\n❌ 일부 기능에 문제가 있습니다. 설정을 확인해주세요.")
    
    print("\n📱 Slack 채널에서 테스트 메시지들을 확인하세요.")
