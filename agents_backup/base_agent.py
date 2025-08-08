"""
경제 뉴스 시스템의 기본 Agent 클래스
"""

import boto3
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Agent 설정 모델"""
    name: str = Field(..., description="Agent 이름")
    model_id: str = Field(default="anthropic.claude-3-sonnet-20240229-v1:0", description="Bedrock 모델 ID")
    region: str = Field(default="us-east-1", description="AWS 리전")
    temperature: float = Field(default=0.7, description="모델 온도")
    max_tokens: int = Field(default=4000, description="최대 토큰 수")


class BaseAgent(ABC):
    """경제 뉴스 시스템의 기본 Agent 클래스"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{config.name}")
        
        # AWS Bedrock 클라이언트 초기화
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=config.region
        )
        
        # LangChain ChatBedrock 초기화
        self.llm = ChatBedrock(
            client=self.bedrock_client,
            model_id=config.model_id,
            model_kwargs={
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }
        )
        
        self.logger.info(f"Agent {config.name} 초기화 완료")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """시스템 프롬프트 반환"""
        pass
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """메인 처리 로직"""
        pass
    
    def invoke_llm(self, messages: List[Dict[str, str]]) -> str:
        """LLM 호출"""
        try:
            # 메시지를 LangChain 형식으로 변환
            langchain_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
                elif msg["role"] == "user":
                    langchain_messages.append(HumanMessage(content=msg["content"]))
            
            response = self.llm.invoke(langchain_messages)
            return response.content
            
        except Exception as e:
            self.logger.error(f"LLM 호출 중 오류 발생: {str(e)}")
            raise
    
    def save_result(self, result: Dict[str, Any], output_path: str) -> None:
        """결과 저장"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            self.logger.info(f"결과 저장 완료: {output_path}")
        except Exception as e:
            self.logger.error(f"결과 저장 중 오류 발생: {str(e)}")
            raise
    
    def log_activity(self, activity: str, details: Dict[str, Any] = None) -> None:
        """활동 로그 기록"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.config.name,
            "activity": activity,
            "details": details or {}
        }
        self.logger.info(f"Activity: {json.dumps(log_entry, ensure_ascii=False)}")
