"""
AWS Bedrock을 활용한 경제 뉴스 자동 생성 에이전트
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from .strands_agent import BaseStrandAgent, StrandContext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_monitoring.event_detector import EconomicEvent, EventType

class BedrockNewsGenerationAgent(BaseStrandAgent):
    """AWS Bedrock을 활용한 뉴스 생성 에이전트"""
    
    def __init__(self, region_name: str = "us-east-1"):
        super().__init__("news_generator", "Economic News Generator")
        self.region_name = region_name
        self.bedrock_client = None
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude 3 Sonnet
        
    async def pre_execute(self, context: StrandContext) -> bool:
        """Bedrock 클라이언트 초기화"""
        try:
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region_name
            )
            self.logger.info("Bedrock client initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            return False
    
    async def execute(self, context: StrandContext) -> Dict[str, Any]:
        """뉴스 생성 실행"""
        try:
            # 입력 데이터에서 경제 이벤트 정보 추출
            event_data = context.input_data.get('economic_event')
            market_analysis = context.shared_memory.get('market_analysis', {})
            
            if not event_data:
                raise ValueError("Economic event data is required")
            
            # 뉴스 기사 생성
            news_article = await self._generate_news_article(event_data, market_analysis)
            
            # 헤드라인 생성
            headline = await self._generate_headline(event_data, news_article)
            
            # 요약 생성
            summary = await self._generate_summary(news_article)
            
            # 태그 생성
            tags = await self._generate_tags(event_data, news_article)
            
            result = {
                'headline': headline,
                'article': news_article,
                'summary': summary,
                'tags': tags,
                'generated_at': datetime.now().isoformat(),
                'event_id': event_data.get('event_id'),
                'word_count': len(news_article.split())
            }
            
            # 공유 메모리에 결과 저장
            context.shared_memory['generated_news'] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"News generation failed: {str(e)}")
            raise
    
    async def _generate_news_article(self, event_data: Dict[str, Any], 
                                   market_analysis: Dict[str, Any]) -> str:
        """뉴스 기사 본문 생성"""
        
        # 프롬프트 구성
        prompt = self._build_article_prompt(event_data, market_analysis)
        
        # Bedrock API 호출
        response = await self._call_bedrock(prompt, max_tokens=2000)
        
        return response.strip()
    
    async def _generate_headline(self, event_data: Dict[str, Any], article: str) -> str:
        """헤드라인 생성"""
        
        prompt = f"""
다음 경제 뉴스 기사에 대한 매력적이고 정확한 헤드라인을 생성해주세요.

이벤트 정보:
- 대상: {event_data.get('name', 'N/A')}
- 이벤트 유형: {event_data.get('event_type', 'N/A')}
- 변화율: {event_data.get('change_percent', 0):.2f}%
- 심각도: {event_data.get('severity', 0):.2f}

기사 내용:
{article[:500]}...

요구사항:
1. 15-20단어 내외로 작성
2. 구체적인 수치 포함
3. 독자의 관심을 끌 수 있는 표현 사용
4. 객관적이고 정확한 정보 전달

헤드라인:"""

        response = await self._call_bedrock(prompt, max_tokens=100)
        return response.strip().replace('"', '').replace("헤드라인:", "").strip()
    
    async def _generate_summary(self, article: str) -> str:
        """기사 요약 생성"""
        
        prompt = f"""
다음 경제 뉴스 기사를 2-3문장으로 요약해주세요.

기사:
{article}

요구사항:
1. 핵심 내용만 간결하게 정리
2. 구체적인 수치와 사실 포함
3. 독자가 빠르게 이해할 수 있도록 작성

요약:"""

        response = await self._call_bedrock(prompt, max_tokens=200)
        return response.strip()
    
    async def _generate_tags(self, event_data: Dict[str, Any], article: str) -> List[str]:
        """기사 태그 생성"""
        
        prompt = f"""
다음 경제 뉴스 기사에 적합한 태그들을 생성해주세요.

이벤트 정보:
- 대상: {event_data.get('name', 'N/A')}
- 이벤트 유형: {event_data.get('event_type', 'N/A')}

기사:
{article[:300]}...

요구사항:
1. 5-8개의 태그 생성
2. 관련 키워드, 업종, 시장 등 포함
3. 검색에 유용한 태그들로 구성
4. 쉼표로 구분하여 나열

태그:"""

        response = await self._call_bedrock(prompt, max_tokens=100)
        tags = [tag.strip() for tag in response.strip().split(',')]
        return [tag for tag in tags if tag and len(tag) > 1][:8]
    
    def _build_article_prompt(self, event_data: Dict[str, Any], 
                            market_analysis: Dict[str, Any]) -> str:
        """기사 생성용 프롬프트 구성"""
        
        event_type_descriptions = {
            'surge': '급등',
            'drop': '급락',
            'volatility': '높은 변동성',
            'volume_spike': '거래량 급증',
            'correlation_break': '상관관계 이탈'
        }
        
        event_type_kr = event_type_descriptions.get(
            event_data.get('event_type', ''), 
            event_data.get('event_type', '')
        )
        
        prompt = f"""
