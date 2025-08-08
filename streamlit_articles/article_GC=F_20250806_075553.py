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
        st.metric("변화율", "+254.60%")
    
    with col3:
        st.metric("심각도", "CRITICAL")
    
    with col4:
        st.metric("발생시간", "07:55")
    
    # 기사 이미지
    if os.path.exists("output/images/GC=F_volume_spike_20250806_075552.png"):
        st.image("output/images/GC=F_volume_spike_20250806_075552.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# GC=F 거래량 급증, 3.6배 증가

GC=F의 거래량이 평균 대비 3.6배 급증하며 이상 거래 패턴을 보이고 있습니다.

금 선물 시장에서 주목할 만한 움직임이 포착되었습니다. 금 선물(GC=F)의 거래량이 평균 대비 3.5배 증가하며 크리티컬 수준의 변동성을 보였습니다. 이는 시장 참여자들의 관심이 급격히 높아졌음을 시사합니다.

현재 금 선물 가격은 3,429.90달러로, 지난 한 달 평균가 3,349.86달러를 상회하고 있습니다. 가격 변동성은 연율 14.01%로 비교적 높은 수준입니다. 이는 최근 한 달 간 최고가와 최저가의 격차가 146달러에 달했기 때문입니다. 

기술적 지표를 살펴보면, 20일 단순이동평균선(3,354.79달러)을 상회하고 있으며, MACD 지표 역시 양수 값을 보이고 있습니다. 이는 단기적으로 상승 모멘텀이 유지되고 있음을 시사합니다. 그러나 RSI 지표는 60.94로 과매수 영역에 근접해 있어 주의가 필요합니다. 

시장 비교 분석 결과, 금 선물은 S&P 500 지수와 음의 상관관계(-0.28)를 보이고 있습니다. 이는 안전자산 선호 현상이 작용한 결과로 풀이됩니다. 지난 한 달간 S&P 500 지수 대비 상대수익률은 34.79%로 우위를 보였습니다.

향후 전망으로는 약간 강세가 예상되지만, 신뢰도는 60% 수준에 그칩니다. 기술적 지표상 단기 상승 모멘텀이 유지되고 있으나, 고점 부근에서 차익실현 매물이 출회할 가능성도 배제할 수 없습니다. 지지선은 3,274달러, 저항선은 3,435달러로 예상됩니다.

종합적으로 금 선물은 최근 변동성 확대와 거래량 급증세를 보이며 시장의 관심이 집중되고 있습니다. 안전자산 선호 현상과 더불어 기술적 모멘텀이 단기적 상승세를 이끌고 있으나, 과매수 영역 진입에 따른 부작용도 경계해야 할 것으로 보입니다. 투자자들은 지지/저항 레벨을 주시하며 리스크 관리에 만전을 기할 필요가 있겠습니다.

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
    review = {'review_timestamp': '2025-08-06T07:55:53.111397', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 225, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.006203647777777778, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.01195219123505976, 'technical_depth': 6}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 4, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '프로 트레이딩 플랫폼 - TradeMax', 'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.', 'target_audience': '전문 트레이더', 'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'], 'cta': '30일 무료 체험', 'advertiser': 'TradeMax Ltd.', 'category': 'trading_platform', 'relevance_score': 6.5, 'rank': 1, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=프로_트레이딩_플랫폼_-_TradeMax&article_symbol=GC=F', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 10.0, 'interest_alignment': 7.5}}, {'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 4.5, 'rank': 2, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=GC=F', 'metrics': {'keyword_relevance': 5.0, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '부동산 투자 플랫폼 - RealtyInvest', 'description': '소액으로 시작하는 부동산 투자. 전문가가 선별한 수익형 부동산에 투자하세요.', 'target_audience': '부동산 투자자', 'relevance_keywords': ['부동산', '투자', '수익형', '소액투자'], 'cta': '투자 상품 보기', 'advertiser': 'RealtyInvest Co.', 'category': 'real_estate', 'relevance_score': 3.0, 'rank': 3, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=부동산_투자_플랫폼_-_RealtyInvest&article_symbol=GC=F', 'metrics': {'keyword_relevance': 7.5, 'audience_match': 0.0, 'interest_alignment': 0.0}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 3429.89990234375, 'previous_close': 3381.89990234375, 'volume': 32195, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
