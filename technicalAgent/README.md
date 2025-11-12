# 技术分析智能体 (Technical Analysis Agent)

基于技术分析理论的专业股票分析智能体，为投资决策系统提供量化技术面依据。

## 功能特性

- **多粒度数据获取**: 支持日K、周K、月K及分钟级数据
- **全面技术指标**: MA、EMA、RSI、MACD、布林带、VWAP、OBV等
- **智能模式识别**: 自动识别技术形态和关键价位
- **风险评估**: 综合波动率和指标信号评估风险等级
- **止损建议**: 基于技术分析提供止损位参考
- **结构化报告**: 生成标准化的JSON格式分析报告

## 核心指标

### 趋势指标
- 移动平均线 (MA5, MA10, MA20, MA60)
- 指数移动平均线 (EMA12, EMA26)

### 动量指标  
- 相对强弱指数 (RSI14)
- 平滑异同移动平均线 (MACD)

### 波动率指标
- 布林带 (上轨、中轨、下轨、带宽)

### 成交量指标
- 成交量加权平均价 (VWAP)
- 能量潮 (OBV)

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基本使用
```bash
cd technicalAgent/src/technical
python run_demo.py --ticker 600418 --timeframe daily --periods 250
```

### 参数说明
- `--ticker`: 股票代码 (默认: 600418)
- `--timeframe`: 时间框架 [daily, weekly, monthly, 5min, 30min, 60min] (默认: daily)
- `--periods`: 分析周期数 (默认: 250)
- `--output`: 自定义输出文件路径

## 输出示例

分析报告包含以下核心信息：
```json
{
  "ticker": "600418",
  "timeframe": "daily",
  "analysis_date": "2025-10-15T09:00:00",
  "overall_trend": "bullish",
  "trend_strength": 0.75,
  "key_signals": [...],
  "indicators": [...],
  "price_levels": [...],
  "risk_assessment": "medium",
  "stop_loss_suggestion": 22.5
}
```

## 项目结构
```
technicalAgent/
├── src/
│   └── technical/
│       ├── schemas.py          # 数据模型定义
│       ├── data_provider.py    # 数据获取接口
│       ├── indicators.py       # 技术指标计算
│       ├── pattern_recognizer.py # 模式识别
│       ├── analyzer.py         # 综合分析器
│       └── run_demo.py         # 演示程序
├── data/
│   └── output/                 # 分析报告输出
├── requirements.txt            # 依赖包
└── README.md                  # 说明文档
```

## 集成使用

技术分析智能体可与决策系统其他组件集成：

```python
from technicalAgent.src.technical.analyzer import TechnicalAnalyzer
from technicalAgent.src.technical.schemas import TechnicalAnalysisRequest, TimeFrame

# 创建分析请求
request = TechnicalAnalysisRequest(
    ticker="600418",
    timeframe=TimeFrame.DAILY,
    periods=250
)

# 执行分析
analyzer = TechnicalAnalyzer()
report = analyzer.analyze(request)

# 获取分析结果
print(f"趋势: {report.overall_trend}")
print(f"风险等级: {report.risk_assessment}")
```

## 数据源

当前使用 [akshare](https://github.com/akfamily/akshare) 作为主要数据源，支持A股市场实时和历史数据。
