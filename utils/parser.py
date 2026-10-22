# utils/parser.py
"""
解析工具：
- 从 LLM 输出中提取代码块
- 从审查结果中判断是否通过
- 提取问题列表
"""

import re
from typing import List, Dict


def extract_code_block(text: str) -> str:
    """
    从 Markdown 文本中提取第一个代码块。
    如果没有代码块，返回原文。
    """
    if not text:
        return ""
    pattern = r"```(?:python|py)?\s*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    return text.strip()


def extract_all_code_blocks(text: str) -> List[str]:
    """提取所有代码块。"""
    if not text:
        return []
    pattern = r"```(?:python|py)?\s*\n(.*?)```"
    return [m.strip() for m in re.findall(pattern, text, re.DOTALL)]


def is_review_passed(review_text: str) -> bool:
    """
    判断审查是否通过。
    规则：
    - 出现 PASS 且没有 FAIL → 通过
    - 出现 FAIL → 不通过
    - 都没有 → 根据是否有问题关键词判断
    """
    if not review_text:
        return False

    upper = review_text.upper()

    if "FAIL" in upper:
        return False
    if "PASS" in upper:
        return True

    # 兜底：没有问题关键词则认为通过
    issue_keywords = ["问题", "错误", "风险", "bug", "issue", "error", "warning"]
    for kw in issue_keywords:
        if kw in review_text.lower():
            return False
    return True


def parse_issues(review_text: str) -> List[Dict[str, str]]:
    """
    从审查文本中解析问题列表。
    支持格式：
    - 严重：xxx
    - [严重] xxx
    - 1. xxx
    """
    issues = []
    if not review_text:
        return issues

    lines = review_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 匹配 "严重：xxx" 或 "[严重] xxx"
        m = re.match(r"^[\[\s]*?(严重|中等|轻微|高|中|低|critical|major|minor)[\]\s：:]+(.+)$",
                     line, re.IGNORECASE)
        if m:
            issues.append({
                "severity": m.group(1),
                "description": m.group(2).strip()
            })
            continue

        # 匹配 "1. xxx"
        m = re.match(r"^\d+[\.、]\s*(.+)$", line)
        if m:
            issues.append({
                "severity": "unknown",
                "description": m.group(1).strip()
            })

    return issues


def truncate(text: str, max_len: int = 200) -> str:
    """截断文本，用于日志展示。"""
    if not text:
        return ""
    text = text.replace("\n", " ")
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def safe_json_loads(text: str, default=None):
    """安全解析 JSON。"""
    import json
    try:
        return json.loads(text)
    except Exception:
        return default