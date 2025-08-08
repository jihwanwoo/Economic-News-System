# 🚀 EC2 터미널에서 실행하기

## 현재 상황
- EC2에 SSH로 접속 완료 ✅
- 프로젝트 폴더: `/home/ec2-user/projects/ABP/economic_news_system`

## 실행 명령어 (순서대로)

### 1. 프로젝트 폴더로 이동
```bash
cd /home/ec2-user/projects/ABP/economic_news_system
```

### 2. 현재 위치 확인
```bash
pwd
ls -la integrated_dashboard.py
```

### 3. 시스템 테스트 (선택사항)
```bash
python test_integrated_dashboard.py
```

### 4. Streamlit 실행
```bash
# 포그라운드 실행 (터미널을 닫으면 종료됨)
streamlit run integrated_dashboard.py

# 또는 백그라운드 실행 (터미널을 닫아도 계속 실행)
nohup streamlit run integrated_dashboard.py --server.port=8501 --server.address=0.0.0.0 > streamlit.log 2>&1 &
```

## 🔗 로컬 PC에서 접속하기

### 방법 1: 새 터미널 창에서 SSH 터널 생성
현재 EC2 연결을 유지한 채로 **로컬 PC의 새 터미널**에서:
```bash
ssh -L 8501:localhost:8501 -i ~/.ssh/your-key.pem ec2-user@98.80.100.116
```

### 방법 2: 현재 연결 종료 후 포트 포워딩으로 재연결
```bash
# 현재 EC2 세션에서
exit

# 로컬 PC에서 포트 포워딩과 함께 재연결
ssh -L 8501:localhost:8501 -i ~/.ssh/your-key.pem ec2-user@98.80.100.116

# 다시 프로젝트 폴더로 이동
cd /home/ec2-user/projects/ABP/economic_news_system

# Streamlit 실행
streamlit run integrated_dashboard.py
```

## 📱 브라우저 접속
SSH 터널이 연결된 상태에서 브라우저에서:
```
http://localhost:8501
```

## 🔍 실행 상태 확인
```bash
# Streamlit 프로세스 확인
ps aux | grep streamlit

# 포트 사용 확인
netstat -tlnp | grep :8501

# 로그 확인 (백그라운드 실행 시)
tail -f streamlit.log
```

## 💡 추천 방법
**방법 2 (재연결)**를 추천합니다:
1. 현재 세션 종료
2. 포트 포워딩으로 재연결
3. Streamlit 실행
4. 브라우저에서 접속
