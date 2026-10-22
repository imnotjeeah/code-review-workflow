# engine/state.py
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class WorkflowState:
    task_id: str
    original_input: str = ""
    current_code: str = ""
    review_comments: str = ""
    fixed_code: str = ""
    final_output: str = ""
    status: str = "INIT"
    iteration: int = 0
    max_iterations: int = 3
    history: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None

    def add_history(self, step: str, agent: str, input_data: Any, output_data: Any):
        self.history.append({
            "step": step,
            "agent": agent,
            "input": input_data,
            "output": output_data,
            "iteration": self.iteration
        })