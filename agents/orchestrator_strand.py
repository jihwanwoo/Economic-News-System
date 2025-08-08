"""
오케스트레이터 Strand Agent
전체 경제 뉴스 생성 워크플로우를 관리하고 조율
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio

from .strands_framework import BaseStrandAgent, StrandContext, StrandMessage, MessageType, StrandOrchestrator, orchestrator
from .data_analysis_strand import DataAnalysisStrand
from .article_writer_strand import ArticleWriterStrand
from .review_strand import ReviewStrand
from .image_generator_strand import ImageGeneratorStrand
from .ad_recommendation_strand import AdRecommendationStrand

class OrchestratorStrand(BaseStrandAgent):
    """오케스트레이터 Strand Agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="orchestrator",
            name="오케스트레이터 에이전트"
        )
        
        self.capabilities = [
            "workflow_management",
            "agent_coordination",
            "quality_control",
            "output_generation",
            "system_monitoring"
        ]
        
        # 하위 에이전트들 초기화 및 등록
        self._initialize_agents()
        
        # 출력 디렉토리 설정
        self.output_dirs = {
            'articles': 'output/automated_articles',
            'streamlit': 'streamlit_articles',
            'charts': 'output/charts',
            'images': 'output/images'
        }
        
        for dir_path in self.output_dirs.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def _initialize_agents(self):
        """하위 에이전트들 초기화 및 등록"""
        
        # 에이전트 인스턴스 생성
        self.data_analyst = DataAnalysisStrand()
        self.article_writer = ArticleWriterStrand()
        self.reviewer = ReviewStrand()
        self.image_generator = ImageGeneratorStrand()
        self.ad_recommender = AdRecommendationStrand()
        
        # 글로벌 오케스트레이터에 등록
        orchestrator.register_agent(self.data_analyst)
        orchestrator.register_agent(self.article_writer)
        orchestrator.register_agent(self.reviewer)
        orchestrator.register_agent(self.image_generator)
        orchestrator.register_agent(self.ad_recommender)
        
        self.logger.info("✅ 모든 하위 에이전트 초기화 완료")
    
    def get_capabilities(self) -> List[str]:
        """에이전트 능력 반환"""
        return self.capabilities
    
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """전체 워크플로우 처리 (비동기)"""
        
        event_data = context.input_data.get('event')
        if not event_data:
            raise Exception("처리할 이벤트 데이터가 없습니다")
        
        symbol = event_data.get('symbol', 'Unknown')
        self.logger.info(f"🚀 {symbol} 전체 워크플로우 시작")
        
        try:
            # 워크플로우 정의
            workflow = [
                'data_analyst',      # 1. 데이터 분석
                'article_writer',    # 2. 기사 작성
                'reviewer',          # 3. 기사 검수
                'image_generator',   # 4. 이미지 생성
                'ad_recommender'     # 5. 광고 추천
            ]
            
            # Strand 실행
            strand_id = f"news_generation_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result_context = await orchestrator.execute_strand(strand_id, context.input_data, workflow)
            
            if result_context.status.value == 'completed':
                # 최종 패키지 생성
                final_package = await self._create_final_package(result_context)
                
                self.logger.info(f"✅ {symbol} 전체 워크플로우 완료")
                return final_package
            else:
                raise Exception(f"워크플로우 실행 실패: {result_context.status}")
                
        except Exception as e:
            self.logger.error(f"❌ {symbol} 워크플로우 실패: {str(e)}")
            raise
    
    def execute_data_analysis(self, context: StrandContext) -> Dict[str, Any]:
        """데이터 분석 실행"""
        try:
            self.logger.info("📊 데이터 분석 시작")
            
            # 데이터 분석 에이전트 실행
            analysis_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="데이터 분석 요청",
                data=context.input_data
            )
            
            # 동기적으로 실행 (Streamlit 호환)
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.data_analyst.process(context, analysis_message)
                )
                self.logger.info("✅ 데이터 분석 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 데이터 분석 실패: {str(e)}")
            return {}
    
    def execute_article_writing(self, context: StrandContext) -> Dict[str, Any]:
        """기사 작성 실행"""
        try:
            self.logger.info("✍️ 기사 작성 시작")
            
            writing_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="기사 작성 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.article_writer.process(context, writing_message)
                )
                self.logger.info("✅ 기사 작성 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 기사 작성 실패: {str(e)}")
            return {}
    
    def execute_image_generation(self, context: StrandContext) -> Dict[str, Any]:
        """이미지 생성 실행"""
        try:
            self.logger.info("🎨 이미지 생성 시작")
            
            image_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="이미지 생성 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.image_generator.process(context, image_message)
                )
                self.logger.info("✅ 이미지 생성 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 이미지 생성 실패: {str(e)}")
            return {}
    
    def execute_review(self, context: StrandContext) -> Dict[str, Any]:
        """기사 검수 실행"""
        try:
            self.logger.info("🔍 기사 검수 시작")
            
            review_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="기사 검수 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.reviewer.process(context, review_message)
                )
                self.logger.info("✅ 기사 검수 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 기사 검수 실패: {str(e)}")
            return {}
    
    def execute_ad_recommendation(self, context: StrandContext) -> Dict[str, Any]:
        """광고 추천 실행"""
        try:
            self.logger.info("📢 광고 추천 시작")
            
            ad_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="광고 추천 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.ad_recommender.process(context, ad_message)
                )
                self.logger.info("✅ 광고 추천 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 광고 추천 실패: {str(e)}")
            return {}
        """데이터 분석 실행"""
        try:
            self.logger.info("📊 데이터 분석 시작")
            
            # 데이터 분석 에이전트 실행
            analysis_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="데이터 분석 요청",
                data=context.input_data
            )
            
            # 동기적으로 실행 (Streamlit 호환)
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.data_analyst.process(context, analysis_message)
                )
                self.logger.info("✅ 데이터 분석 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 데이터 분석 실패: {str(e)}")
            return {}
    
    def execute_article_writing(self, context: StrandContext) -> Dict[str, Any]:
        """기사 작성 실행"""
        try:
            self.logger.info("✍️ 기사 작성 시작")
            
            writing_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="기사 작성 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.article_writer.process(context, writing_message)
                )
                self.logger.info("✅ 기사 작성 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 기사 작성 실패: {str(e)}")
            return {}
    
    def execute_image_generation(self, context: StrandContext) -> Dict[str, Any]:
        """이미지 생성 실행"""
        try:
            self.logger.info("🎨 이미지 생성 시작")
            
            image_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="이미지 생성 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.image_generator.process(context, image_message)
                )
                self.logger.info("✅ 이미지 생성 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 이미지 생성 실패: {str(e)}")
            return {}
    
    def execute_review(self, context: StrandContext) -> Dict[str, Any]:
        """기사 검수 실행"""
        try:
            self.logger.info("🔍 기사 검수 시작")
            
            review_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="기사 검수 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.reviewer.process(context, review_message)
                )
                self.logger.info("✅ 기사 검수 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 기사 검수 실패: {str(e)}")
            return {}
    
    def execute_ad_recommendation(self, context: StrandContext) -> Dict[str, Any]:
        """광고 추천 실행"""
        try:
            self.logger.info("📢 광고 추천 시작")
            
            ad_message = StrandMessage(
                message_type=MessageType.REQUEST,
                content="광고 추천 요청",
                data=context.input_data
            )
            
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    self.ad_recommender.process(context, ad_message)
                )
                self.logger.info("✅ 광고 추천 완료")
                return result
            finally:
                loop.close()
                
        except Exception as e:
            self.logger.error(f"❌ 광고 추천 실패: {str(e)}")
            return {}
    
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """전체 워크플로우 처리"""
        
        event_data = context.input_data.get('event')
        if not event_data:
            raise Exception("처리할 이벤트 데이터가 없습니다")
        
        symbol = event_data.get('symbol', 'Unknown')
        self.logger.info(f"🚀 {symbol} 전체 워크플로우 시작")
        
        try:
            # 워크플로우 정의
            workflow = [
                'data_analyst',      # 1. 데이터 분석
                'article_writer',    # 2. 기사 작성
                'reviewer',          # 3. 기사 검수
                'image_generator',   # 4. 이미지 생성
                'ad_recommender'     # 5. 광고 추천
            ]
            
            # Strand 실행
            strand_id = f"news_generation_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result_context = await orchestrator.execute_strand(strand_id, context.input_data, workflow)
            
            if result_context.status.value == 'completed':
                # 최종 패키지 생성
                final_package = await self._create_final_package(result_context)
                
                # 출력 파일 생성
                output_files = await self._generate_output_files(final_package)
                
                # Streamlit 페이지 생성
                streamlit_page = await self._generate_streamlit_page(final_package)
                
                result = {
                    'status': 'success',
                    'package': final_package,
                    'output_files': output_files,
                    'streamlit_page': streamlit_page,
                    'execution_time': (datetime.now() - result_context.created_at).total_seconds(),
                    'strand_id': strand_id
                }
                
                self.logger.info(f"✅ {symbol} 전체 워크플로우 완료")
                return result
            else:
                raise Exception(f"워크플로우 실행 실패: {result_context.error}")
                
        except Exception as e:
            self.logger.error(f"❌ 워크플로우 실행 실패: {e}")
            raise
    
    async def _create_final_package(self, context: StrandContext) -> Dict[str, Any]:
        """최종 패키지 생성"""
        
        # 각 에이전트 결과 수집
        data_analysis = context.results.get('data_analyst', {})
        article = context.results.get('article_writer', {})
        review_result = context.results.get('reviewer', {})
        images = context.results.get('image_generator', {})
        advertisements = context.results.get('ad_recommender', {})
        
        # 이벤트 데이터
        event_data = context.input_data.get('event', {})
        
        # 최종 패키지 구성
        package = {
            'event': event_data,
            'data_analysis': data_analysis,
            'article': article,
            'review_result': review_result,
            'images': images,
            'advertisements': advertisements.get('recommended_ads', []),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'strand_id': context.strand_id,
                'processing_time_seconds': (datetime.now() - context.created_at).total_seconds(),
                'quality_score': review_result.get('overall_score', 0),
                'agent_versions': {
                    'data_analyst': '1.0.0',
                    'article_writer': '1.0.0',
                    'reviewer': '1.0.0',
                    'image_generator': '1.0.0',
                    'ad_recommender': '1.0.0'
                }
            }
        }
        
        return package
    
    async def _generate_output_files(self, package: Dict[str, Any]) -> Dict[str, str]:
        """출력 파일 생성"""
        
        symbol = package['event'].get('symbol', 'Unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        output_files = {}
        
        try:
            # 1. JSON 파일 저장
            json_filename = f"{symbol}_{timestamp}.json"
            json_filepath = os.path.join(self.output_dirs['articles'], json_filename)
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(package, f, ensure_ascii=False, indent=2, default=str)
            
            output_files['json'] = json_filepath
            
            # 2. HTML 파일 생성
            html_content = await self._generate_html_article(package)
            html_filename = f"{symbol}_{timestamp}.html"
            html_filepath = os.path.join(self.output_dirs['articles'], html_filename)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            output_files['html'] = html_filepath
            
            self.logger.info(f"📁 출력 파일 생성 완료: {len(output_files)}개")
            return output_files
            
        except Exception as e:
            self.logger.error(f"❌ 출력 파일 생성 실패: {e}")
            return output_files
    
    async def _generate_html_article(self, package: Dict[str, Any]) -> str:
        """HTML 기사 생성"""
        
        article = package.get('article', {})
        event = package.get('event', {})
        images = package.get('images', {})
        ads = package.get('advertisements', [])
        review = package.get('review_result', {})
        
        # f-string에서 백슬래시 문제 해결을 위해 변수로 분리
        newline_br = '<br>'
        
        html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.get('title', '경제 뉴스')}</title>
    <style>
        body {{ font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ background: #f4f4f4; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .title {{ font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }}
        .meta {{ color: #666; font-size: 14px; }}
        .lead {{ font-size: 18px; font-weight: 500; color: #444; margin: 20px 0; }}
        .content {{ margin: 20px 0; }}
        .conclusion {{ background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .image {{ text-align: center; margin: 20px 0; }}
        .ads {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .ad-item {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        .quality-score {{ background: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">{article.get('title', '경제 뉴스')}</div>
            <div class="meta">
                심볼: {event.get('symbol', 'N/A')} | 
                이벤트: {event.get('event_type', 'N/A')} | 
                생성시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>
        
        <div class="lead">{article.get('lead', '')}</div>
        
        {f"<div class='image'><img src='{images.get('main_image', '')}' alt='기사 이미지' style='max-width: 100%; height: auto;'></div>" if images.get('main_image') else ""}
        
        <div class="content">
            {article.get('body', '').replace(chr(10), newline_br)}
        </div>
        
        <div class="conclusion">
            <strong>결론:</strong><br>
            {article.get('conclusion', '')}
        </div>
        
        {f"<div class='quality-score'><strong>품질 점수:</strong> {review.get('overall_score', 'N/A')}/10</div>" if review.get('overall_score') else ""}
        
        <div class="ads">
            <h3>관련 서비스</h3>
            {"".join([f"<div class='ad-item'><strong>{ad.get('title', '')}</strong>{newline_br}{ad.get('description', '')}{newline_br}<em>{ad.get('cta', '')}</em></div>" for ad in ads[:3]])}
        </div>
        
        <div class="meta" style="margin-top: 30px; text-align: center; color: #999;">
            본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다.{newline_br}
            투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.
        </div>
    </div>
</body>
</html>""".strip()
        
        return html_template
    
    async def _generate_streamlit_page(self, package: Dict[str, Any]) -> str:
        """Streamlit 페이지 생성"""
        
        symbol = package['event'].get('symbol', 'Unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"article_{symbol}_{timestamp}.py"
        filepath = os.path.join(self.output_dirs['streamlit'], filename)
        
        try:
            article = package.get('article', {})
            event = package.get('event', {})
            images = package.get('images', {})
            ads = package.get('advertisements', [])
            review = package.get('review_result', {})
            data_analysis = package.get('data_analysis', {})
            
            # 차트 경로들 수집
            chart_paths = data_analysis.get('chart_paths', [])
            
            # Streamlit 코드 템플릿 (f-string 문제 해결)
            streamlit_template = '''#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
{symbol} - {title}
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
    page_title="{title}",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 {title}")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "{symbol}")
    
    with col2:
        st.metric("이벤트", "{event_type}")
    
    with col3:
        st.metric("품질점수", "{quality_score}/10")
    
    with col4:
        st.metric("생성시간", "{gen_time}")
    
    # 기사 이미지
    {image_code}
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""{lead}

{body}

## 결론

{conclusion}

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = {chart_paths_list}
    chart_paths = [path for path in chart_paths if os.path.exists(path)]
    
    if chart_paths:
        for i, chart_path in enumerate(chart_paths):
            st.markdown(f"### 📊 Chart {{i+1}}")
            try:
                if chart_path.endswith('.html'):
                    # HTML 파일을 iframe으로 표시
                    with open(chart_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    components.html(html_content, height=600, scrolling=True)
                elif chart_path.endswith(('.png', '.jpg', '.jpeg')):
                    # 이미지 파일 표시
                    st.image(chart_path, caption=f"Chart {{i+1}}", use_column_width=True)
                else:
                    st.info(f"Chart file: {{os.path.basename(chart_path)}}")
            except Exception as e:
                st.error(f"Chart loading error: {{str(e)}}")
                st.info(f"Chart file path: {{chart_path}}")
    else:
        st.info("No charts available for this article.")
    
    # 검수 결과
    {review_code}
    
    # 광고 추천
    st.markdown("## 📢 관련 서비스")
    ads_data = {ads_data}
    
    if ads_data:
        for i, ad in enumerate(ads_data[:3]):
            with st.expander(f"{{ad.get('title', f'서비스 {{i+1}}')}}", expanded=False):
                st.write(ad.get('description', ''))
                if ad.get('cta'):
                    st.button(ad.get('cta', '자세히 보기'), key=f"ad_{{i}}")
    else:
        st.info("추천 서비스가 없습니다.")

if __name__ == "__main__":
    main()
'''
            
            # 템플릿 변수 준비
            image_code = ""
            if images.get('article_image'):
                article_image_path = images.get('article_image', '')
                image_code += f'''
    # 기사 관련 이미지
    if os.path.exists("{article_image_path}"):
        st.image("{article_image_path}", caption="기사 관련 일러스트레이션", use_column_width=True)
    '''
            
            if images.get('event_image'):
                event_image_path = images.get('event_image', '')
                image_code += f'''
    if os.path.exists("{event_image_path}"):
        st.image("{event_image_path}", caption="이벤트 분석 차트", use_column_width=True)
    '''
            
            if images.get('wordcloud'):
                wordcloud_path = images.get('wordcloud', '')
                image_code += f'''
    if os.path.exists("{wordcloud_path}"):
        st.image("{wordcloud_path}", caption="기사 키워드 워드클라우드", use_column_width=True)
    '''
            
            if not image_code:
                image_code = "    # 이미지 없음"
            
            review_code = ""
            if review:
                review_code = '''st.markdown("## 🔍 검수 결과")
    st.json(''' + str(review) + ''')'''
            
            # 템플릿 포맷팅
            streamlit_code = streamlit_template.format(
                symbol=symbol,
                title=article.get('title', '경제 뉴스'),
                event_type=event.get('event_type', 'N/A').upper(),
                quality_score=review.get('overall_score', 'N/A'),
                gen_time=datetime.now().strftime('%H:%M'),
                image_code=image_code,
                lead=article.get('lead', ''),
                body=article.get('body', ''),
                conclusion=article.get('conclusion', ''),
                chart_paths_list=chart_paths,
                review_code=review_code,
                ads_data=ads
            )
            
            # 광고 섹션을 기사 뒤에 추가
            ads_section = '''
    # 📢 관련 서비스 및 상품 추천
    
    st.markdown("---")
    st.markdown("### 🎯 맞춤형 추천 서비스")
    
    ads_data = ''' + str(ads) + '''
    
    if ads_data and len(ads_data) >= 3:
        # 3개 광고를 컬럼으로 표시
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ad = ads_data[0]
            st.markdown(f"#### 🔹 {ad.get('title', '서비스 1')}")
            st.write(ad.get('description', ''))
            if ad.get('cta'):
                st.button(ad.get('cta', '자세히 보기'), key="ad_1", use_container_width=True)
            st.markdown(f"**카테고리:** {ad.get('category', 'general')}")
            if ad.get('match_reasons'):
                st.markdown(f"**추천 이유:** {', '.join(ad.get('match_reasons', [])[:2])}")
        
        with col2:
            ad = ads_data[1]
            st.markdown(f"#### 🔹 {ad.get('title', '서비스 2')}")
            st.write(ad.get('description', ''))
            if ad.get('cta'):
                st.button(ad.get('cta', '자세히 보기'), key="ad_2", use_container_width=True)
            st.markdown(f"**카테고리:** {ad.get('category', 'general')}")
            if ad.get('match_reasons'):
                st.markdown(f"**추천 이유:** {', '.join(ad.get('match_reasons', [])[:2])}")
        
        with col3:
            ad = ads_data[2]
            st.markdown(f"#### 🔹 {ad.get('title', '서비스 3')}")
            st.write(ad.get('description', ''))
            if ad.get('cta'):
                st.button(ad.get('cta', '자세히 보기'), key="ad_3", use_container_width=True)
            st.markdown(f"**카테고리:** {ad.get('category', 'general')}")
            if ad.get('match_reasons'):
                st.markdown(f"**추천 이유:** {', '.join(ad.get('match_reasons', [])[:2])}")
    else:
        st.info("현재 추천 가능한 서비스가 없습니다.")
    
    st.markdown("---")
    st.markdown("*위 추천 서비스들은 기사 내용을 분석하여 AI가 자동으로 선별한 것입니다.*")
'''
            
            # 기존 광고 섹션을 새로운 것으로 교체
            streamlit_code = streamlit_code.replace(
                '''    # 광고 추천
    st.markdown("## 📢 관련 서비스")
    ads_data = ''' + str(ads) + '''
    
    if ads_data:
        for i, ad in enumerate(ads_data[:3]):
            with st.expander(f"{ad.get('title', f'서비스 {i+1}')}", expanded=False):
                st.write(ad.get('description', ''))
                if ad.get('cta'):
                    st.button(ad.get('cta', '자세히 보기'), key=f"ad_{i}")
    else:
        st.info("추천 서비스가 없습니다.")''',
                ads_section
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(streamlit_code)
            
            self.logger.info(f"📄 Streamlit 페이지 생성: {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"❌ Streamlit 페이지 생성 실패: {e}")
            return ""
    
    async def process_multiple_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """여러 이벤트 동시 처리"""
        
        self.logger.info(f"🔄 {len(events)}개 이벤트 동시 처리 시작")
        
        tasks = []
        for i, event in enumerate(events):
            context = StrandContext(
                strand_id=f"multi_event_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                input_data={'event': event}
            )
            tasks.append(self.process(context))
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful_results = []
            failed_count = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"❌ 이벤트 {i+1} 처리 실패: {result}")
                    failed_count += 1
                else:
                    successful_results.append(result)
            
            self.logger.info(f"✅ 다중 이벤트 처리 완료: {len(successful_results)}개 성공, {failed_count}개 실패")
            return successful_results
            
        except Exception as e:
            self.logger.error(f"❌ 다중 이벤트 처리 실패: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """시스템 상태 조회"""
        
        return {
            'orchestrator_status': 'active',
            'registered_agents': list(orchestrator.agents.keys()),
            'agent_capabilities': orchestrator.list_agents(),
            'output_directories': self.output_dirs,
            'last_check': datetime.now().isoformat()
        }

# 전역 오케스트레이터 인스턴스
main_orchestrator = OrchestratorStrand()
