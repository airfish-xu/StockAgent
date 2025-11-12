#!/usr/bin/env python3
"""
总控智能体启动脚本
提供便捷的方式启动总控智能体（支持传统模式和LangGraph模式）
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 添加tushare token配置
import warnings
import tushare as ts
import os
import pandas as pd

# 抑制pandas兼容性警告
warnings.filterwarnings('ignore', category=FutureWarning, module='tushare')
warnings.filterwarnings('ignore', category=FutureWarning, module='pandas')

# pandas兼容性补丁 - 修复DataFrame.append()方法
if not hasattr(pd.DataFrame, 'append'):
    def dataframe_append(self, other, ignore_index=False, verify_integrity=False, sort=False):
        """兼容性补丁：模拟旧的DataFrame.append()方法"""
        return pd.concat([self, other], ignore_index=ignore_index, sort=sort)
    
    pd.DataFrame.append = dataframe_append

token = os.getenv('TUSHARE_TOKEN')
if token:
    ts.set_token(token)
else:
    print("警告: 未设置TUSHARE_TOKEN环境变量，tushare功能可能无法正常使用")

def main():
    """主启动函数"""
    print("=" * 60)
    print("牛散投资分析总控智能体")
    print("=" * 60)
    
    # 检查依赖
    try:
        import tkinter
        print("✓ GUI支持可用")
    except ImportError:
        print("✗ GUI支持不可用，将使用命令行模式")
    
    # 检查数据库
    db_path = project_root / "collectinfoAgent" / "data" / "holdings.db"
    if db_path.exists():
        print("✓ 持仓数据库存在")
    else:
        print("⚠ 持仓数据库不存在，请先运行数据收集智能体")
    
    # 选择运行模式
    print("\n请选择运行模式:")
    print("1. 图形界面模式 (LangGraph模式)")
    print("2. 命令行模式 (传统模式)")
    print("3. LangGraph模式 (新一代架构)")
    print("4. 测试模式")
    
    choice = input("\n请输入选择 (1-4, 默认1): ").strip()
    
    if choice == "2":
        # 命令行模式（传统）
        investor = input("请输入要分析的牛散姓名 (如: 葛卫东): ").strip()
        if not investor:
            print("未输入投资人姓名，退出")
            return
            
        from master_agent.main import run_cli_analysis
        run_cli_analysis(investor)
        
    elif choice == "3":
        # LangGraph模式
        investor = input("请输入要分析的牛散姓名 (如: 葛卫东): ").strip()
        if not investor:
            print("未输入投资人姓名，退出")
            return
            
        print(f"\n启动LangGraph模式分析: {investor}")
        from master_agent.langgraph_coordinator import LangGraphCoordinator
        coordinator = LangGraphCoordinator()
        result = coordinator.analyze_investor(investor)
        
        print(f"\n分析完成!")
        print(f"成功: {result['success']}")
        print(f"分析股票数量: {result['analyzed_stocks']}/{result['total_stocks']}")
        print(f"耗时: {result['duration_seconds']:.2f}秒")
        
        if result['error']:
            print(f"错误: {result['error']}")
        else:
            print("结果已保存到输出目录")
            
    elif choice == "4":
        # 测试模式
        print("\n运行测试...")
        from master_agent.data_manager import DataManager
        from master_agent.config import load_config
        
        config = load_config()
        data_manager = DataManager()
        
        # 测试数据库连接
        investors = data_manager.get_all_investors()
        print(f"数据库中的投资人: {investors}")
        
        if investors:
            # 测试获取持仓数据
            holdings = data_manager.get_investor_holdings(investors[0])
            print(f"第一个投资人的持仓数量: {len(holdings)}")
            
            # 测试LangGraph协调器
            try:
                from master_agent.langgraph_coordinator import LangGraphCoordinator
                coordinator = LangGraphCoordinator()
                print("✓ LangGraph协调器初始化成功")
            except Exception as e:
                print(f"✗ LangGraph协调器初始化失败: {e}")
            
    else:
        # 图形界面模式 (默认) - 使用LangGraph模式
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox
            import threading
            from master_agent.langgraph_coordinator import LangGraphCoordinator
            
            class LangGraphGUI:
                """基于LangGraph的图形界面"""
                
                def __init__(self, root):
                    self.root = root
                    self.root.title("牛散投资分析 - LangGraph模式")
                    self.root.geometry("600x400")
                    
                    # 创建主框架
                    main_frame = ttk.Frame(root, padding="10")
                    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                    
                    # 标题
                    title_label = ttk.Label(main_frame, text="牛散投资分析系统", 
                                          font=("Arial", 16, "bold"))
                    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
                    
                    # 模式说明
                    mode_label = ttk.Label(main_frame, text="运行模式: LangGraph图形模式", 
                                          font=("Arial", 10, "italic"))
                    mode_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
                    
                    # 投资人选择
                    ttk.Label(main_frame, text="选择投资人:").grid(row=2, column=0, sticky=tk.W, pady=5)
                    self.investor_var = tk.StringVar()
                    investor_combo = ttk.Combobox(main_frame, textvariable=self.investor_var, width=20)
                    investor_combo['values'] = self.get_investors()
                    investor_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
                    
                    # 分析按钮
                    analyze_btn = ttk.Button(main_frame, text="开始分析", command=self.start_analysis)
                    analyze_btn.grid(row=3, column=0, columnspan=2, pady=10)
                    
                    # 进度显示
                    self.progress_var = tk.StringVar(value="准备就绪")
                    progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
                    progress_label.grid(row=4, column=0, columnspan=2, pady=5)
                    
                    # 进度条
                    self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
                    self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
                    
                    # 结果文本框
                    ttk.Label(main_frame, text="分析结果:").grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
                    self.result_text = tk.Text(main_frame, height=10, width=60)
                    self.result_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
                    
                    # 配置网格权重
                    root.columnconfigure(0, weight=1)
                    root.rowconfigure(0, weight=1)
                    main_frame.columnconfigure(1, weight=1)
                    main_frame.rowconfigure(7, weight=1)
                    
                    self.coordinator = None
                    
                def get_investors(self):
                    """获取投资人列表"""
                    try:
                        from master_agent.data_manager import DataManager
                        data_manager = DataManager()
                        return data_manager.get_all_investors()
                    except:
                        return ["葛卫东", "葛贵莲", "王孝安", "何雪萍"]
                
                def start_analysis(self):
                    """开始分析"""
                    investor = self.investor_var.get()
                    if not investor:
                        messagebox.showerror("错误", "请选择投资人")
                        return
                    
                    # 在新线程中运行分析
                    self.progress_var.set(f"正在分析 {investor}...")
                    self.progress.start()
                    self.result_text.delete(1.0, tk.END)
                    self.result_text.insert(tk.END, f"开始分析投资人: {investor}\n")
                    
                    thread = threading.Thread(target=self.run_analysis, args=(investor,))
                    thread.daemon = True
                    thread.start()
                
                def run_analysis(self, investor):
                    """运行分析"""
                    try:
                        self.coordinator = LangGraphCoordinator()
                        result = self.coordinator.analyze_investor(investor)
                        
                        # 在主线程中更新UI
                        self.root.after(0, self.analysis_complete, result, investor)
                        
                    except Exception as e:
                        self.root.after(0, self.analysis_error, str(e))
                
                def analysis_complete(self, result, investor):
                    """分析完成"""
                    self.progress.stop()
                    self.progress_var.set("分析完成")
                    
                    self.result_text.insert(tk.END, f"\n=== 分析结果 ===\n")
                    self.result_text.insert(tk.END, f"成功: {result['success']}\n")
                    self.result_text.insert(tk.END, f"分析股票数量: {result['analyzed_stocks']}/{result['total_stocks']}\n")
                    self.result_text.insert(tk.END, f"耗时: {result['duration_seconds']:.2f}秒\n")
                    
                    if result['error']:
                        self.result_text.insert(tk.END, f"错误: {result['error']}\n")
                    else:
                        self.result_text.insert(tk.END, "✓ 结果已保存到输出目录\n")
                        
                        # 显示详细结果
                        if result['results']:
                            self.result_text.insert(tk.END, f"\n=== 详细分析结果 ===\n")
                            for stock_code, analysis in result['results'].items():
                                stock_name = analysis['holding_info']['stock_name']
                                self.result_text.insert(tk.END, f"\n{stock_name} ({stock_code}):\n")
                                
                                # 技术分析结果
                                tech = analysis.get('technical', {})
                                if tech:
                                    trend = tech.get('overall_trend', '未知')
                                    strength = tech.get('trend_strength', 0)
                                    self.result_text.insert(tk.END, f"  技术面: {trend} (强度: {strength:.2f})\n")
                                
                                # 辩论分析结果
                                debate = analysis.get('debate', {})
                                if debate and 'summary' in debate:
                                    long_points = len(debate['summary'].get('long_core_points', []))
                                    short_points = len(debate['summary'].get('short_core_points', []))
                                    self.result_text.insert(tk.END, f"  多空观点: 多头{long_points}点 vs 空头{short_points}点\n")
                                
                                # 决策结果
                                decision = analysis.get('decision', {})
                                if decision:
                                    suggestion = decision.get('suggestion', '未知')
                                    self.result_text.insert(tk.END, f"  决策建议: {suggestion}\n")
                    
                    messagebox.showinfo("完成", f"分析 {investor} 完成!")
                
                def analysis_error(self, error_msg):
                    """分析错误"""
                    self.progress.stop()
                    self.progress_var.set("分析失败")
                    self.result_text.insert(tk.END, f"\n错误: {error_msg}\n")
                    messagebox.showerror("错误", f"分析失败: {error_msg}")
            
            root = tk.Tk()
            app = LangGraphGUI(root)
            root.mainloop()
            
        except Exception as e:
            print(f"启动LangGraph图形界面失败: {e}")
            print("请尝试使用命令行模式")

if __name__ == "__main__":
    main()