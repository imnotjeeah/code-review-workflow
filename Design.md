# Design.md

## 1. 项目目标

搭建一个 2-3 个 Agent 协作的简单 Workflow，理解 Workflow 编排、Agent 间通信、状态管理等核心概念。

## 2. 选题

代码审查流程：编码 → 审查 → 修复。

## 3. 总体设计

### 3.1 架构图

```text
用户输入
   ↓
WorkflowEngine
   ↓
CodingAgent → ReviewAgent → 判断是否通过
                              ↓ 不通过
                           FixAgent
                              ↓
                           ReviewAgent（复审）
                              ↓ 通过
                           输出结果
```

### 3.2 模块划分

| 模块 | 职责 |
|------|------|
| WorkflowEngine | 流程编排、条件分支、循环控制 |
| WorkflowState | 全局状态管理 |
| Message | Agent 间通信载体 |
| BaseAgent | Agent 抽象基类 |
| CodingAgent | 整理代码 |
| ReviewAgent | 审查代码 |
| FixAgent | 修复代码 |
| Logger | 日志与状态追踪 |

### 3.3 Agent 间通信

Agent 之间不直接调用，而是通过 Message 传递数据。

```python
Message(
    sender="ReviewAgent",
    receiver="WorkflowEngine",
    content="审查意见...",
    msg_type="review_result",
    metadata={"passed": False}
)
```

WorkflowEngine 根据 `metadata.passed` 决定下一步。

### 3.4 状态管理

WorkflowState 保存：

- `original_input`：用户原始输入
- `current_code`：当前代码
- `review_comments`：审查意见
- `iteration`：迭代次数
- `max_iterations`：最大迭代次数
- `history`：执行历史
- `status`：当前状态

### 3.5 流程控制

- 顺序执行：CodingAgent → ReviewAgent
- 条件分支：审查通过 → 输出；不通过 → FixAgent
- 循环：FixAgent → ReviewAgent，直到通过或达到最大迭代

### 3.6 错误处理

- LLMClient 调用失败重试 3 次
- WorkflowEngine 用 try/except 捕获异常
- 出错时状态标记为 `ERROR`
- 保留当前已有代码
- 日志记录错误信息

## 4. 可扩展性

- 新增 Agent：继承 BaseAgent，实现 `run()`
- 修改流程：在 WorkflowEngine 中调整
- 可接入 LLM：修改各 Agent 的 `run()`

## 5. 运行说明

见 README.md。

## 6. 总结

本项目实现了一个可运行的简单 Workflow MVP，满足 Homework2 的基本要求，并支持条件分支、循环、日志追踪和错误处理。