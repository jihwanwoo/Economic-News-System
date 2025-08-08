# VS Code Remote SSH 설정 가이드

## 1단계: VS Code 확장 설치
1. VS Code 실행
2. 확장 마켓플레이스에서 "Remote - SSH" 설치

## 2단계: SSH 설정 파일 구성
`~/.ssh/config` 파일에 추가:

```
Host ec2-economic-news
    HostName [EC2-PUBLIC-IP]
    User ec2-user
    IdentityFile ~/.ssh/your-key.pem
    LocalForward 8501 localhost:8501
```

## 3단계: VS Code에서 원격 연결
1. `Ctrl+Shift+P` (또는 `Cmd+Shift+P`)
2. "Remote-SSH: Connect to Host" 선택
3. "ec2-economic-news" 선택

## 4단계: 원격 터미널에서 Streamlit 실행
VS Code 내장 터미널에서:
```bash
cd /home/ec2-user/projects/ABP/economic_news_system
streamlit run integrated_dashboard.py
```

## 5단계: 브라우저 접속
`http://localhost:8501`

## 장점
- 코드 편집과 실행을 동시에
- 포트 포워딩 자동 설정
- 파일 탐색기 통합
- Git 연동 가능
