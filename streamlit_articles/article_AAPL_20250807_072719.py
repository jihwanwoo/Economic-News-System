#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
AAPL - 애플 주가 3% 이상 상승, 신제품 기대감에 투자자 관심 집중
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
    page_title="애플 주가 3% 이상 상승, 신제품 기대감에 투자자 관심 집중",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 애플 주가 3% 이상 상승, 신제품 기대감에 투자자 관심 집중")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "AAPL")
    
    with col2:
        st.metric("이벤트", "PRICE_CHANGE")
    
    with col3:
        st.metric("품질점수", "7.9/10")
    
    with col4:
        st.metric("생성시간", "07:27")
    
    # 기사 이미지
    
    # 기사 관련 이미지
    if os.path.exists("output/images/AAPL_article_illustration_20250807_072718.png"):
        st.image("output/images/AAPL_article_illustration_20250807_072718.png", caption="기사 관련 일러스트레이션", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_price_change_20250807_072718.png"):
        st.image("output/images/AAPL_price_change_20250807_072718.png", caption="이벤트 분석 차트", use_column_width=True)
    
    if os.path.exists("output/images/AAPL_wordcloud_20250807_072718.png"):
        st.image("output/images/AAPL_wordcloud_20250807_072718.png", caption="기사 키워드 워드클라우드", use_column_width=True)
    
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""애플(AAPL) 주가가 7일 장중 3.2% 이상 급등하며 213달러를 상회했다. 이번 주가 상승은 향후 신제품 출시에 대한 기대감과 긍정적인 실적 전망이 반영된 것으로 보인다. 애플의 주가 움직임은 기술주 전반에 영향을 미치고 있다.

애플 주가가 7일 213.25달러로 장을 마감하며 전일 대비 3.26% 상승했다. 이날 애플 주식 거래량은 1억600만주를 기록해 평소보다 2배 이상 많은 거래가 이뤄진 것으로 나타났다. 이번 애플 주가 상승은 업계에서 기대하는 신제품 출시 기대감이 주요 원인으로 꼽힌다. 애플은 오는 9월 연례 신제품 발표회를 개최할 예정이며, 새로운 아이폰과 애플워치 등 플래그십 제품군을 공개할 것으로 예상된다. 시장 전문가들은 애플의 신제품이 혁신적인 기능을 탑재하고 있을 것으로 내다보고 있다. 기술적 분석 결과도 애플 주가 상승을 뒷받침한다. RSI(상대강도지수)가 55.6을 기록해 과매수 국면은 아니며, 20일 이동평균선 상향 돌파로 상승세가 지속될 가능성이 높다. MACD 지표 역시 0.07을 기록하며 긍정적인 모습을 보였다. 실적 전망도 긍정적이다. 시장 전문가들은 애플이 서비스 부문 성장과 더불어 신제품 판매 호조로 내년 실적이 크게 개선될 것으로 내다보고 있다. 또한 차량 사업 진출 등 새로운 성장동력 확보에 대한 기대감도 주가에 영향을 미친 것으로 분석된다. 다만 일부 전문가들은 주가 상승 폭이 다소 과했다는 지적도 나오고 있다. 기술주 전반에 걸친 밸류에이션 부담과 경기 둔화 우려 등을 감안하면 과도한 기대는 경계할 필요가 있다는 의견이다.

## 결론

애플 주가는 신제품 출시 기대감과 실적 개선 전망 등에 힘입어 강세를 보였다. 기술적 지표 역시 상승세를 뒷받침하고 있으나, 밸류에이션 부담과 경기 둔화 우려 등 변수도 상존해 추가 상승에는 다소 제동이 걸릴 수 있다는 지적이다. 투자자들은 향후 실적과 신제품 성과를 주시하며 리스크 관리에 주력할 필요가 있을 것으로 보인다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = ['output/charts/AAPL_price_volume_20250807_072650.html', 'output/charts/AAPL_technical_20250807_072650.html', 'output/charts/AAPL_recent_20250807_072650.html', 'output/charts/AAPL_comparison_20250807_072650.html']
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
    st.json({'overall_score': 7.9, 'detailed_scores': {'content_accuracy': 8.0, 'readability': 7.0, 'completeness': 7.6, 'compliance': 9.0, 'engagement': 9.3}, 'improvements': [], 'review_timestamp': '2025-08-07T07:27:18.153321', 'reviewer': '기사 검수 에이전트', 'status': 'approved'})
    

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
