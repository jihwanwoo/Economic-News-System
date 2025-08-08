#!/usr/bin/env python3
"""
SSH 터널링 설정 가이드 생성기
"""

import os
import subprocess
import platform

def get_system_info():
    """시스템 정보 확인"""
    return {
        'os': platform.system(),
        'platform': platform.platform(),
        'python_version': platform.python_version()
    }

def check_ssh_key():
    """SSH 키 파일 확인"""
    common_paths = [
        '~/.ssh/id_rsa',
        '~/.ssh/id_ed25519',
        '~/Downloads/*.pem',
        '~/.aws/*.pem'
    ]
    
    found_keys = []
    for path in common_paths:
        expanded_path = os.path.expanduser(path)
        if '*' in expanded_path:
            import glob
            found_keys.extend(glob.glob(expanded_path))
        elif os.path.exists(expanded_path):
            found_keys.append(expanded_path)
    
    return found_keys

def generate_tunnel_commands():
    """터널링 명령어 생성"""
    
    print("🔧 SSH 터널링 완전 가이드")
    print("=" * 60)
    
    # 시스템 정보
    sys_info = get_system_info()
    print(f"\n💻 시스템 정보:")
    print(f"  OS: {sys_info['os']}")
    print(f"  플랫폼: {sys_info['platform']}")
    
    # SSH 키 확인
    print(f"\n🔑 SSH 키 파일 확인:")
    ssh_keys = check_ssh_key()
    if ssh_keys:
        print(f"  발견된 키 파일들:")
        for key in ssh_keys:
            print(f"    - {key}")
    else:
        print(f"  ⚠️ 일반적인 위치에서 SSH 키를 찾을 수 없습니다.")
    
    print(f"\n" + "=" * 60)
    print(f"📖 단계별 SSH 터널링 가이드")
    print(f"=" * 60)
    
    # 1단계: 준비사항
    print(f"\n1️⃣ 준비사항 확인")
    print(f"-" * 30)
    print(f"✅ EC2 인스턴스의 공개 IP 주소")
    print(f"✅ EC2 접속용 SSH 키 파일 (.pem)")
    print(f"✅ 로컬 컴퓨터의 터미널/명령 프롬프트")
    
    # 2단계: SSH 터널 생성
    print(f"\n2️⃣ SSH 터널 생성")
    print(f"-" * 30)
    
    if sys_info['os'] == 'Windows':
        print(f"🪟 Windows 사용자:")
        print(f"  PowerShell 또는 Git Bash에서 실행:")
        print(f"  ssh -L 8501:localhost:8501 -i \"C:\\path\\to\\your-key.pem\" ec2-user@YOUR_EC2_IP")
        print(f"")
        print(f"  예시:")
        print(f"  ssh -L 8501:localhost:8501 -i \"C:\\Users\\YourName\\Downloads\\my-key.pem\" ec2-user@1.2.3.4")
    else:
        print(f"🐧 Linux/Mac 사용자:")
        print(f"  터미널에서 실행:")
        print(f"  ssh -L 8501:localhost:8501 -i /path/to/your-key.pem ec2-user@YOUR_EC2_IP")
        print(f"")
        print(f"  예시:")
        print(f"  ssh -L 8501:localhost:8501 -i ~/.ssh/my-key.pem ec2-user@1.2.3.4")
    
    # 3단계: 권한 설정
    print(f"\n3️⃣ SSH 키 권한 설정 (Linux/Mac)")
    print(f"-" * 30)
    print(f"  chmod 400 /path/to/your-key.pem")
    
    # 4단계: 터널 연결 확인
    print(f"\n4️⃣ 터널 연결 확인")
    print(f"-" * 30)
    print(f"  성공 시 다음과 같은 메시지가 나타납니다:")
    print(f"  'Welcome to Ubuntu...' 또는 EC2 로그인 프롬프트")
    print(f"  터널이 백그라운드에서 실행됩니다.")
    
    # 5단계: Streamlit 실행
    print(f"\n5️⃣ EC2에서 Streamlit 실행")
    print(f"-" * 30)
    print(f"  SSH 연결된 터미널에서:")
    print(f"  cd /home/ec2-user/projects/ABP/economic_news_system")
    print(f"  source /home/ec2-user/dl_env/bin/activate")
    print(f"  ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3 streamlit run streamlit_intelligence_dashboard.py")
    
    # 6단계: 브라우저 접근
    print(f"\n6️⃣ 로컬 브라우저에서 접근")
    print(f"-" * 30)
    print(f"  브라우저 주소창에 입력:")
    print(f"  http://localhost:8501")
    print(f"  또는")
    print(f"  http://127.0.0.1:8501")
    
    # 문제 해결
    print(f"\n🔧 문제 해결")
    print(f"-" * 30)
    print(f"❌ 'Permission denied (publickey)' 오류:")
    print(f"   - SSH 키 파일 경로 확인")
    print(f"   - 키 파일 권한 확인 (chmod 400)")
    print(f"   - EC2 IP 주소 확인")
    print(f"")
    print(f"❌ 'Connection refused' 오류:")
    print(f"   - EC2 인스턴스가 실행 중인지 확인")
    print(f"   - 보안 그룹에서 SSH(22) 포트 허용 확인")
    print(f"")
    print(f"❌ 'localhost:8501'에 접근 안됨:")
    print(f"   - SSH 터널이 정상 연결되었는지 확인")
    print(f"   - EC2에서 Streamlit이 실행 중인지 확인")
    print(f"   - 방화벽 설정 확인")
    
    # 고급 옵션
    print(f"\n🚀 고급 옵션")
    print(f"-" * 30)
    print(f"백그라운드 실행:")
    print(f"  ssh -L 8501:localhost:8501 -i your-key.pem -f -N ec2-user@YOUR_EC2_IP")
    print(f"")
    print(f"여러 포트 터널링:")
    print(f"  ssh -L 8501:localhost:8501 -L 8502:localhost:8502 -i your-key.pem ec2-user@YOUR_EC2_IP")
    print(f"")
    print(f"터널 종료:")
    print(f"  ps aux | grep ssh")
    print(f"  kill [SSH_PROCESS_ID]")
    
    # 자동화 스크립트 생성
    print(f"\n📝 자동화 스크립트 생성")
    print(f"-" * 30)
    
    if sys_info['os'] == 'Windows':
        script_content = """@echo off
echo 🔧 SSH 터널링 시작...
echo.
echo ⚠️ 다음 정보를 입력하세요:
set /p EC2_IP="EC2 IP 주소: "
set /p KEY_PATH="SSH 키 파일 경로: "

echo.
echo 🚀 터널 생성 중...
ssh -L 8501:localhost:8501 -i "%KEY_PATH%" ec2-user@%EC2_IP%

pause"""
        
        with open('ssh_tunnel.bat', 'w') as f:
            f.write(script_content)
        print(f"  Windows 배치 파일 생성: ssh_tunnel.bat")
    
    else:
        script_content = """#!/bin/bash
echo "🔧 SSH 터널링 시작..."
echo
echo "⚠️ 다음 정보를 입력하세요:"
read -p "EC2 IP 주소: " EC2_IP
read -p "SSH 키 파일 경로: " KEY_PATH

echo
echo "🚀 터널 생성 중..."
ssh -L 8501:localhost:8501 -i "$KEY_PATH" ec2-user@$EC2_IP"""
        
        with open('ssh_tunnel.sh', 'w') as f:
            f.write(script_content)
        os.chmod('ssh_tunnel.sh', 0o755)
        print(f"  Linux/Mac 스크립트 생성: ssh_tunnel.sh")
        print(f"  실행: ./ssh_tunnel.sh")

if __name__ == "__main__":
    generate_tunnel_commands()
