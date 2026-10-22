# agents/review_agent.py
from agents.base_agent import BaseAgent
from engine.state import WorkflowState
from engine.message import Message

class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReviewAgent")

    def run(self, state: WorkflowState, message: Message = None) -> Message:
        code = message.content if message else state.current_code

        # MVP：用简单规则模拟审查；高分版可接 LLM
        issues = []
        if "eval(" in code:
            issues.append("严重：使用了 eval，存在安全风险")
        if "except:" in code:
            issues.append("中等：捕获异常过于宽泛")
        if "print(" in code and "def " in code:
            issues.append("轻微：函数内直接 print，建议使用 logging")
        if "TODO" in code:
            issues.append("轻微：存在未完成 TODO")

        if issues:
            review_result = "\n".join(issues)
            passed = False
        else:
            review_result = "审查通过，未发现明显问题。"
            passed = True

        state.review_comments = review_result
        state.status = "REVIEWED"
        state.add_history("review", self.name, code, review_result)

        return Message(
            sender=self.name,
            receiver="WorkflowEngine",
            content=review_result,
            msg_type="review_result",
            metadata={"passed": passed, "issues_count": len(issues)}
        )