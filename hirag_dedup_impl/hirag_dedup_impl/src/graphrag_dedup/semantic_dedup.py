from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .schema import Node, Edge
from .textnorm import normalize_text


DEFAULT_ALIAS_DICT = {
    "aspirin": {"acetylsalicylic acid", "asa"},
    "myocardial infarction": {"heart attack", "mi"},
    "hypertension": {"high blood pressure"},
    "ibuprofen": {"advil"},
}


class SemanticDeduplicator:
    def __init__(self, similarity_threshold: float = 0.58, alias_dictionary: Dict[str, set] | None = None):
        self.similarity_threshold = similarity_threshold
        self.alias_dictionary = alias_dictionary or DEFAULT_ALIAS_DICT

    def _equivalent_by_alias(self, a: str, b: str) -> bool:
        an = normalize_text(a)
        bn = normalize_text(b)
        if an == bn:
            return True
        for canon, aliases in self.alias_dictionary.items():
            normalized = {normalize_text(canon)} | {normalize_text(x) for x in aliases}
            if an in normalized and bn in normalized:
                return True
        return False

    def deduplicate(self, nodes: List[Node], edges: List[Edge]) -> Tuple[List[Node], List[Edge], Dict[str, str]]:
        labels = []
        for n in nodes:
            pieces = [n.name] + n.aliases
            labels.append(" ; ".join(sorted(set(filter(None, pieces)))))

        vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
        X = vectorizer.fit_transform(labels)
        sim = cosine_similarity(X)

        parent = list(range(len(nodes)))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                cond = sim[i, j] >= self.similarity_threshold or self._equivalent_by_alias(nodes[i].name, nodes[j].name)
                if cond and nodes[i].type == nodes[j].type:
                    union(i, j)

        groups: Dict[int, List[int]] = {}
        for i in range(len(nodes)):
            groups.setdefault(find(i), []).append(i)

        mapping: Dict[str, str] = {}
        new_nodes: List[Node] = []
        root_to_newid: Dict[int, str] = {}

        for root, idxs in groups.items():
            members = [nodes[i] for i in idxs]
            rep = sorted(members, key=lambda n: (len(normalize_text(n.name)), n.name))[0]
            root_to_newid[root] = rep.node_id
            aliases = set(rep.aliases)
            source_chunks = set(rep.source_chunks)
            for m in members:
                aliases.add(m.name)
                aliases.update(m.aliases)
                source_chunks.update(m.source_chunks)
                mapping[m.node_id] = rep.node_id
            rep.aliases = sorted(a for a in aliases if a and a != rep.name)
            rep.source_chunks = sorted(source_chunks)
            rep.dedup_mode = "semantic"
            new_nodes.append(rep)

        edge_map: Dict[tuple, Edge] = {}
        for edge in edges:
            s = mapping[edge.source]
            t = mapping[edge.target]
            key = (s, t, normalize_text(edge.relation))
            if key not in edge_map:
                edge_map[key] = Edge(
                    edge_id=edge.edge_id,
                    source=s,
                    target=t,
                    relation=edge.relation,
                    source_chunks=list(edge.source_chunks),
                    framework=edge.framework,
                    dedup_mode="semantic",
                )
            else:
                edge_map[key].source_chunks = sorted(set(edge_map[key].source_chunks) | set(edge.source_chunks))

        return new_nodes, list(edge_map.values()), mapping