당신은 경제 전문 기자입니다. 다음 경제 이벤트에 대한 전문적이고 객관적인 뉴스 기사를 작성해주세요.

=== 이벤트 정보 ===
- 대상: {event_data.get('name', 'N/A')} ({event_data.get('symbol', 'N/A')})
- 이벤트 유형: {event_type_kr}
- 현재가: {event_data.get('current_price', 0):,.2f}
- 변화율: {event_data.get('change_percent', 0):+.2f}%
- 거래량: {event_data.get('volume', 0):,}
- 심각도: {event_data.get('severity', 0):.2f}/1.0
- 발생 시간: {event_data.get('timestamp', 'N/A')}

=== 기술적 분석 정보 ===
{json.dumps(event_data.get('technical_indicators', {}), indent=2, ensure_ascii=False)}

=== 시장 컨텍스트 ===
{json.dumps(event_data.get('market_context', {}), indent=2, ensure_ascii=False)}

=== 추가 분석 정보 ===
{json.dumps(market_analysis, indent=2, ensure_ascii=False)}

=== 기사 작성 요구사항 ===
1. 구조: 리드 문단 → 상세 분석 → 시장 영향 → 전망
2. 길이: 800-1200단어
3. 톤: 전문적이고 객관적
4. 포함 요소:
   - 구체적인 수치와 데이터
   - 기술적 분석 내용
   - 시장 전문가 관점
   - 투자자들에게 미칠 영향
   - 향후 전망과 주의사항

5. 문체: 신문 기사 형식, 명확하고 간결한 문장
6. 객관성: 추측보다는 사실에 기반한 분석

기사:"""

        return prompt
    
    async def _call_bedrock(self, prompt: str, max_tokens: int = 1000) -> str:
        """Bedrock API 호출"""
        try:
            # Claude 3 모델용 메시지 형식
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": messages,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                raise Exception("No content in Bedrock response")
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                self.logger.error("Access denied to Bedrock. Check your AWS credentials and permissions.")
                # 테스트용 더미 응답
                return self._generate_dummy_response(prompt)
            else:
                self.logger.error(f"Bedrock API error: {error_code}")
                raise
        except Exception as e:
            self.logger.error(f"Bedrock call failed: {str(e)}")
            # 테스트용 더미 응답
            return self._generate_dummy_response(prompt)
    
    def _generate_dummy_response(self, prompt: str) -> str:
        """테스트용 더미 응답 생성"""
        if "헤드라인" in prompt:
            return "경제 지표 급변동 발생, 시장 주목"
        elif "요약" in prompt:
            return "주요 경제 지표에서 급격한 변동이 발생했습니다. 투자자들의 관심이 집중되고 있으며, 시장 동향을 주의 깊게 살펴볼 필요가 있습니다."
        elif "태그" in prompt:
            return "경제, 주식, 시장동향, 투자, 금융"
        else:
            return """
[더미 뉴스 기사]

경제 시장에서 주목할 만한 변동이 발생했습니다. 

최근 시장 데이터에 따르면, 주요 경제 지표에서 상당한 움직임이 관찰되고 있습니다. 이러한 변화는 투자자들과 시장 참여자들에게 중요한 신호로 받아들여지고 있습니다.

전문가들은 이번 변동의 배경에 대해 다양한 분석을 제시하고 있습니다. 기술적 분석 관점에서 볼 때, 현재의 시장 상황은 여러 지표들이 복합적으로 작용한 결과로 보입니다.

시장 참여자들은 향후 동향을 주의 깊게 관찰하며, 적절한 투자 전략을 수립할 필요가 있습니다. 특히 리스크 관리와 포트폴리오 다변화의 중요성이 더욱 부각되고 있습니다.

앞으로의 시장 전망에 대해서는 신중한 접근이 필요하며, 지속적인 모니터링과 분석이 요구됩니다.

