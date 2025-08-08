#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
GC=F - GC=F 거래량 급증
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
    page_title="GC=F 거래량 급증",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 GC=F 거래량 급증")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "GC=F")
    
    with col2:
        st.metric("변화율", "+257.34%")
    
    with col3:
        st.metric("심각도", "CRITICAL")
    
    with col4:
        st.metric("발생시간", "08:12")
    
    # 기사 이미지
    if os.path.exists("output/images/GC=F_volume_spike_20250806_081257.png"):
        st.image("output/images/GC=F_volume_spike_20250806_081257.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# GC=F 거래량 급증, 3.8배 증가

GC=F의 거래량이 평균 대비 3.8배 급증하며 이상 거래 패턴을 보이고 있습니다.

금년 상반기 귀금속 선물 시장에서는 금값 상승에 따른 변동성 확대로 인해 투자자들의 이목이 집중되고 있다. 최근 COMEX 금 선물(GC=F)의 거래량이 평균 대비 3.6배 증가하며 주목할 만한 변화를 보였다.  

현재 가격 데이터를 살펴보면, GC=F는 3,428.80달러에 거래되고 있으며 20일 단순이동평균선인 3,354.74달러를 상회하고 있다. 이는 단기적으로 상승세가 지속되고 있음을 시사한다. MACD 지표 또한 6.12의 양수값을 기록하며 매수신호를 나타내고 있다. 하지만 RSI 지표가 60.84로 과열 구간에 진입했다는 점에서 단기 조정이 예상된다.

변동성 측면에서 GC=F의 연율화 변동성은 13.98%로 비교적 높은 수준이다. 이는 최근 1개월간 가격 등락폭이 크다는 것을 의미하며, 변동성 확대에 따른 리스크 관리가 필요해 보인다. 한편 거래량 비중은 3.84배로 매우 높아 시장 참여자들의 관심이 집중되고 있음을 알 수 있다.

시장 비교 분석 결과, GC=F는 S&P 500 지수(SPY)와 음(-)의 상관관계를 보이고 있으며, 베타 값 또한 -0.39로 나타났다. 이는 주식 시장 하락 시 금 선물의 가치가 상대적으로 상승할 수 있음을 시사한다. 최근 1개월간 시장 수익률 대비 초과수익률도 34.79%로 우수한 성과를 거두었다.

향후 전망으로는 전문가 예측 결과 금 선물 가격이 단기적으로 약간 강세를 보일 것으로 내다봤다. 지지선은 3,274.17달러, 저항선은 3,435.31달러로 예상되며, 신뢰도는 60%에 달한다. 다만 최근 가격 상승에 따른 과열 조짐과 변동성 확대 가능성을 고려할 때 단기 조정 리스크에 유의해야 할 것으로 보인다.

종합적으로 금 선물 시장에 대한 투자심리가 강세를 보이고 있으나, 과열된 변동성과 주식 시장 동향에 따른 리스크 요인이 상존하고 있어 적절한 리스크 관리가 필요할 것으로 판단된다.

## 결론

GC=F의 급등은 투자자들의 관심을 끌고 있으며, 기술적 분석 결과 '약간 강세' 전망을 보이고 있습니다. 투자자들은 충분한 분석과 리스크 관리를 통해 신중한 투자 결정을 내리시기 바랍니다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시 (HTML 파일 올바른 처리)
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
    review = {'review_timestamp': '2025-08-06T08:12:57.905161', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 247, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.0073588916666666665, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.014652014652014652, 'technical_depth': 6}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 6, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("품질 점수", f"{review.get('quality_score', 0):.1f}/10")
    
    with col2:
        st.metric("신뢰도", f"{review.get('credibility_score', 0):.1f}/10")
    
    if review.get('suggestions'):
        st.markdown("**개선 제안:**")
        for suggestion in review['suggestions']:
            st.markdown(f"• {suggestion}")
    
    # 광고 추천
    st.markdown("## 📢 관련 광고")
    
    ads = [{'title': '프로 트레이딩 플랫폼 - TradeMax', 'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.', 'target_audience': '전문 트레이더', 'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'], 'cta': '30일 무료 체험', 'advertiser': 'TradeMax Ltd.', 'category': 'trading_platform', 'relevance_score': 6.5, 'rank': 1, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=프로_트레이딩_플랫폼_-_TradeMax&article_symbol=GC=F', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 10.0, 'interest_alignment': 7.5}}, {'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 5.5, 'rank': 2, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=GC=F', 'metrics': {'keyword_relevance': 7.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '부동산 투자 플랫폼 - RealtyInvest', 'description': '소액으로 시작하는 부동산 투자. 전문가가 선별한 수익형 부동산에 투자하세요.', 'target_audience': '부동산 투자자', 'relevance_keywords': ['부동산', '투자', '수익형', '소액투자'], 'cta': '투자 상품 보기', 'advertiser': 'RealtyInvest Co.', 'category': 'real_estate', 'relevance_score': 3.0, 'rank': 3, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=부동산_투자_플랫폼_-_RealtyInvest&article_symbol=GC=F', 'metrics': {'keyword_relevance': 7.5, 'audience_match': 0.0, 'interest_alignment': 0.0}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 3428.800048828125, 'previous_close': 3381.89990234375, 'volume': 34526, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
