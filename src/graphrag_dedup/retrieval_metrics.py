from __future__ import annotations

from typing import Dict, List


def _recall_at_k(retrieved: List[str], gold: List[str], k: int) -> float:
    if not gold:
        return 0.0
    r = set(retrieved[:k])
    g = set(gold)
    return len(r & g) / len(g)


def _precision_at_k(retrieved: List[str], gold: List[str], k: int) -> float:
    if k == 0:
        return 0.0
    r = set(retrieved[:k])
    g = set(gold)
    return len(r & g) / min(k, max(1, len(retrieved[:k])))


def _mrr(retrieved: List[str], gold: List[str]) -> float:
    gold_set = set(gold)
    for idx, item in enumerate(retrieved, start=1):
        if item in gold_set:
            return 1.0 / idx
    return 0.0


def evaluate_retrieval(results: List[Dict], k_values: List[int]) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    for k in k_values:
        recalls, precisions, hits = [], [], []
        for row in results:
            retrieved = [str(x).lower().strip() for x in row["retrieved_node_names"]]
            gold = [str(x).lower().strip() for x in row["gold_node_names"]]
            r = _recall_at_k(retrieved, gold, k)
            p = _precision_at_k(retrieved, gold, k)
            recalls.append(r)
            precisions.append(p)
            hits.append(1.0 if r > 0 else 0.0)
        metrics[f"Recall@{k}"] = round(sum(recalls) / max(len(recalls), 1), 6)
        metrics[f"Precision@{k}"] = round(sum(precisions) / max(len(precisions), 1), 6)
        metrics[f"HitRate@{k}"] = round(sum(hits) / max(len(hits), 1), 6)
    metrics["MRR"] = round(sum(_mrr([str(x).lower().strip() for x in r["retrieved_node_names"]], [str(x).lower().strip() for x in r["gold_node_names"]]) for r in results) / max(len(results), 1), 6)
    return metrics
