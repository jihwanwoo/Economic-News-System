#!/usr/bin/env python3
"""
경제 뉴스 자동 생성 시스템 - 전체 실행 스크립트
모든 기능을 통합하여 실행할 수 있는 종합 스크립트
"""

import os
import sys
import asyncio
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import json

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import AgentConfig
from agents.orchestrator_agent import OrchestratorAgent
from notifications.integrated_slack_monitor import SlackIntegratedMonitor
from data_monitoring.integrated_event_system import IntegratedEventSystem
from config.settings import load_config

class CompleteSystemRunner:
    """전체 시스템 실행 클래스"""
    
    def __init__(self, config_file: str = None):
        self.logger = logging.getLogger(__name__)
        
        # 설정 로드
        self.config = load_config(config_file) if config_file else load_config()
        
        # 환경 변수 확인
        self.aws_configured = self._check_aws_credentials()
        self.slack_configured = self._check_slack_webhook()
        
        # 시스템 구성 요소 초기화
        self.orchestrator = None
        self.slack_monitor = None
        self.event_system = None
        
        # 실행 모드
        self.available_modes = {
            'full': '전체 시스템 실행 (뉴스 생성 + Slack 알림)',
            'news-only': 'AI 뉴스 생성만 실행',
            'monitoring-only': '이벤트 모니터링만 실행',
            'slack-only': 'Slack 알림 시스템만 실행',
            'dashboard': 'Streamlit 대시보드 실행',
            'test': '시스템 테스트 실행',
            'setup': '초기 설정 및 환경 확인'
        }
    
    def _check_aws_credentials(self) -> bool:
        """AWS 자격증명 확인"""
        try:
            import boto3
            session = boto3.Session()
            credentials = session.get_credentials()
            return credentials is not None
        except Exception:
            return False
    
    def _check_slack_webhook(self) -> bool:
        """Slack 웹훅 URL 확인"""
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if webhook_url and webhook_url != "YOUR_SLACK_WEBHOOK_URL_HERE":
            return True
        
        # 파일에서 확인
        try:
            with open('config/slack_webhook.txt', 'r') as f:
                url = f.read().strip()
                return bool(url and url.startswith('https://hooks.slack.com'))
        except FileNotFoundError:
            return False
    
    def setup_logging(self, log_level: str = "INFO"):
        """로깅 설정"""
        os.makedirs('logs', exist_ok=True)
        
        log_file = f"logs/complete_system_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def print_system_status(self):
        """시스템 상태 출력"""
        print("🤖 경제 뉴스 자동 생성 시스템")
        print("=" * 60)
        print(f"📅 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 작업 디렉토리: {os.getcwd()}")
        print()
        
        print("🔧 시스템 구성 요소 상태:")
        print(f"  ✅ AWS Bedrock: {'설정됨' if self.aws_configured else '❌ 미설정'}")
        print(f"  ✅ Slack 알림: {'설정됨' if self.slack_configured else '❌ 미설정'}")
        print(f"  ✅ 설정 파일: {'로드됨' if self.config else '❌ 오류'}")
        print()
        
        print("🚀 사용 가능한 실행 모드:")
        for mode, description in self.available_modes.items():
            status = "✅" if self._can_run_mode(mode) else "⚠️"
            print(f"  {status} {mode}: {description}")
        print()
    
    def _can_run_mode(self, mode: str) -> bool:
        """특정 모드 실행 가능 여부 확인"""
        if mode in ['full', 'news-only']:
            return self.aws_configured
        elif mode in ['slack-only']:
            return self.slack_configured
        elif mode in ['monitoring-only', 'dashboard', 'test', 'setup']:
            return True
        return False
    
    async def run_full_system(self):
        """전체 시스템 실행"""
        print("🚀 전체 시스템 실행 시작")
        print("-" * 40)
        
        if not self.aws_configured:
            print("❌ AWS 자격증명이 설정되지 않았습니다.")
            return False
        
        try:
            # 1. 이벤트 감지 시스템 실행
            print("📊 1단계: 고도화된 이벤트 감지 실행 중...")
            event_system = IntegratedEventSystem()
            event_result = await event_system.run_comprehensive_analysis()
            
            if "error" in event_result:
                print(f"❌ 이벤트 감지 실패: {event_result['error']}")
                return False
            
            print(f"✅ 이벤트 감지 완료: {event_result['total_events']}개 이벤트")
            
            # 2. AI 뉴스 생성
            print("\n🤖 2단계: AI 뉴스 생성 실행 중...")
            orchestrator = self._get_orchestrator()
            
            # 이벤트 데이터를 뉴스 생성에 활용
            news_input = {
                "mode": "full",
                "event_data": event_result,
                "article_type": "comprehensive_analysis",
                "length": "medium"
            }
            
            news_result = orchestrator.process(news_input)
            
            if news_result.get('status') == 'success':
                print(f"✅ AI 뉴스 생성 완료: {news_result.get('articles_generated', 1)}개 기사")
            else:
                print("⚠️ AI 뉴스 생성 부분 실패")
            
            # 3. Slack 알림 전송
            if self.slack_configured:
                print("\n📱 3단계: Slack 알림 전송 중...")
                slack_monitor = self._get_slack_monitor()
                
                # 통합 결과 생성
                integrated_result = {
                    "timestamp": datetime.now().isoformat(),
                    "total_events": event_result['total_events'],
                    "news_generated": True,
                    "priority_alerts": self._extract_priority_alerts(event_result),
                    "risk_assessment": event_result['analysis_summary'],
                    "advanced_analysis": event_result
                }
                
                await slack_monitor._process_monitoring_result(integrated_result)
                print("✅ Slack 알림 전송 완료")
            else:
                print("⚠️ Slack 설정이 없어 알림 전송 건너뜀")
            
            # 4. 결과 저장
            self._save_complete_result(event_result, news_result)
            
            print("\n🎉 전체 시스템 실행 완료!")
            return True
            
        except Exception as e:
            self.logger.error(f"전체 시스템 실행 중 오류: {str(e)}")
            print(f"❌ 실행 중 오류 발생: {str(e)}")
            return False
    
    async def run_news_only(self):
        """AI 뉴스 생성만 실행"""
        print("🤖 AI 뉴스 생성 실행")
        print("-" * 30)
        
        if not self.aws_configured:
            print("❌ AWS 자격증명이 설정되지 않았습니다.")
            return False
        
        try:
            orchestrator = self._get_orchestrator()
            
            news_input = {
                "mode": "full",
                "article_type": "market_summary",
                "length": "medium"
            }
            
            result = orchestrator.process(news_input)
            
            if result.get('status') == 'success':
                print(f"✅ AI 뉴스 생성 완료: {result.get('articles_generated', 1)}개 기사")
                return True
            else:
                print("❌ AI 뉴스 생성 실패")
                return False
                
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            return False
    
    async def run_monitoring_only(self):
        """이벤트 모니터링만 실행"""
        print("📊 이벤트 모니터링 실행")
        print("-" * 30)
        
        try:
            event_system = IntegratedEventSystem()
            result = await event_system.run_comprehensive_analysis()
            
            if "error" not in result:
                print(f"✅ 모니터링 완료: {result['total_events']}개 이벤트 감지")
                print(f"위험도: {result['analysis_summary']['risk_level']}")
                return True
            else:
                print(f"❌ 모니터링 실패: {result['error']}")
                return False
                
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            return False
    
    async def run_slack_only(self):
        """Slack 알림 시스템만 실행"""
        print("📱 Slack 알림 시스템 실행")
        print("-" * 30)
        
        if not self.slack_configured:
            print("❌ Slack 웹훅이 설정되지 않았습니다.")
            return False
        
        try:
            slack_monitor = self._get_slack_monitor()
            result = await slack_monitor.run_single_analysis_with_alerts()
            
            if "error" not in result:
                print(f"✅ Slack 알림 완료: {result['total_events']}개 이벤트")
                return True
            else:
                print(f"❌ Slack 알림 실패: {result['error']}")
                return False
                
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            return False
    
    def run_dashboard(self):
        """Streamlit 대시보드 실행"""
        print("📈 Streamlit 대시보드 실행")
        print("-" * 30)
        
        try:
            import subprocess
            
            print("🚀 대시보드를 시작합니다...")
            print("브라우저에서 http://localhost:8501 을 열어주세요")
            print("Ctrl+C로 중지할 수 있습니다")
            
            # Streamlit 실행
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                "streamlit_app/app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0"
            ])
            
            return True
            
        except KeyboardInterrupt:
            print("\n👋 대시보드가 중지되었습니다.")
            return True
        except Exception as e:
            print(f"❌ 대시보드 실행 실패: {str(e)}")
            return False
    
    def run_test(self):
        """시스템 테스트 실행"""
        print("🧪 시스템 테스트 실행")
        print("-" * 30)
        
        try:
            import subprocess
            
            # 기본 테스트 실행
            result = subprocess.run([sys.executable, "test_system.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 시스템 테스트 통과")
                print(result.stdout)
                return True
            else:
                print("❌ 시스템 테스트 실패")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ 테스트 실행 실패: {str(e)}")
            return False
    
    def run_setup(self):
        """초기 설정 및 환경 확인"""
        print("⚙️ 시스템 설정 및 환경 확인")
        print("-" * 40)
        
        # 1. 디렉토리 생성
        print("📁 필요한 디렉토리 생성 중...")
        directories = ['logs', 'output', 'config']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"  ✅ {directory}/ 디렉토리 준비됨")
        
        # 2. 환경 변수 확인
        print("\n🔧 환경 변수 확인:")
        env_vars = {
            'AWS_ACCESS_KEY_ID': 'AWS 액세스 키',
            'AWS_SECRET_ACCESS_KEY': 'AWS 시크릿 키',
            'AWS_DEFAULT_REGION': 'AWS 리전',
            'SLACK_WEBHOOK_URL': 'Slack 웹훅 URL'
        }
        
        for var, description in env_vars.items():
            value = os.getenv(var)
            if value:
                masked_value = value[:10] + "..." if len(value) > 10 else value
                print(f"  ✅ {var}: {masked_value}")
            else:
                print(f"  ❌ {var}: 미설정 ({description})")
        
        # 3. 의존성 확인
        print("\n📦 Python 패키지 확인:")
        required_packages = [
            'boto3', 'streamlit', 'pandas', 'numpy', 
            'yfinance', 'aiohttp', 'plotly', 'scipy'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package}")
            except ImportError:
                print(f"  ❌ {package} (미설치)")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n📥 누락된 패키지 설치:")
            print(f"pip install {' '.join(missing_packages)}")
        
        # 4. 설정 파일 생성
        print("\n📝 설정 파일 확인:")
        if not os.path.exists('.env'):
            if os.path.exists('.env.example'):
                print("  📋 .env.example을 .env로 복사하여 설정을 완료하세요")
                print("  cp .env.example .env")
            else:
                print("  ⚠️ .env.example 파일이 없습니다")
        else:
            print("  ✅ .env 파일 존재")
        
        # 5. 권한 확인
        print("\n🔐 실행 권한 확인:")
        executable_files = [
            'start_slack_monitoring.py',
            'demo_slack_alerts.py',
            'demo_streamlit.py'
        ]
        
        for file in executable_files:
            if os.path.exists(file):
                if os.access(file, os.X_OK):
                    print(f"  ✅ {file}")
                else:
                    print(f"  🔧 {file} (권한 설정 중...)")
                    os.chmod(file, 0o755)
            else:
                print(f"  ❌ {file} (파일 없음)")
        
        print("\n✅ 설정 확인 완료!")
        print("\n📋 다음 단계:")
        print("1. .env 파일에 실제 값 입력")
        print("2. AWS 자격증명 설정: aws configure")
        print("3. Slack 웹훅 URL 설정")
        print("4. 시스템 테스트: python run_complete_system.py --mode test")
        
        return True
    
    def _get_orchestrator(self):
        """오케스트레이터 Agent 가져오기"""
        if not self.orchestrator:
            agent_config = AgentConfig(
                name="CompleteSystemOrchestrator",
                model_id=self.config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
                region=self.config.get("aws_region", "us-east-1"),
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 4000)
            )
            self.orchestrator = OrchestratorAgent(agent_config)
        
        return self.orchestrator
    
    def _get_slack_monitor(self):
        """Slack 모니터 가져오기"""
        if not self.slack_monitor:
            webhook_url = os.getenv("SLACK_WEBHOOK_URL")
            if not webhook_url:
                try:
                    with open('config/slack_webhook.txt', 'r') as f:
                        webhook_url = f.read().strip()
                except FileNotFoundError:
                    pass
            
            if webhook_url:
                self.slack_monitor = SlackIntegratedMonitor(webhook_url)
        
        return self.slack_monitor
    
    def _extract_priority_alerts(self, event_result: Dict) -> List[Dict]:
        """이벤트 결과에서 우선순위 알림 추출"""
        alerts = []
        
        for event in event_result.get('events', []):
            if event.get('severity', 0) > 0.6:
                alerts.append({
                    'symbol': event.get('symbol', 'UNKNOWN'),
                    'message': event.get('description', ''),
                    'severity': event.get('severity', 0),
                    'timestamp': event.get('timestamp', datetime.now().isoformat()),
                    'type': event.get('event_type', 'unknown')
                })
        
        return sorted(alerts, key=lambda x: x['severity'], reverse=True)[:5]
    
    def _save_complete_result(self, event_result: Dict, news_result: Dict):
        """전체 실행 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        complete_result = {
            "execution_info": {
                "timestamp": timestamp,
                "mode": "complete_system",
                "aws_configured": self.aws_configured,
                "slack_configured": self.slack_configured
            },
            "event_analysis": event_result,
            "news_generation": news_result,
            "summary": {
                "total_events": event_result.get('total_events', 0),
                "articles_generated": news_result.get('articles_generated', 0),
                "risk_level": event_result.get('analysis_summary', {}).get('risk_level', 'unknown'),
                "execution_success": True
            }
        }
        
        filename = f"output/complete_system_{timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(complete_result, f, ensure_ascii=False, indent=2)
            print(f"💾 전체 결과 저장: {filename}")
        except Exception as e:
            print(f"❌ 결과 저장 실패: {str(e)}")

async def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="경제 뉴스 자동 생성 시스템 - 전체 실행")
    parser.add_argument("--mode", choices=['full', 'news-only', 'monitoring-only', 'slack-only', 'dashboard', 'test', 'setup'], 
                       default='full', help="실행 모드 선택")
    parser.add_argument("--config", help="설정 파일 경로")
    parser.add_argument("--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help="로그 레벨")
    parser.add_argument("--interactive", action='store_true', help="대화형 모드")
    
    args = parser.parse_args()
    
    # 시스템 실행기 초기화
    runner = CompleteSystemRunner(args.config)
    runner.setup_logging(args.log_level)
    
    # 시스템 상태 출력
    runner.print_system_status()
    
    # 대화형 모드
    if args.interactive:
        while True:
            print("\n🎯 실행할 모드를 선택하세요:")
            for i, (mode, desc) in enumerate(runner.available_modes.items(), 1):
                status = "✅" if runner._can_run_mode(mode) else "⚠️"
                print(f"  {i}. {status} {mode}: {desc}")
            print("  0. 종료")
            
            try:
                choice = input("\n선택 (1-7, 0): ").strip()
                if choice == '0':
                    print("👋 시스템을 종료합니다.")
                    break
                
                mode_list = list(runner.available_modes.keys())
                if choice.isdigit() and 1 <= int(choice) <= len(mode_list):
                    selected_mode = mode_list[int(choice) - 1]
                    args.mode = selected_mode
                else:
                    print("❌ 잘못된 선택입니다.")
                    continue
                    
            except KeyboardInterrupt:
                print("\n👋 사용자에 의한 종료")
                break
            except Exception as e:
                print(f"❌ 입력 오류: {str(e)}")
                continue
            
            # 선택된 모드 실행
            await execute_mode(runner, args.mode)
    else:
        # 단일 모드 실행
        await execute_mode(runner, args.mode)

async def execute_mode(runner: CompleteSystemRunner, mode: str):
    """선택된 모드 실행"""
    print(f"\n🚀 '{mode}' 모드 실행 시작...")
    
    try:
        if mode == 'full':
            success = await runner.run_full_system()
        elif mode == 'news-only':
            success = await runner.run_news_only()
        elif mode == 'monitoring-only':
            success = await runner.run_monitoring_only()
        elif mode == 'slack-only':
            success = await runner.run_slack_only()
        elif mode == 'dashboard':
            success = runner.run_dashboard()
        elif mode == 'test':
            success = runner.run_test()
        elif mode == 'setup':
            success = runner.run_setup()
        else:
            print(f"❌ 알 수 없는 모드: {mode}")
            success = False
        
        if success:
            print(f"✅ '{mode}' 모드 실행 완료!")
        else:
            print(f"❌ '{mode}' 모드 실행 실패!")
            
    except KeyboardInterrupt:
        print(f"\n👋 '{mode}' 모드가 사용자에 의해 중지되었습니다.")
    except Exception as e:
        print(f"❌ '{mode}' 모드 실행 중 오류: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
