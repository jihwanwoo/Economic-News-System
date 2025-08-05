# 🚀 경제 뉴스 자동 생성 통합 파이프라인 사용법

## 📋 개요

이 통합 파이프라인은 경제 데이터 모니터링부터 AI 기사 생성, 품질 검수, 맞춤형 광고 추천까지 전 과정을 **한 번의 명령**으로 실행할 수 있는 완전 자동화 시스템입니다.

## 🎯 파이프라인 단계

1. **📊 경제 데이터 모니터링**: 실시간 주식, 지수, 경제 지표 수집
2. **🚨 이벤트 감지**: 시장 하락, 변동성 증가 등 주요 이벤트 자동 감지
3. **🤖 경제 분석**: AI 기반 시장 동향 및 리스크 분석
4. **📰 기사 생성**: AWS Bedrock Claude를 활용한 고품질 경제 기사 작성
5. **📊 품질 검수**: 자동 품질 평가 및 점수 산정
6. **📢 광고 추천**: 기사 내용 기반 맞춤형 광고 생성

## 🚀 실행 방법

### 방법 1: 간단 실행 (추천)
```bash
# 기본 실행
./run_news_pipeline.sh

# 또는
bash run_news_pipeline.sh
```

### 방법 2: Python 직접 실행
```bash
# 기본 실행
python run_full_pipeline.py

# 설정 파일 지정
python run_full_pipeline.py --config config/custom.json

# 로그 레벨 조정
python run_full_pipeline.py --log-level DEBUG

# 출력 디렉토리 변경
python run_full_pipeline.py --output-dir /path/to/output
```

### 방법 3: 고급 옵션
```bash
# 모든 옵션 사용
python run_full_pipeline.py \
    --config config/production.json \
    --log-level INFO \
    --output-dir results/$(date +%Y%m%d)
```

## ⚙️ 명령줄 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--config` | `config/default.json` | 설정 파일 경로 |
| `--log-level` | `INFO` | 로그 레벨 (DEBUG, INFO, WARNING, ERROR) |
| `--output-dir` | `output` | 결과 파일 저장 디렉토리 |

## 📁 출력 파일

실행 완료 후 다음 파일들이 생성됩니다:

```
output/
├── full_pipeline_YYYYMMDD_HHMMSS.json    # 전체 실행 결과 (JSON)
└── article_YYYYMMDD_HHMMSS.html          # 완성된 기사 (HTML)
```

### 📄 JSON 결과 파일 구조
```json
{
  "execution_id": "20250804_143022",
  "timestamp": "2025-08-04T14:30:22.123456",
  "duration_seconds": 67.2,
  "pipeline_steps": {
    "1_monitoring": { "status": "completed", "data_points": 8 },
    "2_event_detection": { "status": "completed", "events_detected": 3 },
    "3_analysis": { "status": "completed", "market_trend": "BEARISH" },
    "4_article_generation": { "status": "completed" },
    "5_quality_review": { "status": "PASSED", "score": 85 },
    "6_advertisement": { "status": "completed", "ads_generated": 3 }
  },
  "summary": {
    "market_trend": "BEARISH",
    "events_count": 3,
    "article_quality": 85,
    "ads_count": 3
  }
}
```

## 📊 실행 예시

