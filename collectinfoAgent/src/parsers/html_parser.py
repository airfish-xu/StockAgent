from typing import Tuple
import requests
from bs4 import BeautifulSoup

def fetch_html(url: str, timeout: int = 20) -> str:
    resp = requests.get(url, timeout=timeout, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    return resp.text

def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # 去掉脚本与样式
    for tag in soup(["script","style","noscript"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    return text
