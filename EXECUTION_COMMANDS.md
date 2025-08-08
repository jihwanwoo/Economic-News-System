# 🚀 경제 뉴스 시스템 실행 명령어 가이드

## 📋 전체 시스템 실행 (추천)

### 1️⃣ **원클릭 실행 (가장 간단)**
```bash
./run_news_system.sh
```

### 2️⃣ **Python 직접 실행**
```bash
python run_complete_news_system.py
```

### 3️⃣ **단계별 실행**
```bash
# 1단계: 이벤트 감지
python event_detection_slack_system.py

# 2단계: 기사 생성 (Strands Agent 시스템)
python -c "
import asyncio
from agents import main_orchestrator
from agents.strands_framework import StrandContext
from datetime import datetime

async def run():
    event = {
        'symbol': 'AAPL',
        'event_type': 'price_change', 
        'severity': 'medium',
        'title': 'AAPL 주가 변동',
        'description': 'AAPL 주가 변동이 감지되었습니다.',
        'timestamp': datetime.now().isoformat()
    }
    
    context = StrandContext(
        strand_id='manual_test',
        input_data={'event': event}
    )
    
    result = await main_orchestrator.process(context)
    print('✅ 기사 생성 완료:', result.get('status'))

asyncio.run(run())
"
```

## 🎯 실행 모드별 명령어

### 🔄 **연속 모니터링 모드**
```bash
# 백그라운드에서 지속적으로 실행
nohup python run_complete_news_system.py &

# 상태 확인
ps aux | grep run_complete_news_system

# 중지
pkill -f run_complete_news_system
```

### 📊 **테스트 모드**
```bash
# 시스템 상태 테스트
python test_strands_system.py

# 개별 컴포넌트 테스트
python -c "
from agents import DataAnalysisStrand
import asyncio

async def test():
    agent = DataAnalysisStrand()
    print('능력:', agent.get_capabilities())

asyncio.run(test())
"
```

### 🌐 **Streamlit 대시보드**
```bash
# 최신 생성된 기사 보기
streamlit run streamlit_articles/$(ls -t streamlit_articles/article_*.py | head -1)

# 또는 간단하게
./run_latest_article.sh
```

## 📈 **실행 결과 확인**

### 생성된 파일 위치:
- **📰 기사**: `output/automated_articles/`
- **📊 차트**: `output/charts/`
- **🖼️ 이미지**: `output/images/`
- **🌐 Streamlit**: `streamlit_articles/`
- **📋 로그**: `logs/`

### 확인 명령어:
```bash
# 최신 기사 확인
ls -la output/automated_articles/ | tail -5

# 생성된 차트 개수
ls output/charts/*.html | wc -l

# 로그 실시간 모니터링
tail -f logs/complete_system_$(date +%Y%m%d).log
```

## 🔧 **문제 해결**

### 환경 설정 확인:
```bash
# 환경 변수 확인
python check_env.py

# AWS 연결 테스트
python test_aws_quick.py

# Slack 웹훅 테스트
python test_slack_webhook.py
```

### 의존성 설치:
```bash
pip install -r requirements.txt
```

### 권한 설정:
```bash
chmod +x *.sh
```

## ⚡ **빠른 실행 체크리스트**

1. **환경 변수 설정 확인**:
   - ✅ `AWS_DEFAULT_REGION=us-east-1`
   - ✅ `ALPHA_VANTAGE_API_KEY=your_key`
   - ✅ `SLACK_WEBHOOK_URL=your_webhook` (선택사항)

2. **디렉토리 구조 확인**:
   ```bash
   ls -la agents/  # 8개 파일 있어야 함
   ```

3. **실행**:
   ```bash
   ./run_news_system.sh
   ```

4. **결과 확인**:
   ```bash
   ls output/automated_articles/
   streamlit run streamlit_articles/$(ls -t streamlit_articles/article_*.py | head -1)
   ```

## 🎉 **성공 시 출력 예시**

```
🚀 경제 뉴스 자동 생성 시스템 시작
==================================================
📊 실행 결과:
상태: success
실행 시간: 45.2초
감지된 이벤트: 2개
생성된 기사: 2개
Slack 알림: 3개

🎉 전체 시스템 실행 완료!

💡 생성된 기사 확인:
  1. streamlit run streamlit_articles/article_AAPL_20250807_120530.py
  2. streamlit run streamlit_articles/article_TSLA_20250807_120545.py
```

## 📞 **지원**

문제 발생 시:
1. 로그 파일 확인: `logs/complete_system_YYYYMMDD.log`
2. 시스템 테스트: `python test_strands_system.py`
3. 환경 설정 확인: `python check_env.py`
