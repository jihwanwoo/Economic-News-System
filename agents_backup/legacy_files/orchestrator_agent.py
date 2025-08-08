#!/usr/bin/env python3
"""
통합 오케스트레이터 에이전트
이벤트 감지부터 기사 발행까지 전체 워크플로우 관리
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio

# 경로 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.data_analysis_agent import DataAnalysisAgent
from agents.article_writer_agent import ArticleWriterAgent
from agents.image_generator_agent import ImageGeneratorAgent
from agents.review_agent import ReviewAgent
from agents.ad_recommendation_agent import AdRecommendationAgent
from event_detection_slack_system import EventMonitoringSystem, EconomicEvent

@dataclass
class ArticlePackage:
    """완성된 기사 패키지"""
    event: EconomicEvent
    data_analysis: Dict[str, Any]
    charts: List[str]  # 차트 파일 경로들
    article: Dict[str, Any]
    article_image: str  # 기사 이미지 경로
    review_result: Dict[str, Any]
    advertisements: List[Dict[str, Any]]
    raw_data: Dict[str, Any]
    streamlit_url: str
    timestamp: datetime

class OrchestratorAgent:
    """통합 오케스트레이터 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 하위 에이전트들 초기화
        self.event_monitor = EventMonitoringSystem()
        self.data_analyst = DataAnalysisAgent()
        self.article_writer = ArticleWriterAgent()
        self.image_generator = ImageGeneratorAgent()
        self.reviewer = ReviewAgent()
        self.ad_recommender = AdRecommendationAgent()
        
        # 출력 디렉토리 설정
        self.output_dir = "output/automated_articles"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.logger.info("✅ 통합 오케스트레이터 에이전트 초기화 완료")
    
    async def run_full_automation_cycle(self) -> List[ArticlePackage]:
        """전체 자동화 사이클 실행"""
        
        self.logger.info("🚀 전체 자동화 사이클 시작")
        
        try:
            # 1. 이벤트 감지
            self.logger.info("1️⃣ 이벤트 감지 중...")
            events = await self._detect_events()
            
            if not events:
                self.logger.info("😴 감지된 이벤트가 없습니다")
                return []
            
            self.logger.info(f"📊 {len(events)}개 이벤트 감지됨")
            
            # 2. 각 이벤트에 대해 기사 생성
            article_packages = []
            
            for i, event in enumerate(events[:3], 1):  # 최대 3개 이벤트 처리
                self.logger.info(f"📝 이벤트 {i}/{min(len(events), 3)} 처리 중: {event.symbol}")
                
                try:
                    package = await self._process_single_event(event)
                    if package:
                        article_packages.append(package)
                        
                        # Streamlit 발행 및 Slack 알림
                        await self._publish_and_notify(package)
                        
                except Exception as e:
                    self.logger.error(f"❌ 이벤트 {event.symbol} 처리 실패: {e}")
                    continue
            
            self.logger.info(f"✅ 전체 자동화 사이클 완료: {len(article_packages)}개 기사 생성")
            return article_packages
            
        except Exception as e:
            self.logger.error(f"❌ 자동화 사이클 실패: {e}")
            return []
    
    async def _detect_events(self) -> List[EconomicEvent]:
        """이벤트 감지"""
        
        try:
            # 이벤트 스캔 실행
            result = self.event_monitor.run_single_scan()
            
            # EconomicEvent 객체로 변환
            events = []
            for event_data in result.get('events', []):
                # 간단한 EconomicEvent 객체 생성 (실제로는 더 복잡한 변환 필요)
                from event_detection_slack_system import EconomicEvent, EventSeverity
                
                event = EconomicEvent(
                    symbol=event_data['symbol'],
                    event_type=event_data['type'],
                    severity=EventSeverity(event_data['severity']),
                    title=event_data['title'],
                    description=event_data['description'],
                    current_value=0,  # 실제 값으로 대체 필요
                    previous_value=0,  # 실제 값으로 대체 필요
                    change_percent=event_data['change_percent'],
                    timestamp=datetime.fromisoformat(event_data['timestamp'])
                )
                events.append(event)
            
            return events
            
        except Exception as e:
            self.logger.error(f"이벤트 감지 실패: {e}")
            return []
    
    async def _process_single_event(self, event: EconomicEvent) -> Optional[ArticlePackage]:
        """단일 이벤트 처리"""
        
        try:
            # 2. 데이터 분석
            self.logger.info(f"📊 {event.symbol} 데이터 분석 중...")
            data_analysis = await self.data_analyst.analyze_event_data(event)
            
            # 3. 차트 생성
            self.logger.info(f"📈 {event.symbol} 차트 생성 중...")
            charts = await self.data_analyst.generate_charts(event, data_analysis)
            
            # 4. 기사 작성
            self.logger.info(f"✍️ {event.symbol} 기사 작성 중...")
            article = await self.article_writer.write_article(event, data_analysis)
            
            # 5. 기사 이미지 생성
            self.logger.info(f"🖼️ {event.symbol} 기사 이미지 생성 중...")
            article_image = await self.image_generator.generate_article_image(article)
            
            # 6. 기사 검수
            self.logger.info(f"🔍 {event.symbol} 기사 검수 중...")
            review_result = await self.reviewer.review_article(article, data_analysis)
            
            # 7. 광고 추천
            self.logger.info(f"📢 {event.symbol} 광고 추천 중...")
            advertisements = await self.ad_recommender.recommend_ads(article, event)
            
            # 8. 패키지 생성
            package = ArticlePackage(
                event=event,
                data_analysis=data_analysis,
                charts=charts,
                article=article,
                article_image=article_image,
                review_result=review_result,
                advertisements=advertisements,
                raw_data=data_analysis.get('raw_data', {}),
                streamlit_url="",  # 나중에 설정
                timestamp=datetime.now()
            )
            
            # 9. 패키지 저장
            await self._save_package(package)
            
            return package
            
        except Exception as e:
            self.logger.error(f"이벤트 처리 실패: {e}")
            return None
    
    async def _save_package(self, package: ArticlePackage):
        """패키지 저장"""
        
        try:
            # 파일명 생성
            timestamp = package.timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"{package.event.symbol}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            # 직렬화 가능한 데이터로 변환
            package_data = {
                'event': {
                    'symbol': package.event.symbol,
                    'event_type': package.event.event_type,
                    'severity': package.event.severity.value,
                    'title': package.event.title,
                    'description': package.event.description,
                    'change_percent': package.event.change_percent,
                    'timestamp': package.event.timestamp.isoformat()
                },
                'data_analysis': package.data_analysis,
                'charts': package.charts,
                'article': package.article,
                'article_image': package.article_image,
                'review_result': package.review_result,
                'advertisements': package.advertisements,
                'raw_data': package.raw_data,
                'streamlit_url': package.streamlit_url,
                'timestamp': package.timestamp.isoformat()
            }
            
            # JSON 파일로 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"💾 패키지 저장 완료: {filepath}")
            
        except Exception as e:
            self.logger.error(f"패키지 저장 실패: {e}")
    
    async def _publish_and_notify(self, package: ArticlePackage):
        """Streamlit 발행 및 Slack 알림 (개선된 버전)"""
        
        try:
            # Streamlit 페이지 생성
            streamlit_url = await self._create_streamlit_page(package)
            package.streamlit_url = streamlit_url
            
            # 패키지 저장
            await self._save_package(package)
            
            # Slack 알림 전송 (다중 메시지 방식)
            await self._send_slack_notification(package)
            
            # 추가로 완전한 기사 게시도 시도
            await self._send_slack_article_complete(package)
            
            # 이미지 정보 전송
            await self._send_slack_with_images(package)
            
        except Exception as e:
            self.logger.error(f"발행 및 알림 실패: {e}")
            import traceback
            self.logger.error(f"상세 오류: {traceback.format_exc()}")
    
    async def _create_streamlit_page(self, package: ArticlePackage) -> str:
        """Streamlit 페이지 생성"""
        
        try:
            # Streamlit 페이지 파일 생성
            timestamp = package.timestamp.strftime("%Y%m%d_%H%M%S")
            page_filename = f"article_{package.event.symbol}_{timestamp}.py"
            page_filepath = os.path.join("streamlit_articles", page_filename)
            
            # 디렉토리 생성
            os.makedirs("streamlit_articles", exist_ok=True)
            
            # Streamlit 페이지 코드 생성
            page_content = self._generate_streamlit_page_content(package)
            
            with open(page_filepath, 'w', encoding='utf-8') as f:
                f.write(page_content)
            
            # URL 생성 (실제 환경에서는 서버 URL 사용)
            streamlit_url = f"http://localhost:8501/article_{package.event.symbol}_{timestamp}"
            
            self.logger.info(f"📄 Streamlit 페이지 생성: {page_filepath}")
            return streamlit_url
            
        except Exception as e:
            self.logger.error(f"Streamlit 페이지 생성 실패: {e}")
            return ""
    
    def _generate_streamlit_page_content(self, package: ArticlePackage) -> str:
        """Streamlit 페이지 콘텐츠 생성 (수정된 버전)"""
        
        article = package.article
        event = package.event
        
        content = f'''#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
{event.symbol} - {event.title}
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="{event.title}",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 {event.title}")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Symbol", "{event.symbol}")
    
    with col2:
        st.metric("Change", "{event.change_percent:+.2f}%")
    
    with col3:
        st.metric("Severity", "{event.severity.value.upper()}")
    
    with col4:
        st.metric("Time", "{event.timestamp.strftime('%H:%M')}")
    
    # 기사 이미지
    article_image_path = "{package.article_image}"
    if article_image_path and os.path.exists(article_image_path):
        st.image(article_image_path, caption="Article Related Image", use_column_width=True)
    
    # 기사 본문
    st.markdown("## 📰 Article Content")
    st.markdown("""{article.get('content', 'Article content could not be loaded.')}""")
    
    st.markdown("---")
    st.markdown("*This article was automatically generated by the AI Economic News System. Additional analysis and expert consultation are recommended for investment decisions.*")
    
    # 데이터 차트
    st.markdown("## 📊 Related Data & Charts")
    
    # 차트 표시 (HTML 파일을 올바르게 처리)
    chart_paths = {package.charts}
    
    if chart_paths:
        for i, chart_path in enumerate(chart_paths):
            if os.path.exists(chart_path):
                st.markdown(f"### 📊 Chart {{i+1}}")
                try:
                    if chart_path.endswith('.html'):
                        # HTML 파일 읽기 및 표시
                        with open(chart_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        components.html(html_content, height=600)
                    else:
                        # 이미지 파일 표시
                        st.image(chart_path, caption=f"Chart {{i+1}}", use_column_width=True)
                except Exception as e:
                    st.error(f"Chart loading error: {{e}}")
                    st.markdown(f"Chart file: `{{chart_path}}`")
    else:
        st.info("No charts available for this article.")
    
    # 검수 결과
    st.markdown("## 🔍 Review Results")
    review = {package.review_result}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Quality Score", f"{{review.get('quality_score', 0):.1f}}/10")
    
    with col2:
        st.metric("Accuracy Score", f"{{review.get('accuracy_score', 0):.1f}}/10")
    
    with col3:
        st.metric("Style Score", f"{{review.get('style_score', 0):.1f}}/10")
    
    with col4:
        st.metric("Overall Score", f"{{review.get('overall_score', 0):.1f}}/10")
    
    # 광고 추천
    st.markdown("## 📢 Related Services")
    ads = {package.advertisements}
    
    if ads:
        for ad in ads[:3]:  # 최대 3개 광고 표시
            with st.expander(f"📢 {{ad.get('title', 'Service Recommendation')}}"):
                st.markdown(f"**Description:** {{ad.get('description', '')}}")
                st.markdown(f"**Target:** {{ad.get('target_audience', '')}}")
                st.markdown(f"**Relevance:** {{ad.get('relevance_score', 0):.1f}}/10")
    
    # Raw 데이터
    st.markdown("## 📋 Raw Data")
    
    with st.expander("View Raw Data"):
        st.json({package.raw_data})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**Generated Time:** {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
    st.markdown("**System:** Automated Economic News Generation System")

if __name__ == "__main__":
    main()
'''
        
        return content
    
    with col2:
        st.metric("신뢰도", f"{{review.get('credibility_score', 0):.1f}}/10")
    
    if review.get('suggestions'):
        st.markdown("**개선 제안:**")
        for suggestion in review['suggestions']:
            st.markdown(f"• {{suggestion}}")
    
    # 광고 추천
    st.markdown("## 📢 관련 광고")
    
    ads = {package.advertisements}
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {{i}}: {{ad.get('title', 'Unknown')}}"):
            st.markdown(f"**설명:** {{ad.get('description', '')}}")
            st.markdown(f"**타겟:** {{ad.get('target_audience', '')}}")
            st.markdown(f"**관련성:** {{ad.get('relevance_score', 0):.1f}}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({package.raw_data})
    
    # 푸터
    st.markdown("---")
    st.markdown("**Generated Time:** " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.markdown("**System:** Automated Economic News Generation System")

if __name__ == "__main__":
    main()
"""
        
        return content
    
    async def _send_slack_notification(self, package: ArticlePackage):
        """Slack 알림 전송 (개선된 버전)"""
        
        try:
            import requests
            from dotenv import load_dotenv
            
            load_dotenv()
            webhook_url = os.getenv('SLACK_WEBHOOK_URL')
            
            if not webhook_url:
                try:
                    with open('config/slack_webhook.txt', 'r') as f:
                        webhook_url = f.read().strip()
                except FileNotFoundError:
                    self.logger.error("❌ Slack 웹훅 URL을 찾을 수 없습니다")
                    return
            
            if not webhook_url:
                self.logger.error("❌ Slack 웹훅 URL이 설정되지 않았습니다")
                return
            
            # 기사 내용 요약 (Slack 메시지 길이 제한 고려)
            article_content = package.article.get('content', '')
            content_summary = article_content[:300] + "..." if len(article_content) > 300 else article_content
            
            # 기본 Slack 메시지 (안전한 형식)
            message = {
                "text": f"📰 새로운 경제 기사: {package.event.title}",
                "attachments": [
                    {
                        "color": "#36a64f",
                        "title": f"📈 {package.event.title}",
                        "text": f"{package.event.description}",
                        "fields": [
                            {
                                "title": "심볼",
                                "value": package.event.symbol,
                                "short": True
                            },
                            {
                                "title": "변화율",
                                "value": f"{package.event.change_percent:+.2f}%",
                                "short": True
                            },
                            {
                                "title": "품질 점수",
                                "value": f"{package.review_result.get('quality_score', 0):.1f}/10",
                                "short": True
                            },
                            {
                                "title": "생성 시간",
                                "value": package.timestamp.strftime('%Y-%m-%d %H:%M'),
                                "short": True
                            }
                        ],
                        "footer": "자동화된 경제 뉴스 시스템",
                        "ts": int(package.timestamp.timestamp())
                    }
                ]
            }
            
            # 첫 번째 메시지 전송 (기본 정보)
            response = requests.post(webhook_url, json=message, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("✅ Slack 기본 알림 전송 성공")
                
                # 두 번째 메시지: 기사 내용
                content_message = {
                    "text": f"📄 {package.event.symbol} 기사 내용:",
                    "attachments": [
                        {
                            "color": "#2eb886",
                            "title": "기사 본문",
                            "text": content_summary,
                            "actions": [
                                {
                                    "type": "button",
                                    "text": "📊 전체 기사 보기",
                                    "url": package.streamlit_url,
                                    "style": "primary"
                                }
                            ]
                        }
                    ]
                }
                
                # 기사 내용 메시지 전송
                content_response = requests.post(webhook_url, json=content_message, timeout=10)
                
                if content_response.status_code == 200:
                    self.logger.info("✅ Slack 기사 내용 전송 성공")
                else:
                    self.logger.warning(f"⚠️ 기사 내용 전송 실패: {content_response.status_code}")
                
                # 세 번째 메시지: 차트 정보 (차트가 있는 경우)
                if package.charts:
                    chart_message = {
                        "text": f"📊 {package.event.symbol} 분석 차트:",
                        "attachments": [
                            {
                                "color": "#ff9500",
                                "title": f"생성된 차트 ({len(package.charts)}개)",
                                "text": f"• 기술적 분석 차트\n• 가격 추세 분석\n• 거래량 분석\n• 종합 대시보드",
                                "footer": f"Streamlit에서 모든 차트를 확인하세요: {package.streamlit_url}"
                            }
                        ]
                    }
                    
                    chart_response = requests.post(webhook_url, json=chart_message, timeout=10)
                    
                    if chart_response.status_code == 200:
                        self.logger.info("✅ Slack 차트 정보 전송 성공")
                    else:
                        self.logger.warning(f"⚠️ 차트 정보 전송 실패: {chart_response.status_code}")
                
                # 네 번째 메시지: 광고 추천 (광고가 있는 경우)
                if package.advertisements:
                    ad_text = "\n".join([f"• {ad.get('title', '제목 없음')}" for ad in package.advertisements[:3]])
                    
                    ad_message = {
                        "text": f"📢 {package.event.symbol} 관련 추천:",
                        "attachments": [
                            {
                                "color": "#36c5f0",
                                "title": f"관련 서비스 추천 ({len(package.advertisements)}개)",
                                "text": ad_text,
                                "footer": "AI가 기사 내용을 분석하여 추천한 관련 서비스입니다"
                            }
                        ]
                    }
                    
                    ad_response = requests.post(webhook_url, json=ad_message, timeout=10)
                    
                    if ad_response.status_code == 200:
                        self.logger.info("✅ Slack 광고 추천 전송 성공")
                    else:
                        self.logger.warning(f"⚠️ 광고 추천 전송 실패: {ad_response.status_code}")
                
            else:
                self.logger.error(f"❌ Slack 알림 전송 실패: {response.status_code}")
                self.logger.error(f"응답 내용: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Slack 알림 전송 오류: {e}")
            import traceback
            self.logger.error(f"상세 오류: {traceback.format_exc()}")
    
    async def _send_slack_article_complete(self, package: ArticlePackage):
        """완전한 기사를 Slack에 게시"""
        
        try:
            import requests
            from dotenv import load_dotenv
            
            load_dotenv()
            webhook_url = os.getenv('SLACK_WEBHOOK_URL')
            
            if not webhook_url:
                self.logger.error("❌ Slack 웹훅 URL이 설정되지 않았습니다")
                return
            
            # 메인 기사 게시 메시지
            main_message = {
                "text": f"📰 경제 뉴스 발행: {package.event.title}",
                "attachments": [
                    {
                        "color": "good",
                        "pretext": "🚀 새로운 경제 기사가 자동 생성되었습니다!",
                        "title": package.event.title,
                        "title_link": package.streamlit_url,
                        "text": package.event.description,
                        "fields": [
                            {
                                "title": "종목",
                                "value": package.event.symbol,
                                "short": True
                            },
                            {
                                "title": "변화율",
                                "value": f"{package.event.change_percent:+.2f}%",
                                "short": True
                            },
                            {
                                "title": "품질 점수",
                                "value": f"{package.review_result.get('quality_score', 0):.1f}/10",
                                "short": True
                            },
                            {
                                "title": "차트 수",
                                "value": f"{len(package.charts)}개",
                                "short": True
                            }
                        ],
                        "footer": "AI 경제 뉴스 시스템",
                        "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                        "ts": int(package.timestamp.timestamp())
                    }
                ]
            }
            
            # 메인 메시지 전송
            response = requests.post(webhook_url, json=main_message, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("✅ Slack 완전한 기사 게시 성공")
                return True
            else:
                self.logger.error(f"❌ Slack 기사 게시 실패: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Slack 완전한 기사 게시 오류: {e}")
            return False
    
    async def _upload_image_to_s3(self, image_path: str, bucket_name: str = "economic-news-images") -> str:
        """이미지를 S3에 업로드하고 공개 URL 반환"""
        
        try:
            import boto3
            from botocore.exceptions import ClientError
            import os
            
            # S3 클라이언트 생성
            s3_client = boto3.client('s3')
            
            # 파일명 생성
            filename = os.path.basename(image_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            s3_key = f"charts/{timestamp}_{filename}"
            
            # S3에 업로드 (버킷이 없으면 생성하지 않고 로컬 URL 사용)
            try:
                s3_client.upload_file(
                    image_path, 
                    bucket_name, 
                    s3_key,
                    ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'}
                )
                
                # 공개 URL 생성
                public_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
                self.logger.info(f"✅ S3 이미지 업로드 성공: {public_url}")
                return public_url
                
            except ClientError as e:
                # S3 업로드 실패 시 로컬 파일 경로 반환 (개발용)
                self.logger.warning(f"⚠️ S3 업로드 실패, 로컬 경로 사용: {e}")
                return f"file://{os.path.abspath(image_path)}"
            
        except Exception as e:
            self.logger.error(f"❌ 이미지 처리 실패: {e}")
            return None
    
    async def _send_slack_with_images(self, package: ArticlePackage):
        """이미지가 포함된 Slack 메시지 전송"""
        
        try:
            import requests
            from dotenv import load_dotenv
            
            load_dotenv()
            webhook_url = os.getenv('SLACK_WEBHOOK_URL')
            
            if not webhook_url:
                self.logger.error("❌ Slack 웹훅 URL이 설정되지 않았습니다")
                return
            
            # 이미지 정보만 포함한 메시지 (실제 이미지 업로드 없이)
            image_info = []
            
            # 기사 이미지 정보
            if package.article_image and os.path.exists(package.article_image):
                image_info.append(f"🖼️ 기사 이미지: {os.path.basename(package.article_image)}")
            
            # 차트 정보
            for i, chart_path in enumerate(package.charts):
                if os.path.exists(chart_path):
                    image_info.append(f"📊 차트 {i+1}: {os.path.basename(chart_path)}")
            
            # 이미지 정보 메시지 전송
            if image_info:
                image_message = {
                    "text": f"📷 {package.event.symbol} 관련 생성된 이미지들:",
                    "attachments": [
                        {
                            "color": "#ff9500",
                            "title": f"생성된 이미지 및 차트 ({len(image_info)}개)",
                            "text": "\n".join(image_info),
                            "footer": f"모든 이미지는 Streamlit 대시보드에서 확인 가능: {package.streamlit_url}"
                        }
                    ]
                }
                
                response = requests.post(webhook_url, json=image_message, timeout=10)
                
                if response.status_code == 200:
                    self.logger.info("✅ Slack 이미지 정보 전송 성공")
                else:
                    self.logger.warning(f"⚠️ Slack 이미지 정보 전송 실패: {response.status_code}")
            
            else:
                self.logger.info("📷 표시할 이미지 정보가 없습니다")
                
        except Exception as e:
            self.logger.error(f"Slack 이미지 정보 전송 오류: {e}")
            import traceback
            self.logger.error(f"상세 오류: {traceback.format_exc()}")

async def main():
    """메인 함수"""
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 통합 자동화 시스템 시작")
    print("=" * 60)
    
    # 오케스트레이터 초기화
    orchestrator = OrchestratorAgent()
    
    # 전체 자동화 사이클 실행
    packages = await orchestrator.run_full_automation_cycle()
    
    print(f"\\n✅ 자동화 완료: {len(packages)}개 기사 생성")
    
    for package in packages:
        print(f"📰 {package.event.symbol}: {package.event.title}")
        print(f"   🔗 Streamlit: {package.streamlit_url}")

if __name__ == "__main__":
    asyncio.run(main())
