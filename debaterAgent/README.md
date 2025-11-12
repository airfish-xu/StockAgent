# 辩论员智能体 (Debater Agent)

## 概述

辩论员智能体是一个基于LangGraph的多智能体辩论系统，能够对投资事件进行多角度分析和辩论，生成全面的投资分析报告。

## 功能特性

- **多角色辩论**: 支持多头和空头角色进行交替辩论
- **智能论点生成**: 基于事件信息自动生成投资论点
- **结构化输出**: 生成包含核心观点、分歧点和总结的完整报告
- **多种LLM支持**: 支持OpenAI、DashScope和本地模拟LLM

## 快速开始

### 安装依赖

```bash
pip install langgraph
```

### 基本使用

```bash
# 使用默认配置运行演示
cd debaterAgent
python src/debater/run_demo.py

# 指定事件文件
python src/debater/run_demo.py --event data/output/event.json

# 设置辩论轮次
python src/debater/run_demo.py --rounds 5

# 使用不同的LLM后端
python src/debater/run_demo.py --llm openai
python src/debater/run_demo.py --llm dashscope
python src/debater/run_demo.py --llm dummy
```

### 命令行参数

- `--event`: 事件JSON文件路径（可选，默认使用内置示例）
- `--rounds`: 最大辩论轮次（默认：3）
- `--llm`: LLM选择（dummy/openai/dashscope，默认：dummy）

## 输入格式

### 事件数据结构

```json
{
  "ticker": "600418",
  "name": "江淮汽车",
  "changeType": "new_position",
  "industry": "汽车制造/新能源",
  "eventTime": "2025-10-10T12:00:00+08:00",
  "sourceUrl": "https://example.com/news/guweidong-jianghuai",
  "extras": {
    "note": "示例事件，非真实数据调用"
  }
}
```

### 字段说明

- `ticker`: 股票代码
- `name`: 公司名称
- `changeType`: 变动类型（new_position/increase/decrease/exit）
- `industry`: 所属行业
- `eventTime`: 事件时间
- `sourceUrl`: 信息来源URL
- `extras`: 额外信息

## 输出结果

### 输出文件

辩论结果保存在 `data/output/debate_{ticker}.json` 文件中，包含：

- 事件信息
- 辩论轮次记录
- 多头和空头观点
- 总结报告

### 输出结构

```json
{
  "event": {
    "ticker": "600418",
    "name": "江淮汽车",
    "changeType": "new_position",
    "industry": "汽车制造/新能源",
    "eventTime": "2025-10-10T12:00:00+08:00",
    "sourceUrl": "https://example.com/news/guweidong-jianghuai",
    "extras": {"note": "示例事件，非真实数据调用"}
  },
  "max_rounds": 3,
  "turns": [
    {
      "round_index": 1,
      "speaker": "bull",
      "claim": "立论观点",
      "supports": ["支撑论据1", "支撑论据2"],
      "rebuttal_target": "反驳目标"
    }
  ],
  "summary": {
    "topic": "江淮汽车（600418）",
    "long_core_points": ["多头核心观点1", "多头核心观点2"],
    "short_core_points": ["空头核心观点1", "空头核心观点2"],
    "divergence_points": ["分歧点1", "分歧点2"],
    "notes": "总结说明"
  }
}
```

## LLM配置

### OpenAI配置

设置环境变量：
```bash
export OPENAI_API_KEY=your_openai_api_key
```

### DashScope配置

设置环境变量：
```bash
export DASHSCOPE_API_KEY=your_dashscope_api_key
```

安装依赖：
```bash
pip install dashscope
```

### 本地模拟模式

使用内置的DummyLLM，无需额外配置，适合测试和演示。

## 集成使用

### 与数据收集员集成

可以从数据收集员智能体的输出中获取事件数据：

```python
from debater.run_demo import load_event, main

# 加载数据收集员生成的事件
event = load_event("collectinfoAgent/data/output/event.json")

# 运行辩论
main(event=event)
```

### 自定义辩论流程

```python
from debater.graph import build_debate_graph
from debater.roles import DummyLLM
from debater.schemas import InputEvent

# 创建自定义事件
event = InputEvent(
    ticker="300203",
    name="聚光科技",
    changeType="increase",
    industry="环保设备"
)

# 构建辩论图
debate_graph = build_debate_graph(llm=DummyLLM(), max_rounds=4)

# 运行辩论
result = debate_graph(event)
```

## 项目结构

```
debaterAgent/
├── src/
│   ├── debater/
│   │   ├── __init__.py
│   │   ├── run_demo.py      # 主入口文件
│   │   ├── graph.py         # 辩论流程图定义
│   │   ├── roles.py         # LLM角色定义
│   │   └── schemas.py       # 数据模型定义
│   └── render_report.py     # 报告渲染工具
├── data/
│   └── output/              # 输出目录
└── README.md
```

## 注意事项

1. **API密钥安全**: 不要将API密钥提交到版本控制系统
2. **网络连接**: 使用云端LLM时需要稳定的网络连接
3. **费用控制**: 注意API调用费用，建议设置使用限制
4. **数据质量**: 输入事件数据的质量直接影响辩论结果

## 故障排除

### 常见问题

1. **导入错误**: 确保在debaterAgent目录下运行脚本
2. **API连接失败**: 检查网络连接和API密钥配置
3. **内存不足**: 减少辩论轮次或使用更小的模型

### 调试模式

启用详细日志输出：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 许可证

本项目基于MIT许可证开源。
