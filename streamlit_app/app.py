"""
경제 뉴스 Streamlit 대시보드
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app.visualization_utils import ChartGenerator, NewsImageGenerator, AdGenerator
from agents.base_agent import AgentConfig
from agents.orchestrator_agent import OrchestratorAgent
from config.settings import load_config


class EconomicNewsDashboard:
    """경제 뉴스 대시보드 클래스"""
    
    def __init__(self):
        self.chart_generator = ChartGenerator()
        self.image_generator = NewsImageGenerator()
        self.ad_generator = AdGenerator()
        self.output_dir = "../output"
        
        # 페이지 설정
        st.set_page_config(
            page_title="경제 뉴스 AI 대시보드",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # 커스텀 CSS
        self.load_custom_css()
    
    def load_custom_css(self):
        """커스텀 CSS 로드"""
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .article-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 8px;
            color: white;
            text-align: center;
        }
        
        .news-headline {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 1rem;
            line-height: 1.2;
        }
        
        .news-lead {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 1.5rem;
            font-style: italic;
        }
        
        .news-content {
            font-size: 1rem;
            line-height: 1.6;
            color: #444;
            text-align: justify;
        }
        
        .tag {
            background-color: #e9ecef;
            color: #495057;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            margin-right: 0.5rem;
            display: inline-block;
        }
        
        .sidebar-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .ad-container {
            border-left: 4px solid #007cba;
            padding-left: 1rem;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def run(self):
        """메인 애플리케이션 실행"""
        # 헤더
        st.markdown("""
        <div class="main-header">
            <h1>📈 경제 뉴스 AI 대시보드</h1>
            <p>AWS Bedrock과 Strands Agent로 생성된 지능형 경제 분석</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 사이드바
        self.create_sidebar()
        
        # 메인 콘텐츠
        self.create_main_content()
    
    def create_sidebar(self):
        """사이드바 생성"""
        st.sidebar.markdown("## 🎛️ 제어판")
        
        # 새 기사 생성 버튼
        if st.sidebar.button("🚀 새 기사 생성", type="primary"):
            self.generate_new_article()
        
        # 기사 목록
        st.sidebar.markdown("## 📰 기사 목록")
        article_files = self.get_article_files()
        
        if article_files:
            selected_file = st.sidebar.selectbox(
                "기사 선택",
                article_files,
                format_func=lambda x: self.format_filename(x)
            )
            st.session_state['selected_article'] = selected_file
        else:
            st.sidebar.warning("생성된 기사가 없습니다.")
            st.session_state['selected_article'] = None
        
        # 설정
        st.sidebar.markdown("## ⚙️ 설정")
        
        show_charts = st.sidebar.checkbox("📊 차트 표시", value=True)
        show_images = st.sidebar.checkbox("🖼️ 이미지 표시", value=True)
        show_ads = st.sidebar.checkbox("📢 광고 표시", value=True)
        
        st.session_state.update({
            'show_charts': show_charts,
            'show_images': show_images,
            'show_ads': show_ads
        })
        
        # 시스템 정보
        st.sidebar.markdown("## ℹ️ 시스템 정보")
        st.sidebar.info(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    def create_main_content(self):
        """메인 콘텐츠 생성"""
        if 'selected_article' not in st.session_state or not st.session_state['selected_article']:
            self.show_welcome_screen()
            return
        
        # 선택된 기사 로드
        article_data = self.load_article_data(st.session_state['selected_article'])
        if not article_data:
            st.error("기사 데이터를 로드할 수 없습니다.")
            return
        
        # 기사 표시
        self.display_article(article_data)
    
    def show_welcome_screen(self):
        """환영 화면 표시"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2>🎯 경제 뉴스 AI 시스템에 오신 것을 환영합니다!</h2>
                <p style="font-size: 1.2rem; color: #666;">
                    AWS Bedrock과 Strands Agent를 활용한 지능형 경제 기사 생성 시스템입니다.
                </p>
                <br>
                <p>사이드바에서 <strong>"새 기사 생성"</strong> 버튼을 클릭하여 시작하세요.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 시스템 기능 소개
            st.markdown("### 🚀 주요 기능")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("""
                - 📊 **실시간 데이터 수집**
                - 🤖 **AI 기반 기사 작성**
                - 📈 **인터랙티브 차트**
                - 🖼️ **자동 이미지 생성**
                """)
            
            with col_b:
                st.markdown("""
                - 🎯 **콘텐츠 최적화**
                - 📢 **맞춤형 광고**
                - 📱 **반응형 디자인**
                - 🔄 **실시간 업데이트**
                """)
    
    def display_article(self, article_data: Dict[str, Any]):
        """기사 표시"""
        # 기사 메타데이터
        collected_data = article_data.get('collected_data', {})
        articles = article_data.get('optimized_articles', article_data.get('articles', []))
        
        if not articles:
            st.error("표시할 기사가 없습니다.")
            return
        
        article_info = articles[0]  # 첫 번째 기사 사용
        article = article_info.get('optimized_article', article_info.get('article', {}))
        
        # 메트릭 표시
        self.display_metrics(collected_data)
        
        # 차트 표시
        if st.session_state.get('show_charts', True):
            self.display_charts(collected_data)
        
        # 기사 본문
        self.display_article_content(article, article_info)
        
        # 광고 표시
        if st.session_state.get('show_ads', True):
            self.display_ads(article)
    
    def display_metrics(self, collected_data: Dict[str, Any]):
        """메트릭 표시"""
        st.markdown("## 📊 시장 현황")
        
        stock_data = collected_data.get('stock_data', {})
        economic_data = collected_data.get('economic_data', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        # S&P 500
        if '^GSPC' in stock_data:
            sp500 = stock_data['^GSPC']
            with col1:
                st.metric(
                    "S&P 500",
                    f"{sp500.get('current_price', 0):.2f}",
                    f"{sp500.get('change_percent', 0):.2f}%"
                )
        
        # 나스닥
        if '^IXIC' in stock_data:
            nasdaq = stock_data['^IXIC']
            with col2:
                st.metric(
                    "나스닥",
                    f"{nasdaq.get('current_price', 0):.2f}",
                    f"{nasdaq.get('change_percent', 0):.2f}%"
                )
        
        # VIX
        if 'VIX' in economic_data:
            vix = economic_data['VIX']
            with col3:
                st.metric(
                    "VIX",
                    f"{vix.get('value', 0):.2f}",
                    vix.get('interpretation', '')
                )
        
        # 달러 인덱스
        if 'DXY' in economic_data:
            dxy = economic_data['DXY']
            with col4:
                st.metric(
                    "달러 인덱스",
                    f"{dxy.get('value', 0):.2f}",
                    dxy.get('interpretation', '')
                )
    
    def display_charts(self, collected_data: Dict[str, Any]):
        """차트 표시"""
        st.markdown("## 📈 시장 분석")
        
        stock_data = collected_data.get('stock_data', {})
        economic_data = collected_data.get('economic_data', {})
        
        # 차트 탭
        tab1, tab2, tab3, tab4 = st.tabs(["주식 현황", "변화율", "섹터 성과", "VIX 지수"])
        
        with tab1:
            fig1 = self.chart_generator.create_stock_price_chart(stock_data)
            st.plotly_chart(fig1, use_container_width=True)
        
        with tab2:
            fig2 = self.chart_generator.create_change_percentage_chart(stock_data)
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            fig3 = self.chart_generator.create_sector_performance_chart(stock_data)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns([1, 1])
            with col1:
                fig4 = self.chart_generator.create_vix_fear_greed_gauge(economic_data)
                st.plotly_chart(fig4, use_container_width=True)
            with col2:
                fig5 = self.chart_generator.create_market_cap_pie_chart(stock_data)
                st.plotly_chart(fig5, use_container_width=True)
    
    def display_article_content(self, article: Dict[str, Any], article_info: Dict[str, Any]):
        """기사 내용 표시"""
        st.markdown("## 📰 경제 뉴스")
        
        # 기사 컨테이너
        with st.container():
            # 헤드라인
            st.markdown(f'<div class="news-headline">{article.get("headline", "제목 없음")}</div>', 
                       unsafe_allow_html=True)
            
            # 리드
            if article.get('lead'):
                st.markdown(f'<div class="news-lead">{article.get("lead")}</div>', 
                           unsafe_allow_html=True)
            
            # 이미지 표시
            if st.session_state.get('show_images', True):
                self.display_article_images(article)
            
            # 본문
            content = article.get('content', '')
            if content:
                # JSON 형태의 내용을 파싱하여 표시
                try:
                    if content.startswith('{') and content.endswith('}'):
                        content_json = json.loads(content)
                        actual_content = content_json.get('content', content)
                    else:
                        actual_content = content
                except:
                    actual_content = content
                
                st.markdown(f'<div class="news-content">{actual_content.replace("<br>", "<br/>")}</div>', 
                           unsafe_allow_html=True)
            
            # 결론
            if article.get('conclusion'):
                st.markdown("### 💡 결론")
                st.info(article.get('conclusion'))
            
            # 태그
            if article.get('tags'):
                st.markdown("### 🏷️ 태그")
                tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in article.get('tags', [])])
                st.markdown(tags_html, unsafe_allow_html=True)
            
            # 품질 정보
            quality_check = article_info.get('quality_check', {})
            if quality_check:
                st.markdown("### 📊 기사 품질 정보")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("전체 점수", f"{quality_check.get('overall_score', 0)}/100")
                with col2:
                    st.metric("정확성", f"{quality_check.get('scores', {}).get('accuracy', 0)}/100")
                with col3:
                    st.metric("가독성", f"{quality_check.get('scores', {}).get('clarity', 0)}/100")
    
    def display_article_images(self, article: Dict[str, Any]):
        """기사 관련 이미지 표시"""
        col1, col2 = st.columns(2)
        
        with col1:
            # 기사 일러스트레이션
            illustration_url = self.image_generator.generate_article_illustration(
                article.get('content', ''), 
                'market_summary'
            )
            if illustration_url:
                st.image(illustration_url, caption="기사 일러스트레이션", use_column_width=True)
        
        with col2:
            # 워드클라우드
            wordcloud_img = self.image_generator.create_wordcloud_from_article(
                article.get('content', '')
            )
            if wordcloud_img:
                st.image(wordcloud_img, caption="키워드 클라우드", use_column_width=True)
    
    def display_ads(self, article: Dict[str, Any]):
        """광고 표시"""
        st.markdown("## 📢 추천 서비스")
        
        # 기사 기반 맞춤 광고 생성
        ads = self.ad_generator.generate_contextual_ads(
            article.get('content', ''),
            article.get('tags', [])
        )
        
        if ads:
            cols = st.columns(len(ads))
            for i, ad in enumerate(ads):
                with cols[i]:
                    ad_html = self.ad_generator.create_ad_html(ad)
                    st.markdown(ad_html, unsafe_allow_html=True)
    
    def generate_new_article(self):
        """새 기사 생성"""
        with st.spinner("새로운 경제 기사를 생성하고 있습니다..."):
            try:
                # 설정 로드
                config = load_config()
                agent_config = AgentConfig(
                    name="StreamlitOrchestrator",
                    model_id=config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
                    region=config.get("aws_region", "us-east-1")
                )
                
                # 오케스트레이터 생성
                orchestrator = OrchestratorAgent(agent_config)
                
                # 전체 파이프라인 실행
                input_data = {
                    "workflow_type": "full_pipeline",
                    "article_configs": [
                        {"article_type": "market_summary", "target_length": "medium"}
                    ]
                }
                
                result = orchestrator.process(input_data)
                
                st.success("새 기사가 성공적으로 생성되었습니다!")
                st.rerun()
                
            except Exception as e:
                st.error(f"기사 생성 중 오류가 발생했습니다: {str(e)}")
    
    def get_article_files(self) -> List[str]:
        """기사 파일 목록 가져오기"""
        output_path = os.path.join(os.path.dirname(__file__), self.output_dir)
        
        if not os.path.exists(output_path):
            return []
        
        files = []
        for filename in os.listdir(output_path):
            if filename.startswith('pipeline_result_') and filename.endswith('.json'):
                files.append(filename)
        
        return sorted(files, reverse=True)  # 최신 파일 먼저
    
    def load_article_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """기사 데이터 로드"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), self.output_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"파일 로드 오류: {str(e)}")
            return None
    
    def format_filename(self, filename: str) -> str:
        """파일명 포맷팅"""
        # pipeline_result_20250804_075502.json -> 2025-08-04 07:55:02
        try:
            timestamp_part = filename.replace('pipeline_result_', '').replace('.json', '')
            date_part = timestamp_part[:8]
            time_part = timestamp_part[9:]
            
            formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
            formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
            
            return f"{formatted_date} {formatted_time}"
        except:
            return filename


def main():
    """메인 함수"""
    dashboard = EconomicNewsDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
