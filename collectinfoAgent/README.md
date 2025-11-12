# 数据收集员智能体（MVP）

## 功能概述
- 多源数据采集（HTML/PDF、API响应）
- 公告文本解析与实体抽取（投资人姓名、股票代码/名称、持股数量、变动方向）
- 结构化存储（SQLite）
- 规则引擎触发预警（如市值阈值、变动比例等）
- 推送（邮件）
- 定时任务（季度/手动触发）

## 快速开始
1. 安装依赖
   ```
   pip install -r requirements.txt
   ```
2. 配置环境变量（邮件推送可选）
   - 复制 `.env.example` 为 `.env`，填入 SMTP 配置
3. 编辑配置文件
   - `config.yaml` 中设置数据源（示例已给出）
4. 运行
   ```
   python src/main.py
   ```
   或启用定时轮询：
   ```
   python src/main.py --schedule
   ```

## 目录结构
- src/
  - main.py (入口)
  - config.py (加载配置)
  - names.py (目标投资人名单)
  - storage.py (SQLite存储)
  - rules.py (规则引擎)
  - push.py (邮件推送)
  - extract.py (基于规则/正则的抽取)
  - parsers/
    - html_parser.py
    - pdf_parser.py
  - sources/
    - exchanges.py (交易所公告抓取占位)
    - eastmoney.py (财经网站抓取占位)

## 备注
- 解析规则为可扩展的正则与规则集合，后续可引入更复杂模型。
- 遵守 robots.txt 与访问频控（在实际抓取模块中实现）。
