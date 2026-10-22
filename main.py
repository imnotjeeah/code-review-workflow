from engine.workflow import WorkflowEngine

def main():
    print("=== Simple Workflow MVP: Code Review Flow ===")
    print("请输入要审查的代码，输入 END 结束：")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    user_input = "\n".join(lines)
    engine = WorkflowEngine()
    state = engine.run(user_input)

    print("\n=== 最终结果 ===")
    print("状态:", state.status)
    print("迭代次数:", state.iteration)
    print("\n最终代码:\n", state.final_output)
    print("\n审查意见:\n", state.review_comments)
    print("\n执行历史:")
    for h in state.history:
        print(h)

if __name__ == "__main__":
    main()