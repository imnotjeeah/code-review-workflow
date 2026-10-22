# agents/fix_agent.py
from agents.base_agent import BaseAgent
from engine.state import WorkflowState
from engine.message import Message

class FixAgent(BaseAgent):
    def __init__(self):
        super().__init__("FixAgent")

    def run(self, state: WorkflowState, message: Message = None) -> Message:
        code = state.current_code
        comments = message.content if message else state.review_comments

        # MVP：用简单替换模拟修复；高分版可接 LLM
        fixed_code = code
        if "eval(" in fixed_code:
            fixed_code = fixed_code.replace("eval(", "ast.literal_eval(")
        if "except:" in fixed_code:
            fixed_code = fixed_code.replace("except:", "except Exception:")
        if "print(" in fixed_code:
            fixed_code = fixed_code.replace("print(", "logging.info(")

        state.fixed_code = fixed_code
        state.current_code = fixed_code
        state.status = "FIXED"
        state.iteration += 1
        state.add_history("fix", self.name, comments, fixed_code)

        return Message(
            sender=self.name,
            receiver="ReviewAgent",
            content=fixed_code,
            msg_type="fixed_code",
            metadata={"iteration": state.iteration}
        )