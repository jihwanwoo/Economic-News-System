"""
Strands Agent 패턴 구현
- 여러 에이전트가 협력하여 복잡한 작업을 수행하는 프레임워크
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

class StrandStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class StrandMessage:
    """에이전트 간 메시지"""
    sender: str
    receiver: str
    message_type: str
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

class BaseStrandAgent(ABC):
    """Strand Agent 기본 클래스"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.logger = logging.getLogger(f"strand_agent.{agent_id}")
        self.dependencies: List[str] = []
        self.subscribers: List[str] = []
        
    @abstractmethod
    async def execute(self, context: StrandContext) -> Dict[str, Any]:
        """에이전트 실행 로직"""
        pass
    
    async def pre_execute(self, context: StrandContext) -> bool:
        """실행 전 검증"""
        return True
    
    async def post_execute(self, context: StrandContext, result: Dict[str, Any]) -> Dict[str, Any]:
        """실행 후 처리"""
        return result
    
    def add_dependency(self, agent_id: str):
        """의존성 추가"""
        if agent_id not in self.dependencies:
            self.dependencies.append(agent_id)
    
    def add_subscriber(self, agent_id: str):
        """구독자 추가"""
        if agent_id not in self.subscribers:
            self.subscribers.append(agent_id)
    
    async def send_message(self, context: StrandContext, receiver: str, 
                          message_type: str, content: Dict[str, Any]):
        """메시지 전송"""
        message = StrandMessage(
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            content=content,
            correlation_id=context.strand_id
        )
        context.messages.append(message)
        self.logger.info(f"Message sent to {receiver}: {message_type}")

class StrandOrchestrator:
    """Strand 오케스트레이터"""
    
    def __init__(self):
        self.agents: Dict[str, BaseStrandAgent] = {}
        self.execution_graph: Dict[str, List[str]] = {}
        self.logger = logging.getLogger("strand_orchestrator")
        
    def register_agent(self, agent: BaseStrandAgent):
        """에이전트 등록"""
        self.agents[agent.agent_id] = agent
        self.execution_graph[agent.agent_id] = agent.dependencies.copy()
        self.logger.info(f"Agent registered: {agent.name} ({agent.agent_id})")
    
    def build_execution_plan(self) -> List[List[str]]:
        """실행 계획 생성 (토폴로지 정렬)"""
        in_degree = {agent_id: 0 for agent_id in self.agents.keys()}
        
        # 의존성 그래프 구성
        for agent_id, dependencies in self.execution_graph.items():
            for dep in dependencies:
                if dep in in_degree:
                    in_degree[agent_id] += 1
        
        # 토폴로지 정렬
        execution_plan = []
        queue = [agent_id for agent_id, degree in in_degree.items() if degree == 0]
        
        while queue:
            current_level = queue.copy()
            queue.clear()
            execution_plan.append(current_level)
            
            for agent_id in current_level:
                # 이 에이전트에 의존하는 다른 에이전트들의 in_degree 감소
                for other_agent_id, dependencies in self.execution_graph.items():
                    if agent_id in dependencies:
                        in_degree[other_agent_id] -= 1
                        if in_degree[other_agent_id] == 0 and other_agent_id not in queue:
                            queue.append(other_agent_id)
        
        return execution_plan
    
    async def execute_strand(self, strand_id: str, input_data: Dict[str, Any]) -> StrandContext:
        """Strand 실행"""
        context = StrandContext(
            strand_id=strand_id,
            input_data=input_data,
            status=StrandStatus.RUNNING
        )
        
        try:
            execution_plan = self.build_execution_plan()
            self.logger.info(f"Execution plan: {execution_plan}")
            
            for level in execution_plan:
                # 같은 레벨의 에이전트들은 병렬 실행
                tasks = []
                for agent_id in level:
                    if agent_id in self.agents:
                        task = self._execute_agent(self.agents[agent_id], context)
                        tasks.append((agent_id, task))
                
                # 병렬 실행 및 결과 수집
                for agent_id, task in tasks:
                    try:
                        result = await task
                        context.results[agent_id] = result
                        self.logger.info(f"Agent {agent_id} completed successfully")
                    except Exception as e:
                        self.logger.error(f"Agent {agent_id} failed: {str(e)}")
                        context.status = StrandStatus.FAILED
                        context.error = f"Agent {agent_id} failed: {str(e)}"
                        return context
            
            context.status = StrandStatus.COMPLETED
            self.logger.info(f"Strand {strand_id} completed successfully")
            
        except Exception as e:
            context.status = StrandStatus.FAILED
            context.error = str(e)
            self.logger.error(f"Strand {strand_id} failed: {str(e)}")
        
        return context
    
    async def _execute_agent(self, agent: BaseStrandAgent, context: StrandContext) -> Dict[str, Any]:
        """개별 에이전트 실행"""
        try:
            # 실행 전 검증
            if not await agent.pre_execute(context):
                raise Exception(f"Pre-execution validation failed for {agent.agent_id}")
            
            # 실행
            result = await agent.execute(context)
            
            # 실행 후 처리
            final_result = await agent.post_execute(context, result)
            
            return final_result
            
        except Exception as e:
            agent.logger.error(f"Execution failed: {str(e)}")
            raise

# 유틸리티 함수들
def create_strand_id() -> str:
    """고유한 Strand ID 생성"""
    return f"strand_{int(datetime.now().timestamp() * 1000)}"

def setup_strand_logging():
    """Strand 로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# 테스트용 샘플 에이전트
class SampleAgent(BaseStrandAgent):
    async def execute(self, context: StrandContext) -> Dict[str, Any]:
        await asyncio.sleep(1)  # 작업 시뮬레이션
        return {"message": f"Hello from {self.name}", "timestamp": datetime.now().isoformat()}

# 테스트 함수
async def test_strands_framework():
    """Strands 프레임워크 테스트"""
    setup_strand_logging()
    
    orchestrator = StrandOrchestrator()
    
    # 테스트 에이전트들 생성
    agent1 = SampleAgent("agent1", "First Agent")
    agent2 = SampleAgent("agent2", "Second Agent")
    agent3 = SampleAgent("agent3", "Third Agent")
    
    # 의존성 설정 (agent3은 agent1과 agent2에 의존)
    agent3.add_dependency("agent1")
    agent3.add_dependency("agent2")
    
    # 에이전트 등록
    orchestrator.register_agent(agent1)
    orchestrator.register_agent(agent2)
    orchestrator.register_agent(agent3)
    
    # Strand 실행
    strand_id = create_strand_id()
    input_data = {"test": "data"}
    
    context = await orchestrator.execute_strand(strand_id, input_data)
    
    print(f"Strand Status: {context.status}")
    print(f"Results: {json.dumps(context.results, indent=2, default=str)}")

if __name__ == "__main__":
    asyncio.run(test_strands_framework())
