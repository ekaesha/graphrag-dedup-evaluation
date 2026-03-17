from __future__ import annotations

from collections import Counter
from typing import Dict, List

from .textnorm import normalize_text


def _tokens(text: str) -> List[str]:
    return normalize_text(text).split()


def exact_match(pred: str, gold: str) -> float:
    return 1.0 if normalize_text(pred) == normalize_text(gold) else 0.0


def token_f1(pred: str, gold: str) -> float:
    p = _tokens(pred)
    g = _tokens(gold)
    if not p or not g:
        return 0.0
    common = Counter(p) & Counter(g)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = num_same / len(p)
    recall = num_same / len(g)
    return 2 * precision * recall / (precision + recall)


def rouge_l(pred: str, gold: str) -> float:
    p = _tokens(pred)
    g = _tokens(gold)
    if not p or not g:
        return 0.0
    dp = [[0] * (len(g) + 1) for _ in range(len(p) + 1)]
    for i in range(1, len(p) + 1):
        for j in range(1, len(g) + 1):
            if p[i - 1] == g[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[-1][-1]
    precision = lcs / len(p)
    recall = lcs / len(g)
    return 0.0 if precision + recall == 0 else (2 * precision * recall / (precision + recall))


def redundancy_score(pred: str, n: int = 3) -> float:
    tokens = _tokens(pred)
    if len(tokens) < n:
        return 0.0
    ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    uniq = len(set(ngrams))
    return 1.0 - (uniq / len(ngrams))


def grounding_proxy(pred: str, evidence_text: str) -> float:
    pt = set(_tokens(pred))
    et = set(_tokens(evidence_text))
    if not pt:
        return 0.0
    return len(pt & et) / len(pt)


def evaluate_qa(rows: List[Dict]) -> Dict[str, float]:
    metrics = {
        "ExactMatch": round(sum(exact_match(r["prediction"], r["gold_answer"]) for r in rows) / max(len(rows), 1), 6),
        "TokenF1": round(sum(token_f1(r["prediction"], r["gold_answer"]) for r in rows) / max(len(rows), 1), 6),
        "ROUGE-L": round(sum(rouge_l(r["prediction"], r["gold_answer"]) for r in rows) / max(len(rows), 1), 6),
        "AnswerRedundancy": round(sum(redundancy_score(r["prediction"]) for r in rows) / max(len(rows), 1), 6),
        "GroundingProxy": round(sum(grounding_proxy(r["prediction"], r.get("evidence_text", "")) for r in rows) / max(len(rows), 1), 6),
    }
    return metrics
