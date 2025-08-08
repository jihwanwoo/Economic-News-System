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
        st.metric("변화율", "+15.06%")
    
    with col3:
        st.metric("심각도", "MEDIUM")
    
    with col4:
        st.metric("발생시간", "07:48")
    
    # 기사 이미지
    if os.path.exists("output/images/^VIX_volatility_20250806_074926.png"):
        st.image("output/images/^VIX_volatility_20250806_074926.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# ^VIX 높은 변동성, 108.3% 기록

^VIX이(가) 108.3%의 높은 변동성을 기록하며 불안정한 모습을 보이고 있습니다.

금융시장의 변동성을 나타내는 지표인 VIX 지수가 최근 15.06% 급등하며 중간 수준의 변화를 보였다. 이는 투자자들의 불안감이 높아지고 있음을 시사한다. 현재 VIX 지수는 17.27로 20일 단순이동평균선인 16.60을 상회하고 있다. 

기술적 분석 결과, MACD 지표의 신호선을 상향 가파르게 넘어서며 상승 모멘텀이 강화되고 있음을 알 수 있다. RSI 지표 역시 53.04로 중립 수준을 소폭 상회하고 있어 단기적으로 상승세가 이어질 가능성이 높다. 볼린저 밴드로 보면 현재가는 상단 밴드에 근접해 있어 단기 과열 양상을 보이고 있다.

통계 지표를 살펴보면 연율화 변동성이 108%를 넘어서며 높은 수준을 기록 중이다. 1개월 평균가격 대비 현재가는 3.86% 높은 수준으로 단기 상승세가 유지되고 있음을 확인할 수 있다. 

향후 VIX 지수는 일부 투자자들의 과도한 낙관론에 제동이 걸리며 약간 강세로 전망된다. 전문가 전망에 따르면 향후 1개월 간 지지선은 14.12, 저항선은 19.07으로 예상된다. 다만 변동성 확대로 인한 투자 위험이 높아질 것으로 보여 무리한 투자는 자제할 필요가 있겠다.

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
    review = {'review_timestamp': '2025-08-06T07:49:27.005128', 'overall_score': 9.4, 'quality_score': 8.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 8.0, 'issues': ['내용이 너무 짧습니다 (167단어 < 200단어)'], 'word_count': 167, 'structure_complete': False}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.00377792, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.010362694300518135, 'technical_depth': 8}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 3, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 3.5, 'rank': 1, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=^VIX', 'metrics': {'keyword_relevance': 5.0, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '프로 트레이딩 플랫폼 - TradeMax', 'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.', 'target_audience': '전문 트레이더', 'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'], 'cta': '30일 무료 체험', 'advertiser': 'TradeMax Ltd.', 'category': 'trading_platform', 'relevance_score': 2.5, 'rank': 2, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=프로_트레이딩_플랫폼_-_TradeMax&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '경제 뉴스 프리미엄 - EcoNews+', 'description': '전문가 분석과 독점 리포트로 시장을 앞서가세요. 실시간 알림 서비스 포함.', 'target_audience': '정보 추구자', 'relevance_keywords': ['뉴스', '분석', '리포트', '정보'], 'cta': '프리미엄 구독', 'advertiser': 'EcoNews Media', 'category': 'news_service', 'relevance_score': 2.5, 'rank': 3, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=경제_뉴스_프리미엄_-_EcoNews+&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 17.270000457763672, 'previous_close': 17.850000381469727, 'volume': 0, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
