# AI Agent 中高级工程进修

这是一个长期学习实验室，面向 AI Agent 初学者，目标是从基础概念和最小实验开始，逐步具备中高级 AI Agent 工程师的能力：架构设计、运行时实现、工具安全、上下文工程、检索与记忆、评测、可观测性和生产化交付。

## 学习原则

1. 先理解事件链和状态变化，再使用框架。
2. 每个主题都必须有可运行实验、测试、设计记录和复盘。
3. 以失败场景验证能力，不以 Demo 能运行作为完成标准。
4. 保留每次学习的决策、疑问、证据和下一步，保证可以连续接续。
5. 优先建立通用工程能力，不追逐短期变化的框架 API。
6. 不默认学习者已经理解大模型、Agent 或后端术语；每个新概念都先用具体例子解释。

## 从哪里开始

- 学习路线：[docs/roadmap.md](docs/roadmap.md)
- 前十二课：[docs/curriculum.md](docs/curriculum.md)
- 全阶段课程地图：[docs/curriculum-map.md](docs/curriculum-map.md)
- 外部参考仓库：[docs/reference-repositories.md](docs/reference-repositories.md)
- 提交与接续规则：[docs/commit-workflow.md](docs/commit-workflow.md)
- 教学质量契约：[docs/curriculum-governance.md](docs/curriculum-governance.md)
- 当前进度：[docs/progress.md](docs/progress.md)
- 能力验收：[docs/assessment.md](docs/assessment.md)
- 复习节奏：[docs/review-cadence.md](docs/review-cadence.md)
- 贯穿式项目：[docs/capstone.md](docs/capstone.md)
- 每次学习模板：[docs/lesson-template.md](docs/lesson-template.md)
- 实验规范：[docs/experiment-guidelines.md](docs/experiment-guidelines.md)
- 学习日志索引：[learning-log/README.md](learning-log/README.md)
- 实验目录：[experiments/](experiments/)

第一次进入仓库时，依次阅读“当前进度 → 当前课次 → 最近一篇学习日志”；日常学习不需要从头重读全部路线。

## 每次学习的固定闭环

```text
目标 → 原理 → 最小实验 → 故障实验 → 测试 → 复盘 → 更新进度 → 下一步
```

## 本地环境

```bash
uv sync
uv run pytest
```

复制 `.env.example` 为 `.env` 后再填写本地密钥；`.env` 不进入 Git。
