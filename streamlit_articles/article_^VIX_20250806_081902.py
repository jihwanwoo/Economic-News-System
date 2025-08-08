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
        st.metric("변화율", "+15.03%")
    
    with col3:
        st.metric("심각도", "MEDIUM")
    
    with col4:
        st.metric("발생시간", "08:17")
    
    # 기사 이미지
    if os.path.exists("output/images/^VIX_volatility_20250806_081902.png"):
        st.image("output/images/^VIX_volatility_20250806_081902.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# ^VIX 높은 변동성, 108.3% 기록

^VIX이(가) 108.3%의 높은 변동성을 기록하며 불안정한 모습을 보이고 있습니다.

금융시장에서 변동성은 투자자들의 주요 관심사이다. 최근 시카고옵션거래소(CBOE)의 변동성지수(VIX) 급등으로 변동성이 다시 한번 주목받고 있다. VIX는 15.03% 상승하며 17.30 수준을 기록했다. 이는 변동성이 중간 수준으로 높아졌음을 의미한다.

기술적 분석을 살펴보면, VIX의 20일 단순이동평균선은 16.60 부근에 위치해 있어 현재 가격이 이를 상회하고 있다. MACD 지표 역시 양전되어 상승 모멘텀을 시사한다. 그러나 RSI 지표는 53.17로 과열 구간에 진입하지 않은 것으로 보인다. 볼린저밴드를 참고하면 VIX 가격은 상단 밴드에 근접해 있어 단기 조정 가능성도 배제할 수 없다.

통계적으로도 VIX의 변동성은 두드러진다. 연율화 변동성이 108%에 달하며, 최근 1개월 평균 대비 현재 가격 프리미엄도 4% 이상이다. 그러나 변동성 지수의 본질상 추세 강도가 높고 단기 변동성이 큰 것이 일반적이므로 이는 예상 범주에 속한다.

VIX와 S&P500 지수(SPY) 간 상관관계는 0.19 수준으로 낮지만, 베타값이 2.17로 높아 주식시장 변동성을 상당 부분 반영한다. 최근 1개월간 VIX는 SPY 대비 6% 이상의 상대적 강세를 보였다.

향후 전망은 VIX가 약간 강세를 보일 것으로 예상된다. 전문가 예측 모델은 VIX에 30점을 부여했으며, 향후 60% 가능성으로 상승세가 이어질 것으로 내다봤다. 다만 지지/저항 수준을 참고하면 상단 저항선 19.07 부근에서 상승세가 제한될 수 있다.

투자자들은 VIX 상승과 더불어 주식시장 변동성 확대 가능성에 유의해야 한다. 변동성 헤지 전략을 점검하고 포트폴리오 리스크를 적절히 관리할 필요가 있다. 그러나 과도한 변동성 공포에 빠져서는 안 되며, 기술적/통계적 분석과 시장 동향을 종합적으로 고려해 투자 의사결정을 내려야 한다.

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
    review = {'review_timestamp': '2025-08-06T08:19:02.563427', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 235, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.006639435277777777, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.022988505747126436, 'technical_depth': 6}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 3, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 5.5, 'rank': 1, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=^VIX', 'metrics': {'keyword_relevance': 10.0, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '프로 트레이딩 플랫폼 - TradeMax', 'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.', 'target_audience': '전문 트레이더', 'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'], 'cta': '30일 무료 체험', 'advertiser': 'TradeMax Ltd.', 'category': 'trading_platform', 'relevance_score': 2.5, 'rank': 2, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=프로_트레이딩_플랫폼_-_TradeMax&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '투자 마스터 클래스 - InvestEdu', 'description': '기초부터 고급까지, 체계적인 투자 교육으로 성공적인 투자자가 되세요.', 'target_audience': '투자 학습자', 'relevance_keywords': ['교육', '학습', '투자기초', '전략'], 'cta': '무료 강의 수강', 'advertiser': 'InvestEdu Academy', 'category': 'education', 'relevance_score': 2.5, 'rank': 3, 'personalized_message': '^VIX의 기술적 패턴을 놓치지 마세요. 더 정확한 분석 도구가 필요하시다면?', 'tracking_url': 'https://ads.example.com/click?ad_id=투자_마스터_클래스_-_InvestEdu&article_symbol=^VIX', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 0.0, 'interest_alignment': 7.5}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 17.299999237060547, 'previous_close': 17.850000381469727, 'volume': 0, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
