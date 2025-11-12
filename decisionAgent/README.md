# 决策员智能体 (Decision Agent)

## 概述

决策员智能体是一个基于规则引擎的投资决策支持系统，旨在自动化完成投资信号识别和决策报告生成。作为投资研究流程中的"虚拟首席分析师"，该智能体能够集成多源数据、应用预设规则和AI推理，对投资动向进行智能化决策判断。

## 核心功能

### 多源数据集成
- 接收数据收集员智能体提供的结构化持仓数据
- 整合辩论员智能体提供的多空观点总结报告
- 支持实时行情、基本面数据、行业新闻等外部信息获取

### 智能规则引擎
- 基于JSON配置的灵活规则系统
- 支持逻辑组合（AND/OR/NOT）和优先级设置
- 实时规则匹配和信号触发

### 结构化报告生成
- 自动生成包含信号摘要、决策依据、综合建议的详细报告
- 支持JSON、Markdown、HTML/PDF等多种输出格式
- 集成风险提示和操作建议

## 快速开始

### 安装依赖
```bash
cd decisionAgent
pip install -r requirements.txt
```

### 基本使用
```bash
# 运行演示程序
python src/decision/run_demo.py

# 使用自定义事件文件
python src/decision/run_demo.py --event-file data/sample_event.json

# 指定输出格式
python src/decision/run_demo.py --output-format markdown
```

### 命令行参数
- `--event`: 指定输入事件文件路径（支持collectinfoAgent或debaterAgent输出格式）
- `--debate`: 指定辩论总结文件路径（debaterAgent输出）
- `--technical`: 指定技术分析文件路径（technicalAgent输出）
- `--rules`: 自定义规则文件路径（默认：rules.json）
- `--output-dir`: 输出目录路径（默认：data/output）

## 多源数据输入支持

decisionAgent支持集成来自不同智能体的分析结果，进行综合决策：

### 1. 事件数据输入（基本面分析）
支持来自collectinfoAgent或debaterAgent的事件数据文件：
```bash
python src/decision/run_demo.py --event ../collectinfoAgent/data/output/event_300203.json
```

### 2. 辩论总结输入（多空观点分析）
支持来自debaterAgent的辩论总结文件：
```bash
python src/decision/run_demo.py --debate ../debaterAgent/data/output/debate_300203.json
```

### 3. 技术分析输入（技术面分析）
支持来自technicalAgent的技术分析文件：
```bash
python src/decision/run_demo.py --technical ../technicalAgent/data/output/technical_300203_daily.json
```

### 4. 综合集成使用
可以同时集成多个分析源：
```bash
python src/decision/run_demo.py \
  --event ../collectinfoAgent/data/output/event_300203.json \
  --debate ../debaterAgent/data/output/debate_300203.json \
  --technical ../technicalAgent/data/output/technical_300203_daily.json
```

## 输入数据格式

### 事件数据格式
```json
{
  "investor": "葛卫东",
  "ticker": "601579",
  "name": "会稽山",
  "changeType": "new_position",
  "amount": 99000000.0,
  "industry": "消费（黄酒）",
  "eventTime": "2024-06-30",
  "sourceUrl": "http://example.com"
}
```

### 市场数据格式
```json
{
  "pe": 35.0,
  "pb": 2.1,
  "pe_pct_3y": 75.0,
  "revenue_growth": 15.2,
  "net_profit_growth": 8.5
}
```

## 技术分析集成

decisionAgent深度集成技术分析数据，支持以下技术指标和信号：

### 技术分析数据包含
- **趋势分析**：整体趋势方向（上涨/下跌/中性）和强度
- **关键信号**：技术形态识别（金叉、死叉、突破等）
- **技术指标**：MA5、MA20、RSI14、MACD等常用指标
- **风险评估**：基于技术面的风险等级评估
- **止损建议**：技术止损位建议

### 技术分析规则集成
规则引擎可以基于技术分析数据进行决策判断，例如：
- 当技术面显示强势上涨趋势时，增强买入信号
- 当出现技术面风险信号时，触发风险提示规则
- 结合基本面和技术面进行综合风险评估

## 规则配置

### 规则结构
规则定义在`rules.json`文件中，支持以下字段：
- `id`: 规则唯一标识
- `name`: 规则名称
- `priority`: 优先级（0-100）
- `action`: 触发动作类型
- `confidence`: 置信度（0-1）
- `reason`: 规则说明
- `condition`: 条件逻辑

