#!/usr/bin/env python3
"""
总控智能体测试脚本
测试各个模块的基本功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_config():
    """测试配置模块"""
    print("测试配置模块...")
    try:
        from master_agent.config import load_config
        config = load_config()
        print(f"✓ 项目根目录: {config.project_root}")
        print(f"✓ 数据库路径: {config.database_path}")
        print(f"✓ 目标投资人: {config.target_investors}")
        return True
    except Exception as e:
        print(f"✗ 配置模块测试失败: {e}")
        return False

def test_data_manager():
    """测试数据管理模块"""
    print("\n测试数据管理模块...")
    try:
        from master_agent.data_manager import DataManager
        data_manager = DataManager()
        
        # 测试获取投资人列表
        investors = data_manager.get_all_investors()
        print(f"✓ 投资人列表: {investors}")
        
        if investors:
            # 测试获取持仓数据
            holdings = data_manager.get_investor_holdings(investors[0])
            print(f"✓ 持仓数据数量: {len(holdings)}")
            
            if holdings:
                print(f"✓ 示例持仓: {holdings[0]}")
        
        return True
    except Exception as e:
        print(f"✗ 数据管理模块测试失败: {e}")
        return False

def test_agent_coordinator():
    """测试智能体协调器"""
    print("\n测试智能体协调器...")
    try:
        from master_agent.agent_coordinator import AgentCoordinator
        coordinator = AgentCoordinator()
        
        # 测试基本功能
        print("✓ 智能体协调器初始化成功")
        
        # 测试数据收集智能体调用（可选）
        # print("测试数据收集智能体...")
        # success = coordinator.run_collectinfo_agent()
        # print(f"数据收集: {'成功' if success else '失败'}")
        
        return True
    except Exception as e:
        print(f"✗ 智能体协调器测试失败: {e}")
        return False

def test_gui_components():
    """测试GUI组件（不实际显示窗口）"""
    print("\n测试GUI组件...")
    try:
        # 测试GUI模块导入
        from master_agent.gui import MasterAgentGUI
        print("✓ GUI模块导入成功")
        
        # 测试配置加载
        from master_agent.config import load_config
        config = load_config()
        print("✓ 配置加载成功")
        
        return True
    except Exception as e:
        print(f"✗ GUI组件测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("总控智能体测试套件")
    print("=" * 60)
    
    tests_passed = 0
    tests_total = 4
    
    # 运行各个测试
    if test_config():
        tests_passed += 1
    
    if test_data_manager():
        tests_passed += 1
    
    if test_agent_coordinator():
        tests_passed += 1
        
    if test_gui_components():
        tests_passed += 1
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print(f"测试结果: {tests_passed}/{tests_total} 通过")
    
    if tests_passed == tests_total:
        print("🎉 所有测试通过！总控智能体可以正常使用。")
        print("\n下一步:")
        print("1. 运行 python run_master_agent.py 启动总控智能体")
        print("2. 选择图形界面模式进行完整分析")
        print("3. 或使用命令行模式分析特定投资人")
    else:
        print("⚠ 部分测试失败，请检查依赖和配置")
        print("\n建议:")
        print("1. 确保所有子智能体已正确安装")
        print("2. 检查数据库文件是否存在")
        print("3. 验证Python环境配置")

if __name__ == "__main__":
    main()