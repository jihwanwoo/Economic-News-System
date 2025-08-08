#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
GOOGL - 구글 주식 거래량 급증, 기술주 랠리 지속 가능성 주목
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
    page_title="구글 주식 거래량 급증, 기술주 랠리 지속 가능성 주목",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 구글 주식 거래량 급증, 기술주 랠리 지속 가능성 주목")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "GOOGL")
    
    with col2:
        st.metric("이벤트", "VOLUME_SPIKE")
    
    with col3:
        st.metric("품질점수", "7.8/10")
    
    with col4:
        st.metric("생성시간", "07:18")
    
    # 기사 이미지
    
    # 기사 관련 이미지
    if os.path.exists("output/images/GOOGL_article_illustration_20250807_071838.png"):
        st.image("output/images/GOOGL_article_illustration_20250807_071838.png", caption="기사 관련 일러스트레이션", use_column_width=True)
    
    if os.path.exists("output/images/GOOGL_fallback_20250807_071838.png"):
        st.image("output/images/GOOGL_fallback_20250807_071838.png", caption="이벤트 분석 차트", use_column_width=True)
    
    if os.path.exists("output/images/GOOGL_wordcloud_20250807_071839.png"):
        st.image("output/images/GOOGL_wordcloud_20250807_071839.png", caption="기사 키워드 워드클라우드", use_column_width=True)
    
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""구글 모회사 알파벳(GOOGL)의 주식 거래량이 평소보다 60% 가량 증가한 것으로 나타났다. 이는 인공지능(AI) 기술 경쟁이 본격화되면서 기술주에 대한 투자 관심이 높아진 데 따른 것으로 분석된다. 이번 거래량 급증이 단기 변동에 그칠지, 아니면 기술주 랠리의 지속 가능성을 시사하는지에 대해 전문가들의 의견이 엇갈린다.

구글 모회사 알파벳(GOOGL)의 주가는 지난 거래일 196.09달러로 거래를 마감했다. 주목할 점은 이날 알파벳의 거래량이 2,152만주로 평소 거래량 대비 약 60% 증가한 것이다. 이처럼 거래량이 급증한 원인에 대해 전문가들은 최근 인공지능(AI) 기술 경쟁 가열로 인한 기술주 관심 증가를 주된 요인으로 꼽고 있다. 구글을 비롯한 빅테크 기업들이 AI 분야에서 공격적인 투자와 인수합병을 단행하면서 관련 기술 선점 경쟁이 가열되고 있기 때문이다. 실제로 알파벳의 기술적 지표를 살펴보면 단기 과열 조짐이 있다. 상대적 강도 지수(RSI)가 69.9로 과매수 구간에 근접했으며, 거래량 비율 역시 0.6배로 평균치를 상회한다. 다만 이는 최근 강세장 영향으로 보이며, 20일 이동평균선 대비 3.7% 프리미엄에 그치고 있어 과도한 수준은 아닌 것으로 분석된다. 한편 알파벳의 연율 변동성은 0.2%에 불과해 단기 변동성은 크지 않은 편이다. 또한 시장 베타값이 1.08로 시장 평균 수준을 유지 중이며, S&P500 지수와의 상관계수도 0.51로 보통 수준이다. 전문가들은 이번 거래량 급증세가 일시적인 현상으로 그칠지, 아니면 기술주 랠리의 지속 가능성을 시사하는지에 대해 엇갈린 견해를 보이고 있다. 베어 시각에서는 빅테크 기업들의 AI 기술력 과시와 마케팅에 주목한 나머지 실제 수익 창출 능력을 간과하고 있다는 지적이 나온다. 이에 따라 단기적으로는 AI 관련 기업들의 주가가 과열될 수 있지만, 실적이 가시화되지 않는다면 거품이 꺼질 수밖에 없다는 것이다. 반면 AI가 새로운 산업혁명을 주도할 것이라는 낙관론도 있다. 구글, 마이크로소프트, 아마존 등 빅테크 기업들이 보유한 방대한 데이터와 기술력, 자금력을 감안할 때 AI 분야에서 실질적인 성과를 내고 새로운 수익을 창출할 것이라는 전망이다. 이 경우 현재의 주가 상승세가 지속될 가능성이 높다.

