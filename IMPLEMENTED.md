# What has been implemented

This delivery already contains a working implementation of the full downstream experiment pipeline for deduplication benchmarking across HiRAG, LightRAG, and Fast GraphRAG.

## Implemented components

- Unified graph schema for all three frameworks
- Lexical deduplication module
- Semantic deduplication module
- Graph metrics computation
- Retrieval benchmark and metrics
- QA benchmark and metrics
- Normalization helper for real framework exports
- End-to-end experiment runner
- Sample medical graph dataset with intentional duplicates
- Generated sample experiment outputs and plots

## Files to start with

- `README.md`
- `config/experiment.yaml`
- `scripts/run_sample_experiment.py`
- `scripts/run_real_experiment.py`
- `scripts/normalize_graph_export.py`

## Ready outputs already generated

Under `results/sample_run/` there are already generated:
- `graph_metrics.csv`
- `retrieval_metrics.csv`
- `qa_metrics.csv`
- `retrieval_results.json`
- `qa_results.json`
- plots for nodes, Recall@5, and ROUGE-L

## What still depends on the real framework environment

The only part not executed here is the upstream graph construction inside the original HiRAG, LightRAG, and Fast GraphRAG repositories themselves. That requires:
- the real framework repos
- their environment setup
- your chosen LLM / embedding backend
- your real FarmDoc corpus or exported graph files

Once you have exported each framework graph, the rest of the experiment is already implemented and runnable.
