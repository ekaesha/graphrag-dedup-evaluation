# GraphRAG Dedup Eval

Evaluation pipeline for studying the effect of deduplication in GraphRAG-style systems.

## Overview

This repository contains an evaluation pipeline for deduplication experiments in graph-based retrieval-augmented generation systems. The project is designed to support graph exports from frameworks such as HiRAG, LightRAG, and Fast GraphRAG.

The pipeline includes:
- graph normalization to a unified schema
- lexical deduplication
- semantic deduplication
- graph-level metrics
- retrieval metrics
- QA evaluation
- sample experiment scripts and outputs

## Repository structure

- `src/` — core implementation
- `scripts/` — experiment runners
- `config/` — configuration files
- `data/` — sample data
- `results/` — sample outputs
- `IMPLEMENTED.md` — summary of implemented components

## Current status

Implemented:
- unified graph schema
- lexical deduplication module
- semantic deduplication module
- graph metrics
- retrieval metrics
- QA metrics
- sample experiment pipeline

In progress:
- integration with real graph exports from HiRAG, LightRAG, and Fast GraphRAG

Planned:
- full-scale experiments on the target domain dataset
- extended ablation study for deduplication strategies

## How to run

Install dependencies:

```bash
py -3.14 -m pip install -r requirements.txt
```

## Important note
This package fully implements the downstream experimental pipeline. Running the original upstream frameworks still requires the actual repositories, their environment, and the user’s local APIs or credentials. The included sample run proves the deduplication/evaluation pipeline works end-to-end.
