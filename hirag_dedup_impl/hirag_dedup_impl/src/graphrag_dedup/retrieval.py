from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

import networkx as nx
from rapidfuzz import fuzz

from .graph_metrics import graph_from_lists
from .schema import Node, Edge
from .textnorm import normalize_text, token_set


def build_node_index(nodes: List[Node]) -> Dict[str, Node]:
    return {n.node_id: n for n in nodes}


class SimpleGraphRetriever:
    def __init__(self, expansion_hops: int = 1):
        self.expansion_hops = expansion_hops

    def retrieve(self, question: str, nodes: List[Node], edges: List[Edge], top_k: int = 5) -> Dict[str, List[str]]:
        G = graph_from_lists(nodes, edges)
        node_index = build_node_index(nodes)
        qnorm = normalize_text(question)
        qtokens = token_set(question)
        scored = []
        for node in nodes:
            label = " ".join([node.name] + node.aliases)
            lnorm = normalize_text(label)
            lexical = fuzz.partial_ratio(qnorm, lnorm) / 100.0
            overlap = len(qtokens & token_set(label)) / max(len(qtokens), 1)
            score = 0.7 * lexical + 0.3 * overlap
            scored.append((score, node.node_id))
        scored.sort(reverse=True)
        seeds = [nid for _, nid in scored[:max(1, min(top_k, 3))]]

        retrieved_nodes = set(seeds)
        for seed in seeds:
            if seed in G:
                lengths = nx.single_source_shortest_path_length(G, seed, cutoff=self.expansion_hops)
                retrieved_nodes.update(lengths.keys())

        ranked = sorted(retrieved_nodes, key=lambda nid: next((1-s for s, x in scored if x == nid), 999))
        ranked = ranked[:top_k]
        retrieved_edges = []
        ranked_set = set(ranked)
        for e in edges:
            if e.source in ranked_set and e.target in ranked_set:
                retrieved_edges.append(e.edge_id)
        return {
            "retrieved_node_ids": ranked,
            "retrieved_edge_ids": retrieved_edges[:top_k],
        }
