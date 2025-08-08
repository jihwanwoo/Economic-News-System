# EC2 보안 그룹 설정 가이드

## AWS 콘솔에서 설정하기

### 1단계: EC2 콘솔 접속
1. AWS 콘솔 → EC2 서비스 이동
2. 왼쪽 메뉴에서 "보안 그룹" 클릭

### 2단계: 보안 그룹 편집
1. 현재 EC2 인스턴스에 연결된 보안 그룹 선택
2. "인바운드 규칙" 탭 클릭
3. "인바운드 규칙 편집" 버튼 클릭

### 3단계: Streamlit 포트 추가
새 규칙 추가:
- **유형**: 사용자 지정 TCP
- **포트 범위**: 8501
- **소스**: 
  - 개인 IP만 허용 (권장): [내 IP]/32
  - 모든 곳에서 허용 (주의): 0.0.0.0/0
- **설명**: Streamlit Dashboard

### 4단계: 규칙 저장
"규칙 저장" 버튼 클릭

## AWS CLI로 설정하기 (선택사항)

```bash
# 보안 그룹 ID 확인
aws ec2 describe-instances --instance-ids [INSTANCE-ID] \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId'

# 인바운드 규칙 추가 (내 IP만 허용)
aws ec2 authorize-security-group-ingress \
  --group-id [SECURITY-GROUP-ID] \
  --protocol tcp \
  --port 8501 \
  --cidr [YOUR-IP]/32

# 또는 모든 IP 허용 (보안 위험)
aws ec2 authorize-security-group-ingress \
  --group-id [SECURITY-GROUP-ID] \
  --protocol tcp \
  --port 8501 \
  --cidr 0.0.0.0/0
```

## ⚠️ 보안 주의사항
- 가능하면 특정 IP만 허용하세요
- 테스트 후 불필요한 규칙은 삭제하세요
- SSH 터널링이 더 안전한 방법입니다
