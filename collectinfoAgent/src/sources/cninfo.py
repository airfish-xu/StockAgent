from typing import List, Dict, Any
import requests
import re

# 巨潮历史公告查询接口
API_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
PDF_BASE = "https://static.cninfo.com.cn/"

# period 映射到 category
CATEGORY_MAP = {
    "quarterly": ["category_sjdbg_szsh"],   # 季报
    "semiannual": ["category_bndbg_szsh"],  # 半年报
    "annual": ["category_ndbg_szsh"],       # 年报
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cninfo.com.cn/",
}

def fetch_semiannual_reports(page_size: int = 100, max_pages: int = 60, max_total: int = 6000, se_date: str = "2025-01-01~2025-12-31") -> List[Dict[str, Any]]:
    """专门获取半年报数据，支持获取6000只股票"""
    return fetch_announcements(
        periods=["semiannual"],
        page_size=page_size,
        max_pages=max_pages,
        max_total=max_total,
        se_date=se_date,
        title_keywords=None
    )


def fetch_announcements(periods: List[str], page_size: int = 50, max_pages: int = 1, max_total: int = 50, se_date: str | None = None, title_keywords: List[str] | None = None) -> List[Dict[str, Any]]:
    all_items: List[Dict[str, Any]] = []
    seen = set()
    columns = ["szse", "sse"]  # 深交所/上交所
    for period in periods:
        cats = CATEGORY_MAP.get(period, [])
        for column in columns:
            for cat in cats:
                for page_num in range(1, max_pages + 1):
                    payload = {
                        "pageNum": page_num,
                        "pageSize": page_size,
                        "column": column,
                        "tabName": "fulltext",
                        "category": cat,
                        "seDate": se_date or "",  # 不限定时间范围，获取所有半年报
                        "plate": "",
                        "stock": "",
                        "searchkey": "",  # 不限定搜索关键词，获取所有半年报
                        "sortName": "announcementTime",  # 按公告时间排序
                        "sortType": "desc",  # 降序排列
                        "trade": "",
                    }
                    try:
                        resp = requests.post(API_URL, data=payload, headers=HEADERS, timeout=15)
                        resp.raise_for_status()
                        data = resp.json()
                    except Exception:
                        break
                    items = data.get("announcements") or data.get("classifiedAnnouncements") or []
                    if not items:
                        break
                    for it in items:
                        title = it.get("announcementTitle") or ""
                        url_path = it.get("adjunctUrl") or ""
                        if not url_path:
                            continue
                        # 修改重复检测逻辑：考虑交易所信息
                        unique_key = f"{column}:{url_path}"
                        if unique_key in seen:
                            continue
                        seen.add(unique_key)
                        pdf_url = PDF_BASE + url_path
                        # 标题过滤：严格限定2025，且排除“更正/更正版/更新后”
                        title_clean = title.replace(" ", "")
                        # 放宽过滤条件，只排除明显无效的报告
                        # 只排除纯英文标题或完全无效的报告
                        if re.search(r"^(英文版|H股公告|境外上市外文版)$", title_clean):
                            continue
                        # 确保是半年报（放宽匹配条件）
                        if not re.search(r"(半年报|半年度报告|中期报告)", title_clean):
                            continue
                        # 不限定年份，获取所有年份的半年报
                        if title_keywords:
                            # 需要同时包含关键词与年份匹配
                            if not any(kw in title for kw in title_keywords):
                                continue
                        all_items.append({
                            "title": title,
                            "pdf_url": pdf_url,
                            "url_path": url_path,
                            "column": column,
                            "category": cat,
                        })
                        if len(all_items) >= max_total:
                            return all_items
    return all_items
