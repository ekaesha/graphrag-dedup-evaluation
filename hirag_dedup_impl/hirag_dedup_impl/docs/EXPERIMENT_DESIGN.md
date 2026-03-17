# Experiment Design

## Goal

Evaluate how deduplication affects GraphRAG-style systems at three levels:

1. graph structure
2. retrieval quality
3. QA quality

## Compared frameworks

- HiRAG
- LightRAG
- Fast GraphRAG

## Compared modes

- `no_dedup`
- `lexical`
- `semantic`

## Expected protocol

1. Build graphs in the upstream framework.
2. Export `nodes.json` and `edges.json`.
3. Normalize to the unified schema if needed.
4. Run the evaluation pipeline.
5. Compare metrics across frameworks and deduplication modes.

## Main hypotheses

- Deduplication reduces graph redundancy.
- Deduplication can improve retrieval by consolidating evidence.
- Deduplication may improve QA quality when duplicate evidence fragments are merged.
- The effect is framework-dependent.

## Core metrics

### Graph metrics

- node count
- edge count
- duplicate reduction rate
- connected components
- density

### Retrieval metrics

- Recall@k
- Precision@k
- HitRate@k
- MRR

### QA metrics

- Exact Match
- Token F1
- ROUGE-L
- Grounding Proxy
- Answer Redundancy

## Notes

This repository is meant to be the evaluation layer. It is intentionally separated from upstream GraphRAG implementations so that the benchmarking logic remains reusable across multiple frameworks.
