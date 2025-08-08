#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
AAPL - 애플 주가 3.2% 상승, 아이폰 14 판매 호조로 기술주 랠리 이어가
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
    page_title="애플 주가 3.2% 상승, 아이폰 14 판매 호조로 기술주 랠리 이어가",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 애플 주가 3.2% 상승, 아이폰 14 판매 호조로 기술주 랠리 이어가")
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
        st.metric("생성시간", "07:17")
    
    # 기사 이미지
    
    # 기사 관련 이미지
    if os.path.exists("output/images/AAPL_article_illustration_20250807_071752.png"):
        st.image("output/images/AAPL_article_illustration_20250807_071752.png", caption="기사 관련 일러스트레이션", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_price_change_20250807_071753.png"):
        st.image("output/images/AAPL_price_change_20250807_071753.png", caption="이벤트 분석 차트", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_wordcloud_20250807_071753.png"):
        st.image("output/images/AAPL_wordcloud_20250807_071753.png", caption="기사 키워드 워드클라우드", use_column_width=True)
    
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""애플(AAPL) 주가가 3.2% 상승하며 기술주 랠리를 이끌었다. 이는 아이폰 14 시리즈 판매 호조와 기대 이상의 실적 전망에 힘입은 것으로 분석된다. 투자자들은 애플의 견조한 성장세에 높은 관심을 보이고 있다.

애플 주가가 전일 대비 3.2% 상승한 213.25달러로 마감했다. 이날 거래량은 1억 600만주를 기록해 평균 거래량 대비 2배 이상 증가했다. 이로써 애플 주가는 최근 20거래일 이동평균선인 210.26달러를 상회했다. 이번 애플 주가 상승은 아이폰 14 시리즈 판매 호조에 따른 것으로 보인다. 시장조사기관들은 아이폰 14 프로 모델의 공급 부족 현상이 지속되고 있다고 전했다. 이는 신제품에 대한 수요가 예상을 뛰어넘고 있음을 시사한다. 업계 전문가들은 애플이 4분기 실적 가이던스를 상향 조정할 가능성이 높다고 내다봤다. 골드만삭스는 "애플의 4분기 매출과 순이익이 컨센서스를 상회할 것"이라며 목표주가를 182달러에서 199달러로 상향 조정했다. 기술적 분석 지표도 애플 주가 상승을 뒷받침한다. 상대강도지수(RSI)가 55.6을 기록해 과매수 구간을 벗어났으며, MACD 지표도 0.07로 플러스 영역에 위치했다. 다만 애플 주가의 베타계수가 1.28로 높아 시장 변동성에 민감한 모습이다. 일각에서는 애플 주가가 지나치게 높게 평가되고 있다는 지적도 있다. 하지만 대다수 전문가들은 애플의 성장 잠재력을 긍정적으로 평가하고 있다. JP모건은 "애플은 아이폰뿐 아니라 서비스, 웨어러블 등 다양한 부문에서 성장하고 있다"며 목표주가를 200달러로 유지했다. 투자자들도 애플의 지속 성장에 베팅하고 있다. 연율 변동성이 0.2%에 불과해 투자 심리가 안정적인 모습이다. 애플 주가는 S&P500 지수와 0.55의 상관관계를 보이며 기술주 랠리를 견인하고 있다.

## 결론

애플 주가는 아이폰 14 시리즈 판매 호조와 기대 이상의 실적 전망에 힘입어 3.2% 상승했다. 투자자들은 애플의 견조한 성장 기조에 주목하고 있으며, 기술주 랠리가 이어질지 관심이 쏠리고 있다. 다만 일부에서는 주가가 고평가 되어 있다는 우려도 제기되고 있어 향후 실적 발표를 지켜봐야 할 것으로 보인다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = ['output/charts/AAPL_price_volume_20250807_071709.html', 'output/charts/AAPL_technical_20250807_071709.html', 'output/charts/AAPL_recent_20250807_071709.html', 'output/charts/AAPL_comparison_20250807_071709.html']
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
    st.json({'overall_score': 7.8, 'detailed_scores': {'content_accuracy': 8.0, 'readability': 7.0, 'completeness': 7.8, 'compliance': 8.0, 'engagement': 8.8}, 'improvements': [], 'review_timestamp': '2025-08-07T07:17:52.452952', 'reviewer': '기사 검수 에이전트', 'status': 'approved'})
    

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
