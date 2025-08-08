#!/usr/bin/env python3
"""
환경변수 설정 확인 스크립트
"""

import os

def check_environment():
    print("🔍 환경변수 설정 확인")
    print("=" * 40)
    
    # API 키 확인
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if api_key:
        print(f"✅ ALPHA_VANTAGE_API_KEY: {api_key[:8]}...{api_key[-4:]}")
    else:
        print("❌ ALPHA_VANTAGE_API_KEY: 설정되지 않음")
    
    # 기타 환경변수 확인
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'Not set')
    print(f"📍 AWS_DEFAULT_REGION: {aws_region}")
    
    # .env 파일 확인
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print(f"✅ .env 파일 존재: {env_file}")
    else:
        print(f"❌ .env 파일 없음: {env_file}")
    
    # config 파일 확인
    config_file = os.path.join(os.path.dirname(__file__), 'config', 'default.json')
    if os.path.exists(config_file):
        print(f"✅ config 파일 존재: {config_file}")
    else:
        print(f"❌ config 파일 없음: {config_file}")

if __name__ == "__main__":
    check_environment()
