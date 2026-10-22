# Simple Workflow MVP - Code Review Flow

一个基于多 Agent 协作的简单 Workflow 编排系统，实现「编码 → 审查 → 修复 → 复审」的完整代码审查流程。

## 项目目标

- 搭建 2-3 个 Agent 协作的 Workflow
- 理解 Workflow 编排、Agent 间通信、状态管理等核心概念
- 支持顺序执行、条件分支、循环、日志追踪、错误处理

## Agent 组成

| Agent | 作用 |
|-------|------|
| CodingAgent | 接收用户输入，整理成待审查代码 |
| ReviewAgent | 审查代码，输出问题和是否通过 |
| FixAgent | 根据审查意见修复代码 |

## 流程

1. 用户输入代码
2. CodingAgent 整理代码
3. ReviewAgent 审查
4. 如果审查不通过，FixAgent 修复，然后回到第 3 步
5. 如果审查通过，或者达到最大迭代次数，输出结果

## 核心概念

- **Message**：Agent 之间传递消息
- **WorkflowState**：保存当前代码、审查意见、迭代次数等状态
- **WorkflowEngine**：控制整个流程，包括顺序、分支、循环
- **Logger**：把执行过程写到 logs/run.log

## 目录结构

```text
workflow-mvp/
├── main.py
├── README.md
├── requirements.txt
├── engine/
│   ├── __init__.py
│   ├── workflow.py
│   ├── state.py
│   ├── message.py
│   └── logger.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── coding_agent.py
│   ├── review_agent.py
│   └── fix_agent.py
├── utils/
│   ├── __init__.py
│   ├── llm_client.py
│   └── parser.py
├── logs/
└── tests/
    └── test_workflow.py
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python main.py
```

输入代码，输入 `END` 结束。

## 示例

输入：

```python
def divide(a, b):
    try:
        return a / b
    except:
        print("error")
        return None
```

输出：

- 状态：DONE
- 最终代码：`except Exception:`、`logging.info(...)`
- 审查意见：审查通过

## 日志

执行过程会写到 `logs/run.log`。

## 可扩展性

- 新增 Agent：继承 `BaseAgent`，实现 `run()` 方法
- 修改流程：改 `engine/workflow.py` 里的 `WorkflowEngine.run()`

## Homework2 说明

本项目在 Homework1 的基础上，将三个 Agent 组织成一个 Workflow：

- 新增 WorkflowEngine 流程编排
- 新增 Message 消息传递
- 新增 WorkflowState 状态管理
- 支持条件分支和循环
- 支持执行日志与错误处理

## 评审标准对照

| 评审维度 | 权重 | 本项目落实情况 |
|----------|------|----------------|
| 流程完整性 | 40% | 编码→审查→修复→复审端到端跑通，状态 DONE / MAX_ITERATION_REACHED |
| Agent 协作 | 30% | 三 Agent 通过 Message 通信，WorkflowState 管理状态，logs/run.log 全程可追踪 |
| 可扩展性 | 20% | 每个 Agent 继承 BaseAgent，WorkflowEngine 只负责编排，新增 Agent 零侵入 |
| 文档 | 10% | README + Design.md + 架构图 + 流程图 |

## 与项目一的关系

| 项目一模块 | 本项目中的角色 |
|------------|----------------|
| CodingAgent | 复用为编码节点 |
| ReviewAgent | 复用为审查节点 |
| FixAgent | 新增修复节点 |
| Message / WorkflowState | 在项目一基础上扩展 |
| LLMClient | 直接复用，新增重试 |