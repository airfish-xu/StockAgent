#!/usr/bin/env python3
"""
批量获取半年报数据 - 支持6000只股票
"""

import sys
import os
import time
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.sources.cninfo import fetch_semiannual_reports

def batch_fetch_semiannual_reports():
    """批量获取半年报数据"""
    print("开始批量获取2025年半年报数据...")
    print("目标：获取约6000只股票的半年报")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # 获取半年报数据
        reports = fetch_semiannual_reports(
            page_size=100,      # 每页100条
            max_pages=60,      # 最多60页
            max_total=6000     # 最多6000份报告
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"获取完成！")
        print(f"成功获取 {len(reports)} 份半年报")
        print(f"耗时: {elapsed_time:.2f} 秒")
        print("=" * 60)
        
        # 统计信息
        sse_count = len([r for r in reports if r['column'] == 'sse'])
        szse_count = len([r for r in reports if r['column'] == 'szse'])
        
        print(f"上交所报告: {sse_count} 份")
        print(f"深交所报告: {szse_count} 份")
        print("=" * 60)
        
        # 显示前10份报告信息
        print("前10份报告信息：")
        for i, report in enumerate(reports[:10]):
            print(f"{i+1:2d}. {report['title'][:50]}...")
            print(f"     交易所: {report['column']}")
            print(f"     PDF链接: {report['pdf_url']}")
            print()
        
        # 保存结果到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/semiannual_reports_{timestamp}.json"
        
        # 确保目录存在
        os.makedirs("data", exist_ok=True)
        
        # 保存JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存到: {output_file}")
        
        # 生成简单的统计报告
        stats_file = f"data/semiannual_stats_{timestamp}.txt"
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("2025年半年报获取统计报告\n")
            f.write("=" * 40 + "\n")
            f.write(f"获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总报告数: {len(reports)}\n")
            f.write(f"上交所报告: {sse_count}\n")
            f.write(f"深交所报告: {szse_count}\n")
            f.write(f"获取耗时: {elapsed_time:.2f} 秒\n")
            f.write("\n报告列表:\n")
            for i, report in enumerate(reports):
                f.write(f"{i+1:4d}. {report['title']}\n")
        
        print(f"统计报告已保存到: {stats_file}")
        
        return reports
        
    except Exception as e:
        print(f"获取过程中出现错误: {e}")
        return []

if __name__ == "__main__":
    batch_fetch_semiannual_reports()