from typing import Any, Dict
import os
import yaml
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

class SourceCfg(BaseModel):
    name: str
    type: str  # "html" | "pdf" | "api" | "cninfo"
    url: str | None = None
    enabled: bool = True
    periods: list[str] | None = None  # for cninfo: ["quarterly","semiannual","annual"]
    page_size: int | None = 50
    max_pages: int | None = 1
    max_total: int | None = 50
    se_date: str | None = None       # 示例："2025-01-01~2025-12-31"
    title_keywords: list[str] | None = None  # 例如 ["报告","季度报告","半年度报告","年度报告"]

class RulesCfg(BaseModel):
    notify_on: list[Dict[str, Any]] = Field(default_factory=list)
    thresholds: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('notify_on', mode='before')
    @classmethod
    def _norm_notify_on(cls, v):
        return v or []

    @field_validator('thresholds', mode='before')
    @classmethod
    def _norm_thresholds(cls, v):
        return v or {}

class ScheduleCfg(BaseModel):
    enabled: bool = False
    interval_minutes: int = 60

class StorageCfg(BaseModel):
    sqlite_path: str = "data/holdings.db"

class PushCfg(BaseModel):
    email_enabled: bool = False

class AppCfg(BaseModel):
    sources: list[SourceCfg] = Field(default_factory=list)
    rules: RulesCfg = RulesCfg()
    schedule: ScheduleCfg = ScheduleCfg()
    storage: StorageCfg = StorageCfg()
    push: PushCfg = PushCfg()

def load_config(path: str = "config.yaml") -> AppCfg:
    load_dotenv()
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # 确保 data 是字典类型，避免 ** 操作符应用于 None
    config_data = data if isinstance(data, dict) else {}
    return AppCfg(**config_data)
