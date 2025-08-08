# 🔗 SSH 터널링으로 Streamlit 접속하기

## ✅ EC2 서버 준비 완료!
Streamlit 서버가 EC2에서 정상적으로 실행 중입니다.
- 서버 주소: 0.0.0.0:8501
- 상태: 🟢 실행 중

## 🖥️ 로컬 PC에서 연결하기

### Windows (PowerShell 또는 CMD)
```cmd
ssh -L 8501:localhost:8501 -i "C:\path\to\your-key.pem" ec2-user@[EC2-PUBLIC-IP]
```

### Mac/Linux (터미널)
```bash
ssh -L 8501:localhost:8501 -i ~/.ssh/your-key.pem ec2-user@[EC2-PUBLIC-IP]
```

## 🔧 실제 명령어 예시

**EC2 퍼블릭 IP를 확인하고 아래 명령어에서 [EC2-PUBLIC-IP] 부분을 실제 IP로 바꾸세요:**

### Windows 예시:
```cmd
ssh -L 8501:localhost:8501 -i "C:\Users\YourName\Downloads\your-key.pem" ec2-user@3.34.123.456
```

### Mac/Linux 예시:
```bash
ssh -L 8501:localhost:8501 -i ~/.ssh/your-key.pem ec2-user@3.34.123.456
```

## 📱 브라우저에서 접속

SSH 터널이 연결되면 브라우저에서 다음 주소로 접속:
```
http://localhost:8501
```

## 🔍 연결 확인 방법

### 1. SSH 터널 연결 성공 시 표시되는 메시지:
```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.2.0-1009-aws x86_64)
...
ec2-user@ip-xxx-xxx-xxx-xxx:~$
```

### 2. 브라우저에서 접속 확인:
- 주소창에 `http://localhost:8501` 입력
- "🤖 경제 뉴스 통합 시스템" 페이지가 로드되면 성공!

## 🛠️ 문제 해결

### SSH 연결 실패 시:
1. **키 파일 권한 확인** (Mac/Linux):
   ```bash
   chmod 400 ~/.ssh/your-key.pem
   ```

2. **EC2 퍼블릭 IP 확인**:
   - AWS 콘솔에서 EC2 인스턴스의 퍼블릭 IP 확인

3. **보안 그룹 확인**:
   - SSH(22) 포트가 열려있는지 확인

### 브라우저 접속 실패 시:
1. **터널 연결 상태 확인**:
   - SSH 터미널이 연결된 상태여야 함

2. **로컬 포트 충돌 확인**:
   ```bash
   # Mac/Linux
   lsof -i :8501
   
   # Windows
   netstat -ano | findstr :8501
   ```

3. **다른 포트 사용**:
   ```bash
   ssh -L 8502:localhost:8501 -i key.pem ec2-user@[IP]
   # 브라우저에서 http://localhost:8502 접속
   ```

## 🎯 성공 확인 체크리스트

- [ ] SSH 터널 연결 성공
- [ ] 브라우저에서 http://localhost:8501 접속 가능
- [ ] Streamlit 대시보드 로딩 완료
- [ ] 사이드바에서 "🚀 모니터링 시작" 버튼 확인
- [ ] 실시간 데이터 업데이트 확인

## 🚀 다음 단계

연결이 성공하면:
1. 사이드바에서 "🚀 모니터링 시작" 클릭
2. 실시간 데이터 모니터링 확인
3. 이벤트 감지 시 Slack 알림 테스트
4. AI 기사 생성 기능 테스트

---

**💡 팁**: SSH 터널은 터미널을 닫으면 연결이 끊어집니다. 
계속 사용하려면 터미널을 열어둔 상태로 유지하세요!
