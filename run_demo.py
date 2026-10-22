from engine.workflow import WorkflowEngine

if __name__ == "__main__":
    code = """
def divide(a, b):
    return a / b
"""
    engine = WorkflowEngine()
    state = engine.run(code)
    print("状态:", state.status)
    print("迭代次数:", state.iteration)
    print("最终代码:\n", state.final_output)