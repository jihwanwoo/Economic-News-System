"""
경제 데이터 모니터링 설정
"""

# 모니터링할 경제 지표 설정
ECONOMIC_INDICATORS = {
    'stock_indices': {
        'KOSPI': {
            'symbol': '^KS11',
            'name': '코스피',
            'threshold_surge': 2.0,  # 2% 이상 상승
            'threshold_drop': -2.0,  # 2% 이상 하락
            'volatility_threshold': 3.0  # 3% 이상 변동성
        },
        'KOSDAQ': {
            'symbol': '^KQ11',
            'name': '코스닥',
            'threshold_surge': 3.0,
            'threshold_drop': -3.0,
            'volatility_threshold': 4.0
        },
        'S&P500': {
            'symbol': '^GSPC',
            'name': 'S&P 500',
            'threshold_surge': 1.5,
            'threshold_drop': -1.5,
            'volatility_threshold': 2.5
        },
        'NASDAQ': {
            'symbol': '^IXIC',
            'name': '나스닥',
            'threshold_surge': 2.0,
            'threshold_drop': -2.0,
            'volatility_threshold': 3.0
        }
    },
    'currencies': {
        'USD_KRW': {
            'symbol': 'USDKRW=X',
            'name': '달러/원',
            'threshold_surge': 1.0,
            'threshold_drop': -1.0,
            'volatility_threshold': 1.5
        },
        'EUR_KRW': {
            'symbol': 'EURKRW=X',
            'name': '유로/원',
            'threshold_surge': 1.0,
            'threshold_drop': -1.0,
            'volatility_threshold': 1.5
        }
    },
    'commodities': {
        'CRUDE_OIL': {
            'symbol': 'CL=F',
            'name': '원유',
            'threshold_surge': 3.0,
            'threshold_drop': -3.0,
            'volatility_threshold': 4.0
        },
        'GOLD': {
            'symbol': 'GC=F',
            'name': '금',
            'threshold_surge': 2.0,
            'threshold_drop': -2.0,
            'volatility_threshold': 2.5
        }
    }
}

# 모니터링 설정
MONITORING_CONFIG = {
    'check_interval': 60,  # 60초마다 체크
    'data_retention_days': 30,  # 30일간 데이터 보관
    'alert_cooldown': 300,  # 5분간 동일 알림 방지
    'batch_size': 10,  # 한 번에 처리할 지표 수
}

# 이벤트 심각도 계산 가중치
SEVERITY_WEIGHTS = {
    'price_change_magnitude': 0.4,  # 가격 변동 크기
    'volume_spike': 0.3,  # 거래량 급증
    'market_correlation': 0.2,  # 시장 연관성
    'historical_significance': 0.1  # 역사적 중요도
}

# 데이터 소스 설정
DATA_SOURCES = {
    'yahoo_finance': {
        'enabled': True,
        'api_key': None,  # Yahoo Finance는 무료
        'rate_limit': 2000  # 시간당 요청 제한
    },
    'alpha_vantage': {
        'enabled': False,
        'api_key': 'YOUR_API_KEY',
        'rate_limit': 500
    },
    'fred': {  # Federal Reserve Economic Data
        'enabled': False,
        'api_key': 'YOUR_FRED_API_KEY',
        'rate_limit': 120
    }
}
