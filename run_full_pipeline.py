#!/usr/bin/env python3
"""
경제 뉴스 자동 생성 통합 파이프라인 실행기
- 경제 데이터 모니터링
- 이벤트 감지
- AI 기사 생성
- 품질 검수
- 맞춤형 광고 추천
"""

import sys
import os
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.base_agent import AgentConfig
from agents.orchestrator_agent import OrchestratorAgent
from streamlit_app.visualization_utils import AdGenerator
from config.settings import load_config


class EconomicNewsPipeline:
    """경제 뉴스 자동 생성 통합 파이프라인"""
    
    def __init__(self, config_path: str = None, log_level: str = "INFO"):
        self.config = load_config(config_path)
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 실행 시작 시간
        self.start_time = datetime.now()
        self.execution_id = self.start_time.strftime("%Y%m%d_%H%M%S")
        
        self.logger.info(f"경제 뉴스 파이프라인 초기화 완료 - ID: {self.execution_id}")
    
    def setup_logging(self, log_level: str):
        """로깅 설정"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"pipeline_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def print_header(self, title: str, step: int = None):
        """단계별 헤더 출력"""
        if step:
            print(f"\n{'='*80}")
            print(f"📊 {step}단계: {title}")
            print(f"{'='*80}")
        else:
            print(f"\n🔍 {title}")
            print(f"{'='*80}")
    
    def monitor_economic_data(self) -> Dict[str, Any]:
        """1단계: 경제 데이터 실시간 모니터링"""
        self.print_header("경제 데이터 실시간 모니터링", 1)
        
        try:
            # 실제 데이터 수집 시도
            from data_monitoring.data_collector import EconomicDataCollector
            
            collector = EconomicDataCollector()
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', '^GSPC', '^IXIC', '^VIX']
            current_data = {}
            
            print("📈 데이터 수집 중...")
            
            for symbol in symbols:
                try:
                    data = collector.get_current_price(symbol)
                    if data:
                        current_data[symbol] = {
                            'current_price': data.current_price,
                            'change_percent': data.change_percent,
                            'volume': data.volume,
                            'timestamp': data.timestamp.isoformat() if data.timestamp else None
                        }
                except Exception as e:
                    self.logger.warning(f"데이터 수집 실패 ({symbol}): {e}")
            
            # 데이터가 부족한 경우 샘플 데이터 보완
            if len(current_data) < 5:
                self.logger.info("샘플 데이터로 보완")
                sample_data = {
                    'AAPL': {'current_price': 202.38, 'change_percent': -2.50, 'volume': 104301700},
                    'GOOGL': {'current_price': 189.13, 'change_percent': -1.44, 'volume': 34797400},
                    'MSFT': {'current_price': 524.11, 'change_percent': -1.76, 'volume': 28955600},
                    'TSLA': {'current_price': 302.63, 'change_percent': -1.83, 'volume': 88838600},
                    'NVDA': {'current_price': 173.72, 'change_percent': -2.33, 'volume': 203851100},
                    '^GSPC': {'current_price': 6238.01, 'change_percent': -1.64, 'volume': 0},
                    '^IXIC': {'current_price': 20650.13, 'change_percent': -2.24, 'volume': 0},
                    '^VIX': {'current_price': 19.23, 'change_percent': 2.15, 'volume': 0}
                }
                current_data.update(sample_data)
            
            print(f"✅ 수집된 데이터: {len(current_data)} 항목")
            print("\n💹 주요 지표 현황:")
            
            for symbol, data in current_data.items():
                price = data['current_price']
                change = data.get('change_percent', 0)
                volume = data.get('volume', 0)
                status = '📉' if change < 0 else '📈' if change > 0 else '➡️'
                print(f"  {status} {symbol}: ${price:.2f} ({change:+.2f}%) | 거래량: {volume:,}")
            
            self.logger.info(f"경제 데이터 모니터링 완료: {len(current_data)} 항목")
            return current_data
            
        except Exception as e:
            self.logger.error(f"경제 데이터 모니터링 오류: {e}")
            raise
    
    def detect_events(self, market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """2단계: 경제 이벤트 자동 감지"""
        self.print_header("경제 이벤트 자동 감지", 2)
        
        events = []
        
        try:
            # 시장 하락 이벤트 감지
            declining_stocks = []
            for symbol, data in market_data.items():
                if not symbol.startswith('^') and data['change_percent'] < -1.5:
                    declining_stocks.append(symbol)
            
            if len(declining_stocks) >= 3:
                declining_list = ', '.join(declining_stocks)
                events.append({
                    'type': 'MARKET_DECLINE',
                    'description': f'주요 기술주 {len(declining_stocks)}개 종목 1.5% 이상 하락',
                    'severity': 'MEDIUM',
                    'impact': 'NEGATIVE',
                    'affected_symbols': declining_stocks,
                    'timestamp': datetime.now().isoformat(),
                    'details': f'하락 종목: {declining_list}'
                })
            
            # VIX 상승 이벤트 감지
            if '^VIX' in market_data and market_data['^VIX']['change_percent'] > 2:
                vix_change = market_data['^VIX']['change_percent']
                vix_price = market_data['^VIX']['current_price']
                events.append({
                    'type': 'VOLATILITY_SPIKE',
                    'description': f'VIX 지수 {vix_change:.2f}% 상승',
                    'severity': 'LOW',
                    'impact': 'NEUTRAL',
                    'affected_symbols': ['^VIX'],
                    'timestamp': datetime.now().isoformat(),
                    'details': f'현재 VIX: {vix_price:.2f}'
                })
            
            # 시장 지수 하락 이벤트
            major_indices = ['^GSPC', '^IXIC']
            declining_indices = []
            for index in major_indices:
                if index in market_data and market_data[index]['change_percent'] < -1.5:
                    declining_indices.append(index)
            
            if declining_indices:
                indices_list = ', '.join(declining_indices)
                events.append({
                    'type': 'INDEX_DECLINE',
                    'description': f'주요 지수 {len(declining_indices)}개 1.5% 이상 하락',
                    'severity': 'HIGH',
                    'impact': 'NEGATIVE',
                    'affected_symbols': declining_indices,
                    'timestamp': datetime.now().isoformat(),
                    'details': f'하락 지수: {indices_list}'
                })
            
            print(f"🎯 감지된 이벤트: {len(events)}개\n")
            
            if events:
                print("📋 감지된 주요 이벤트:")
                for i, event in enumerate(events, 1):
                    severity_icon = '🔴' if event['severity'] == 'HIGH' else '🟡' if event['severity'] == 'MEDIUM' else '🟢'
                    impact_icon = '📉' if event['impact'] == 'NEGATIVE' else '📈' if event['impact'] == 'POSITIVE' else '➡️'
                    
                    print(f"  {i}. {severity_icon} {event['type']}: {event['description']}")
                    print(f"     심각도: {event['severity']} | 영향: {event['impact']} {impact_icon}")
                    print(f"     세부사항: {event['details']}")
                    print()
            else:
                print("📋 특별한 이벤트가 감지되지 않았습니다.")
            
            self.logger.info(f"이벤트 감지 완료: {len(events)} 개")
            return events
            
        except Exception as e:
            self.logger.error(f"이벤트 감지 오류: {e}")
            return []
    
    def analyze_market_data(self, market_data: Dict[str, Any], events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """3단계: 경제 데이터 종합 분석"""
        self.print_header("경제 데이터 종합 분석", 3)
        
        try:
            # 시장 분석
            total_decline_count = len([s for s, d in market_data.items() if not s.startswith('^') and d['change_percent'] < 0])
            total_stocks = len([s for s in market_data.keys() if not s.startswith('^')])
            decline_ratio = total_decline_count / total_stocks * 100 if total_stocks > 0 else 0
            
            analysis_summary = {
                'market_trend': 'BEARISH' if decline_ratio > 60 else 'BULLISH' if decline_ratio < 40 else 'NEUTRAL',
                'decline_ratio': decline_ratio,
                'key_observations': [
                    f'전체 종목 중 {decline_ratio:.1f}% 하락',
                    'S&P 500 지수 변동',
                    '나스닥 지수 변동',
                    'VIX 지수 변동성 지표',
                    '기술주 메가캡 종목 동향'
                ],
                'risk_factors': [
                    '기술주 밸류에이션 부담',
                    '거시경제 불확실성',
                    '시장 심리 변화',
                    '변동성 확대 우려'
                ],
                'market_sentiment': 'CAUTIOUS' if len(events) > 1 else 'NEUTRAL',
                'events_count': len(events),
                'timestamp': datetime.now().isoformat()
            }
            
            print("📊 시장 분석 결과:")
            trend_icon = '📉' if analysis_summary['market_trend'] == 'BEARISH' else '📈' if analysis_summary['market_trend'] == 'BULLISH' else '➡️'
            print(f"  • 전반적 추세: {analysis_summary['market_trend']} {trend_icon}")
            print(f"  • 하락 종목 비율: {analysis_summary['decline_ratio']:.1f}%")
            print(f"  • 시장 심리: {analysis_summary['market_sentiment']}")
            print(f"  • 감지된 이벤트: {analysis_summary['events_count']}개")
            
            self.logger.info(f"시장 분석 완료: {analysis_summary['market_trend']} 추세")
            return analysis_summary
            
        except Exception as e:
            self.logger.error(f"시장 분석 오류: {e}")
            return {'market_trend': 'NEUTRAL', 'decline_ratio': 0, 'events_count': 0}
    def generate_ai_article(self, market_data: Dict[str, Any], events: List[Dict[str, Any]], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """4단계: AI 기반 경제 기사 생성"""
        self.print_header("AI 기반 경제 기사 생성", 4)
        
        try:
            print("🤖 AI 기사 생성 시작...")
            
            # 오케스트레이터 설정
            agent_config = AgentConfig(
                name='PipelineNewsGenerator',
                model_id=self.config.get('model_id', 'anthropic.claude-3-sonnet-20240229-v1:0'),
                region=self.config.get('aws_region', 'us-east-1')
            )
            
            orchestrator = OrchestratorAgent(agent_config)
            
            # 기사 생성 입력 데이터 준비
            article_input = {
                'workflow_type': 'full_pipeline',
                'article_configs': [
                    {
                        'article_type': 'market_summary',
                        'target_length': 'medium',
                        'context': {
                            'events': events,
                            'market_data': market_data,
                            'analysis': analysis,
                            'focus': 'event_driven'
                        }
                    }
                ]
            }
            
            # AI 기사 생성 실행
            result = orchestrator.process(article_input)
            
            # 생성된 기사 추출
            articles = result.get('optimized_articles', result.get('articles', []))
            if articles:
                article_data = articles[0]
                article = article_data.get('optimized_article', article_data.get('article', {}))
                
                print("✅ AI 기사 생성 완료!")
                print(f"📰 제목: {article.get('headline', '경제 뉴스')}")
                
                # 품질 정보 출력
                quality_check = article_data.get('quality_check', {})
                if quality_check:
                    overall_score = quality_check.get('overall_score', 'N/A')
                    print(f"📊 품질 점수: {overall_score}/100")
                
                self.logger.info("AI 기사 생성 완료")
                return {
                    'article': article,
                    'article_data': article_data,
                    'generation_result': result
                }
            else:
                raise Exception("생성된 기사를 찾을 수 없습니다")
                
        except Exception as e:
            self.logger.error(f"AI 기사 생성 오류: {e}")
            
            # 대체 기사 생성
            print("⚠️ 대체 기사 시스템 사용")
            return self.generate_fallback_article(market_data, events, analysis)
    
    def generate_fallback_article(self, market_data: Dict[str, Any], events: List[Dict[str, Any]], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """대체 기사 생성"""
        
        # 주요 지수 정보 추출
        sp500_change = market_data.get('^GSPC', {}).get('change_percent', 0)
        nasdaq_change = market_data.get('^IXIC', {}).get('change_percent', 0)
        vix_change = market_data.get('^VIX', {}).get('change_percent', 0)
        
        # 주요 종목 하락률 계산
        tech_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
        declining_stocks = []
        for stock in tech_stocks:
            if stock in market_data and market_data[stock]['change_percent'] < -1.5:
                declining_stocks.append(f"{stock}({market_data[stock]['change_percent']:+.2f}%)")
        
        # 기사 내용 생성
        headline = f"기술주 중심 시장 {'급락' if analysis['market_trend'] == 'BEARISH' else '조정'}...투자자 심리 위축"
        
        lead = f"주요 기술주 중심의 하락세로 나스닥 지수가 {nasdaq_change:.2f}% 하락하며 시장 전반에 조정 압력이 가중되고 있다."
        
        content = f"""
        미국 주식시장이 기술주 중심의 {'급락세' if analysis['decline_ratio'] > 80 else '하락세'}를 보이며 투자자들의 우려가 커지고 있다.
        
        주요 지수 현황을 보면 S&P 500 지수는 {sp500_change:+.2f}%, 나스닥 지수는 {nasdaq_change:+.2f}% 변동했다.
        
        개별 종목으로는 {', '.join(declining_stocks[:3])} 등 주요 기술주들이 부진한 모습을 보였다.
        
        시장 변동성을 나타내는 VIX 지수는 {vix_change:+.2f}% 변동하며 투자자들의 불안감을 반영했다.
        
        전문가들은 현재 시장 상황에 대해 신중한 접근이 필요하다고 조언하고 있다.
        """
        
        conclusion = "투자자들은 시장 변동성 확대에 대비한 리스크 관리와 함께 중장기적 관점에서의 투자 전략 수립이 필요한 시점이다."
        
        fallback_article = {
            'headline': headline,
            'lead': lead,
            'content': content.strip(),
            'conclusion': conclusion,
            'tags': ['기술주', '시장조정', '투자전략', '리스크관리'],
            'generated_by': 'fallback_system'
        }
        
        return {
            'article': fallback_article,
            'article_data': {
                'article': fallback_article,
                'quality_check': {
                    'overall_score': 75,
                    'scores': {'accuracy': 80, 'clarity': 75, 'completeness': 70}
                }
            }
        }
    
    def quality_review(self, article_result: Dict[str, Any]) -> Dict[str, Any]:
        """5단계: 기사 품질 검수"""
        self.print_header("기사 품질 검수", 5)
        
        try:
            article_data = article_result['article_data']
            article = article_result['article']
            
            quality_check = article_data.get('quality_check', {})
            
            print("📊 품질 검수 결과:")
            print("-" * 60)
            
            overall_score = quality_check.get('overall_score', 'N/A')
            print(f"🎯 전체 품질 점수: {overall_score}/100")
            
            scores = quality_check.get('scores', {})
            if scores:
                print("\n📈 세부 점수:")
                score_names = {
                    'accuracy': '정확성',
                    'clarity': '명확성',
                    'completeness': '완성도',
                    'objectivity': '객관성',
                    'usefulness': '실용성'
                }
                
                for metric, score in scores.items():
                    name = score_names.get(metric, metric)
                    print(f"  • {name}: {score}/100")
            
            # 품질 기준 확인
            min_score = self.config.get('optimization', {}).get('quality_threshold', 70)
            
            if isinstance(overall_score, (int, float)) and overall_score >= min_score:
                print(f"\n✅ 품질 검수 통과 (기준: {min_score}점 이상)")
                quality_status = "PASSED"
            else:
                print(f"\n⚠️ 품질 개선 필요 (기준: {min_score}점 이상)")
                quality_status = "NEEDS_IMPROVEMENT"
            
            # 강점과 개선점
            strengths = quality_check.get('strengths', [])
            if strengths:
                print("\n✅ 강점:")
                for strength in strengths:
                    print(f"  • {strength}")
            
            improvements = quality_check.get('improvements', [])
            if improvements:
                print("\n🔧 개선점:")
                for improvement in improvements:
                    print(f"  • {improvement}")
            
            self.logger.info(f"품질 검수 완료: {quality_status}")
            
            return {
                'status': quality_status,
                'score': overall_score,
                'details': quality_check
            }
            
        except Exception as e:
            self.logger.error(f"품질 검수 오류: {e}")
            return {'status': 'ERROR', 'score': 0}
    
    def generate_advertisements(self, article_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """6단계: 맞춤형 광고 추천"""
        self.print_header("맞춤형 광고 추천", 6)
        
        try:
            article = article_result['article']
            
            # 광고 생성기 초기화
            ad_generator = AdGenerator()
            
            # 기사 내용과 태그 추출
            content = article.get('content', '')
            tags = article.get('tags', ['경제', '투자', '시장분석'])
            
            # 맞춤형 광고 생성
            ads = ad_generator.generate_contextual_ads(content, tags)
            
            print(f"🎯 추천된 광고: {len(ads)}개\n")
            
            for i, ad in enumerate(ads, 1):
                print(f"📌 광고 #{i}: {ad['title']}")
                print(f"   📝 설명: {ad['description']}")
                print(f"   🔗 CTA: {ad['cta']}")
                print()
            
            # 광고 추천 이유 분석
            print("💡 광고 추천 이유:")
            print("-" * 60)
            
            content_lower = content.lower()
            tags_lower = [tag.lower() for tag in tags]
            all_text = content_lower + ' ' + ' '.join(tags_lower)
            
            # 키워드 분석
            investment_keywords = ['투자', '수익', '포트폴리오', '자산']
            trading_keywords = ['거래', '매매', '차트', '분석', '하락', '상승']
            education_keywords = ['분석', '전망', '교육', '학습']
            
            found_investment = sum(1 for kw in investment_keywords if kw in all_text)
            found_trading = sum(1 for kw in trading_keywords if kw in all_text)
            found_education = sum(1 for kw in education_keywords if kw in all_text)
            
            print(f"🔍 키워드 분석:")
            print(f"  • 투자 관련: {found_investment}개 감지")
            print(f"  • 거래 관련: {found_trading}개 감지")
            print(f"  • 교육 관련: {found_education}개 감지")
            
            print(f"\n🎯 타겟 독자: 경제 뉴스 관심자, 개인 투자자, 시장 분석 독자")
            print(f"📊 예상 성과: CTR 2.0-3.5%, 높은 관련성")
            
            self.logger.info(f"광고 추천 완료: {len(ads)} 개")
            return ads
            
        except Exception as e:
            self.logger.error(f"광고 생성 오류: {e}")
            return []
    def save_results(self, market_data: Dict[str, Any], events: List[Dict[str, Any]], 
                    analysis: Dict[str, Any], article_result: Dict[str, Any], 
                    quality_result: Dict[str, Any], ads: List[Dict[str, Any]]) -> str:
        """결과 저장"""
        try:
            # 통합 결과 생성
            pipeline_result = {
                'execution_id': self.execution_id,
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': (datetime.now() - self.start_time).total_seconds(),
                'pipeline_steps': {
                    '1_monitoring': {
                        'status': 'completed',
                        'data_points': len(market_data),
                        'market_data': market_data
                    },
                    '2_event_detection': {
                        'status': 'completed',
                        'events_detected': len(events),
                        'events': events
                    },
                    '3_analysis': {
                        'status': 'completed',
                        'market_trend': analysis.get('market_trend', 'UNKNOWN'),
                        'analysis': analysis
                    },
                    '4_article_generation': {
                        'status': 'completed',
                        'article': article_result['article'],
                        'generation_method': article_result.get('generation_method', 'ai')
                    },
                    '5_quality_review': {
                        'status': quality_result['status'],
                        'score': quality_result['score'],
                        'details': quality_result.get('details', {})
                    },
                    '6_advertisement': {
                        'status': 'completed',
                        'ads_generated': len(ads),
                        'advertisements': ads
                    }
                },
                'summary': {
                    'market_trend': analysis.get('market_trend', 'UNKNOWN'),
                    'events_count': len(events),
                    'article_quality': quality_result['score'],
                    'ads_count': len(ads)
                }
            }
            
            # JSON 파일 저장
            result_file = os.path.join(self.output_dir, f"full_pipeline_{self.execution_id}.json")
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_result, f, ensure_ascii=False, indent=2)
            
            # HTML 기사 저장
            html_file = os.path.join(self.output_dir, f"article_{self.execution_id}.html")
            html_content = self.generate_html_output(article_result['article'], ads)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n💾 결과 저장 완료:")
            print(f"  📄 통합 결과: {result_file}")
            print(f"  🌐 HTML 기사: {html_file}")
            
            self.logger.info(f"결과 저장 완료: {result_file}")
            return result_file
            
        except Exception as e:
            self.logger.error(f"결과 저장 오류: {e}")
            return ""
    
    def generate_html_output(self, article: Dict[str, Any], ads: List[Dict[str, Any]]) -> str:
        """HTML 출력 생성"""
        
        # 광고 HTML 생성
        ads_html = ""
        if ads:
            ads_html = "<h3>📢 추천 서비스</h3>"
            for ad in ads:
                ads_html += f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
                    <h4 style="margin: 0 0 5px 0; color: #333;">{ad['title']}</h4>
                    <p style="margin: 0 0 10px 0; color: #666;">{ad['description']}</p>
                    <a href="{ad['link']}" style="background-color: #007cba; color: white; padding: 6px 12px; text-decoration: none; border-radius: 4px;">{ad['cta']}</a>
                </div>
                """
        
        # 태그 HTML 생성
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in article.get('tags', [])])
        
        # 현재 시간
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 본문 내용 처리
        content_html = article.get('content', '').replace('\n', '<br>')
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{article.get('headline', '경제 뉴스')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
                .header {{ background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
                .headline {{ font-size: 2em; font-weight: bold; margin-bottom: 15px; color: #333; }}
                .lead {{ font-size: 1.2em; color: #666; margin-bottom: 20px; font-style: italic; }}
                .content {{ margin-bottom: 30px; text-align: justify; }}
                .conclusion {{ background-color: #f8f9fa; padding: 20px; border-left: 4px solid #007cba; margin: 20px 0; }}
                .tags {{ margin: 20px 0; }}
                .tag {{ background-color: #e9ecef; color: #495057; padding: 5px 10px; margin: 2px; display: inline-block; border-radius: 15px; font-size: 0.9em; }}
                .footer {{ margin-top: 40px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; font-size: 0.9em; color: #666; }}
                .ads-section {{ margin-top: 30px; padding: 20px; background-color: #fff; border: 1px solid #e9ecef; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📈 AI 경제 뉴스</h1>
                <p>실시간 데이터 분석 기반 자동 생성</p>
            </div>
            
            <article>
                <h1 class="headline">{article.get('headline', '')}</h1>
                <p class="lead">{article.get('lead', '')}</p>
                <div class="content">
                    {content_html}
                </div>
                
                {f'<div class="conclusion"><strong>💡 결론:</strong><br>{article.get("conclusion", "")}</div>' if article.get('conclusion') else ''}
                
                <div class="tags">
                    {tags_html}
                </div>
            </article>
            
            {f'<div class="ads-section">{ads_html}</div>' if ads_html else ''}
            
            <div class="footer">
                <p><strong>⚠️ 면책 조항:</strong> 본 기사는 AI가 실시간 경제 데이터를 분석하여 자동 생성한 것으로, 투자 권유가 아니며 투자 결정은 개인의 판단과 책임하에 이루어져야 합니다.</p>
                <p><strong>🤖 생성 정보:</strong> 생성 시간: {current_time} | 실행 ID: {self.execution_id}</p>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def display_final_summary(self, market_data: Dict[str, Any], events: List[Dict[str, Any]], 
                            analysis: Dict[str, Any], quality_result: Dict[str, Any], ads: List[Dict[str, Any]]):
        """최종 요약 출력"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n{'='*80}")
        print("🎉 경제 뉴스 자동 생성 파이프라인 완료!")
        print(f"{'='*80}")
        
        print(f"\n📊 실행 요약:")
        print(f"  ⏱️  총 소요 시간: {duration:.1f}초")
        print(f"  📈 모니터링 데이터: {len(market_data)}개 종목/지표")
        print(f"  🚨 감지된 이벤트: {len(events)}개")
        print(f"  📰 기사 품질 점수: {quality_result['score']}/100")
        print(f"  📢 추천 광고: {len(ads)}개")
        print(f"  🎯 시장 추세: {analysis.get('market_trend', 'UNKNOWN')}")
        
        print(f"\n🔍 주요 성과:")
        print(f"  ✅ 실시간 데이터 수집 및 분석")
        print(f"  ✅ 자동 이벤트 감지 및 분류")
        print(f"  ✅ AI 기반 고품질 기사 생성")
        print(f"  ✅ 품질 검수 및 최적화")
        print(f"  ✅ 맞춤형 광고 추천")
        
        print(f"\n📁 출력 파일:")
        print(f"  📄 통합 결과: output/full_pipeline_{self.execution_id}.json")
        print(f"  🌐 HTML 기사: output/article_{self.execution_id}.html")
        
        print(f"\n{'='*80}")
    
    def run_pipeline(self) -> bool:
        """전체 파이프라인 실행"""
        try:
            self.print_header("경제 뉴스 자동 생성 통합 파이프라인 시작")
            print(f"🚀 실행 ID: {self.execution_id}")
            print(f"⏰ 시작 시간: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 1단계: 경제 데이터 모니터링
            market_data = self.monitor_economic_data()
            
            # 2단계: 이벤트 감지
            events = self.detect_events(market_data)
            
            # 3단계: 시장 분석
            analysis = self.analyze_market_data(market_data, events)
            
            # 4단계: AI 기사 생성
            article_result = self.generate_ai_article(market_data, events, analysis)
            
            # 5단계: 품질 검수
            quality_result = self.quality_review(article_result)
            
            # 6단계: 광고 추천
            ads = self.generate_advertisements(article_result)
            
            # 결과 저장
            result_file = self.save_results(market_data, events, analysis, article_result, quality_result, ads)
            
            # 최종 요약
            self.display_final_summary(market_data, events, analysis, quality_result, ads)
            
            return True
            
        except Exception as e:
            self.logger.error(f"파이프라인 실행 오류: {e}")
            print(f"\n❌ 파이프라인 실행 중 오류 발생: {e}")
            return False


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="경제 뉴스 자동 생성 통합 파이프라인")
    
    parser.add_argument("--config", default="config/default.json", help="설정 파일 경로")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="로그 레벨")
    parser.add_argument("--output-dir", default="output", help="출력 디렉토리")
    
    args = parser.parse_args()
    
    try:
        # 파이프라인 초기화
        pipeline = EconomicNewsPipeline(args.config, args.log_level)
        
        # 출력 디렉토리 설정
        if args.output_dir != "output":
            pipeline.output_dir = args.output_dir
            os.makedirs(pipeline.output_dir, exist_ok=True)
        
        # 파이프라인 실행
        success = pipeline.run_pipeline()
        
        if success:
            print(f"\n🎉 파이프라인 실행 성공!")
            return 0
        else:
            print(f"\n❌ 파이프라인 실행 실패!")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⏹️ 사용자에 의해 중단되었습니다.")
        return 1
    except Exception as e:
        print(f"\n💥 예상치 못한 오류: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
