# 🌐 EC2 보안 그룹으로 직접 접속하기

## SSH 터널링에 문제가 있을 때 사용하는 방법

### 1단계: AWS 콘솔에서 보안 그룹 설정

1. **AWS 콘솔 → EC2 → 보안 그룹**
2. **현재 인스턴스의 보안 그룹 선택**
3. **"인바운드 규칙" → "인바운드 규칙 편집"**
4. **"규칙 추가" 클릭**

새 규칙 설정:
- **유형**: 사용자 지정 TCP
- **포트 범위**: 8501
- **소스**: 내 IP (권장) 또는 0.0.0.0/0 (모든 곳)
- **설명**: Streamlit Dashboard

### 2단계: 브라우저에서 직접 접속

```
http://98.80.100.116:8501
```

### 3단계: 테스트 후 보안 규칙 삭제 (권장)

보안을 위해 테스트 완료 후 8501 포트 규칙을 삭제하세요.

## ⚠️ 보안 주의사항

- 가능하면 "내 IP"만 허용하세요
- 테스트 완료 후 규칙을 삭제하세요
- SSH 터널링이 더 안전한 방법입니다

## 🔧 AWS CLI로 설정 (선택사항)

```bash
# 보안 그룹 ID 확인
aws ec2 describe-instances --instance-ids i-your-instance-id

# 8501 포트 열기 (내 IP만)
aws ec2 authorize-security-group-ingress \
  --group-id sg-your-security-group-id \
  --protocol tcp \
  --port 8501 \
  --cidr YOUR-IP/32

# 테스트 후 규칙 삭제
aws ec2 revoke-security-group-ingress \
  --group-id sg-your-security-group-id \
  --protocol tcp \
  --port 8501 \
  --cidr YOUR-IP/32
```