※ 이는 테스트용 더미 기사입니다. 실제 Bedrock 연동 시 전문적인 기사가 생성됩니다.
"""

class NewsStructureAgent(BaseStrandAgent):
    """뉴스 구조화 및 포맷팅 에이전트"""
    
    def __init__(self):
        super().__init__("news_formatter", "News Structure Formatter")
        self.add_dependency("news_generator")
    
    async def execute(self, context: StrandContext) -> Dict[str, Any]:
        """뉴스 구조화 실행"""
        try:
            generated_news = context.shared_memory.get('generated_news')
            if not generated_news:
                raise ValueError("Generated news not found in shared memory")
            
            # HTML 형식으로 구조화
            structured_news = self._format_to_html(generated_news)
            
            # JSON 형식으로도 구조화
            json_news = self._format_to_json(generated_news)
            
            # 메타데이터 추가
            metadata = self._generate_metadata(generated_news)
            
            result = {
                'html_format': structured_news,
                'json_format': json_news,
                'metadata': metadata,
                'formatted_at': datetime.now().isoformat()
            }
            
            context.shared_memory['formatted_news'] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"News formatting failed: {str(e)}")
            raise
    
    def _format_to_html(self, news_data: Dict[str, Any]) -> str:
        """HTML 형식으로 포맷팅"""
        html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{news_data['headline']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
        .headline {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
        .summary {{ font-style: italic; margin-bottom: 20px; padding: 10px; background-color: #f5f5f5; }}
        .article {{ text-align: justify; }}
        .tags {{ margin-top: 20px; }}
        .tag {{ display: inline-block; background-color: #007bff; color: white; padding: 2px 8px; margin: 2px; border-radius: 3px; font-size: 12px; }}
        .metadata {{ margin-top: 30px; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="headline">{news_data['headline']}</div>
    <div class="summary">{news_data['summary']}</div>
    <div class="article">{news_data['article'].replace(chr(10), '<br>')}</div>
    <div class="tags">
        {''.join([f'<span class="tag">{tag}</span>' for tag in news_data.get('tags', [])])}
    </div>
    <div class="metadata">
        생성일시: {news_data['generated_at']}<br>
        단어 수: {news_data['word_count']}개
    </div>
</body>
</html>
"""
        return html
    
    def _format_to_json(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """JSON 형식으로 포맷팅"""
        return {
            "article": {
                "headline": news_data['headline'],
                "summary": news_data['summary'],
                "content": news_data['article'],
                "tags": news_data.get('tags', []),
                "metadata": {
                    "generated_at": news_data['generated_at'],
                    "word_count": news_data['word_count'],
                    "event_id": news_data.get('event_id')
                }
            }
        }
    
    def _generate_metadata(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """메타데이터 생성"""
        return {
            "content_type": "economic_news",
            "language": "ko",
            "word_count": news_data['word_count'],
            "estimated_reading_time": max(1, news_data['word_count'] // 200),  # 분 단위
            "tags_count": len(news_data.get('tags', [])),
            "generated_at": news_data['generated_at'],
            "event_id": news_data.get('event_id')
        }

# 테스트 함수
async def test_news_generation():
    """뉴스 생성 에이전트 테스트"""
    from .strands_agent import StrandOrchestrator, create_strand_id
    
    # 샘플 경제 이벤트 데이터
    sample_event = {
        'event_id': 'TEST_001',
        'symbol': '^KS11',
        'name': 'KOSPI',
        'event_type': 'surge',
        'current_price': 3150.0,
        'change_percent': 2.5,
        'volume': 500000,
        'severity': 0.8,
        'timestamp': datetime.now().isoformat(),
        'technical_indicators': {
            'rsi': 65.5,
            'sma_20': 3100.0,
            'bollinger_position': 0.8
        },
        'market_context': {
            'market_cap': 2000000000000,
            'previous_close': 3073.0
        }
    }
    
    # Strands 오케스트레이터 설정
    orchestrator = StrandOrchestrator()
    
    # 에이전트들 생성 및 등록
    news_generator = BedrockNewsGenerationAgent()
    news_formatter = NewsStructureAgent()
    
    orchestrator.register_agent(news_generator)
    orchestrator.register_agent(news_formatter)
    
    # 실행
    strand_id = create_strand_id()
    input_data = {'economic_event': sample_event}
    
    context = await orchestrator.execute_strand(strand_id, input_data)
    
    print(f"Execution Status: {context.status}")
    if context.status.value == "completed":
        print("\n=== Generated News ===")
        news_result = context.results.get('news_generator', {})
        print(f"Headline: {news_result.get('headline', 'N/A')}")
        print(f"Summary: {news_result.get('summary', 'N/A')}")
        print(f"Tags: {', '.join(news_result.get('tags', []))}")
        print(f"Word Count: {news_result.get('word_count', 0)}")
        
        # HTML 파일로 저장
        formatted_result = context.results.get('news_formatter', {})
        if formatted_result:
            html_content = formatted_result.get('html_format', '')
            with open('/home/ec2-user/projects/ABP/economic_news_system/logs/sample_news.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("\nHTML 파일이 저장되었습니다: logs/sample_news.html")
    else:
        print(f"Error: {context.error}")

if __name__ == "__main__":
    asyncio.run(test_news_generation())
