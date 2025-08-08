#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
^VIX - ^VIX 높은 변동성
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
    page_title="^VIX 높은 변동성",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 ^VIX 높은 변동성")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "^VIX")
    
    with col2:
        st.metric("변화율", "+15.08%")
    
    with col3:
        st.metric("심각도", "MEDIUM")
    
    with col4:
        st.metric("발생시간", "07:55")
    
    # 기사 이미지
    if os.path.exists("output/images/^VIX_volatility_20250806_075636.png"):
        st.image("output/images/^VIX_volatility_20250806_075636.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# ^VIX 높은 변동성, 108.4% 기록

^VIX이(가) 108.4%의 높은 변동성을 기록하며 불안정한 모습을 보이고 있습니다.

변동성 지수인 VIX(CBOE Volatility Index)가 최근 15.08% 급등하면서 투자자들의 우려가 높아지고 있습니다. 이는 중간 수준의 변화율로, 시장 참여자들의 관심이 요구됩니다.

현재 VIX 지수는 17.22 수준으로, 지난 한 달 평균인 16.63보다 높은 수준입니다. 표준편차 1.19를 고려하면 현재 가격은 평균을 상회하는 것으로 판단됩니다. 이는 변동성 확대에 대한 우려가 반영된 것으로 보입니다.

기술적 지표를 살펴보면, MACD(0.247)가 신호선(0.071)을 상회하고 있어 상승 모멘텀이 있는 것으로 분석됩니다. 그러나 RSI(52.8)는 중립적인 수준을 보이고 있습니다. 볼린저 밴드도 현재 가격이 중간 수준에 위치하고 있음을 시사합니다.

시장 비교 측면에서, VIX는 베타 계수 2.2로 시장 대비 높은 변동성을 보이고 있습니다. 그러나 S&P 500 지수(SPY)와의 상관관계는 0.197로 낮은 편입니다. 지난 한 달간 VIX의 상대 성과는 5.74%로 양호한 수준입니다.

통계 정보를 살펴보면, VIX의 연율화 변동성은 108.42%로 매우 높은 수준입니다. 그러나 거래량 비율은 1.0으로 평균적인 수준을 유지하고 있습니다. 추세 강도는 1.39로 강한 상승 추세를 보이고 있습니다.

전망 측면에서, 전문가들은 VIX가 단기적으로 약간 강세를 보일 것으로 예상하고 있습니다. 지원선은 14.12, 저항선은 19.06으로 예측되고 있습니다. 신뢰도는 60%로 중간 수준입니다.

종합적으로 볼 때, VIX의 급등세는 시장 변동성 확대를 반영하고 있습니다. 기술적 지표와 통계 정보는 상승 모멘텀을 시사하고 있으나, 과도한 변동성은 주의가 필요합니다. 투자자들은 포트폴리오 리스크 관리에 유의해야 할 것으로 보입니다.

## 결론

^VIX의 급등은 투자자들의 관심을 끌고 있으며, 기술적 분석 결과 '약간 강세' 전망을 보이고 있습니다. 투자자들은 충분한 분석과 리스크 관리를 통해 신중한 투자 결정을 내리시기 바랍니다.

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
    review = {'review_timestamp': '2025-08-06T07:56:36.470505', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 217, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.006860171111111111, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.00411522633744856, 'technical_depth': 5}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 4, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 4.5, 'rank': 1, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=^VIX', 'metrics': {'keyword_relevance': 7.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '프로 트레이딩 플랫폼 - TradeMax', 'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.', 'target_audience': '전문 트레이더', 'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'], 'cta': '30일 무료 체험', 'advertiser': 'TradeMax Ltd.', 'category': 'trading_platform', 'relevance_score': 2.5, 'rank': 2, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=프로_트레이딩_플랫폼_-_TradeMax&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '경제 뉴스 프리미엄 - EcoNews+', 'description': '전문가 분석과 독점 리포트로 시장을 앞서가세요. 실시간 알림 서비스 포함.', 'target_audience': '정보 추구자', 'relevance_keywords': ['뉴스', '분석', '리포트', '정보'], 'cta': '프리미엄 구독', 'advertiser': 'EcoNews Media', 'category': 'news_service', 'relevance_score': 2.5, 'rank': 3, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=경제_뉴스_프리미엄_-_EcoNews+&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 17.219999313354492, 'previous_close': 17.850000381469727, 'volume': 0, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
