# 外部参考仓库

这些仓库用于补充案例、代码风格和工程实践。它们不是本项目的主线，学习时以本仓库的课程编号、质量契约和进度文件为准。

## 推荐顺序

### 第一阶段：建立 Agent 直觉

#### [akash-pal/agent-from-scratch](https://github.com/akash-pal/agent-from-scratch)

- 语言：TypeScript
- 适合课程：01～12
- 借鉴内容：不用 Agent 框架直接实现模型调用、工具契约、评测集、循环和人工审核。
- 阅读方式：先读设计文档，再对照本仓库的事件链和失败测试；不要把它当成生产模板。

#### [hexo-ai/agent-from-scratch](https://github.com/hexo-ai/agent-from-scratch)

- 语言：Python
- 适合课程：01～09
- 借鉴内容：用很小的代码理解单 Agent 和多 Agent 的基本结构。
- 限制：代码规模较小，不能替代状态持久化、评测、权限和部署学习。

### 第二阶段：工程化 Agent

#### [ed-donner/agents](https://github.com/ed-donner/agents)

- 适合课程：13～60
- 借鉴内容：工具调用、多个 Agent 框架、MCP、部署和完整课程组织方式。
- 学习策略：一次只选择当前课程需要的框架，不并行追完所有框架。

#### [dasdatasensei/agentic-AI-engineering-course](https://github.com/dasdatasensei/agentic-AI-engineering-course)

- 适合课程：29～68
- 借鉴内容：以一个研究分析平台持续演进，覆盖 RAG、多 Agent、FastAPI、观测、安全和部署。
- 学习策略：重点观察“前一阶段产物如何进入后一阶段”，对照我们的贯穿式综合项目。

### 第三阶段：深入原理和专项能力

#### [nerdai/llm-agents-from-scratch](https://github.com/nerdai/llm-agents-from-scratch)

- 适合课程：37～44，以及阶段八的原理复习
- 借鉴内容：从原理手写 Agent，并逐步深入多 Agent、MCP 和 A2A。
- 前置要求：先通过最小 Agent Loop 和状态管理验收。

#### [amitbad/llm-evaluation](https://github.com/amitbad/llm-evaluation)

- 适合课程：45～52
- 借鉴内容：确定性评测、LLM-as-a-Judge、幻觉、提示注入、RAG、Agent 轨迹和观测。
- 学习策略：先理解评测目标和数据集设计，再使用具体评测框架。

## 使用规则

1. 主线一次只推进一个课程编号，外部仓库只作为该课的补充材料。
2. 外部仓库的代码必须经过本项目的测试、失败场景和复盘要求，才能计入能力证据。
3. 外部仓库的框架用法不能直接替代原理解释。
4. 使用易变化的模型、SDK、协议或价格信息时，在学习日志中记录核验日期。
5. 外部仓库停止维护、依赖失效或内容与主线冲突时，只替换参考资料，不改变已通过的能力标准。
6. 不复制外部仓库的密钥、个人数据、业务数据或大段实现；只保留必要的学习笔记和自己的实验。

## 参考记录模板

每次使用外部仓库后，在学习日志中记录：

```text
参考仓库：
对应课程：
借鉴的具体概念：
保留到自己项目的设计：
没有采用的设计及原因：
验证结果：
```
