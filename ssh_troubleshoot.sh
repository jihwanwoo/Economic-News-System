#!/bin/bash
# SSH 연결 문제 해결 스크립트

echo "🔧 SSH 연결 문제 해결"
echo "=" * 40

echo ""
echo "1️⃣ SSH 키 파일 확인:"
echo "ls -la ~/Desktop/keys/jihwanw_key.pem"
ls -la ~/Desktop/keys/jihwanw_key.pem

echo ""
echo "2️⃣ SSH 키 권한 재설정:"
echo "chmod 600 ~/Desktop/keys/jihwanw_key.pem"
chmod 600 ~/Desktop/keys/jihwanw_key.pem

echo ""
echo "3️⃣ SSH 키 파일 형식 확인:"
echo "file ~/Desktop/keys/jihwanw_key.pem"
file ~/Desktop/keys/jihwanw_key.pem

echo ""
echo "4️⃣ SSH 키 첫 줄 확인:"
echo "head -1 ~/Desktop/keys/jihwanw_key.pem"
head -1 ~/Desktop/keys/jihwanw_key.pem

echo ""
echo "5️⃣ SSH 연결 테스트 (디버그 모드):"
echo "ssh -v -o ConnectTimeout=10 -i ~/Desktop/keys/jihwanw_key.pem ec2-user@98.80.100.116 'echo Connection successful'"

echo ""
echo "🔧 해결 방법들:"
echo "=" * 20
echo ""
echo "방법 1: 키 권한 재설정"
echo "chmod 400 ~/Desktop/keys/jihwanw_key.pem"
echo ""
echo "방법 2: SSH 에이전트 사용"
echo "ssh-add ~/Desktop/keys/jihwanw_key.pem"
echo "ssh -L 8501:localhost:8501 ec2-user@98.80.100.116"
echo ""
echo "방법 3: 다른 사용자명 시도"
echo "ssh -L 8501:localhost:8501 -i ~/Desktop/keys/jihwanw_key.pem ubuntu@98.80.100.116"
echo ""
echo "방법 4: SSH 설정 파일 사용"
echo "~/.ssh/config 파일 생성"
