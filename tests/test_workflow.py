import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.workflow import WorkflowEngine


def test_workflow_runs():
    """测试 Workflow 能跑通。"""
    engine = WorkflowEngine()
    code = """
def divide(a, b):
    try:
        return a / b
    except:
        print("error")
        return None
"""
    state = engine.run(code)
    assert state.status in ["DONE", "MAX_ITERATION_REACHED", "ERROR"]
    assert state.final_output is not None


def test_review_passed():
    """测试无问题代码能通过审查。"""
    engine = WorkflowEngine()
    code = "def add(a, b):\n    return a + b\n"
    state = engine.run(code)
    assert state.status == "DONE"


def test_fix_loop():
    """测试有问题代码会触发修复循环。"""
    engine = WorkflowEngine()
    code = """
def divide(a, b):
    try:
        return a / b
    except:
        print("error")
        return None
"""
    state = engine.run(code)
    assert state.iteration >= 1