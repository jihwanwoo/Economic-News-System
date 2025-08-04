#!/usr/bin/env python3
"""
경제 뉴스 자동 생성 시스템 메인 실행 스크립트
"""

import os
import sys
import argparse
import logging
import json
from datetime import datetime
from typing import Dict, Any

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import AgentConfig
from agents.orchestrator_agent import OrchestratorAgent
from config.settings import load_config


def setup_logging(log_level: str = "INFO") -> None:
    """로깅 설정"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"economic_news_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_orchestrator(config: Dict[str, Any]) -> OrchestratorAgent:
    """오케스트레이터 Agent 생성"""
    agent_config = AgentConfig(
        name="EconomicNewsOrchestrator",
        model_id=config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
        region=config.get("aws_region", "us-east-1"),
        temperature=config.get("temperature", 0.7),
        max_tokens=config.get("max_tokens", 4000)
    )
    
    return OrchestratorAgent(agent_config)


def run_full_pipeline(orchestrator: OrchestratorAgent, args: argparse.Namespace) -> Dict[str, Any]:
    """전체 파이프라인 실행"""
    print("🚀 경제 뉴스 생성 파이프라인을 시작합니다...")
    
    # 기사 설정
    article_configs = []
    if args.market_summary:
        article_configs.append({"article_type": "market_summary", "target_length": "medium"})
    if args.stock_focus:
        article_configs.append({"article_type": "stock_focus", "target_length": "short"})
    if args.economic_outlook:
        article_configs.append({"article_type": "economic_outlook", "target_length": "long"})
    
    # 기본값 설정
    if not article_configs:
        article_configs = [
            {"article_type": "market_summary", "target_length": "medium"},
            {"article_type": "stock_focus", "target_length": "short"}
        ]
    
    input_data = {
        "workflow_type": "full_pipeline",
        "article_configs": article_configs
    }
    
    result = orchestrator.process(input_data)
    
    print(f"✅ 파이프라인 완료! {len(result.get('articles', []))}개 기사 생성됨")
    print(f"📁 결과 저장 위치: {orchestrator.output_dir}")
    
    return result


def run_data_collection(orchestrator: OrchestratorAgent) -> Dict[str, Any]:
    """데이터 수집만 실행"""
    print("📊 경제 데이터 수집을 시작합니다...")
    
    input_data = {"workflow_type": "data_only"}
    result = orchestrator.process(input_data)
    
    print("✅ 데이터 수집 완료!")
    print(f"📈 수집된 주식 데이터: {len(result.get('collected_data', {}).get('stock_data', {}))}개 종목")
    print(f"📰 수집된 뉴스: {len(result.get('collected_data', {}).get('news_data', []))}개 기사")
    
    return result


def run_article_generation(orchestrator: OrchestratorAgent, args: argparse.Namespace) -> Dict[str, Any]:
    """기사 생성만 실행"""
    print("✍️ 경제 기사 생성을 시작합니다...")
    
    article_config = {
        "article_type": args.article_type or "market_summary",
        "target_length": args.length or "medium"
    }
    
    input_data = {
        "workflow_type": "article_only",
        "article_config": article_config
    }
    
    result = orchestrator.process(input_data)
    
    print("✅ 기사 생성 완료!")
    print(f"📝 기사 유형: {article_config['article_type']}")
    print(f"📏 목표 길이: {article_config['target_length']}")
    
    return result


def run_scheduled_mode(orchestrator: OrchestratorAgent) -> None:
    """스케줄 모드 실행"""
    print("⏰ 스케줄 모드를 시작합니다...")
    print("정기적으로 경제 뉴스를 생성합니다. Ctrl+C로 중단할 수 있습니다.")
    
    try:
        orchestrator.schedule_automated_runs()
    except KeyboardInterrupt:
        print("\n⏹️ 스케줄 모드가 중단되었습니다.")


def show_status(orchestrator: OrchestratorAgent) -> None:
    """시스템 상태 표시"""
    status = orchestrator.get_system_status()
    
    print("📊 시스템 상태:")
    print(f"  ⏰ 현재 시간: {status['timestamp']}")
    print(f"  🤖 Agent 상태: {status['agents_status']}")
    print(f"  📁 출력 디렉토리: {status['output_directory']}")
    print(f"  ⚙️ 스케줄 설정: {status['schedule_config']}")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="경제 뉴스 자동 생성 시스템")
    
    # 실행 모드
    parser.add_argument("--mode", choices=["full", "data", "article", "schedule", "status"], 
                       default="full", help="실행 모드 선택")
    
    # 기사 유형 선택
    parser.add_argument("--market-summary", action="store_true", help="시장 종합 분석 기사 생성")
    parser.add_argument("--stock-focus", action="store_true", help="개별 종목 분석 기사 생성")
    parser.add_argument("--economic-outlook", action="store_true", help="경제 전망 기사 생성")
    
    # 기사 설정
    parser.add_argument("--article-type", choices=["market_summary", "stock_focus", "economic_outlook"],
                       help="기사 유형 (article 모드용)")
    parser.add_argument("--length", choices=["short", "medium", "long"], 
                       help="기사 길이 (article 모드용)")
    
    # 시스템 설정
    parser.add_argument("--config", default="config/default.json", help="설정 파일 경로")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="로그 레벨")
    
    args = parser.parse_args()
    
    # 로깅 설정
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # 설정 로드
        config = load_config(args.config)
        logger.info(f"설정 로드 완료: {args.config}")
        
        # 오케스트레이터 생성
        orchestrator = create_orchestrator(config)
        logger.info("오케스트레이터 초기화 완료")
        
        # 모드별 실행
        if args.mode == "full":
            result = run_full_pipeline(orchestrator, args)
        elif args.mode == "data":
            result = run_data_collection(orchestrator)
        elif args.mode == "article":
            result = run_article_generation(orchestrator, args)
        elif args.mode == "schedule":
            run_scheduled_mode(orchestrator)
            return
        elif args.mode == "status":
            show_status(orchestrator)
            return
        
        # 결과 요약 출력
        if 'result' in locals():
            print(f"\n📋 실행 요약:")
            print(f"  ⏰ 실행 시간: {result.get('timestamp', 'N/A')}")
            if 'pipeline_duration' in result:
                print(f"  ⏱️ 소요 시간: {result['pipeline_duration']:.2f}초")
        
        logger.info("프로그램 실행 완료")
        
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {str(e)}")
        print(f"❌ 오류 발생: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
