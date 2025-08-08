#!/usr/bin/env python3
"""
빠른 AWS 자격증명 테스트
configure 파일에서 자격증명을 로드하고 빠르게 검증
"""

import os
import sys
import configparser
from pathlib import Path

def load_aws_from_configure():
    """configure 파일에서 AWS 자격증명 로드"""
    config_file = Path("configure")
    
    if not config_file.exists():
        print("❌ configure 파일이 없습니다")
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
        
        print("✅ configure 파일에서 AWS 자격증명 로드 완료")
        print(f"   Access Key: {os.environ['AWS_ACCESS_KEY_ID'][:10]}...")
        print(f"   Region: {os.environ['AWS_DEFAULT_REGION']}")
        
        return True
        
    except Exception as e:
        print(f"❌ configure 파일 읽기 오류: {e}")
        return False

def test_aws_connection():
    """AWS 연결 테스트 (빠른 버전)"""
    try:
        import boto3
        from botocore.config import Config
        
        # 빠른 연결을 위한 설정
        config = Config(
            connect_timeout=5,
            read_timeout=10,
            retries={'max_attempts': 1}
        )
        
        # STS 클라이언트로 자격증명 확인
        sts = boto3.client('sts', config=config)
        response = sts.get_caller_identity()
        
        print("✅ AWS 연결 테스트 성공")
        print(f"   Account: {response.get('Account')}")
        print(f"   User ARN: {response.get('Arn')}")
        
        return True
        
    except ImportError:
        print("❌ boto3 라이브러리가 설치되지 않았습니다")
        print("   pip install boto3 명령으로 설치하세요")
        return False
        
    except Exception as e:
        print(f"❌ AWS 연결 테스트 실패: {e}")
        return False

def test_bedrock_access():
    """Bedrock 액세스 테스트"""
    try:
        import boto3
        from botocore.config import Config
        
        config = Config(
            connect_timeout=5,
            read_timeout=10,
            retries={'max_attempts': 1}
        )
        
        bedrock = boto3.client('bedrock', config=config)
        
        # 사용 가능한 모델 목록 확인 (간단한 테스트)
        response = bedrock.list_foundation_models()
        
        claude_models = [
            model for model in response.get('modelSummaries', [])
            if 'claude' in model.get('modelId', '').lower()
        ]
        
        print(f"✅ Bedrock 액세스 성공 (Claude 모델 {len(claude_models)}개 사용 가능)")
        
        return True
        
    except Exception as e:
        print(f"❌ Bedrock 액세스 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("🔍 빠른 AWS 자격증명 테스트")
    print("=" * 40)
    
    # 1. configure 파일에서 자격증명 로드
    if not load_aws_from_configure():
        sys.exit(1)
    
    print()
    
    # 2. AWS 연결 테스트
    print("🔍 AWS 연결 테스트 중...")
    if not test_aws_connection():
        sys.exit(1)
    
    print()
    
    # 3. Bedrock 액세스 테스트
    print("🔍 Bedrock 액세스 테스트 중...")
    test_bedrock_access()
    
    print()
    print("🎉 모든 테스트 완료!")
