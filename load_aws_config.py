#!/usr/bin/env python3
"""
AWS 자격증명 로더
configure 파일에서 AWS 자격증명을 읽어와 환경변수로 설정
"""

import os
import configparser
from pathlib import Path

def load_aws_credentials():
    """configure 파일에서 AWS 자격증명을 로드하여 환경변수로 설정"""
    
    config_file = Path(__file__).parent / "configure"
    
    if not config_file.exists():
        print(f"❌ configure 파일을 찾을 수 없습니다: {config_file}")
        return False
    
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        
        if 'aws' not in config:
            print("❌ configure 파일에 [aws] 섹션이 없습니다")
            return False
        
        aws_config = config['aws']
        
        # 환경변수 설정
        os.environ['AWS_ACCESS_KEY_ID'] = aws_config.get('aws_access_key_id', '')
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_config.get('aws_secret_access_key', '')
        os.environ['AWS_DEFAULT_REGION'] = aws_config.get('aws_default_region', 'us-east-1')
        
        print("✅ AWS 자격증명이 configure 파일에서 성공적으로 로드되었습니다")
        print(f"   - Access Key ID: {os.environ['AWS_ACCESS_KEY_ID'][:10]}...")
        print(f"   - Region: {os.environ['AWS_DEFAULT_REGION']}")
        
        return True
        
    except Exception as e:
        print(f"❌ configure 파일 읽기 오류: {e}")
        return False

def verify_aws_credentials():
    """AWS 자격증명 유효성 검증"""
    try:
        import boto3
        
        # STS 클라이언트로 자격증명 확인
        sts = boto3.client('sts')
        response = sts.get_caller_identity()
        
        print("✅ AWS 자격증명 검증 성공")
        print(f"   - Account: {response.get('Account')}")
        print(f"   - User ARN: {response.get('Arn')}")
        
        return True
        
    except Exception as e:
        print(f"❌ AWS 자격증명 검증 실패: {e}")
        return False

if __name__ == "__main__":
    print("🔍 AWS 자격증명 로드 중...")
    
    if load_aws_credentials():
        print("\n🔍 AWS 자격증명 검증 중...")
        verify_aws_credentials()
    else:
        print("❌ AWS 자격증명 로드 실패")
