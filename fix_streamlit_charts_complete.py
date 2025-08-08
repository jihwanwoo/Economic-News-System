#!/usr/bin/env python3
"""
Streamlit 차트 표시 오류 완전 수정
HTML 파일을 이미지로 표시하려는 오류 해결
"""

import os
import glob
import re

def fix_all_streamlit_files():
    """모든 Streamlit 파일의 차트 표시 오류 수정"""
    
    print("🔧 Streamlit 파일 차트 표시 오류 수정 시작...")
    
    # streamlit_articles 디렉토리의 모든 파일 찾기
    article_files = glob.glob("streamlit_articles/article_*.py")
    
    if not article_files:
        print("❌ 수정할 Streamlit 파일이 없습니다.")
        return False
    
    success_count = 0
    
    for file_path in article_files:
        try:
            print(f"수정 중: {file_path}")
            
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 문제가 되는 코드 패턴 찾기 및 수정
            # 패턴 1: st.image(chart_path, caption=f"차트 {i+1}")
            if 'st.image(chart_path' in content:
                # 잘못된 차트 표시 코드를 올바른 코드로 교체
                old_pattern = r'# 차트 표시.*?st\.image\(chart_path.*?\)'
                new_code = '''# 차트 표시 (HTML 파일 올바른 처리)
    chart_paths = [path for path in chart_paths if os.path.exists(path)]
    
    if chart_paths:
        for i, chart_path in enumerate(chart_paths):
            st.markdown(f"### 📊 Chart {i+1}")
            try:
                if chart_path.endswith('.html'):
                    # HTML 파일을 iframe으로 표시
                    with open(chart_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    st.components.v1.html(html_content, height=600, scrolling=True)
                elif chart_path.endswith(('.png', '.jpg', '.jpeg')):
                    # 이미지 파일 표시
                    st.image(chart_path, caption=f"Chart {i+1}", use_column_width=True)
                else:
                    st.info(f"Chart file: {os.path.basename(chart_path)}")
            except Exception as e:
                st.error(f"Chart loading error: {str(e)}")
                st.info(f"Chart file path: {chart_path}")
    else:
        st.info("No charts available for this article.")'''
                
                content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)
            
            # 패턴 2: for i, chart_path in enumerate([...]):
            chart_list_pattern = r'for i, chart_path in enumerate\(\[.*?\]\):\s*if os\.path\.exists\(chart_path\):\s*st\.image\(chart_path.*?\)'
            if re.search(chart_list_pattern, content, re.DOTALL):
                content = re.sub(chart_list_pattern, new_code, content, flags=re.DOTALL)
            
            # streamlit.components.v1 import 추가 확인
            if 'import streamlit.components.v1' not in content and 'components.v1.html' in content:
                # import 부분에 components 추가
                import_pattern = r'(import streamlit as st)'
                replacement = r'\1\nimport streamlit.components.v1 as components'
                content = re.sub(import_pattern, replacement, content)
                
                # components.v1.html을 components.html로 변경
                content = content.replace('st.components.v1.html', 'components.html')
            
            # 파일 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 수정 완료: {file_path}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ 수정 실패: {file_path} - {e}")
    
    print(f"\n🎉 총 {success_count}개 파일 수정 완료!")
    return success_count > 0

def create_sample_fixed_streamlit():
    """수정된 Streamlit 파일 샘플 생성"""
    
    sample_content = '''#!/usr/bin/env python3
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
'''
    
    # 샘플 파일 저장
    os.makedirs("streamlit_articles", exist_ok=True)
    sample_path = "streamlit_articles/sample_fixed_article.py"
    
    with open(sample_path, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"✅ 수정된 샘플 파일 생성: {sample_path}")
    return sample_path

if __name__ == "__main__":
    print("🚀 Streamlit 차트 표시 오류 완전 수정")
    print("=" * 60)
    
    # 기존 파일들 수정
    success = fix_all_streamlit_files()
    
    # 샘플 파일 생성
    sample_path = create_sample_fixed_streamlit()
    
    if success:
        print("\n🎉 모든 Streamlit 파일 수정 완료!")
        print("📊 이제 HTML 차트가 올바르게 표시됩니다.")
        print(f"📄 샘플 파일 실행: streamlit run {sample_path}")
    else:
        print("\n❌ 일부 파일 수정에 실패했습니다.")
    
    print("\n💡 사용법:")
    print("   python run_article_pages.py")
    print("   또는")
    print("   streamlit run streamlit_articles/[파일명].py")
