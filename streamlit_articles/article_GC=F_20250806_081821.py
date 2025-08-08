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
        st.metric("변화율", "+258.43%")
    
    with col3:
        st.metric("심각도", "CRITICAL")
    
    with col4:
        st.metric("발생시간", "08:17")
    
    # 기사 이미지
    if os.path.exists("output/images/GC=F_volume_spike_20250806_081821.png"):
        st.image("output/images/GC=F_volume_spike_20250806_081821.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# GC=F 거래량 급증, 3.9배 증가

GC=F의 거래량이 평균 대비 3.9배 급증하며 이상 거래 패턴을 보이고 있습니다.

GC=F 상품의 거래량이 평균 대비 3.6배 증가한 것은 주목할 만한 사건입니다. 이는 시장 참여자들의 이 상품에 대한 관심이 크게 높아졌음을 시사합니다. 

현재 가격은 3,423.90달러로, 지난 한 달 평균 가격 3,349.60달러보다 2.22% 높은 수준입니다. 가격 변동성은 연율 13.83%로 다소 높은 편입니다. 20일 단순이동평균선인 3,354.49달러를 상회하고 있어 단기 상승세가 유지되는 모습입니다.

기술적 지표를 살펴보면, MACD 지표의 본선과 신호선이 상향 교차했고, RSI 지표 역시 60선 부근에 위치해 상승 모멘텀이 유지되고 있습니다. 볼린저 밴드 상단인 3,434.14달러를 근접하고 있어 단기 과열 조짐도 엿보입니다.

시장 비교 분석 결과, 베타 값이 -0.39로 시장 대비 반대 방향으로 움직이는 경향을 보입니다. S&P 500 지수와의 상관관계도 -0.28로 낮은 편입니다. 지난 한 달간 상대 성과는 34.79%로 우수했습니다.

전망 모델에 따르면, GC=F는 단기적으로 약간 강세를 보일 것으로 예측되며, 지지선과 저항선은 각각 3,274.85달러와 3,434.14달러 수준입니다. 전망 점수는 30점, 신뢰도는 60%입니다.

투자자들은 GC=F의 최근 거래량 급증과 단기 상승 모멘텀, 시장 대비 독립적인 가격 움직임을 주목할 필요가 있습니다. 다만 볼린저 밴드 상단에 근접한 만큼 과열 조정 가능성도 배제할 수 없습니다. 리스크 관리를 병행하며 기술적, 펀더멘털 요인을 지속 모니터링하는 것이 바람직해 보입니다.

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
    review = {'review_timestamp': '2025-08-06T08:18:21.573876', 'overall_score': 10.0, 'quality_score': 10.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 10.0, 'issues': [], 'word_count': 202, 'structure_complete': True}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.005936355833333334, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.0043859649122807015, 'technical_depth': 8}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 3, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
    
    ads = [{'title': '프로 트레이딩 플랫폼 - TradeMax', 'description': '실시간 차트, 기술적 분석 도구, 알고리즘 트레이딩까지. 전문 트레이더를 위한 올인원 솔루션.', 'target_audience': '전문 트레이더', 'relevance_keywords': ['트레이딩', '차트', '기술적분석', '알고리즘'], 'cta': '30일 무료 체험', 'advertiser': 'TradeMax Ltd.', 'category': 'trading_platform', 'relevance_score': 6.5, 'rank': 1, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=프로_트레이딩_플랫폼_-_TradeMax&article_symbol=GC=F', 'metrics': {'keyword_relevance': 2.5, 'audience_match': 10.0, 'interest_alignment': 7.5}}, {'title': '스마트 투자 플랫폼 - InvestSmart', 'description': 'AI 기반 포트폴리오 관리와 실시간 시장 분석으로 스마트한 투자를 시작하세요.', 'target_audience': '개인 투자자', 'relevance_keywords': ['투자', '포트폴리오', '주식', '분석'], 'cta': '무료 체험 시작하기', 'advertiser': 'InvestSmart Inc.', 'category': 'investment_platform', 'relevance_score': 4.5, 'rank': 2, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=스마트_투자_플랫폼_-_InvestSmart&article_symbol=GC=F', 'metrics': {'keyword_relevance': 5.0, 'audience_match': 0.0, 'interest_alignment': 7.5}}, {'title': '모바일 트레이딩 앱 - QuickTrade', 'description': '언제 어디서나 빠른 매매. 실시간 알림과 간편한 주문으로 기회를 놓치지 마세요.', 'target_audience': '모바일 트레이더', 'relevance_keywords': ['모바일', '실시간', '알림', '빠른매매'], 'cta': '앱 다운로드', 'advertiser': 'QuickTrade App', 'category': 'mobile_trading', 'relevance_score': 2.5, 'rank': 3, 'personalized_message': 'GC=F 분석에 관심이 있으시군요! 전문 트레이더를 위한 고급 도구를 확인해보세요.', 'tracking_url': 'https://ads.example.com/click?ad_id=모바일_트레이딩_앱_-_QuickTrade&article_symbol=GC=F', 'metrics': {'keyword_relevance': 0.0, 'audience_match': 0.0, 'interest_alignment': 7.5}}]
    for i, ad in enumerate(ads[:3], 1):
        with st.expander(f"광고 {i}: {ad.get('title', 'Unknown')}"):
            st.markdown(f"**설명:** {ad.get('description', '')}")
            st.markdown(f"**타겟:** {ad.get('target_audience', '')}")
            st.markdown(f"**관련성:** {ad.get('relevance_score', 0):.1f}/10")
    
    # Raw 데이터
    st.markdown("## 📋 원시 데이터")
    
    with st.expander("Raw 데이터 보기"):
        st.json({'current_price': 3423.89990234375, 'previous_close': 3381.89990234375, 'volume': 35546, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
