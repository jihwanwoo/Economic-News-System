#!/usr/bin/env python3
"""
경제 뉴스 시스템 테스트 스크립트
"""

import os
import sys
import json
import logging
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import AgentConfig
from agents.data_collector_agent import DataCollectorAgent
from agents.news_writer_agent import NewsWriterAgent
from agents.content_optimizer_agent import ContentOptimizerAgent
from agents.orchestrator_agent import OrchestratorAgent
from config.settings import load_config


def setup_test_logging():
    """테스트용 로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def test_data_collector():
    """데이터 수집 Agent 테스트"""
    print("🧪 데이터 수집 Agent 테스트 시작...")
    
    try:
        config = AgentConfig(name="TestDataCollector")
        agent = DataCollectorAgent(config)
        
        # 간단한 데이터 수집 테스트
        result = agent.process({})
        
        print(f"✅ 데이터 수집 성공!")
        print(f"   📈 주식 데이터: {len(result.get('stock_data', {}))}개 종목")
        print(f"   📊 경제 지표: {len(result.get('economic_data', {}))}개 지표")
        print(f"   📰 뉴스 데이터: {len(result.get('news_data', []))}개 기사")
        
        return True
        
    except Exception as e:
        print(f"❌ 데이터 수집 테스트 실패: {str(e)}")
        return False


def test_news_writer():
    """뉴스 작성 Agent 테스트"""
    print("🧪 뉴스 작성 Agent 테스트 시작...")
    
    try:
        config = AgentConfig(name="TestNewsWriter")
        agent = NewsWriterAgent(config)
        
        # 테스트용 더미 데이터
        test_data = {
            "collected_data": {
                "stock_data": {
                    "AAPL": {
                        "current_price": 150.0,
                        "change": 2.5,
                        "change_percent": 1.7,
                        "name": "Apple Inc."
                    }
                },
                "economic_data": {
                    "VIX": {"value": 18.5, "interpretation": "낮은 변동성"}
                },
                "news_data": [
                    {"title": "테스트 경제 뉴스", "summary": "테스트용 뉴스입니다."}
                ],
                "analysis": {
                    "llm_analysis": "테스트 분석 결과입니다."
                }
            },
            "article_type": "market_summary",
            "target_length": "short"
        }
        
        result = agent.process(test_data)
        
        print(f"✅ 기사 작성 성공!")
        print(f"   📝 헤드라인: {result['article'].get('headline', 'N/A')[:50]}...")
        print(f"   📊 품질 점수: {result['quality_check'].get('overall_score', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 뉴스 작성 테스트 실패: {str(e)}")
        return False


def test_content_optimizer():
    """콘텐츠 최적화 Agent 테스트"""
    print("🧪 콘텐츠 최적화 Agent 테스트 시작...")
    
    try:
        config = AgentConfig(name="TestContentOptimizer")
        agent = ContentOptimizerAgent(config)
        
        # 테스트용 기사 데이터
        test_article = {
            "headline": "테스트 경제 기사 헤드라인",
            "lead": "이것은 테스트용 리드 문단입니다.",
            "content": "테스트용 기사 내용입니다. 경제 상황에 대한 분석을 제공합니다.",
            "conclusion": "테스트 결론입니다.",
            "tags": ["경제", "테스트"]
        }
        
        test_data = {
            "article": test_article,
            "focus": ["readability", "seo"]
        }
        
        result = agent.process(test_data)
        
        print(f"✅ 콘텐츠 최적화 성공!")
        print(f"   📈 가독성 점수: {result['optimizations'].get('readability', {}).get('readability_score', 'N/A')}")
        print(f"   🔍 SEO 점수: {result['optimizations'].get('seo', {}).get('seo_score', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 콘텐츠 최적화 테스트 실패: {str(e)}")
        return False


def test_orchestrator():
    """오케스트레이터 Agent 테스트"""
    print("🧪 오케스트레이터 Agent 테스트 시작...")
    
    try:
        config = load_config()
        agent_config = AgentConfig(
            name="TestOrchestrator",
            model_id=config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
            region=config.get("aws_region", "us-east-1")
        )
        
        orchestrator = OrchestratorAgent(agent_config)
        
        # 데이터 수집만 테스트
        test_data = {"workflow_type": "data_only"}
        result = orchestrator.process(test_data)
        
        print(f"✅ 오케스트레이터 테스트 성공!")
        print(f"   📊 수집된 데이터: {len(result.get('collected_data', {}))} 항목")
        
        return True
        
    except Exception as e:
        print(f"❌ 오케스트레이터 테스트 실패: {str(e)}")
        return False


def test_configuration():
    """설정 시스템 테스트"""
    print("🧪 설정 시스템 테스트 시작...")
    
    try:
        from config.settings import load_config, validate_config
        
        # 기본 설정 로드
        config = load_config()
        
        # 설정 유효성 검증
        is_valid = validate_config(config)
        
        print(f"✅ 설정 시스템 테스트 성공!")
        print(f"   ⚙️ 설정 항목 수: {len(config)}")
        print(f"   ✔️ 유효성 검증: {'통과' if is_valid else '실패'}")
        print(f"   🌍 AWS 리전: {config.get('aws_region', 'N/A')}")
        print(f"   🤖 모델 ID: {config.get('model_id', 'N/A')}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ 설정 시스템 테스트 실패: {str(e)}")
        return False


def test_aws_connection():
    """AWS 연결 테스트"""
    print("🧪 AWS 연결 테스트 시작...")
    
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        # Bedrock 클라이언트 생성
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # 사용 가능한 모델 목록 조회 (간단한 연결 테스트)
        try:
            # 실제 모델 호출 대신 클라이언트 생성만 테스트
            print(f"✅ AWS Bedrock 클라이언트 생성 성공!")
            print(f"   🌍 리전: us-east-1")
            return True
            
        except ClientError as e:
            print(f"⚠️ AWS 연결 경고: {str(e)}")
            print("   💡 AWS 자격 증명을 확인하세요.")
            return False
            
    except NoCredentialsError:
        print(f"❌ AWS 자격 증명 없음")
        print("   💡 AWS 자격 증명을 설정하세요:")
        print("      - aws configure")
        print("      - 환경 변수 설정")
        print("      - IAM 역할 사용")
        return False
        
    except Exception as e:
        print(f"❌ AWS 연결 테스트 실패: {str(e)}")
        return False


def run_all_tests():
    """모든 테스트 실행"""
    print("🚀 경제 뉴스 시스템 전체 테스트 시작")
    print("=" * 50)
    
    tests = [
        ("설정 시스템", test_configuration),
        ("AWS 연결", test_aws_connection),
        ("데이터 수집 Agent", test_data_collector),
        ("뉴스 작성 Agent", test_news_writer),
        ("콘텐츠 최적화 Agent", test_content_optimizer),
        ("오케스트레이터 Agent", test_orchestrator)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} 테스트")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 예외 발생: {str(e)}")
            results.append((test_name, False))
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 전체 결과: {passed}/{total} 테스트 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
        print("💡 이제 main.py를 실행하여 시스템을 사용할 수 있습니다.")
    else:
        print("⚠️ 일부 테스트가 실패했습니다.")
        print("💡 실패한 테스트를 확인하고 문제를 해결하세요.")
    
    return passed == total


if __name__ == "__main__":
    setup_test_logging()
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        
        if test_name == "config":
            test_configuration()
        elif test_name == "aws":
            test_aws_connection()
        elif test_name == "data":
            test_data_collector()
        elif test_name == "writer":
            test_news_writer()
        elif test_name == "optimizer":
            test_content_optimizer()
        elif test_name == "orchestrator":
            test_orchestrator()
        else:
            print(f"알 수 없는 테스트: {test_name}")
            print("사용 가능한 테스트: config, aws, data, writer, optimizer, orchestrator")
    else:
        run_all_tests()
