"""
Strands Agent 프레임워크 - 경제 뉴스 시스템용
여러 에이전트가 협력하여 복잡한 작업을 수행하는 프레임워크
"""

import asyncio
import logging
import boto3
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage

class StrandStatus(Enum):
    """Strand 실행 상태"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MessageType(Enum):
    """메시지 타입"""
    DATA_REQUEST = "data_request"
    DATA_RESPONSE = "data_response"
    TASK_ASSIGNMENT = "task_assignment"
    TASK_COMPLETION = "task_completion"
    ERROR_NOTIFICATION = "error_notification"
    STATUS_UPDATE = "status_update"

@dataclass
class StrandMessage:
    """에이전트 간 메시지"""
    sender: str
    receiver: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None

@dataclass
class StrandContext:
    """Strand 실행 컨텍스트"""
    strand_id: str
    input_data: Dict[str, Any]
    shared_memory: Dict[str, Any] = field(default_factory=dict)
    messages: List[StrandMessage] = field(default_factory=list)
    status: StrandStatus = StrandStatus.PENDING
    results: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

class BaseStrandAgent(ABC):
    """Strand Agent 기본 클래스"""
    
    def __init__(self, agent_id: str, name: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.agent_id = agent_id
        self.name = name
        self.model_id = model_id
        self.logger = logging.getLogger(f"strand_agent.{agent_id}")
        self.dependencies: List[str] = []
        self.capabilities: List[str] = []
        
        # AWS Bedrock 클라이언트 초기화
        try:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name='us-east-1'
            )
            
            # LangChain ChatBedrock 초기화
            self.llm = ChatBedrock(
                client=self.bedrock_client,
                model_id=model_id,
                model_kwargs={
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            )
            self.logger.info(f"✅ {name} Agent 초기화 완료")
        except Exception as e:
            self.logger.error(f"❌ {name} Agent 초기화 실패: {e}")
            self.bedrock_client = None
            self.llm = None
    
    @abstractmethod
    async def process(self, context: StrandContext, message: Optional[StrandMessage] = None) -> Dict[str, Any]:
        """에이전트의 주요 처리 로직"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """에이전트의 능력 목록 반환"""
        pass
    
    async def send_message(self, context: StrandContext, receiver: str, message_type: MessageType, content: Dict[str, Any]):
        """다른 에이전트에게 메시지 전송"""
        message = StrandMessage(
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            content=content,
            correlation_id=context.strand_id
        )
        context.messages.append(message)
        self.logger.info(f"📤 메시지 전송: {self.agent_id} -> {receiver} ({message_type.value})")
    
    async def get_shared_data(self, context: StrandContext, key: str) -> Any:
        """공유 메모리에서 데이터 조회"""
        return context.shared_memory.get(key)
    
    async def set_shared_data(self, context: StrandContext, key: str, value: Any):
        """공유 메모리에 데이터 저장"""
        context.shared_memory[key] = value
        self.logger.debug(f"💾 공유 데이터 저장: {key}")
    
    async def call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """LLM 호출"""
        if not self.llm:
            raise Exception("LLM이 초기화되지 않았습니다")
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            self.logger.error(f"❌ LLM 호출 실패: {e}")
            raise

class StrandOrchestrator:
    """Strand 오케스트레이터 - 에이전트들의 협력을 조율"""
    
    def __init__(self):
        self.agents: Dict[str, BaseStrandAgent] = {}
        self.logger = logging.getLogger("strand_orchestrator")
        self.active_strands: Dict[str, StrandContext] = {}
    
    def register_agent(self, agent: BaseStrandAgent):
        """에이전트 등록"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"🤖 에이전트 등록: {agent.name} ({agent.agent_id})")
    
    async def execute_strand(self, strand_id: str, input_data: Dict[str, Any], workflow: List[str]) -> StrandContext:
        """Strand 실행"""
        context = StrandContext(
            strand_id=strand_id,
            input_data=input_data,
            status=StrandStatus.RUNNING
        )
        
        self.active_strands[strand_id] = context
        self.logger.info(f"🚀 Strand 실행 시작: {strand_id}")
        
        try:
            # 워크플로우에 따라 에이전트들을 순차적으로 실행
            for agent_id in workflow:
                if agent_id not in self.agents:
                    raise Exception(f"에이전트를 찾을 수 없습니다: {agent_id}")
                
                agent = self.agents[agent_id]
                self.logger.info(f"🔄 에이전트 실행: {agent.name}")
                
                # 에이전트 실행
                result = await agent.process(context)
                context.results[agent_id] = result
                
                # 상태 업데이트
                await agent.set_shared_data(context, f"{agent_id}_result", result)
            
            context.status = StrandStatus.COMPLETED
            self.logger.info(f"✅ Strand 실행 완료: {strand_id}")
            
        except Exception as e:
            context.status = StrandStatus.FAILED
            context.error = str(e)
            self.logger.error(f"❌ Strand 실행 실패: {strand_id} - {e}")
        
        return context
    
    async def get_strand_status(self, strand_id: str) -> Optional[StrandContext]:
        """Strand 상태 조회"""
        return self.active_strands.get(strand_id)
    
    def list_agents(self) -> Dict[str, List[str]]:
        """등록된 에이전트 목록과 능력"""
        return {
            agent_id: agent.get_capabilities() 
            for agent_id, agent in self.agents.items()
        }

# 전역 오케스트레이터 인스턴스
orchestrator = StrandOrchestrator()
