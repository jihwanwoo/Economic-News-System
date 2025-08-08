#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
AAPL - 애플 주가 3.5% 상승, 테크 시장 선전
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
    page_title="애플 주가 3.5% 상승, 테크 시장 선전",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 애플 주가 3.5% 상승, 테크 시장 선전")
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
        st.metric("생성시간", "02:32")
    
    # 기사 이미지
    
    # 기사 관련 이미지
    if os.path.exists("output/images/AAPL_article_illustration_20250807_023218.png"):
        st.image("output/images/AAPL_article_illustration_20250807_023218.png", caption="기사 관련 일러스트레이션", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_price_change_20250807_023219.png"):
        st.image("output/images/AAPL_price_change_20250807_023219.png", caption="이벤트 분석 차트", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_wordcloud_20250807_023219.png"):
        st.image("output/images/AAPL_wordcloud_20250807_023219.png", caption="기사 키워드 워드클라우드", use_column_width=True)
    
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""애플(AAPL) 주가가 3.5% 급등하며 시가총액 2조 달러 기업들 중 가장 높은 상승세를 보였다. 긍정적 실적 전망과 신제품 출시 기대감이 주가 상승을 견인했다.

지난 8월 7일 애플 주가는 3.5% 상승한 213.25달러로 마감했다. 거래량도 일평균의 2배 수준인 1억 600만주를 기록하며 투자자들의 큰 관심을 받았다. 이번 애플 주가 상승은 시장 예상치를 웃도는 기업 실적과 신제품 출시 기대감이 작용한 것으로 분석된다. 최근 분기 실적 발표에서 애플은 전년 대비 5.6% 증가한 830억 달러의 매출을 기록하며 분석가 컨센서스를 상회했다. 특히 아이폰과 서비스 부문 매출이 견조한 성장세를 보였다. CEO 팀 쿡은 "고객 만족도와 제품 라인업이 강화되면서 하반기 실적도 긍정적일 것"이라고 강조했다. 이에 따라 투자자들은 신제품 출시 기대감도 높아졌다. 한편 기술적 분석에서도 애플 주가 상승 신호가 포착됐다. RSI(상대강도지수)가 55.6으로 중립 수준을 상회했고, 단기 이동평균선을 상향 돌파하며 상승 모멘텀을 확인했다. MACD 지표도 0.07로 플러스 전환되는 등 매수 시그널이 발생했다. 다만 연율 변동성이 0.2%로 낮아 단기 급등 가능성은 제한적이라는 지적이다. 업계 전문가들은 "애플의 실적이 견조하지만 밸류에이션 부담으로 주가 상승 폭은 제한될 수 있다"고 평가했다. 결과적으로 이번 애플 주가 상승은 실적 호조와 신제품 기대감이 주요 원인으로 꼽힌다. 투자자들의 관심이 지속되면서 단기적인 상승세가 이어질 것으로 예상된다.

## 결론

애플의 3.5% 주가 상승은 양호한 실적과 향후 신제품 출시에 대한 기대감이 반영된 결과다. 기술적 지표에서도 상승 신호가 감지됐지만, 밸류에이션 부담으로 상승 폭은 제한적일 수 있다는 전망이다. 애플 주가는 당분간 강세를 보일 것으로 예상되나, 추가 상승을 위해선 실적과 혁신 제품이 관건이 될 전망이다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = ['output/charts/AAPL_price_volume_20250807_023148.html', 'output/charts/AAPL_technical_20250807_023148.html', 'output/charts/AAPL_recent_20250807_023148.html', 'output/charts/AAPL_comparison_20250807_023148.html']
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
    st.json({'overall_score': 7.8, 'detailed_scores': {'content_accuracy': 8.0, 'readability': 7.0, 'completeness': 7.8, 'compliance': 8.0, 'engagement': 9.200000000000001}, 'improvements': [], 'review_timestamp': '2025-08-07T02:32:18.862283', 'reviewer': '기사 검수 에이전트', 'status': 'approved'})
    

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
