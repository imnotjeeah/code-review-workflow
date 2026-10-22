# agents/base_agent.py
from abc import ABC, abstractmethod
from engine.state import WorkflowState
from engine.message import Message

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state: WorkflowState, message: Message = None) -> Message:
        pass