## 결론

알파벳을 비롯한 기술주 랠리가 이어질지, 아니면 일시적 변동에 그칠지에 대해서는 전문가들 사이에서도 견해 차이가 있다. 다만 기술주 투자에는 AI 기술 발전과 실제 수익 창출 능력에 대한 면밀한 분석이 필요할 것으로 보인다. 단기적으로는 AI 관련 이슈에 주가가 민감하게 반응할 수 있지만, 중장기적으로는 실적과 성장성에 기반한 합리적 투자 판단이 요구된다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = ['output/charts/GOOGL_price_volume_20250807_071754.html', 'output/charts/GOOGL_technical_20250807_071754.html', 'output/charts/GOOGL_recent_20250807_071754.html', 'output/charts/GOOGL_comparison_20250807_071754.html']
    chart_paths = [path for path in chart_paths if os.path.exists(path)]
    
    if chart_paths:
        for i, chart_path in enumerate(chart_paths):
            st.markdown(f"### 📊 Chart {i+1}")
            try:
                if chart_path.endswith('.html'):
                    # HTML 파일을 iframe으로 표시
                    with open(chart_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    components.html(html_content, height=600, scrolling=True)
                elif chart_path.endswith(('.png', '.jpg', '.jpeg')):
                    # 이미지 파일 표시
                    st.image(chart_path, caption=f"Chart {i+1}", use_column_width=True)
                else:
                    st.info(f"Chart file: {os.path.basename(chart_path)}")
            except Exception as e:
                st.error(f"Chart loading error: {str(e)}")
                st.info(f"Chart file path: {chart_path}")
    else:
        st.info("No charts available for this article.")
    
    # 검수 결과
    st.markdown("## 🔍 검수 결과")
    st.json({'overall_score': 7.8, 'detailed_scores': {'content_accuracy': 7.5, 'readability': 7.5, 'completeness': 7.8, 'compliance': 8.0, 'engagement': 8.700000000000001}, 'improvements': [], 'review_timestamp': '2025-08-07T07:18:38.367528', 'reviewer': '기사 검수 에이전트', 'status': 'approved'})
    

    # 📢 관련 서비스 및 상품 추천
    
    st.markdown("---")
    st.markdown("### 🎯 맞춤형 추천 서비스")
    
    ads_data = [{'id': 'inv_001', 'title': '스마트 투자 플랫폼', 'description': 'AI 기반 포트폴리오 관리로 안전하고 수익성 높은 투자를 시작하세요. GOOGL과 같은 활발한 거래 상황에서 더욱 유용합니다.', 'cta': '무료 투자 상담 받기', 'category': 'investment_platforms', 'match_score': 9, 'match_reasons': ['volume_spike 이벤트에 적합', '관련 키워드: 수익, 투자', '리스크 수준 적합'], 'personalization': {'symbol_context': 'GOOGL', 'event_context': 'volume_spike', 'relevance_score': 0.9}}, {'id': 'tool_001', 'title': '실시간 트레이딩 도구', 'description': '전문 트레이더들이 사용하는 고급 차트와 분석 도구를 경험하세요. GOOGL과 같은 활발한 거래 상황에서 더욱 유용합니다.', 'cta': '프리미엄 도구 체험', 'category': 'trading_tools', 'match_score': 7, 'match_reasons': ['volume_spike 이벤트에 적합', '관련 키워드: 분석', '리스크 수준 적합'], 'personalization': {'symbol_context': 'GOOGL', 'event_context': 'volume_spike', 'relevance_score': 0.7}}, {'id': 'edu_002', 'title': '경제 뉴스 구독 서비스', 'description': '실시간 경제 분석과 전문가 의견으로 시장을 앞서가세요. GOOGL과 같은 활발한 거래 상황에서 더욱 유용합니다.', 'cta': '프리미엄 구독', 'category': 'education_services', 'match_score': 7, 'match_reasons': ['volume_spike 이벤트에 적합', '관련 키워드: 분석', '리스크 수준 적합'], 'personalization': {'symbol_context': 'GOOGL', 'event_context': 'volume_spike', 'relevance_score': 0.7}}]
    
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


if __name__ == "__main__":
    main()
