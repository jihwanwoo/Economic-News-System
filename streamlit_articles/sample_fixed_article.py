#!/usr/bin/env python3
"""
수정된 Streamlit 기사 페이지 샘플
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Economic News Article",
    page_icon="📈",
    layout="wide"
)

def main():
    """메인 함수"""
    
    # 헤더
    st.title("📈 Sample Economic News Article")
    st.markdown("---")
    
    # 기사 메타데이터
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Symbol", "SAMPLE")
    
    with col2:
        st.metric("Change", "+2.5%")
    
    with col3:
        st.metric("Severity", "MEDIUM")
    
    with col4:
        st.metric("Time", "09:30")
    
    # 기사 본문
    st.markdown("## 📰 Article Content")
    st.markdown("""
    This is a sample article content that demonstrates the fixed chart display functionality.
    The charts below will be properly displayed using HTML components instead of image display.
    """)
    
    # 데이터 차트 (수정된 버전)
    st.markdown("## 📊 Related Data & Charts")
    
    # 차트 파일 경로 (실제 파일이 있다면)
    chart_paths = [
        "output/charts/sample_chart1.html",
        "output/charts/sample_chart2.html"
    ]
    
    # 존재하는 차트만 필터링
    existing_charts = [path for path in chart_paths if os.path.exists(path)]
    
    if existing_charts:
        for i, chart_path in enumerate(existing_charts):
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
        st.info("No charts available for this article. Charts will be displayed here when available.")
    
    # 검수 결과
    st.markdown("## 🔍 Review Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Quality Score", "9.5/10")
    
    with col2:
        st.metric("Accuracy Score", "9.0/10")
    
    with col3:
        st.metric("Style Score", "9.2/10")
    
    with col4:
        st.metric("Overall Score", "9.2/10")
    
    # 광고 추천
    st.markdown("## 📢 Related Services")
    
    with st.expander("📢 Smart Trading Platform"):
        st.markdown("**Description:** Advanced trading tools with real-time analysis")
        st.markdown("**Target:** Active traders and technical analysts")
        st.markdown("**Relevance:** 8.5/10")
    
    with st.expander("📢 Investment Education"):
        st.markdown("**Description:** Comprehensive investment education program")
        st.markdown("**Target:** Beginner to intermediate investors")
        st.markdown("**Relevance:** 7.8/10")
    
    with st.expander("📢 Portfolio Management"):
        st.markdown("**Description:** AI-powered portfolio optimization service")
        st.markdown("**Target:** Long-term investors")
        st.markdown("**Relevance:** 8.0/10")
    
    # 푸터
    st.markdown("---")
    st.markdown(f"**Generated Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**System:** Automated Economic News Generation System")

if __name__ == "__main__":
    main()