### 성공적인 실행 예시
```bash
$ ./run_news_pipeline.sh

🚀 경제 뉴스 자동 생성 파이프라인 시작
==================================================
✅ 가상환경 활성화됨: /home/user/venv
✅ AWS 자격증명 확인됨

📊 파이프라인 실행 중...
==================================================

================================================================================
📊 1단계: 경제 데이터 실시간 모니터링
================================================================================
📈 데이터 수집 중...
✅ 수집된 데이터: 8 항목

💹 주요 지표 현황:
  📉 AAPL: $202.38 (-2.50%) | 거래량: 104,301,700
  📉 NVDA: $173.72 (-2.33%) | 거래량: 203,851,100
  📉 ^GSPC: $6238.01 (-1.64%) | 거래량: 0
  📈 ^VIX: $19.23 (+2.15%) | 거래량: 0

================================================================================
📊 2단계: 경제 이벤트 자동 감지
================================================================================
🎯 감지된 이벤트: 3개

📋 감지된 주요 이벤트:
  1. 🟡 MARKET_DECLINE: 주요 기술주 4개 종목 1.5% 이상 하락
     심각도: MEDIUM | 영향: NEGATIVE 📉
  2. 🔴 INDEX_DECLINE: 주요 지수 2개 1.5% 이상 하락
     심각도: HIGH | 영향: NEGATIVE 📉

================================================================================
📊 3단계: 경제 데이터 종합 분석
================================================================================
📊 시장 분석 결과:
  • 전반적 추세: BEARISH 📉
  • 하락 종목 비율: 100.0%
  • 시장 심리: CAUTIOUS

================================================================================
📊 4단계: AI 기반 경제 기사 생성
================================================================================
🤖 AI 기사 생성 시작...
✅ AI 기사 생성 완료!
📰 제목: 기술주 급락에 주요 지수 하락...투자자 심리 위축

================================================================================
📊 5단계: 기사 품질 검수
================================================================================
📊 품질 검수 결과:
🎯 전체 품질 점수: 85/100
✅ 품질 검수 통과 (기준: 70점 이상)

================================================================================
📊 6단계: 맞춤형 광고 추천
================================================================================
🎯 추천된 광고: 3개

📌 광고 #1: 스마트 투자 플랫폼
   📝 설명: AI 기반 포트폴리오 관리로 더 나은 수익을 경험하세요
   🔗 CTA: 무료 체험하기

💾 결과 저장 완료:
  📄 통합 결과: output/full_pipeline_20250804_143022.json
  🌐 HTML 기사: output/article_20250804_143022.html

================================================================================
🎉 경제 뉴스 자동 생성 파이프라인 완료!
================================================================================

📊 실행 요약:
  ⏱️  총 소요 시간: 67.2초
  📈 모니터링 데이터: 8개 종목/지표
  🚨 감지된 이벤트: 3개
  📰 기사 품질 점수: 85/100
  📢 추천 광고: 3개
  🎯 시장 추세: BEARISH

🎉 파이프라인 실행 완료!
📁 결과 파일은 output/ 디렉토리에서 확인하세요.
```

## 🔧 문제 해결

### 일반적인 오류

#### 1. AWS 자격증명 오류
```bash
❌ AWS 자격증명을 확인할 수 없습니다.
```
**해결방법:**
```bash
aws configure
# 또는
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

#### 2. 의존성 오류
```bash
ModuleNotFoundError: No module named 'langchain_aws'
```
**해결방법:**
```bash
pip install -r requirements.txt
```

#### 3. 권한 오류
```bash
Permission denied: ./run_news_pipeline.sh
```
**해결방법:**
```bash
chmod +x run_news_pipeline.sh
```

#### 4. Bedrock 모델 액세스 오류
```bash
AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel
```
**해결방법:**
- AWS 콘솔에서 Bedrock 모델 액세스 권한 확인
- IAM 정책에 Bedrock 권한 추가

### 디버깅

```bash
# 상세 로그로 실행
python run_full_pipeline.py --log-level DEBUG

# 로그 파일 확인
tail -f logs/pipeline_$(date +%Y%m%d).log
```

## 📈 성능 최적화

### 실행 시간 단축
- **캐싱 활용**: 최근 데이터 캐시 사용
- **병렬 처리**: 데이터 수집 병렬화
- **모델 최적화**: 더 빠른 Bedrock 모델 사용

### 품질 향상
- **설정 조정**: `config/default.json`에서 파라미터 튜닝
- **프롬프트 개선**: Agent별 시스템 프롬프트 최적화
- **데이터 소스 확장**: 더 많은 경제 지표 추가

## 🔄 자동화 설정

### Cron 작업 설정
```bash
# 매시간 실행
0 * * * * cd /path/to/economic_news_system && ./run_news_pipeline.sh

# 시장 개장 시간에만 실행 (평일 9-16시)
0 9-16 * * 1-5 cd /path/to/economic_news_system && ./run_news_pipeline.sh
```

### 시스템 서비스 등록
```bash
# systemd 서비스 파일 생성
sudo nano /etc/systemd/system/economic-news.service

# 서비스 활성화
sudo systemctl enable economic-news.service
sudo systemctl start economic-news.service
```

## 📞 지원

문제가 발생하거나 질문이 있으시면:
1. 로그 파일 확인 (`logs/pipeline_YYYYMMDD.log`)
2. GitHub Issues 생성
3. 설정 파일 검토 (`config/default.json`)

---

**💡 팁**: 첫 실행 전에 `python test_system.py`로 시스템 테스트를 권장합니다.
