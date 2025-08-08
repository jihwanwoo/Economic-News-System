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
        st.metric("변화율", "+253.28%")
    
    with col3:
        st.metric("심각도", "CRITICAL")
    
    with col4:
        st.metric("발생시간", "07:48")
    
    # 기사 이미지
    if os.path.exists("output/images/GC=F_volume_spike_20250806_074850.png"):
        st.image("output/images/GC=F_volume_spike_20250806_074850.png", caption="기사 관련 이미지")
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""# GC=F 거래량 급증, 3.5배 증가

GC=F의 거래량이 평균 대비 3.5배 급증하며 이상 거래 패턴을 보이고 있습니다.

금 선물 시장에서 GC=F 종목의 거래량이 평균 대비 3.5배 이상 급증하는 '볼륨 스파이크' 현상이 발생했습니다. 이는 단기간에 많은 거래가 일어났음을 시사하며, 시장 참여자들의 관심이 해당 종목에 집중되고 있음을 의미합니다.

현재 GC=F의 가격은 3,426.80달러로, 지난 한 달 간 평균가격 3,349.72달러보다 2.30% 높은 수준입니다. 가격의 표준편차는 39.67달러로, 상대적으로 변동성이 크지 않은 편입니다. 그러나 연간 변동성은 13.91%로 다소 높은 수치를 보이고 있습니다.

기술적 지표를 살펴보면, 20일 이동평균선(3,354.64달러)을 상회하고 있어 단기 상승세를 시현하고 있습니다. MACD 지표 또한 5.98로 양수를 기록하며 상승 모멘텀을 보이고 있습니다. 그러나 RSI 지표는 60.64로 과열 구간에 진입한 상태입니다. 볼린저 밴드로 보면 현재가는 상단 밴드(3,434.83달러)에 근접해 있어 단기 조정이 있을 수 있습니다.

다만 현재로서는 GC=F와 유사한 대체 투자처가 없어 직접적인 시장 비교 분석은 어려운 상황입니다.

전반적으로 GC=F는 단기적으로 약간의 상승세가 예상되나, 과열 조짐으로 인해 급격한 상승보다는 박스권 등락세가 전망됩니다. 트렌드 강도는 0.48로 중립적인 모습입니다. 전문가 전망에 따르면 향후 약세 전환 가능성이 30% 수준이며, 지지선은 3,274.45달러, 저항선은 3,434.83달러로 예상됩니다. 투자자들은 이러한 기술적, 전략적 분석을 바탕으로 리스크 관리에 유의해야 할 것입니다.

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
    review = {'review_timestamp': '2025-08-06T07:48:51.034714', 'overall_score': 9.4, 'quality_score': 8.0, 'accuracy_score': 10.0, 'style_score': 10.0, 'compliance_score': 10.0, 'approval_status': 'approved', 'suggestions': [], 'detailed_review': {'content_quality': {'score': 8.0, 'issues': ['내용이 너무 짧습니다 (194단어 < 200단어)'], 'word_count': 194, 'structure_complete': False}, 'data_accuracy': {'score': 10.0, 'issues': [], 'data_freshness': 0.005392000555555556, 'data_completeness': 100.0}, 'style_guidelines': {'score': 10.0, 'issues': [], 'objectivity_score': 10, 'speculation_ratio': 0.013636363636363636, 'technical_depth': 7}, 'compliance': {'score': 10.0, 'issues': [], 'has_disclaimer': True, 'has_sources': True, 'risk_warnings': 3, 'compliance_level': 'high'}}, 'reviewer': 'AI 검수 시스템'}
    
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
        st.json({'current_price': 3426.800048828125, 'previous_close': 3381.89990234375, 'volume': 31166, 'high_52w': nan, 'low_52w': nan})
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**시스템:** 자동화된 경제 뉴스 생성 시스템")

if __name__ == "__main__":
    main()
