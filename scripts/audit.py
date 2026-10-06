#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generic deterministic audit for RDD HTML reports.

Usage:
    python3 scripts/audit.py REPORT.html AUDIT_SPEC.json

The audit checks internal consistency only. It does not verify whether external
facts are true; source verification remains part of the research workflow.
"""
from __future__ import annotations

import argparse
import ast
import json
import operator
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_ALLOW_CONTEXT_TERMS = [
    "先前", "已更正", "已刪除", "已降級", "已移除", "已更新",
    "是錯的", "不可直接對照", "未能在", "找不到一手", "舊值",
    "不能主張", "不成立",
]

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}


def safe_eval(expression: str) -> Any:
    """Evaluate a numeric/boolean expression without Python eval()."""
    node = ast.parse(expression, mode="eval").body

    def visit(n: ast.AST) -> Any:
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float, bool)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _BIN_OPS:
            return _BIN_OPS[type(n.op)](visit(n.left), visit(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _UNARY_OPS:
            return _UNARY_OPS[type(n.op)](visit(n.operand))
        if isinstance(n, ast.Compare):
            left = visit(n.left)
            for op_node, right_node in zip(n.ops, n.comparators):
                op = _CMP_OPS.get(type(op_node))
                if op is None:
                    raise ValueError(f"unsupported comparison: {type(op_node).__name__}")
                right = visit(right_node)
                if not op(left, right):
                    return False
                left = right
            return True
        if isinstance(n, ast.BoolOp) and isinstance(n.op, (ast.And, ast.Or)):
            values = [bool(visit(v)) for v in n.values]
            return all(values) if isinstance(n.op, ast.And) else any(values)
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name)
            and n.func.id == "abs"
            and len(n.args) == 1
            and not n.keywords
        ):
            return abs(visit(n.args[0]))
        raise ValueError(f"unsupported expression node: {type(n).__name__}")

    return visit(node)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("audit spec must be a JSON object")
    return data


def scan_claims(
    text: str,
    claims: list[dict[str, Any]],
    allow_terms: list[str],
    context_chars: int,
) -> list[str]:
    failures: list[str] = []
    allow_re = re.compile("|".join(re.escape(x) for x in allow_terms)) if allow_terms else None

    for item in claims:
        pattern = item["pattern"]
        reason = item.get("reason", pattern)
        flags = re.IGNORECASE if item.get("ignore_case") else 0
        for match in re.finditer(pattern, text, flags):
            lo = max(0, match.start() - context_chars)
            hi = min(len(text), match.end() + context_chars)
            context = text[lo:hi]
            if allow_re and allow_re.search(context):
                continue
            snippet = re.sub(r"\s+", " ", text[max(0, match.start()-45):match.end()+45])
            failures.append(f"[{reason}] …{snippet}…")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()

    html = args.report.read_text(encoding="utf-8")
    spec = load_json(args.spec)

    correction_marker = spec.get("correction_marker", "已移除或更正的主張")
    idx = html.find(correction_marker)
    body = html[:idx] if idx >= 0 else html

    allow_terms = spec.get("allow_context_terms", DEFAULT_ALLOW_CONTEXT_TERMS)
    context_chars = int(spec.get("allow_context_chars", 160))
    failures: list[str] = []

    claims = list(spec.get("stale_claims", [])) + list(spec.get("resolved_claims", []))
    claim_failures = scan_claims(body, claims, allow_terms, context_chars)
    if claim_failures:
        print("═══ Stale / resolved claim scan ═══")
        for failure in claim_failures:
            print("  ✗", failure)
        failures.extend(claim_failures)

    canonical = spec.get("canonical_values", [])
    if canonical:
        print("\n═══ Canonical values ═══")
    for item in canonical:
        value = str(item["value"])
        label = item.get("label", value)
        minimum = int(item.get("min_occurrences", 1))
        count = body.count(value)
        ok = count >= minimum
        print(f"  {'✓' if ok else '✗'} {label}: {value!r} — {count} occurrence(s), need {minimum}")
        if not ok:
            failures.append(f"missing canonical value: {label} ({value})")

    arithmetic = spec.get("arithmetic", [])
    if arithmetic:
        print("\n═══ Arithmetic assertions ═══")
    for item in arithmetic:
        label = item.get("label", item["expression"])
        expression = item["expression"]
        try:
            ok = bool(safe_eval(expression))
        except Exception as exc:
            ok = False
            print(f"  ✗ {label}: invalid expression ({exc})")
            failures.append(f"invalid arithmetic assertion: {label}")
            continue
        print(f"  {'✓' if ok else '✗'} {label}")
        if not ok:
            failures.append(f"arithmetic assertion failed: {label}")

    print(f"\n{'═'*40}\nFailure count: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
