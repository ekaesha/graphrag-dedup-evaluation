from __future__ import annotations

from typing import Dict, List

import networkx as nx

from .schema import Node, Edge
from .textnorm import normalize_text


def graph_from_lists(nodes: List[Node], edges: List[Edge]) -> nx.Graph:
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.node_id, name=node.name, type=node.type)
    for edge in edges:
        G.add_edge(edge.source, edge.target, relation=edge.relation)
    return G


def count_near_duplicate_names(nodes: List[Node]) -> int:
    seen = {}
    dups = 0
    for n in nodes:
        key = (n.type, normalize_text(n.name))
        if key in seen:
            dups += 1
        seen[key] = True
    return dups


def count_duplicate_edges(edges: List[Edge]) -> int:
    seen = set()
    dups = 0
    for e in edges:
        key = (e.source, e.target, normalize_text(e.relation))
        if key in seen:
            dups += 1
        seen.add(key)
    return dups


def duplicate_reduction_rate(before: int, after: int) -> float:
    if before == 0:
        return 0.0
    return (before - after) / before


def compute_graph_metrics(nodes: List[Node], edges: List[Edge], baseline_nodes: int | None = None, baseline_edges: int | None = None) -> Dict[str, float]:
    G = graph_from_lists(nodes, edges)
    node_count = len(nodes)
    edge_count = len(edges)
    avg_degree = 0.0 if node_count == 0 else sum(dict(G.degree()).values()) / node_count
    components = nx.number_connected_components(G) if node_count else 0
    density = nx.density(G) if node_count > 1 else 0.0
    out = {
        "nodes": node_count,
        "edges": edge_count,
        "avg_degree": round(avg_degree, 4),
        "connected_components": components,
        "density": round(density, 6),
        "duplicate_names_remaining": count_near_duplicate_names(nodes),
        "duplicate_edges_remaining": count_duplicate_edges(edges),
    }
    if baseline_nodes is not None:
        out["node_drr"] = round(duplicate_reduction_rate(baseline_nodes, node_count), 6)
    if baseline_edges is not None:
        out["edge_drr"] = round(duplicate_reduction_rate(baseline_edges, edge_count), 6)
    return out
