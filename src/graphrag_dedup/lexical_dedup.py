from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from rapidfuzz import fuzz

from .schema import Node, Edge
from .textnorm import normalize_text


class LexicalDeduplicator:
    def __init__(self, fuzzy_threshold: int = 92):
        self.fuzzy_threshold = fuzzy_threshold

    def _canonical_label(self, node: Node) -> str:
        return normalize_text(node.name)

    def deduplicate(self, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], List[Edge], Dict[str, str]]:
        canonical_nodes: List[Node] = []
        mapping: Dict[str, str] = {}
        groups: List[List[Node]] = []

        for node in nodes:
            assigned = False
            norm = self._canonical_label(node)
            for group in groups:
                rep = group[0]
                rep_norm = self._canonical_label(rep)
                if norm == rep_norm or fuzz.ratio(norm, rep_norm) >= self.fuzzy_threshold:
                    group.append(node)
                    mapping[node.node_id] = rep.node_id
                    assigned = True
                    break
            if not assigned:
                groups.append([node])
                mapping[node.node_id] = node.node_id

        for group in groups:
            rep = group[0]
            aliases = set(rep.aliases)
            source_chunks = set(rep.source_chunks)
            best_name = rep.name
            for node in group[1:]:
                aliases.add(node.name)
                aliases.update(node.aliases)
                source_chunks.update(node.source_chunks)
                if len(node.name) < len(best_name):
                    best_name = node.name
            rep.name = best_name
            rep.aliases = sorted(a for a in aliases if a and a != rep.name)
            rep.source_chunks = sorted(source_chunks)
            canonical_nodes.append(rep)

        new_edges_map: Dict[tuple, Edge] = {}
        for edge in edges:
            new_source = mapping[edge.source]
            new_target = mapping[edge.target]
            key = (new_source, new_target, normalize_text(edge.relation))
            if key not in new_edges_map:
                new_edge = Edge(
                    edge_id=edge.edge_id,
                    source=new_source,
                    target=new_target,
                    relation=edge.relation,
                    source_chunks=list(edge.source_chunks),
                    framework=edge.framework,
                    dedup_mode="lexical",
                )
                new_edges_map[key] = new_edge
            else:
                merged = new_edges_map[key]
                merged.source_chunks = sorted(set(merged.source_chunks) | set(edge.source_chunks))

        for node in canonical_nodes:
            node.dedup_mode = "lexical"
        return canonical_nodes, list(new_edges_map.values()), mapping
