#!/usr/bin/env python3
"""
통합 자동화 시스템 테스트
이벤트 감지부터 Streamlit 발행까지 전체 워크플로우 테스트
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 필요한 패키지 설치 확인
def check_and_install_packages():
    """필요한 패키지 확인 및 설치"""
    
    required_packages = [
        'matplotlib', 'seaborn', 'pillow', 'boto3'
    ]
    
    import subprocess
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"📦 {package} 설치 중...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# 패키지 설치
check_and_install_packages()

# 에이전트 import
from agents.orchestrator_agent import OrchestratorAgent

async def test_full_automation():
    """전체 자동화 시스템 테스트"""
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/automation_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )
    
    print("🚀 통합 자동화 시스템 테스트 시작")
    print("=" * 80)
    
    try:
        # 출력 디렉토리 생성
        os.makedirs('logs', exist_ok=True)
        os.makedirs('output/automated_articles', exist_ok=True)
        os.makedirs('output/charts', exist_ok=True)
        os.makedirs('output/images', exist_ok=True)
        os.makedirs('streamlit_articles', exist_ok=True)
        
        print("📁 출력 디렉토리 생성 완료")
        
        # 오케스트레이터 초기화
        print("\n🎭 오케스트레이터 에이전트 초기화 중...")
        orchestrator = OrchestratorAgent()
        
        # 전체 자동화 사이클 실행
        print("\n🔄 전체 자동화 사이클 실행 중...")
        print("   1️⃣ 이벤트 감지")
        print("   2️⃣ 데이터 분석 및 차트 생성")
        print("   3️⃣ 기사 작성")
        print("   4️⃣ 이미지 생성")
        print("   5️⃣ 기사 검수")
        print("   6️⃣ 광고 추천")
        print("   7️⃣ Streamlit 페이지 생성")
        print("   8️⃣ Slack 알림 전송")
        
        # 자동화 실행
        article_packages = await orchestrator.run_full_automation_cycle()
        
        # 결과 출력
        print("\n" + "=" * 80)
        print("✅ 통합 자동화 시스템 테스트 완료!")
        print(f"📊 생성된 기사 수: {len(article_packages)}개")
        
        if article_packages:
            print("\n📰 생성된 기사 목록:")
            for i, package in enumerate(article_packages, 1):
                print(f"   {i}. {package.event.symbol}: {package.event.title}")
                print(f"      📈 변화율: {package.event.change_percent:+.2f}%")
                print(f"      🔍 검수 점수: {package.review_result.get('overall_score', 0):.1f}/10")
                print(f"      📢 추천 광고: {len(package.advertisements)}개")
                print(f"      🔗 Streamlit URL: {package.streamlit_url}")
                print()
        
        # 파일 생성 확인
        print("📁 생성된 파일 확인:")
        
        # 기사 파일
        article_files = os.listdir('output/automated_articles')
        print(f"   📄 기사 파일: {len(article_files)}개")
        
        # 차트 파일
        if os.path.exists('output/charts'):
            chart_files = os.listdir('output/charts')
            print(f"   📊 차트 파일: {len(chart_files)}개")
        
        # 이미지 파일
        if os.path.exists('output/images'):
            image_files = os.listdir('output/images')
            print(f"   🖼️ 이미지 파일: {len(image_files)}개")
        
        # Streamlit 페이지
        if os.path.exists('streamlit_articles'):
            streamlit_files = os.listdir('streamlit_articles')
            print(f"   📱 Streamlit 페이지: {len(streamlit_files)}개")
        
        # 성공 메시지
        print("\n🎉 모든 워크플로우가 성공적으로 완료되었습니다!")
        print("📱 Slack 채널에서 알림을 확인하세요.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 자동화 시스템 테스트 실패: {e}")
        logging.error(f"자동화 테스트 실패: {e}")
        return False

def test_individual_agents():
    """개별 에이전트 테스트"""
    
    print("\n🧪 개별 에이전트 테스트")
    print("-" * 40)
    
    # 간단한 테스트 이벤트 생성
    from event_detection_slack_system import EconomicEvent, EventSeverity
    
    test_event = EconomicEvent(
        symbol="AAPL",
        event_type="price_change",
        severity=EventSeverity.HIGH,
        title="AAPL 급등 감지",
        description="AAPL이 3.5% 급등했습니다.",
        current_value=175.0,
        previous_value=169.0,
        change_percent=3.55,
        timestamp=datetime.now()
    )
    
    # 1. 데이터 분석 에이전트 테스트
    try:
        from agents.data_analysis_agent import DataAnalysisAgent
        
        print("📊 데이터 분석 에이전트 테스트...")
        data_agent = DataAnalysisAgent()
        
        # 비동기 함수를 동기적으로 실행
        import asyncio
        analysis_result = asyncio.run(data_agent.analyze_event_data(test_event))
        
        if 'error' not in analysis_result:
            print("   ✅ 데이터 분석 성공")
        else:
            print(f"   ❌ 데이터 분석 실패: {analysis_result['error']}")
            
    except Exception as e:
        print(f"   ❌ 데이터 분석 에이전트 오류: {e}")
    
    # 2. 기사 작성 에이전트 테스트
    try:
        from agents.article_writer_agent import ArticleWriterAgent
        
        print("✍️ 기사 작성 에이전트 테스트...")
        writer_agent = ArticleWriterAgent()
        
        # 샘플 분석 데이터
        sample_analysis = {
            'raw_data': {'current_price': 175.0, 'change_percent': 3.55},
            'technical_indicators': {'rsi': 65, 'sma_20': 170.0},
            'forecast': {'outlook': '강세'}
        }
        
        article_result = asyncio.run(writer_agent.write_article(test_event, sample_analysis))
        
        if 'error' not in article_result:
            print("   ✅ 기사 작성 성공")
            print(f"   📝 단어 수: {article_result.get('word_count', 0)}")
        else:
            print(f"   ❌ 기사 작성 실패: {article_result['error']}")
            
    except Exception as e:
        print(f"   ❌ 기사 작성 에이전트 오류: {e}")
    
    # 3. 검수 에이전트 테스트
    try:
        from agents.review_agent import ReviewAgent
        
        print("🔍 검수 에이전트 테스트...")
        review_agent = ReviewAgent()
        
        # 샘플 기사
        sample_article = {
            'title': 'AAPL 급등 분석',
            'content': '애플 주식이 급등했습니다. 기술적 분석 결과 강세 전망입니다. 투자 시 신중한 판단이 필요합니다.',
            'word_count': 20,
            'author': 'AI 시스템',
            'metadata': {'symbol': 'AAPL', 'sources': ['Yahoo Finance']}
        }
        
        review_result = asyncio.run(review_agent.review_article(sample_article, sample_analysis))
        
        if 'error' not in review_result:
            print("   ✅ 기사 검수 성공")
            print(f"   📊 전체 점수: {review_result.get('overall_score', 0):.1f}/10")
        else:
            print(f"   ❌ 기사 검수 실패: {review_result['error']}")
            
    except Exception as e:
        print(f"   ❌ 검수 에이전트 오류: {e}")
    
    # 4. 광고 추천 에이전트 테스트
    try:
        from agents.ad_recommendation_agent import AdRecommendationAgent
        
        print("📢 광고 추천 에이전트 테스트...")
        ad_agent = AdRecommendationAgent()
        
        ad_result = asyncio.run(ad_agent.recommend_ads(sample_article, test_event))
        
        if ad_result:
            print("   ✅ 광고 추천 성공")
            print(f"   📢 추천 광고 수: {len(ad_result)}")
        else:
            print("   ❌ 광고 추천 실패")
            
    except Exception as e:
        print(f"   ❌ 광고 추천 에이전트 오류: {e}")

def main():
    """메인 함수"""
    
    print("🤖 통합 자동화 시스템 테스트 도구")
    print("=" * 80)
    
    # 사용자 선택
    print("\n테스트 옵션을 선택하세요:")
    print("1. 전체 자동화 시스템 테스트 (권장)")
    print("2. 개별 에이전트 테스트")
    print("3. 둘 다 실행")
    
    try:
        choice = input("\n선택 (1-3): ").strip()
        
        if choice == "1":
            success = asyncio.run(test_full_automation())
        elif choice == "2":
            test_individual_agents()
            success = True
        elif choice == "3":
            test_individual_agents()
            success = asyncio.run(test_full_automation())
        else:
            print("❌ 잘못된 선택입니다.")
            return
        
        if success:
            print("\n🎉 테스트 완료!")
            print("📱 Slack 채널에서 결과를 확인하세요.")
        else:
            print("\n❌ 테스트 중 오류가 발생했습니다.")
            print("📋 로그 파일을 확인하세요.")
            
    except KeyboardInterrupt:
        print("\n⏹️ 테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")

if __name__ == "__main__":
    main()
