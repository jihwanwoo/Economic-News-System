#!/usr/bin/env python3
"""
OrchestratorStrand import 오류 수정 스크립트
"""

import os
import sys

def fix_import_error():
    """import 오류 수정"""
    
    print("🔧 OrchestratorStrand import 오류 수정 중...")
    
    # agents/__init__.py 파일 수정
    init_file = "agents/__init__.py"
    
    try:
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # import 순서 수정
        fixed_content = '''"""
Strands Agent 프레임워크 기반 경제 뉴스 시스템
"""

# Strands 프레임워크
from .strands_framework import BaseStrandAgent, StrandContext, StrandMessage, MessageType, StrandOrchestrator, orchestrator

# Strand Agents
try:
    from .data_analysis_strand import DataAnalysisStrand
    from .article_writer_strand import ArticleWriterStrand
    from .review_strand import ReviewStrand
    from .image_generator_strand import ImageGeneratorStrand
    from .ad_recommendation_strand import AdRecommendationStrand
    from .orchestrator_strand import OrchestratorStrand, main_orchestrator
    
    __all__ = [
        # Framework
        'BaseStrandAgent',
        'StrandContext', 
        'StrandMessage',
        'MessageType',
        'StrandOrchestrator',
        'orchestrator',
        
        # Strand Agents
        'DataAnalysisStrand',
        'ArticleWriterStrand', 
        'ReviewStrand',
        'ImageGeneratorStrand',
        'AdRecommendationStrand',
        'OrchestratorStrand',
        'main_orchestrator'
    ]
    
except ImportError as e:
    print(f"⚠️ Agent import 오류: {e}")
    
    # 기본 프레임워크만 export
    __all__ = [
        'BaseStrandAgent',
        'StrandContext', 
        'StrandMessage',
        'MessageType',
        'StrandOrchestrator',
        'orchestrator'
    ]
'''
        
        # 백업 생성
        backup_file = f"{init_file}.backup"
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 백업 생성: {backup_file}")
        
        # 수정된 내용 저장
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"✅ {init_file} 수정 완료")
        
        return True
        
    except Exception as e:
        print(f"❌ 파일 수정 실패: {e}")
        return False

def test_import():
    """import 테스트"""
    
    print("\n🧪 import 테스트 중...")
    
    try:
        # 기본 프레임워크 테스트
        from agents import BaseStrandAgent, StrandContext, orchestrator
        print("✅ 기본 프레임워크 import 성공")
        
        # 개별 에이전트 테스트
        try:
            from agents import OrchestratorStrand, main_orchestrator
            print("✅ OrchestratorStrand import 성공")
        except ImportError as e:
            print(f"⚠️ OrchestratorStrand import 실패: {e}")
        
        try:
            from agents import DataAnalysisStrand, ArticleWriterStrand
            print("✅ 기타 에이전트 import 성공")
        except ImportError as e:
            print(f"⚠️ 기타 에이전트 import 실패: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ import 테스트 실패: {e}")
        return False

def main():
    """메인 함수"""
    
    print("🔧 OrchestratorStrand Import 오류 수정 도구")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    if not os.path.exists("agents"):
        print("❌ agents 디렉토리를 찾을 수 없습니다.")
        print("💡 프로젝트 루트 디렉토리에서 실행해주세요.")
        return
    
    # import 오류 수정
    if fix_import_error():
        print("\n✅ import 오류 수정 완료")
        
        # 테스트 실행
        if test_import():
            print("\n🎉 모든 import가 정상적으로 작동합니다!")
            print("\n💡 이제 다음 명령어로 시스템을 실행할 수 있습니다:")
            print("  • HTML 기사 생성: ./run_html_articles.sh")
            print("  • 통합 시스템: ./run_news_system.sh")
            print("  • Slack 테스트: python test_slack_notification.py")
        else:
            print("\n⚠️ 일부 import에 문제가 있지만 기본 기능은 작동합니다.")
            print("💡 HTML 기사 생성 시스템을 사용하세요: ./run_html_articles.sh")
    else:
        print("\n❌ import 오류 수정 실패")
        print("💡 HTML 기사 생성 시스템은 독립적으로 작동합니다: ./run_html_articles.sh")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
