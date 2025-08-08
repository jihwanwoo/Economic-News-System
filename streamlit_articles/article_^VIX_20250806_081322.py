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
        st.metric("변화율", "-3.36%")
    
    with col3:
        st.metric("심각도", "MEDIUM")
    
    with col4:
        st.metric("발생시간", "08:12")
    
    # 기사 이미지
    if os.path.exists("output/images/^VIX_price_change_20250806_081322.png"):
        st.image("output/images/^VIX_price_change_20250806_081322.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# ^VIX 급락 3.4%, 주목받는 움직임

^VIX이(가) 2025년 08월 06일에 -3.36% 하락하며 시장의 주목을 받고 있습니다. 현재 주가는 17.25달러를 기록하고 있습니다.

변동성 지수인 VIX가 3.36% 하락하며 17.25 포인트를 기록했습니다. 이는 지난 한 달 동안 VIX 평균치인 16.63보다 높은 수준입니다. 그러나 이번 하락세는 투자자들의 위험 회피 심리가 다소 완화되고 있음을 시사합니다. 

기술적 분석 결과, VIX의 20일 단순이동평균선은 16.59로 현재 가격을 하회하고 있습니다. MACD 지표 역시 0.25의 양의 값을 보이며 상승 추세를 나타내고 있습니다. 그러나 RSI 지수가 52.96으로 중립 수준을 약간 상회하는 데 그치고 있어 단기적 상승 모멘텀은 강하지 않은 상황입니다. 볼린저 밴드로 보면 현재 VIX 가격은 상단 밴드(19.07)와 하단 밴드(14.12) 사이에 위치해 있습니다.

변동성이 연율 108.36%에 달하는 등 VIX는 여전히 높은 변동성을 보이고 있습니다. 하지만 지난 한 달간 VIX의 상대 강도 지수가 1.41로 나타나 상승 추세력이 있음을 알 수 있습니다.

시장 벤치마크 대비 VIX의 움직임을 살펴보면, 베타 계수가 2.19로 매우 높아 S&P 500 지수에 비해 훨씬 큰 변동성을 보이고 있습니다. 그러나 상관계수는 0.20에 불과해 S&P 500과의 동조화 정도는 높지 않습니다. 지난 한 달간 VIX의 상대 성과는 5.91%로 S&P 500을 상회했습니다.

전반적으로 VIX의 단기 전망은 약간 강세를 보일 것으로 예상됩니다. 전문가 평가 결과 향후 전망 점수가 30점(100점 만점)으로 나왔으며, 신뢰도 60%로 약간 강세를 예상하고 있습니다. 핵심 레벨로는 지지선 14.12, 저항선 19.07이 제시되었습니다.

종합적으로 볼 때, 투자자들의 위험 회피 심리가 다소 완화되는 모습이지만 여전히 높은 변동성이 예상되는 상황입니다. 단기적으로는 약간의 상승세가 이어질 것으로 보이나, 중장기적으로는 경기 불확실성에 따른 변동성 확대 가능성에 유의해야 할 것입니다.

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
    review = {'review_timestamp': '2025-08-06T08:13:22.483452', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 247, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.0066526127777777775, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.014652014652014652, 'technical_depth': 8}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 4, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 3.5, 'rank': 1, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=^VIX', 'metrics': {'keyword_relevance': 5.0, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '경제 뉴스 프리미엄 - EcoNews+', 'description': '전문가 분석과 독점 리포트로 시장을 앞서가세요. 실시간 알림 서비스 포함.', 'target_audience': '정보 추구자', 'relevance_keywords': ['뉴스', '분석', '리포트', '정보'], 'cta': '프리미엄 구독', 'advertiser': 'EcoNews Media', 'category': 'news_service', 'relevance_score': 2.5, 'rank': 2, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=경제_뉴스_프리미엄_-_EcoNews+&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '부동산 투자 플랫폼 - RealtyInvest', 'description': '소액으로 시작하는 부동산 투자. 전문가가 선별한 수익형 부동산에 투자하세요.', 'target_audience': '부동산 투자자', 'relevance_keywords': ['부동산', '투자', '수익형', '소액투자'], 'cta': '투자 상품 보기', 'advertiser': 'RealtyInvest Co.', 'category': 'real_estate', 'relevance_score': 2.0, 'rank': 3, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=부동산_투자_플랫폼_-_RealtyInvest&article_symbol=^VIX', 'metrics': {'keyword_relevance': 5.0, 'audience_match': 0.0, 'interest_alignment': 0.0}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 17.25, 'previous_close': 17.850000381469727, 'volume': 0, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
