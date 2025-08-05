# 🤖 경제 뉴스 자동 생성 시스템

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AWS](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![Slack](https://img.shields.io/badge/Slack-Integration-4A154B.svg)](https://slack.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

AWS Bedrock과 고도화된 Agent 시스템을 활용한 지능형 경제 기사 자동 생성 및 실시간 알림 시스템입니다.

## 🚀 주요 기능

### 📊 **고도화된 이벤트 감지**
- **기술적 분석**: RSI, MACD, 볼린저 밴드 등 13가지 지표
- **감정 분석**: 뉴스 피드 기반 시장 심리 분석
- **상관관계 분석**: 시장 간 상관관계 이탈 감지
- **섹터 로테이션**: 자금 흐름 패턴 분석

### 🤖 **AI 기반 뉴스 생성**
- **AWS Bedrock Claude**: 고품질 경제 기사 자동 생성
- **다중 Agent 시스템**: 전문화된 Agent들의 협업
- **콘텐츠 최적화**: 가독성, SEO, 독자 참여도 최적화

### 📱 **실시간 Slack 알림**
- **즉시 알림**: 긴급 시장 이벤트 실시간 전송
- **시장 요약**: 정기적인 종합 분석 리포트
- **스마트 필터링**: 알림 피로도 최소화
- **모바일 지원**: Slack 앱을 통한 모바일 알림

### 📈 **Streamlit 대시보드**
- **인터랙티브 차트**: 실시간 시장 데이터 시각화
- **AI 생성 기사**: 웹 기반 기사 뷰어
- **자동 이미지**: 기사 일러스트레이션 및 워드클라우드

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                      │
│                 (웹 인터페이스 & 시각화)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Enhanced Monitor System                       │
│              (고도화된 모니터링 시스템)                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌────▼─────┐ ┌────▼──────────┐
│ Technical    │ │ Sentiment│ │ Correlation   │
│ Analysis     │ │ Analysis │ │ Analysis      │
│ Agent        │ │ Agent    │ │ Agent         │
└──────────────┘ └──────────┘ └───────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │      Slack Notifier       │
        │    (실시간 알림 전송)       │
        └───────────────────────────┘
```

## 📋 요구사항

### 시스템 요구사항
- Python 3.8+
- AWS 계정 및 Bedrock 액세스 권한
- Slack 워크스페이스 (알림용)
- 인터넷 연결 (데이터 수집용)

### AWS 권한
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🛠️ 설치 및 설정

### 1. 저장소 클론
```bash
git clone https://github.com/jihwanwoo/Economic-News-System.git
cd Economic-News-System
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. AWS 자격 증명 설정
```bash
# AWS CLI 설정
aws configure

# 또는 환경 변수 설정
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 4. Slack 웹훅 설정
```bash
# Slack 웹훅 URL 설정
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# 또는 설정 파일 생성
cp config/slack_config_template.json config/slack_config.json
# config/slack_config.json 편집
```

### 5. 시스템 테스트
```bash
# 전체 시스템 테스트
python test_system.py

# Slack 알림 테스트
python demo_slack_alerts.py
```

## 🎯 사용법

### 📱 **Slack 알림 시스템 (추천)**

#### 즉시 테스트
```bash
python demo_slack_alerts.py
```

#### 연속 모니터링 시작
```bash
# 백그라운드 실행
./start_background_monitoring.sh

# 상태 확인
./check_monitoring_status.sh

# 중지
./stop_monitoring.sh
```

### 📊 **Streamlit 대시보드**
```bash
# 대시보드 실행
python demo_streamlit.py

# 또는 직접 실행
python run_streamlit.py
```

### 🖥️ **명령줄 인터페이스**
```bash
# 전체 파이프라인 실행
python main.py --mode full

# 특정 유형의 기사 생성
python main.py --mode full --market-summary --stock-focus

# 고도화된 이벤트 감지만 실행
python data_monitoring/integrated_event_system.py
```

## 📊 알림 유형

### 🚨 **긴급 알림** (심각도 0.6 이상)
- 📈 주식 급등/급락 (5% 이상)
- ⚡ 높은 변동성 (15% 이상)
- 📊 거래량 급증 (평균 대비 3배)
- 🚀 기술적 돌파 (볼린저 밴드, RSI)
- 💭 시장 감정 급변
- 🔄 모멘텀 다이버전스

### 📋 **시장 요약** (1시간마다)
- 전체 위험도 평가
- 감지된 이벤트 요약
- 주요 인사이트
- 투자 시사점

### 📰 **뉴스 업데이트**
- AI 생성 기사 완료 알림
- 주요 포인트 요약

## ⚙️ 설정 커스터마이징

### Slack 알림 설정
```json
{
  "notification_settings": {
    "send_summary": true,
    "send_critical_alerts": true,
    "summary_interval_minutes": 60,
    "min_alert_severity": 0.6,
    "max_alerts_per_hour": 15,
    "cooldown_minutes": 15
  }
}
```

### 모니터링 대상 심볼
```python
monitoring_symbols = [
    # 주요 지수
    "^GSPC", "^IXIC", "^DJI", "^VIX",
    
    # 주요 개별 종목
    "AAPL", "GOOGL", "MSFT", "TSLA", "NVDA",
    
    # 섹터 ETF
    "XLK", "XLF", "XLE", "XLV"
]
```

## 📁 출력 파일

생성된 콘텐츠는 `output/` 디렉토리에 저장됩니다:

```
output/
├── pipeline_result_20240804_143022.json    # 전체 실행 결과
├── article_20240804_143022_1.html          # HTML 형식 기사
├── slack_demo_20240804_143022.json         # Slack 알림 결과
└── advanced_events_20240804_143022.json    # 고급 이벤트 감지 결과
```

## 🔍 모니터링 및 관리

### 로그 확인
```bash
# 실시간 로그 모니터링
tail -f logs/background_monitoring.log

# 오류 로그 검색
grep "ERROR" logs/slack_monitoring.log

# 알림 통계
grep "Slack 알림 전송 성공" logs/slack_monitoring.log | wc -l
```

### 성능 모니터링
```bash
# 시스템 상태 확인
./check_monitoring_status.sh

# 디스크 사용량 확인
du -sh logs/ output/
```

## 🚨 문제 해결

### 일반적인 문제들

**AWS 자격 증명 오류**
```bash
aws configure list
aws sts get-caller-identity
```

**Slack 웹훅 오류**
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"테스트 메시지"}' \
$SLACK_WEBHOOK_URL
```

**알림이 너무 많음**
```bash
# config/slack_config.json에서 조정
"min_alert_severity": 0.8,  # 0.6에서 0.8로 증가
"max_alerts_per_hour": 8    # 15에서 8로 감소
```

## 📈 성능 최적화

- **캐싱**: 데이터 수집 결과 캐싱으로 API 호출 최소화
- **병렬 처리**: 여러 Agent 동시 실행
- **배치 처리**: 대량 기사 생성 시 배치 모드 사용
- **알림 최적화**: 스마트 필터링으로 중요한 알림만 전송

## 🔒 보안 고려사항

- AWS 자격 증명 안전한 관리
- Slack 웹훅 URL 환경 변수 사용
- 민감한 정보 `.gitignore`에 추가
- 생성된 콘텐츠 검토 및 승인 프로세스

## 🤝 기여

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면:
- GitHub Issues에 문제 보고
- 로그 파일 확인 (`logs/` 디렉토리)
- 설정 파일 및 환경 변수 재확인

---

**주의사항**: 
- 이 시스템은 투자 조언을 제공하지 않습니다
- 생성된 콘텐츠는 정보 제공 목적으로만 사용하세요
- 중요한 투자 결정은 전문가와 상담하세요

## 🎉 특별 감사

- AWS Bedrock Claude 모델
- Yahoo Finance API
- Slack API
- Streamlit 커뮤니티

## 🚀 주요 기능

- **자동 데이터 수집**: 주식 시장, 경제 지표, 뉴스 피드에서 실시간 데이터 수집
- **지능형 기사 작성**: AWS Bedrock Claude 모델을 활용한 고품질 경제 기사 생성
- **콘텐츠 최적화**: 가독성, SEO, 독자 참여도 최적화
- **다중 Agent 시스템**: 전문화된 Agent들의 협업을 통한 효율적 워크플로우
- **📊 Streamlit 대시보드**: 인터랙티브 웹 인터페이스로 기사와 차트 시각화
- **🖼️ 자동 이미지 생성**: 기사 내용 기반 일러스트레이션 및 워드클라우드
- **📢 맞춤형 광고**: 기사 내용 분석 기반 관련 광고 추천

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                      │
│                 (웹 인터페이스 & 시각화)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Orchestrator Agent                       │
│                   (전체 시스템 조율)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌────▼─────┐ ┌────▼──────────┐
│ Data         │ │ News     │ │ Content       │
│ Collector    │ │ Writer   │ │ Optimizer     │
│ Agent        │ │ Agent    │ │ Agent         │
└──────────────┘ └──────────┘ └───────────────┘
```

### Agent 구성

1. **Data Collector Agent**: 경제 데이터 수집 및 분석
2. **News Writer Agent**: 경제 기사 작성
3. **Content Optimizer Agent**: 콘텐츠 품질 최적화
4. **Orchestrator Agent**: 전체 워크플로우 관리
5. **Streamlit Dashboard**: 웹 기반 시각화 및 사용자 인터페이스

## 📋 요구사항

### 시스템 요구사항
- Python 3.8+
- AWS 계정 및 Bedrock 액세스 권한
- 인터넷 연결 (데이터 수집용)

### AWS 권한
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🛠️ 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. AWS 자격 증명 설정
```bash
# AWS CLI 설정
aws configure

# 또는 환경 변수 설정
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 3. 설정 파일 확인
```bash
# 기본 설정 파일 확인
cat config/default.json

# 필요시 설정 수정
cp config/default.json config/custom.json
# config/custom.json 편집
```

### 4. 시스템 테스트
```bash
# 전체 시스템 테스트
python test_system.py

# 개별 컴포넌트 테스트
python test_system.py aws      # AWS 연결 테스트
python test_system.py data     # 데이터 수집 테스트
python test_system.py writer   # 기사 작성 테스트
```

## 🎯 사용법

### 📊 Streamlit 대시보드 (추천)

```bash
# 대시보드 데모 실행
python demo_streamlit.py

# 또는 직접 실행
python run_streamlit.py
```

**대시보드 기능:**
- 🎛️ **사이드바 제어판**: 새 기사 생성, 기사 선택, 표시 옵션 설정
- 📈 **실시간 메트릭**: S&P 500, 나스닥, VIX, 달러 인덱스 현황
- 📊 **인터랙티브 차트**: 주식 현황, 변화율, 섹터 성과, VIX 게이지
- 📰 **AI 생성 기사**: 헤드라인, 본문, 결론, 품질 점수
- 🖼️ **자동 이미지**: 기사 일러스트레이션, 워드클라우드
- 📢 **맞춤 광고**: 기사 내용 기반 관련 서비스 추천

### 명령줄 인터페이스

```bash
# 전체 파이프라인 실행 (데이터 수집 + 기사 작성 + 최적화)
python main.py --mode full

# 특정 유형의 기사 생성
python main.py --mode full --market-summary --stock-focus

# 데이터 수집만 실행
python main.py --mode data

# 기사 작성만 실행
python main.py --mode article --article-type market_summary --length medium
```

### 고급 사용법

```bash
# 사용자 정의 설정 파일 사용
python main.py --config config/custom.json --mode full

# 로그 레벨 조정
python main.py --log-level DEBUG --mode full

# 스케줄 모드 (자동화)
python main.py --mode schedule
```

### 실행 모드

| 모드 | 설명 | 예시 |
|------|------|------|
| `full` | 전체 파이프라인 실행 | `--mode full` |
| `data` | 데이터 수집만 | `--mode data` |
| `article` | 기사 작성만 | `--mode article` |
| `schedule` | 자동화 스케줄 실행 | `--mode schedule` |
| `status` | 시스템 상태 확인 | `--mode status` |

### 기사 유형

- `market_summary`: 시장 종합 분석
- `stock_focus`: 개별 종목 분석  
- `economic_outlook`: 경제 전망
- `sector_analysis`: 섹터별 분석

## 📁 출력 파일

생성된 콘텐츠는 `output/` 디렉토리에 저장됩니다:

```
output/
├── pipeline_result_20240804_143022.json    # 전체 실행 결과
├── article_20240804_143022_1.html          # HTML 형식 기사
├── article_20240804_143022_2.html
└── collected_data_20240804_143022.json     # 수집된 데이터
```

### 출력 형식

- **JSON**: 구조화된 데이터 및 메타데이터
- **HTML**: 웹 게시용 완성된 기사
- **Streamlit**: 인터랙티브 웹 대시보드
- **로그**: 실행 과정 및 오류 정보

## 📊 Streamlit 대시보드 상세 기능

### 🎛️ 제어판 (사이드바)
- **새 기사 생성**: 실시간 데이터 수집 및 AI 기사 작성
- **기사 목록**: 생성된 기사 선택 및 탐색
- **표시 옵션**: 차트, 이미지, 광고 표시 설정
- **시스템 정보**: 마지막 업데이트 시간 및 상태

### 📈 시장 현황 메트릭
- **S&P 500**: 현재가, 변화율, 실시간 업데이트
- **나스닥**: 기술주 중심 지수 현황
- **VIX**: 공포 지수 및 시장 변동성
- **달러 인덱스**: 달러 강세/약세 지표

### 📊 인터랙티브 차트
1. **주식 현황**: 주요 종목 가격 및 거래량
2. **변화율**: 종목별 등락률 비교
3. **섹터 성과**: 업종별 평균 수익률
4. **VIX 게이지**: 공포/탐욕 지수 시각화
5. **시가총액**: 주요 종목 비중 파이 차트

### 🖼️ 자동 이미지 생성
- **기사 일러스트레이션**: 내용 기반 맞춤 이미지
- **워드클라우드**: 핵심 키워드 시각화
- **차트 이미지**: 데이터 기반 그래프

### 📢 맞춤형 광고 시스템
- **투자 플랫폼**: 스마트 투자, 로보어드바이저
- **트레이딩 도구**: 실시간 거래, 프리미엄 차트
- **교육 서비스**: 투자 교육, 경제 뉴스 구독
- **컨텍스트 매칭**: 기사 내용 및 태그 기반 광고 선택

## ⚙️ 설정 옵션

### 주요 설정 항목

```json
{
  "aws_region": "us-east-1",
  "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
  "temperature": 0.7,
  "max_tokens": 4000,
  
  "data_collection": {
    "stock_symbols": ["AAPL", "GOOGL", "MSFT"],
    "update_interval_minutes": 30
  },
  
  "article_generation": {
    "default_types": ["market_summary"],
    "default_length": "medium"
  },
  
  "schedule": {
    "enabled": false,
    "data_collection_interval": 30,
    "article_generation_interval": 60
  }
}
```

## 🔧 개발 및 확장

### 새로운 Agent 추가

1. `agents/` 디렉토리에 새 Agent 클래스 생성
2. `BaseAgent`를 상속받아 구현
3. `OrchestratorAgent`에 통합

```python
from agents.base_agent import BaseAgent, AgentConfig

class CustomAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return "Your custom prompt"
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your custom logic
        return result
```

### Streamlit 컴포넌트 확장

```python
# streamlit_app/custom_components.py
import streamlit as st

def create_custom_chart(data):
    # 새로운 차트 컴포넌트
    pass

def add_custom_widget():
    # 새로운 위젯 추가
    pass
```

### 새로운 데이터 소스 추가

`DataCollectorAgent`의 `collect_*` 메서드를 확장하여 새로운 데이터 소스를 추가할 수 있습니다.

## 📊 모니터링 및 로깅

### 로그 파일 위치
- 실행 로그: `logs/economic_news_YYYYMMDD.log`
- 오류 로그: 콘솔 및 로그 파일에 기록

### 성능 모니터링
```bash
# 시스템 상태 확인
python main.py --mode status

# Streamlit 대시보드에서 실시간 모니터링
python demo_streamlit.py

# 로그 실시간 모니터링
tail -f logs/economic_news_$(date +%Y%m%d).log
```

## 🚨 문제 해결

### 일반적인 문제

1. **AWS 자격 증명 오류**
   ```bash
   aws configure list
   aws sts get-caller-identity
   ```

2. **Bedrock 모델 액세스 오류**
   - AWS 콘솔에서 Bedrock 모델 액세스 권한 확인
   - 지원되는 리전에서 실행 확인

3. **Streamlit 실행 오류**
   ```bash
   # 포트 충돌 확인
   lsof -i :8501
   
   # 의존성 재설치
   pip install -r requirements.txt
   ```

4. **데이터 수집 실패**
   - 인터넷 연결 확인
   - API 제한 및 Rate Limiting 확인

5. **메모리 부족**
   - `max_tokens` 설정 조정
   - 동시 처리 수 제한

### 디버깅

```bash
# 디버그 모드 실행
python main.py --log-level DEBUG --mode data

# 개별 컴포넌트 테스트
python test_system.py [component_name]

# Streamlit 디버그 모드
streamlit run streamlit_app/app.py --logger.level debug
```

## 📈 성능 최적화

- **캐싱**: 데이터 수집 결과 캐싱으로 API 호출 최소화
- **병렬 처리**: 여러 Agent 동시 실행
- **배치 처리**: 대량 기사 생성 시 배치 모드 사용
- **Streamlit 캐싱**: `@st.cache_data` 데코레이터 활용

## 🔒 보안 고려사항

- AWS 자격 증명 안전한 관리
- API 키 환경 변수 사용
- 생성된 콘텐츠 검토 및 승인 프로세스
- Streamlit 보안 설정 (HTTPS, 인증)

## 🌐 배포 옵션

### 로컬 개발
```bash
python demo_streamlit.py
```

### 클라우드 배포
```bash
# Streamlit Cloud
streamlit run streamlit_app/app.py

# Docker 컨테이너
docker build -t economic-news-dashboard .
docker run -p 8501:8501 economic-news-dashboard
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.

---

**주의**: 이 시스템은 투자 조언을 제공하지 않습니다. 생성된 콘텐츠는 정보 제공 목적으로만 사용하세요.
