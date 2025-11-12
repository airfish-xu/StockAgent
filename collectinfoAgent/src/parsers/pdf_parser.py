from typing import Optional, List
import pdfplumber
import requests
import io

def fetch_pdf_bytes(url: str, timeout: int = 30) -> bytes:
    resp = requests.get(url, timeout=timeout, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    return resp.content

def extract_text_from_pdf_bytes(data: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            text_parts.append(txt)
    return "\n".join(text_parts)

def extract_tables_text_from_pdf_bytes(data: bytes) -> str:
    """尽力从PDF表格中提取文本（用于前十大股东表）。"""
    table_texts: List[str] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            try:
                tables = page.extract_tables() or []
            except Exception:
                tables = []
            for tbl in tables:
                rows = []
                for row in tbl or []:
                    cells = [c.strip() if isinstance(c, str) else "" for c in row]
                    rows.append(" ".join(cells))
                if rows:
                    table_texts.append("\n".join(rows))
    return "\n".join(table_texts)

def extract_text_with_tables(data: bytes) -> str:
    """合并正文与表格文本，提升股东名识别概率。"""
    body = extract_text_from_pdf_bytes(data)
    tables = extract_tables_text_from_pdf_bytes(data)
    if tables:
        return body + "\n" + tables
    return body