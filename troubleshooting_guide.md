# 🛠️ 연결 문제 해결 가이드

## 일반적인 문제들

### 1. SSH 터널 연결 실패
**증상**: `ssh: connect to host [IP] port 22: Connection refused`

**해결책**:
```bash
# EC2 인스턴스 상태 확인
aws ec2 describe-instances --instance-ids [INSTANCE-ID]

# 보안 그룹에서 SSH(22) 포트 확인
# 키 파일 권한 확인 (Mac/Linux)
chmod 400 ~/.ssh/your-key.pem
```

### 2. Streamlit 서버 시작 실패
**증상**: `ModuleNotFoundError` 또는 `ImportError`

**해결책**:
```bash
# 가상환경 활성화 (있는 경우)
source venv/bin/activate

# 의존성 재설치
pip install -r requirements.txt

# Python 경로 확인
which python
python --version
```

### 3. 포트 8501 접속 불가
**증상**: 브라우저에서 "연결할 수 없음"

**해결책**:
```bash
# 포트 사용 확인
netstat -tlnp | grep :8501

# 방화벽 확인 (Ubuntu)
sudo ufw status

# Streamlit 프로세스 재시작
pkill -f streamlit
./start_streamlit_with_tunnel.sh
```

### 4. 로컬 포트 충돌
**증상**: `bind: Address already in use`

**해결책**:
```bash
# 다른 포트 사용
ssh -L 8502:localhost:8501 -i key.pem ec2-user@[IP]

# 또는 기존 프로세스 종료
lsof -ti:8501 | xargs kill -9
```

## 연결 테스트 명령어

### EC2에서 실행
```bash
# 서버 상태 확인
./check_streamlit_status.sh

# 수동 테스트
curl http://localhost:8501
```

### 로컬에서 실행
```bash
# SSH 연결 테스트
ssh -i key.pem ec2-user@[EC2-IP] "echo 'SSH 연결 성공'"

# 포트 포워딩 테스트
curl http://localhost:8501
```

## 성능 최적화

### 1. 메모리 사용량 줄이기
```python
# Streamlit 설정 추가
st.set_page_config(
    page_title="Economic News",
    layout="wide",
    initial_sidebar_state="collapsed"  # 사이드바 접기
)
```

### 2. 캐싱 활용
```python
@st.cache_data(ttl=60)  # 60초 캐시
def load_market_data():
    # 데이터 로딩 로직
    pass
```

### 3. 백그라운드 실행
```bash
# nohup으로 백그라운드 실행
nohup streamlit run app.py > streamlit.log 2>&1 &

# screen 사용
screen -S streamlit
streamlit run app.py
# Ctrl+A, D로 detach
```
