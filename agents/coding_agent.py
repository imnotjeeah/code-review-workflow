# agents/coding_agent.py
from agents.base_agent import BaseAgent
from engine.state import WorkflowState
from engine.message import Message

class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodingAgent")

    def run(self, state: WorkflowState, message: Message = None) -> Message:
        if message and message.content:
            raw_code = message.content
        else:
            raw_code = state.original_input

        # MVP：这里可以接 LLM，也可以先用规则整理
        code = raw_code.strip()
        if not code:
            code = "def add(a, b):\n    return a + b\n"

        state.current_code = code
        state.status = "CODED"
        state.add_history("coding", self.name, raw_code, code)

        return Message(
            sender=self.name,
            receiver="ReviewAgent",
            content=code,
            msg_type="code",
            metadata={"stage": "initial_code"}
        )