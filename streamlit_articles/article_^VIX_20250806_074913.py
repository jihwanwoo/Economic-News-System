#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
^VIX - ^VIX 급락 감지
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
    page_title="^VIX 급락 감지",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 ^VIX 급락 감지")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "^VIX")
    
    with col2:
        st.metric("변화율", "-3.31%")
    
    with col3:
        st.metric("심각도", "MEDIUM")
    
    with col4:
        st.metric("발생시간", "07:48")
    
    # 기사 이미지
    if os.path.exists("output/images/^VIX_price_change_20250806_074913.png"):
        st.image("output/images/^VIX_price_change_20250806_074913.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# ^VIX 급락 3.3%, 주목받는 움직임

^VIX이(가) 2025년 08월 06일에 -3.31% 하락하며 시장의 주목을 받고 있습니다. 현재 주가는 17.27달러를 기록하고 있습니다.

변동성 지수(VIX)가 3.31% 하락하며 17.27 수준을 기록했다. 이는 지난 한 달 동안 VIX의 평균 수준인 16.63보다 높은 수치이며, 전통적인 20일 단순이동평균선(SMA) 16.60을 상회한다. 단기 변동성이 여전히 높은 가운데, 이번 하락은 투자자들의 위험 회피 심리가 다소 완화되고 있음을 시사한다.

기술적 분석 지표를 살펴보면, MACD 지표가 0.25로 양수 값을 유지하고 있어 상승 모멘텀이 이어지고 있음을 알 수 있다. 그러나 신호선과의 격차가 점차 좁혀지고 있어 상승세가 곧 꺾일 수 있음을 시사한다. RSI 지표 역시 53.04로 중립 수준을 보이고 있어 단기적으로 변동성이 지속될 것으로 예상된다. 볼린저 밴드의 상단(19.07)과 하단(14.12)을 감안할 때, 현재 가격은 중간 수준에 위치해 있다.

통계 분석 결과를 살펴보면, VIX의 연간 변동성은 108.31%로 매우 높은 수준이다. 그러나 최근 1개월 동안의 가격 변동폭이 평균 수준에 비해 3.86배 높은 것으로 나타나 단기 변동성이 점차 줄어들고 있음을 시사한다. 또한 추세 강도가 1.43으로 비교적 강한 상승세를 보이고 있다.

시장 전문가들은 VIX의 전망에 대해 30점의 낮은 점수를 매겼으며, 향후 약간 강세를 보일 것으로 예상하고 있다. 그러나 60%의 낮은 신뢰도를 감안할 때 불확실성이 여전히 높은 상황이다. 지원선 14.12와 저항선 19.07 사이에서 가격이 등락할 것으로 예상된다.

종합적으로 볼 때, VIX의 단기 변동성은 다소 완화되고 있으나 여전히 높은 수준을 유지하고 있다. 투자자들의 위험 회피 심리가 약화되면서 주식시장의 변동성도 점차 안정을 찾아가고 있지만, 향후 경기 둔화 및 지정학적 리스크 등 불확실성이 상존하고 있어 주의가 필요하다.

## 결론

^VIX의 현재 움직임은 기술적 분석 결과 '약간 강세' 전망을 보이고 있습니다. 투자자들은 충분한 분석과 리스크 관리를 통해 신중한 투자 결정을 내리시기 바랍니다.

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
    review = {'review_timestamp': '2025-08-06T07:49:13.110330', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 241, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.006053036944444444, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.011235955056179775, 'technical_depth': 7}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 6, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 4.5, 'rank': 1, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=^VIX', 'metrics': {'keyword_relevance': 7.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '경제 뉴스 프리미엄 - EcoNews+', 'description': '전문가 분석과 독점 리포트로 시장을 앞서가세요. 실시간 알림 서비스 포함.', 'target_audience': '정보 추구자', 'relevance_keywords': ['뉴스', '분석', '리포트', '정보'], 'cta': '프리미엄 구독', 'advertiser': 'EcoNews Media', 'category': 'news_service', 'relevance_score': 2.5, 'rank': 2, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=경제_뉴스_프리미엄_-_EcoNews+&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '부동산 투자 플랫폼 - RealtyInvest', 'description': '소액으로 시작하는 부동산 투자. 전문가가 선별한 수익형 부동산에 투자하세요.', 'target_audience': '부동산 투자자', 'relevance_keywords': ['부동산', '투자', '수익형', '소액투자'], 'cta': '투자 상품 보기', 'advertiser': 'RealtyInvest Co.', 'category': 'real_estate', 'relevance_score': 2.0, 'rank': 3, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=부동산_투자_플랫폼_-_RealtyInvest&article_symbol=^VIX', 'metrics': {'keyword_relevance': 5.0, 'audience_match': 0.0, 'interest_alignment': 0.0}}]
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
