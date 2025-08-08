#!/usr/bin/env python3
"""
EC2에서 Streamlit 외부 접근 설정 도우미
"""

import requests
import subprocess
import os

def get_public_ip():
    """현재 EC2 인스턴스의 공개 IP 확인"""
    try:
        response = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4', timeout=5)
        return response.text
    except:
        return None

def get_local_ip():
    """로컬 IP 확인"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return None

def check_streamlit_running():
    """Streamlit 실행 상태 확인"""
    try:
        result = subprocess.run(['pgrep', '-f', 'streamlit'], capture_output=True, text=True)
        return len(result.stdout.strip()) > 0
    except:
        return False

def main():
    print("🔧 Streamlit 외부 접근 설정 도우미")
    print("=" * 50)
    
    # 1. IP 정보 확인
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    
    print(f"\n📍 IP 정보:")
    print(f"  EC2 공개 IP: {public_ip}")
    print(f"  로컬 공개 IP: {local_ip}")
    
    # 2. Streamlit 실행 상태 확인
    is_running = check_streamlit_running()
    print(f"\n🚀 Streamlit 상태: {'실행 중' if is_running else '중지됨'}")
    
    # 3. 해결 방법 제시
    print(f"\n🔧 해결 방법들:")
    print(f"-" * 30)
    
    print(f"\n1️⃣ SSH 터널링 (가장 간단):")
    print(f"   로컬 컴퓨터에서 실행:")
    print(f"   ssh -L 8501:localhost:8501 -i your-key.pem ec2-user@{public_ip}")
    print(f"   그 후 브라우저에서: http://localhost:8501")
    
    print(f"\n2️⃣ EC2 보안 그룹 설정:")
    print(f"   AWS 콘솔 → EC2 → 보안 그룹 → 인바운드 규칙 추가")
    print(f"   - 유형: 사용자 지정 TCP")
    print(f"   - 포트: 8501")
    print(f"   - 소스: {local_ip}/32 (본인 IP만)")
    print(f"   그 후 브라우저에서: http://{public_ip}:8501")
    
    print(f"\n3️⃣ Streamlit 실행 명령어:")
    print(f"   cd /home/ec2-user/projects/ABP/economic_news_system")
    print(f"   source /home/ec2-user/dl_env/bin/activate")
    print(f"   ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3 streamlit run streamlit_intelligence_dashboard.py --server.address 0.0.0.0 --server.port 8501")
    
    # 4. 보안 주의사항
    print(f"\n⚠️ 보안 주의사항:")
    print(f"   - 본인 IP만 허용하도록 설정")
    print(f"   - 사용 후 보안 그룹 규칙 제거")
    print(f"   - 민감한 데이터 노출 주의")
    
    # 5. 자동 실행 스크립트 생성
    script_content = f"""#!/bin/bash
# Streamlit 자동 실행 스크립트

echo "🚀 Streamlit Intelligence 대시보드 시작"
cd /home/ec2-user/projects/ABP/economic_news_system
source /home/ec2-user/dl_env/bin/activate

export ALPHA_VANTAGE_API_KEY=9TLAUWS4L3099YK3

echo "📊 대시보드 실행 중..."
echo "접근 URL: http://{public_ip}:8501"
echo "로컬 터널: http://localhost:8501"

streamlit run streamlit_intelligence_dashboard.py --server.address 0.0.0.0 --server.port 8501
"""
    
    with open('start_streamlit.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('start_streamlit.sh', 0o755)
    
    print(f"\n📝 자동 실행 스크립트 생성: start_streamlit.sh")
    print(f"   실행: ./start_streamlit.sh")

if __name__ == "__main__":
    main()