### 条件操作符
- `eq`: 等于
- `ne`: 不等于
- `gt`: 大于
- `ge`: 大于等于
- `lt`: 小于
- `le`: 小于等于
- `in`: 包含在列表中
- `contains`: 字符串包含
- `exists`: 字段存在

### 示例规则
```json
{
  "id": "R1",
  "name": "大佬新进消费高额持仓-强烈关注",
  "priority": 90,
  "action": "strong_watch",
  "confidence": 0.85,
  "reason": "投资人+行业+金额匹配",
  "condition": {
    "all": [
      { "path": "event.investor", "op": "in", "value": ["葛卫东", "葛贵莲"] },
      { "path": "event.changeType", "op": "eq", "value": "new_position" },
      { "path": "event.industry", "op": "contains", "value": "消费" },
      { "path": "event.amount", "op": "ge", "value": 100000000.0 }
    ]
  }
}
```

## 综合决策报告

decisionAgent能够生成包含多维度分析的综合性决策报告：

### 报告结构
- **信号摘要**: 触发信号类型、时间、核心条件
- **决策依据**: 触发规则详情、多空观点、数据快照
- **综合建议**: 基于信号强度的操作建议
- **风险提示**: 关联风险类型和级别

### 示例输出
```markdown
# 投资决策报告

## 信号摘要
- **信号类型**: 积极关注
- **触发时间**: 2024-06-30
- **核心条件**: 葛卫东新进持仓，金额0.99亿元，估值合理

## 决策依据
- **触发规则**: R2 - 新进入仓+估值合理-积极关注
- **多空观点**: 多头3点，空头2点
- **数据快照**: PE=35.0, 持仓金额=0.99亿元

## 综合建议
建议加入重点关注列表，持续跟踪后续财报验证基本面

## 风险提示
- 中等估值风险
- 行业竞争风险
```

## 项目结构
```
decisionAgent/
├── src/
│   └── decision/
│       ├── run_demo.py          # 主演示程序
│       ├── decision_engine.py   # 决策引擎核心
│       ├── rule_parser.py       # 规则解析器
│       └── report_generator.py  # 报告生成器
├── data/
│   └── output/                  # 输出目录
├── rules.json                   # 规则配置文件
└── README.md                   # 本文档
```

## 智能体集成工作流

decisionAgent设计为整个智能体系统的决策中枢，支持完整的集成工作流：

### 1. 数据收集员智能体 → 决策员智能体
```python
# 接收数据收集员的事件
event_data = collectinfo_agent.get_latest_event()
decision_engine = DecisionEngine()
result = decision_engine.process_event(event_data)
```

### 2. 辩论员智能体 → 决策员智能体
```python
# 获取辩论观点
debate_summary = debater_agent.get_debate_summary(ticker)
result = decision_engine.process_with_debate(event_data, debate_summary)
```

### 3. 技术分析智能体 → 决策员智能体
```python
# 集成技术分析数据
technical_data = technical_agent.get_analysis(ticker)
result = decision_engine.process_with_technical(event_data, technical_data)
```

### 4. 完整工作流集成
```python
# 综合所有分析源
event_data = collectinfo_agent.get_latest_event()
debate_summary = debater_agent.get_debate_summary(ticker)
technical_data = technical_agent.get_analysis(ticker)

result = decision_engine.process_comprehensive(
    event=event_data,
    debate=debate_summary,
    technical=technical_data
)
```

## 集成使用
```python
from decision_engine import DecisionEngine

# 接收数据收集员的事件
event_data = collectinfo_agent.get_latest_event()
decision_engine = DecisionEngine()
result = decision_engine.process_event(event_data)
```

### 与辩论员智能体集成
```python
# 获取辩论观点
debate_summary = debater_agent.get_debate_summary(ticker)
result = decision_engine.process_with_debate(event_data, debate_summary)
```

## 性能要求
- **响应时间**: 端到端延迟 < 5秒
- **准确性**: 规则匹配100%准确
- **可用性**: 全年无故障运行时间 ≥ 99.9%

## 故障排除

### 常见问题
1. **规则不匹配**: 检查规则条件语法和数据类型
2. **数据格式错误**: 验证输入数据是否符合JSON schema
3. **依赖缺失**: 确保所有Python依赖包已正确安装

### 调试模式
```bash
python src/decision/run_demo.py --debug
```

## 后续演进
- 机器学习信号有效性预测
- 个性化规则推荐
- 多维信号融合
- 自动化交易接口集成

## 技术支持
如有问题请参考项目文档或联系开发团队。
