#!/usr/bin/env python3
"""
orchestrator_agent.py 간단 수정
"""

def fix_orchestrator():
    """orchestrator_agent.py 수정"""
    
    try:
        # 파일 읽기
        with open('agents/orchestrator_agent.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # _generate_streamlit_page_content 메서드 찾기
        start_line = -1
        end_line = -1
        
        for i, line in enumerate(lines):
            if 'def _generate_streamlit_page_content(self, package: ArticlePackage) -> str:' in line:
                start_line = i
            elif start_line != -1 and line.strip().startswith('def ') and i > start_line + 5:
                end_line = i
                break
            elif start_line != -1 and 'async def _send_slack_notification' in line:
                end_line = i
                break
        
        if start_line == -1:
            print("❌ _generate_streamlit_page_content 메서드를 찾을 수 없습니다")
            return False
        
        if end_line == -1:
            end_line = len(lines)
        
        # 새로운 메서드 작성
        new_method = '''    def _generate_streamlit_page_content(self, package: ArticlePackage) -> str:
        """Streamlit 페이지 콘텐츠 생성"""
        
        article = package.article
        event = package.event
        
        # 간단한 Streamlit 페이지 생성
        page_code = f"""#!/usr/bin/env python3
import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="{event.title}", page_icon="📈", layout="wide")

def main():
    st.title("📈 {event.title}")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Symbol", "{event.symbol}")
    with col2:
        st.metric("Change", "{event.change_percent:+.2f}%")
    with col3:
        st.metric("Severity", "{event.severity.value.upper()}")
    with col4:
        st.metric("Time", "{event.timestamp.strftime('%H:%M')}")
    
    st.markdown("## 📰 Article Content")
    st.markdown('''{article.get('content', 'Content not available')}''')
    
    st.markdown("## 📊 Charts")
    st.info("Charts are available as HTML files in the output/charts directory")
    
    st.markdown("## 🔍 Review Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Quality Score", "{package.review_result.get('quality_score', 0):.1f}/10")
    with col2:
        st.metric("Overall Score", "{package.review_result.get('overall_score', 0):.1f}/10")
    
    st.markdown("## 📢 Related Services")
    st.info("Service recommendations will be displayed here")
    
    st.markdown("---")
    st.markdown("**Generated Time:** " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    st.markdown("**System:** Automated Economic News Generation System")

if __name__ == "__main__":
    main()
"""
        
        return page_code
    
'''
        
        # 라인 교체
        new_lines = lines[:start_line] + [new_method] + lines[end_line:]
        
        # 파일 저장
        with open('agents/orchestrator_agent.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print("✅ orchestrator_agent.py 수정 완료")
        return True
        
    except Exception as e:
        print(f"❌ 수정 실패: {e}")
        return False

def test_syntax():
    """문법 검사"""
    
    try:
        import subprocess
        import sys
        
        result = subprocess.run([sys.executable, '-m', 'py_compile', 'agents/orchestrator_agent.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 문법 검사 통과")
            return True
        else:
            print(f"❌ 문법 오류: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 문법 검사 실패: {e}")
        return False

if __name__ == "__main__":
    print("🔧 orchestrator_agent.py 간단 수정")
    
    success = fix_orchestrator()
    if success:
        syntax_ok = test_syntax()
        if syntax_ok:
            print("🎉 수정 완료!")
        else:
            print("❌ 문법 오류가 남아있습니다")
    else:
        print("❌ 수정 실패")
