# engine/workflow.py
from engine.state import WorkflowState
from engine.message import Message
from engine.logger import Logger
from agents.coding_agent import CodingAgent
from agents.review_agent import ReviewAgent
from agents.fix_agent import FixAgent
import uuid

class WorkflowEngine:
    def __init__(self):
        self.coding_agent = CodingAgent()
        self.review_agent = ReviewAgent()
        self.fix_agent = FixAgent()
        self.logger = Logger()

    def run(self, user_input: str) -> WorkflowState:
        state = WorkflowState(
            task_id=str(uuid.uuid4()),
            original_input=user_input,
            max_iterations=3
        )
        self.logger.log(f"Workflow started: {state.task_id}")

        try:
            # 1. 编码
            msg = Message(sender="User", receiver="CodingAgent", content=user_input)
            msg = self.coding_agent.run(state, msg)

            # 2. 审查 + 修复循环
            while state.iteration < state.max_iterations:
                msg = self.review_agent.run(state, msg)
                passed = msg.metadata.get("passed", False)

                if passed:
                    state.status = "DONE"
                    state.final_output = state.current_code
                    break

                msg = self.fix_agent.run(state, msg)

            if state.iteration >= state.max_iterations and state.status != "DONE":
                state.status = "MAX_ITERATION_REACHED"
                state.final_output = state.current_code

        except Exception as e:
            # 错误处理：记录错误，保留已有结果
            state.status = "ERROR"
            state.error = str(e)
            state.final_output = state.current_code
            self.logger.log(f"Workflow error: {e}")

        self.logger.log(f"Workflow finished: {state.status}")
        return state