#!/usr/bin/env python3
"""
데이터 분석 에이전트
이벤트 관련 데이터를 분석하고 차트를 생성
"""

import os
import sys
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json


import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 사용 안함
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

class DataAnalysisAgent:
    """데이터 분석 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.logger = logging.getLogger(__name__)
        
        # 출력 디렉토리 설정
        self.charts_dir = "output/charts"
        os.makedirs(self.charts_dir, exist_ok=True)
        
        self.logger.info("✅ 데이터 분석 에이전트 초기화 완료")
    
    async def analyze_event_data(self, event) -> Dict[str, Any]:
        """이벤트 관련 데이터 분석"""
        
        self.logger.info(f"📊 {event.symbol} 데이터 분석 시작")
        
        try:
            # 1. 기본 데이터 수집
            ticker = yf.Ticker(event.symbol)
            
            # 다양한 기간의 데이터 수집
            data_1d = ticker.history(period="1d", interval="5m")  # 1일 5분봉
            data_5d = ticker.history(period="5d", interval="1h")   # 5일 1시간봉
            data_1m = ticker.history(period="1mo", interval="1d")  # 1개월 일봉
            data_3m = ticker.history(period="3mo", interval="1d")  # 3개월 일봉
            
            # 2. 기술적 지표 계산
            technical_indicators = self._calculate_technical_indicators(data_1m)
            
            # 3. 통계 분석
            statistics = self._calculate_statistics(data_1m, data_5d)
            
            # 4. 시장 비교 분석
            market_comparison = await self._compare_with_market(event.symbol, data_1m)
            
            # 5. 뉴스 및 이벤트 영향 분석
            event_impact = self._analyze_event_impact(event, data_1d, data_5d)
            
            # 6. 예측 및 전망
            forecast = self._generate_forecast(data_1m, technical_indicators)
            
            # 분석 결과 종합
            analysis_result = {
                'symbol': event.symbol,
                'analysis_timestamp': datetime.now().isoformat(),
                'raw_data': {
                    'current_price': float(data_1m['Close'].iloc[-1]),
                    'previous_close': float(data_1m['Close'].iloc[-2]),
                    'volume': int(data_1m['Volume'].iloc[-1]),
                    'high_52w': float(data_1m['High'].rolling(252).max().iloc[-1]),
                    'low_52w': float(data_1m['Low'].rolling(252).min().iloc[-1])
                },
                'technical_indicators': technical_indicators,
                'statistics': statistics,
                'market_comparison': market_comparison,
                'event_impact': event_impact,
                'forecast': forecast,
                'data_quality': {
                    'data_points_1d': len(data_1d),
                    'data_points_5d': len(data_5d),
                    'data_points_1m': len(data_1m),
                    'data_completeness': self._assess_data_quality(data_1m)
                }
            }
            
            self.logger.info(f"✅ {event.symbol} 데이터 분석 완료")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"❌ 데이터 분석 실패: {e}")
            return {
                'symbol': event.symbol,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    async def generate_charts(self, event, analysis_data: Dict[str, Any]) -> List[str]:
        """차트 생성"""
        
        self.logger.info(f"📈 {event.symbol} 차트 생성 시작")
        
        chart_paths = []
        
        try:
            # 데이터 재수집 (차트용)
            ticker = yf.Ticker(event.symbol)
            data_1m = ticker.history(period="1mo", interval="1d")
            data_5d = ticker.history(period="5d", interval="1h")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 1. 가격 및 거래량 차트
            price_chart_path = await self._create_price_volume_chart(
                event.symbol, data_1m, f"{event.symbol}_price_volume_{timestamp}.html"
            )
            chart_paths.append(price_chart_path)
            
            # 2. 기술적 지표 차트
            technical_chart_path = await self._create_technical_indicators_chart(
                event.symbol, data_1m, analysis_data.get('technical_indicators', {}),
                f"{event.symbol}_technical_{timestamp}.html"
            )
            chart_paths.append(technical_chart_path)
            
            # 3. 최근 5일 상세 차트
            recent_chart_path = await self._create_recent_detail_chart(
                event.symbol, data_5d, f"{event.symbol}_recent_{timestamp}.html"
            )
            chart_paths.append(recent_chart_path)
            
            # 4. 시장 비교 차트
            if analysis_data.get('market_comparison'):
                comparison_chart_path = await self._create_market_comparison_chart(
                    event.symbol, analysis_data['market_comparison'],
                    f"{event.symbol}_comparison_{timestamp}.html"
                )
                chart_paths.append(comparison_chart_path)
            
            self.logger.info(f"✅ {event.symbol} 차트 생성 완료: {len(chart_paths)}개")
            return chart_paths
            
        except Exception as e:
            self.logger.error(f"❌ 차트 생성 실패: {e}")
            return []
    
    def _calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """기술적 지표 계산"""
        
        try:
            close = data['Close']
            high = data['High']
            low = data['Low']
            volume = data['Volume']
            
            # 이동평균
            sma_20 = close.rolling(20).mean()
            sma_50 = close.rolling(50).mean()
            ema_12 = close.ewm(span=12).mean()
            ema_26 = close.ewm(span=26).mean()
            
            # MACD
            macd = ema_12 - ema_26
            macd_signal = macd.ewm(span=9).mean()
            macd_histogram = macd - macd_signal
            
            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # 볼린저 밴드
            bb_middle = close.rolling(20).mean()
            bb_std = close.rolling(20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            return {
                'sma_20': float(sma_20.iloc[-1]) if not pd.isna(sma_20.iloc[-1]) else None,
                'sma_50': float(sma_50.iloc[-1]) if not pd.isna(sma_50.iloc[-1]) else None,
                'macd': float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else None,
                'macd_signal': float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else None,
                'rsi': float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None,
                'bb_upper': float(bb_upper.iloc[-1]) if not pd.isna(bb_upper.iloc[-1]) else None,
                'bb_lower': float(bb_lower.iloc[-1]) if not pd.isna(bb_lower.iloc[-1]) else None,
                'current_price': float(close.iloc[-1])
            }
            
        except Exception as e:
            self.logger.error(f"기술적 지표 계산 실패: {e}")
            return {}
    
    def _calculate_statistics(self, data_1m: pd.DataFrame, data_5d: pd.DataFrame) -> Dict[str, Any]:
        """통계 분석"""
        
        try:
            close_1m = data_1m['Close']
            volume_1m = data_1m['Volume']
            
            # 변동성 계산
            daily_returns = close_1m.pct_change().dropna()
            volatility_1m = daily_returns.std() * np.sqrt(252) * 100  # 연환산 변동성
            
            # 거래량 분석
            avg_volume_20d = volume_1m.rolling(20).mean().iloc[-1]
            current_volume = volume_1m.iloc[-1]
            volume_ratio = current_volume / avg_volume_20d if avg_volume_20d > 0 else 1
            
            # 가격 통계
            price_stats = {
                'mean_1m': float(close_1m.mean()),
                'std_1m': float(close_1m.std()),
                'min_1m': float(close_1m.min()),
                'max_1m': float(close_1m.max()),
                'current_vs_mean': float((close_1m.iloc[-1] / close_1m.mean() - 1) * 100)
            }
            
            return {
                'volatility_annualized': float(volatility_1m),
                'volume_ratio': float(volume_ratio),
                'price_statistics': price_stats,
                'trend_strength': self._calculate_trend_strength(close_1m)
            }
            
        except Exception as e:
            self.logger.error(f"통계 계산 실패: {e}")
            return {}
    
    async def _compare_with_market(self, symbol: str, data: pd.DataFrame) -> Dict[str, Any]:
        """시장 비교 분석 (오류 수정 버전)"""
        
        try:
            # S&P 500과 비교
            spy = yf.Ticker("SPY")
            spy_data = spy.history(period="1mo", interval="1d")
            
            if len(spy_data) == 0:
                self.logger.warning("SPY 데이터를 가져올 수 없습니다")
                return self._get_default_market_comparison()
            
            # 수익률 계산
            symbol_returns = data['Close'].pct_change().dropna()
            spy_returns = spy_data['Close'].pct_change().dropna()
            
            # 데이터 길이 확인
            if len(symbol_returns) == 0 or len(spy_returns) == 0:
                self.logger.warning("수익률 데이터가 비어있습니다")
                return self._get_default_market_comparison()
            
            # 베타 계산 (안전한 방식)
            try:
                # 공통 날짜 인덱스 찾기
                common_dates = symbol_returns.index.intersection(spy_returns.index)
                
                if len(common_dates) < 2:
                    self.logger.warning("공통 날짜가 충분하지 않습니다")
                    # 길이 맞추기 (더 짧은 것에 맞춤)
                    min_length = min(len(symbol_returns), len(spy_returns))
                    if min_length < 2:
                        return self._get_default_market_comparison()
                    
                    # 최근 데이터로 정렬
                    symbol_values = symbol_returns.iloc[-min_length:].values
                    spy_values = spy_returns.iloc[-min_length:].values
                else:
                    # 공통 날짜로 정렬
                    symbol_values = symbol_returns.loc[common_dates].values
                    spy_values = spy_returns.loc[common_dates].values
                
                # 길이 강제 확인 및 맞춤
                if len(symbol_values) != len(spy_values):
                    min_len = min(len(symbol_values), len(spy_values))
                    symbol_values = symbol_values[:min_len]
                    spy_values = spy_values[:min_len]
                
                # NaN 값 제거 (동시에)
                valid_mask = ~(np.isnan(symbol_values) | np.isnan(spy_values))
                symbol_clean = symbol_values[valid_mask]
                spy_clean = spy_values[valid_mask]
                
                # 최종 길이 확인
                if len(symbol_clean) != len(spy_clean):
                    self.logger.error(f"NaN 제거 후에도 길이 불일치: {len(symbol_clean)} vs {len(spy_clean)}")
                    return self._get_default_market_comparison()
                
                if len(symbol_clean) < 2:
                    self.logger.warning("유효한 데이터가 충분하지 않습니다")
                    return self._get_default_market_comparison()
                
                # 통계 계산 (더 안전한 방식)
                try:
                    # 베타 계산
                    spy_variance = np.var(spy_clean, ddof=1)
                    if spy_variance > 0:
                        covariance = np.cov(symbol_clean, spy_clean, ddof=1)[0, 1]
                        beta = covariance / spy_variance
                    else:
                        beta = 1.0
                    
                    # 상관관계 계산
                    if len(symbol_clean) > 1 and np.std(symbol_clean) > 0 and np.std(spy_clean) > 0:
                        correlation = np.corrcoef(symbol_clean, spy_clean)[0, 1]
                    else:
                        correlation = 0.0
                    
                    # 상대 성과 계산
                    symbol_total_return = np.sum(symbol_clean)
                    spy_total_return = np.sum(spy_clean)
                    relative_performance = (symbol_total_return - spy_total_return) * 100
                    
                    return {
                        'beta': float(beta) if not np.isnan(beta) else 1.0,
                        'correlation_with_spy': float(correlation) if not np.isnan(correlation) else 0.0,
                        'relative_performance_1m': float(relative_performance) if not np.isnan(relative_performance) else 0.0,
                        'market_benchmark': 'SPY',
                        'data_points_used': len(symbol_clean)
                    }
                    
                except Exception as stat_error:
                    self.logger.error(f"통계 계산 실패: {stat_error}")
                    return self._get_default_market_comparison()
                
            except Exception as calc_error:
                self.logger.error(f"베타/상관관계 계산 실패: {calc_error}")
                return self._get_default_market_comparison()
            
        except Exception as e:
            self.logger.error(f"시장 비교 분석 실패: {e}")
            return self._get_default_market_comparison()
    
    def _get_default_market_comparison(self) -> Dict[str, Any]:
        """기본 시장 비교 결과 반환"""
        return {
            'beta': 1.0,
            'correlation_with_spy': 0.0,
            'relative_performance_1m': 0.0,
            'market_benchmark': 'SPY',
            'error': 'calculation_failed'
        }
    
    def _analyze_event_impact(self, event, data_1d: pd.DataFrame, data_5d: pd.DataFrame) -> Dict[str, Any]:
        """이벤트 영향 분석"""
        
        try:
            # 이벤트 전후 비교
            if len(data_1d) > 0:
                recent_volatility = data_1d['Close'].pct_change().std() * 100
                recent_volume_avg = data_1d['Volume'].mean()
            else:
                recent_volatility = 0
                recent_volume_avg = 0
            
            if len(data_5d) > 0:
                baseline_volatility = data_5d['Close'].pct_change().std() * 100
                baseline_volume_avg = data_5d['Volume'].mean()
            else:
                baseline_volatility = recent_volatility
                baseline_volume_avg = recent_volume_avg
            
            return {
                'event_type': event.event_type,
                'event_severity': event.severity.value,
                'volatility_increase': float(recent_volatility - baseline_volatility),
                'volume_increase': float((recent_volume_avg / baseline_volume_avg - 1) * 100) if baseline_volume_avg > 0 else 0,
                'price_impact': float(event.change_percent),
                'impact_assessment': self._assess_impact_level(event.change_percent, recent_volatility)
            }
            
        except Exception as e:
            self.logger.error(f"이벤트 영향 분석 실패: {e}")
            return {}
    
    def _generate_forecast(self, data: pd.DataFrame, technical_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """예측 및 전망 생성"""
        
        try:
            close = data['Close']
            current_price = close.iloc[-1]
            
            # 단순 기술적 분석 기반 전망
            rsi = technical_indicators.get('rsi', 50)
            macd = technical_indicators.get('macd', 0)
            
            # 전망 점수 계산 (-100 ~ +100)
            forecast_score = 0
            
            # RSI 기반
            if rsi > 70:
                forecast_score -= 30  # 과매수
            elif rsi < 30:
                forecast_score += 30  # 과매도
            
            # MACD 기반
            if macd > 0:
                forecast_score += 20
            else:
                forecast_score -= 20
            
            # 추세 기반
            sma_20 = technical_indicators.get('sma_20')
            if sma_20 and current_price > sma_20:
                forecast_score += 10
            elif sma_20 and current_price < sma_20:
                forecast_score -= 10
            
            # 전망 레벨 결정
            if forecast_score > 30:
                outlook = "강세"
            elif forecast_score > 10:
                outlook = "약간 강세"
            elif forecast_score > -10:
                outlook = "중립"
            elif forecast_score > -30:
                outlook = "약간 약세"
            else:
                outlook = "약세"
            
            return {
                'forecast_score': int(forecast_score),
                'outlook': outlook,
                'confidence_level': min(abs(forecast_score) / 50 * 100, 100),
                'key_levels': {
                    'support': float(technical_indicators.get('bb_lower', current_price * 0.95)),
                    'resistance': float(technical_indicators.get('bb_upper', current_price * 1.05))
                }
            }
            
        except Exception as e:
            self.logger.error(f"예측 생성 실패: {e}")
            return {}
    
    async def _create_price_volume_chart(self, symbol: str, data: pd.DataFrame, filename: str) -> str:
        """Price and Volume Chart Generation"""
        
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f'{symbol} Price', 'Volume'),
                row_width=[0.7, 0.3]
            )
            
            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # Volume chart
            colors = ['red' if close < open else 'green' 
                     for close, open in zip(data['Close'], data['Open'])]
            
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name='Volume',
                    marker_color=colors
                ),
                row=2, col=1
            )
            
            # Layout update
            fig.update_layout(
                title=f'{symbol} Price and Volume Analysis',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                yaxis2_title='Volume',
                template='plotly_white',
                height=600,
                showlegend=False
            )
            
            # Save chart
            output_dir = "output/charts"
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            fig.write_html(filepath)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Price volume chart creation failed: {e}")
            return ""
            
            # 거래량 차트
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name='거래량',
                    marker_color='rgba(158,202,225,0.8)'
                ),
                row=2, col=1
            )
            
            # 레이아웃 설정
            fig.update_layout(
                title=f'{symbol} 가격 및 거래량 분석',
                xaxis_rangeslider_visible=False,
                height=600
            )
            
            # 파일 저장
            filepath = os.path.join(self.charts_dir, filename)
            fig.write_html(filepath)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"가격 차트 생성 실패: {e}")
            return ""
    
    async def _create_technical_indicators_chart(self, symbol: str, data: pd.DataFrame, 
                                               indicators: Dict[str, Any], filename: str) -> str:
        """기술적 지표 차트 생성"""
        
        try:
            fig = make_subplots(
                rows=3, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f'{symbol} 가격 + 이동평균', 'MACD', 'RSI')
            )
            
            # 가격 + 이동평균
            fig.add_trace(
                go.Scatter(x=data.index, y=data['Close'], name='종가', line=dict(color='blue')),
                row=1, col=1
            )
            
            # 이동평균 추가 (계산)
            sma_20 = data['Close'].rolling(20).mean()
            sma_50 = data['Close'].rolling(50).mean()
            
            fig.add_trace(
                go.Scatter(x=data.index, y=sma_20, name='SMA 20', line=dict(color='orange')),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=data.index, y=sma_50, name='SMA 50', line=dict(color='red')),
                row=1, col=1
            )
            
            # MACD (간단 계산)
            ema_12 = data['Close'].ewm(span=12).mean()
            ema_26 = data['Close'].ewm(span=26).mean()
            macd = ema_12 - ema_26
            macd_signal = macd.ewm(span=9).mean()
            
            fig.add_trace(
                go.Scatter(x=data.index, y=macd, name='MACD', line=dict(color='blue')),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=data.index, y=macd_signal, name='Signal', line=dict(color='red')),
                row=2, col=1
            )
            
            # RSI (간단 계산)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            fig.add_trace(
                go.Scatter(x=data.index, y=rsi, name='RSI', line=dict(color='purple')),
                row=3, col=1
            )
            
            # RSI 기준선
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
            
            fig.update_layout(
                title=f'{symbol} 기술적 지표 분석',
                height=800
            )
            
            # 파일 저장
            filepath = os.path.join(self.charts_dir, filename)
            fig.write_html(filepath)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"기술적 지표 차트 생성 실패: {e}")
            return ""
    
    async def _create_recent_detail_chart(self, symbol: str, data: pd.DataFrame, filename: str) -> str:
        """최근 상세 차트 생성"""
        
        try:
            fig = go.Figure()
            
            # 라인 차트
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines+markers',
                    name='종가',
                    line=dict(color='blue', width=2),
                    marker=dict(size=4)
                )
            )
            
            fig.update_layout(
                title=f'{symbol} 최근 5일 상세 차트',
                xaxis_title='시간',
                yaxis_title='가격',
                height=400
            )
            
            # 파일 저장
            filepath = os.path.join(self.charts_dir, filename)
            fig.write_html(filepath)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"상세 차트 생성 실패: {e}")
            return ""
    
    async def _create_market_comparison_chart(self, symbol: str, comparison_data: Dict[str, Any], filename: str) -> str:
        """시장 비교 차트 생성"""
        
        try:
            # 간단한 비교 차트 (실제로는 더 복잡한 구현 필요)
            fig = go.Figure()
            
            # 베타와 상관관계 표시
            fig.add_trace(
                go.Bar(
                    x=['베타', '상관관계', '상대성과'],
                    y=[
                        comparison_data.get('beta', 1),
                        comparison_data.get('correlation_with_spy', 0),
                        comparison_data.get('relative_performance_1m', 0)
                    ],
                    name='시장 비교 지표'
                )
            )
            
            fig.update_layout(
                title=f'{symbol} vs 시장 비교',
                yaxis_title='값',
                height=400
            )
            
            # 파일 저장
            filepath = os.path.join(self.charts_dir, filename)
            fig.write_html(filepath)
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"시장 비교 차트 생성 실패: {e}")
            return ""
    
    def _calculate_trend_strength(self, close_prices: pd.Series) -> float:
        """추세 강도 계산"""
        
        try:
            # 선형 회귀를 통한 추세 강도 계산
            x = np.arange(len(close_prices))
            y = close_prices.values
            
            # 기울기 계산
            slope = np.polyfit(x, y, 1)[0]
            
            # 정규화 (0-100 스케일)
            trend_strength = min(abs(slope) / close_prices.mean() * 1000, 100)
            
            return float(trend_strength)
            
        except Exception as e:
            self.logger.error(f"추세 강도 계산 실패: {e}")
            return 0.0
    
    def _assess_data_quality(self, data: pd.DataFrame) -> float:
        """데이터 품질 평가"""
        
        try:
            # 결측값 비율
            missing_ratio = data.isnull().sum().sum() / (len(data) * len(data.columns))
            
            # 품질 점수 (0-100)
            quality_score = (1 - missing_ratio) * 100
            
            return float(quality_score)
            
        except Exception as e:
            self.logger.error(f"데이터 품질 평가 실패: {e}")
            return 0.0
    
    def _assess_impact_level(self, change_percent: float, volatility: float) -> str:
        """영향 수준 평가"""
        
        abs_change = abs(change_percent)
        
        if abs_change > 10 or volatility > 30:
            return "매우 높음"
        elif abs_change > 5 or volatility > 20:
            return "높음"
        elif abs_change > 2 or volatility > 15:
            return "보통"
        else:
            return "낮음"
