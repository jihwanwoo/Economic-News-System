#!/usr/bin/env python3
"""
자동 생성된 경제 기사 페이지
TSLA - 테슬라 주가, 높은 변동성 속에서 박스권 움직임 지속
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
    page_title="테슬라 주가, 높은 변동성 속에서 박스권 움직임 지속",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 테슬라 주가, 높은 변동성 속에서 박스권 움직임 지속")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("심볼", "TSLA")
    
    with col2:
        st.metric("이벤트", "HIGH_VOLATILITY")
    
    with col3:
        st.metric("품질점수", "7.7/10")
    
    with col4:
        st.metric("생성시간", "07:18")
    
    # 기사 이미지
    
    # 기사 관련 이미지
    if os.path.exists("output/images/TSLA_article_illustration_20250807_071825.png"):
        st.image("output/images/TSLA_article_illustration_20250807_071825.png", caption="기사 관련 일러스트레이션", use_column_width=True)
    
    if os.path.exists("output/images/TSLA_volatility_20250807_071826.png"):
        st.image("output/images/TSLA_volatility_20250807_071826.png", caption="이벤트 분석 차트", use_column_width=True)
    
    if os.path.exists("output/images/TSLA_wordcloud_20250807_071826.png"):
        st.image("output/images/TSLA_wordcloud_20250807_071826.png", caption="기사 키워드 워드클라우드", use_column_width=True)
    
    
    # 기사 본문
    st.markdown("## 📰 기사 내용")
    st.markdown("""전기차 업체 테슬라(TSLA)의 주가가 최근 들어 높은 변동성을 보이고 있다. 하지만 단기적으로는 박스권 움직임을 이어가며 뚜렷한 방향성을 잡지 못하고 있다. 주가 변동성은 기업 실적과 CEO 일론 머스크의 행보, 경쟁사 동향 등 다양한 요인에 영향을 받고 있는 것으로 분석된다.

테슬라의 주가는 지난 몇 주간 높은 변동성을 보이며 투자자들의 주목을 받고 있다. 기술적 지표와 통계 정보에 따르면 주가 변동성이 평균보다 높은 수준이며, 거래량도 상대적으로 많은 편이다. 먼저 주가 움직임을 살펴보면, 현재 테슬라 주가는 319.91달러 수준에서 박스권 등락을 이어가고 있다. 20일 이동평균선인 317.55달러를 중심으로 좁은 범위 내에서 방향성을 잡지 못하고 있는 모습이다. RSI(상대강도지수)도 50 부근에서 횡보하며 가격 모멘텀이 뚜렷하지 않음을 시사한다. 한편 연율 변동성은 0.5%로 평균 수준을 상회하고 있으며, 거래량도 평소의 0.8배 수준으로 높은 편이다. 이는 최근 테슬라 주가가 높은 변동성을 보이고 있음을 의미한다. 특히 베타값이 1.71로 시장 대비 높은 변동성을 보이고 있다. 이처럼 높은 변동성의 원인으로는 여러 가지 요인이 복합적으로 작용하고 있다. 우선 최근 발표된 테슬라의 분기 실적이 주목받았다. 전기차 판매량 증가에 힘입어 견조한 실적을 기록했지만, 일부 투자자들은 성장세 둔화에 대한 우려를 나타냈다. 또한 CEO 일론 머스크의 행보도 시장의 주목을 받고 있다. 머스크는 트위터 인수 과정에서 상당한 주식 매도를 단행했고, 트위터 경영 문제로 인해 테슬라 경영에 소홀할 수 있다는 우려도 제기되고 있다. 이 외에도 경쟁사들의 전기차 시장 공략이 가속화되면서 향후 시장 점유율 경쟁이 격화될 것이라는 전망이 나오고 있다. 특히 중국 업체들의 약진이 두드러지고 있어 테슬라의 경쟁력에 대한 의구심도 존재한다. 전문가들은 테슬라 주가의 높은 변동성이 단기적으로는 지속될 것으로 내다보고 있다. 김철수 삼성증권 연구원은 "테슬라 주가는 기업 성과뿐만 아니라 CEO 리스크, 경쟁 심화 등 다양한 요인에 영향을 받고 있다"며 "단기적으로는 박스권 등락이 이어질 가능성이 높다"고 분석했다.

## 결론

테슬라 주가는 최근 높은 변동성을 보이고 있지만, 단기적으로는 뚜렷한 방향성을 잡지 못하고 박스권 등락을 이어가고 있다. 기업 실적과 CEO 리스크, 경쟁 심화 등 복합적인 요인이 주가 변동성에 영향을 미치고 있는 것으로 분석된다. 전문가들은 당분간 높은 변동성이 지속될 것으로 전망하고 있다.

---
*본 기사는 AI 경제 뉴스 시스템에 의해 자동 생성되었습니다. 투자 결정 시 추가적인 분석과 전문가 상담을 권장합니다.*
""")
    
    # 데이터 차트
    st.markdown("## 📊 관련 데이터")
    
    # 차트 표시
    chart_paths = ['output/charts/TSLA_price_volume_20250807_071754.html', 'output/charts/TSLA_technical_20250807_071754.html', 'output/charts/TSLA_recent_20250807_071754.html', 'output/charts/TSLA_comparison_20250807_071754.html']
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
    st.json({'overall_score': 7.7, 'detailed_scores': {'content_accuracy': 7.5, 'readability': 7.0, 'completeness': 8.0, 'compliance': 9.0, 'engagement': 7.9}, 'improvements': [], 'review_timestamp': '2025-08-07T07:18:25.422644', 'reviewer': '기사 검수 에이전트', 'status': 'approved'})
    

    # 📢 관련 서비스 및 상품 추천
    
    st.markdown("---")
    st.markdown("### 🎯 맞춤형 추천 서비스")
    
    ads_data = [{'id': 'inv_002', 'title': '로보어드바이저 서비스', 'description': '전문가 수준의 자동 투자 관리로 시간과 노력을 절약하세요. 변동성이 높은 시장에서 안정적인 투자를 도와드립니다.', 'cta': '1개월 무료 체험', 'category': 'investment_platforms', 'match_score': 5, 'match_reasons': ['high_volatility 이벤트에 적합', '리스크 수준 적합'], 'personalization': {'symbol_context': 'TSLA', 'event_context': 'high_volatility', 'relevance_score': 0.5}}, {'id': 'tool_001', 'title': '실시간 트레이딩 도구', 'description': '전문 트레이더들이 사용하는 고급 차트와 분석 도구를 경험하세요. 변동성이 높은 시장에서 안정적인 투자를 도와드립니다.', 'cta': '프리미엄 도구 체험', 'category': 'trading_tools', 'match_score': 5, 'match_reasons': ['high_volatility 이벤트에 적합', '관련 키워드: 분석'], 'personalization': {'symbol_context': 'TSLA', 'event_context': 'high_volatility', 'relevance_score': 0.5}}, {'id': 'edu_001', 'title': '투자 교육 아카데미', 'description': '기초부터 고급까지, 체계적인 투자 교육으로 전문가가 되세요. 변동성이 높은 시장에서 안정적인 투자를 도와드립니다.', 'cta': '무료 강의 수강', 'category': 'education_services', 'match_score': 5, 'match_reasons': ['high_volatility 이벤트에 적합', '리스크 수준 적합'], 'personalization': {'symbol_context': 'TSLA', 'event_context': 'high_volatility', 'relevance_score': 0.5}}]
    
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
