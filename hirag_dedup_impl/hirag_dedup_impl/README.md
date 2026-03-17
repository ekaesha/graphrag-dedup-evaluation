# Deduplication benchmark for HiRAG, LightRAG, and Fast GraphRAG

This package implements the full experimental scaffold for comparing deduplication across three GraphRAG-style systems:
- HiRAG
- LightRAG
- Fast GraphRAG

It covers:
- unified graph export format
- lexical deduplication
- semantic deduplication
- graph-level metrics
- retrieval benchmark
- QA metrics
- reproducible experiment runner
- a working sample dataset with duplicates

## What is implemented

### 1. Unified graph schema
Every framework is normalized to the same format:
- `nodes.json`
- `edges.json`

### 2. Deduplication modes
- `no_dedup`
- `lexical`
- `semantic`

### 3. Metrics
#### Graph metrics
- node count
- edge count
- average degree
- connected components
- density
- duplicate reduction rate (DRR)

#### Retrieval metrics
- Recall@k
- Precision@k
- MRR
- Hit Rate

#### QA metrics
- token-level F1
- exact match
- ROUGE-L
- answer redundancy
- grounding proxy

## Project layout

```text
hirag_dedup_impl/
├── config/
├── data/
├── results/
├── scripts/
└── src/graphrag_dedup/
```

## Quick start

Run the full sample experiment:

```bash
python scripts/run_sample_experiment.py
```

This generates results in `results/sample_run/`.

## Real-data workflow

1. Export graphs from HiRAG, LightRAG, and Fast GraphRAG.
2. Normalize them into the unified schema.
3. Put them under:

```text
results/real_run/exports/<framework>/no_dedup/
```

4. Run:

```bash
python scripts/run_real_experiment.py --input-root results/real_run/exports --output-root results/real_run
```
```

## Unified schema

### nodes.json
```json
[
  {
    "node_id": "n1",
    "name": "Aspirin",
    "type": "Drug",
    "aliases": ["aspirin", "acetylsalicylic acid"],
    "source_chunks": ["c1", "c2"],
    "framework": "hirag",
    "dedup_mode": "no_dedup"
  }
]
```

### edges.json
```json
[
  {
    "edge_id": "e1",
    "source": "n1",
    "target": "n2",
    "relation": "treats",
    "source_chunks": ["c3"],
    "framework": "hirag",
    "dedup_mode": "no_dedup"
  }
]
```

## Important note
This package fully implements the downstream experimental pipeline. Running the original upstream frameworks still requires the actual repositories, their environment, and the user’s local APIs or credentials. The included sample run proves the deduplication/evaluation pipeline works end-to-end.
