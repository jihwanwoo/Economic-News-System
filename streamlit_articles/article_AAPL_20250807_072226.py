#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
AAPL - 애플 주가 3.2% 상승, 신제품 출시 기대감 반영
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
    page_title="애플 주가 3.2% 상승, 신제품 출시 기대감 반영",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 애플 주가 3.2% 상승, 신제품 출시 기대감 반영")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "AAPL")
    
    with col2:
        st.metric("이벤트", "PRICE_CHANGE")
    
    with col3:
        st.metric("품질점수", "7.8/10")
    
    with col4:
        st.metric("생성시간", "07:22")
    
    # 기사 이미지
    
    # 기사 관련 이미지
    if os.path.exists("output/images/AAPL_article_illustration_20250807_072225.png"):
        st.image("output/images/AAPL_article_illustration_20250807_072225.png", caption="기사 관련 일러스트레이션", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_price_change_20250807_072225.png"):
        st.image("output/images/AAPL_price_change_20250807_072225.png", caption="이벤트 분석 차트", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_wordcloud_20250807_072226.png"):
        st.image("output/images/AAPL_wordcloud_20250807_072226.png", caption="기사 키워드 워드클라우드", use_column_width=True)
    
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""애플(AAPL) 주가가 7일 3.2% 상승한 213.25달러를 기록했다. 이는 올해 9월 새로운 아이폰 모델 출시 기대감이 반영된 것으로 보인다. 거래량도 일평균의 2배 수준을 기록하며 투자자들의 관심이 집중되고 있다.

애플 주가는 연중 최고가 수준에 근접하며 강세를 보이고 있다. 이번 상승세는 새로운 아이폰 14 시리즈 출시를 앞두고 있는 가운데 나온 것으로 분석된다. 기술적 지표를 살펴보면 RSI 55.6, MACD 0.07 등 상승 모멘텀이 유지되고 있는 것으로 나타났다. 20일 이동평균선 210.26달러를 상회하며 단기 상승세를 이어가고 있다. 거래량 역시 일평균의 2배 수준을 기록하며 투자자들의 관심이 집중되고 있음을 시사했다. 연율 변동성 0.2%로 낮은 수준을 유지하며 안정적인 흐름을 보이고 있다. 업계 전문가들은 이번 아이폰 14의 출시가 기대 이상의 성과를 낼 것이라는 전망이 나오고 있다. 특히 프리미엄 모델인 아이폰 14 프로 라인업에 대한 기대감이 높은 상황이다. 골드만삭스 애널리스트 로드 홀은 "아이폰 14 프로 모델의 카메라 업그레이드와 신규 기능이 고객 수요를 이끌 것"이라며 "애플의 프리미엄 전략이 성과를 낼 것으로 예상된다"고 분석했다. 한편 애플 주가의 베타값 1.28, SPY 상관계수 0.55 등을 고려할 때 시장 동향을 상회하는 움직임을 보이고 있다. 이는 단순한 시장 반등세를 넘어 애플 고유의 펀더멘털 개선이 반영된 것으로 해석된다.

## 결론

애플 주가가 3.2% 상승하며 신제품 출시 기대감이 반영되고 있다. 기술적 지표와 거래량 증가 등 상승 모멘텀이 유지되는 가운데, 업계 전문가들 역시 프리미엄 전략의 성공 가능성을 높게 보고 있다. 다만 주가 고평가 우려 등 리스크 요인도 상존하고 있어 지속 관찰이 필요해 보인다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = ['output/charts/AAPL_price_volume_20250807_072207.html', 'output/charts/AAPL_technical_20250807_072207.html', 'output/charts/AAPL_recent_20250807_072207.html', 'output/charts/AAPL_comparison_20250807_072207.html']
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
    st.json({'overall_score': 7.8, 'detailed_scores': {'content_accuracy': 7.5, 'readability': 7.0, 'completeness': 7.8, 'compliance': 9.0, 'engagement': 9.0}, 'improvements': [], 'review_timestamp': '2025-08-07T07:22:25.285064', 'reviewer': '기사 검수 에이전트', 'status': 'approved'})
    

    # 📢 관련 서비스 및 상품 추천
    
    st.markdown("---")
    st.markdown("### 🎯 맞춤형 추천 서비스")
    
    ads_data = [{'id': 'inv_001', 'title': '스마트 투자 플랫폼', 'description': 'AI 기반 포트폴리오 관리로 안전하고 수익성 높은 투자를 시작하세요.', 'cta': '무료 투자 상담 받기', 'category': 'investment_platforms', 'match_score': 7, 'match_reasons': ['price_change 이벤트에 적합', '관련 키워드: 투자', '리스크 수준 적합'], 'personalization': {'symbol_context': 'AAPL', 'event_context': 'price_change', 'relevance_score': 0.7}}, {'id': 'tool_002', 'title': '모바일 트레이딩 앱', 'description': '언제 어디서나 빠르고 안전한 모바일 거래를 즐기세요.', 'cta': '앱 다운로드', 'category': 'trading_tools', 'match_score': 7, 'match_reasons': ['price_change 이벤트에 적합', '관련 키워드: 거래', '리스크 수준 적합'], 'personalization': {'symbol_context': 'AAPL', 'event_context': 'price_change', 'relevance_score': 0.7}}, {'id': 'edu_002', 'title': '경제 뉴스 구독 서비스', 'description': '실시간 경제 분석과 전문가 의견으로 시장을 앞서가세요.', 'cta': '프리미엄 구독', 'category': 'education_services', 'match_score': 7, 'match_reasons': ['price_change 이벤트에 적합', '관련 키워드: 분석', '리스크 수준 적합'], 'personalization': {'symbol_context': 'AAPL', 'event_context': 'price_change', 'relevance_score': 0.7}}]
    
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
