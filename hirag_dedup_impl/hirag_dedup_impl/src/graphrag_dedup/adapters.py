from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .io import dump_json
from .schema import Node, Edge


def normalize_export(raw_nodes: List[Dict], raw_edges: List[Dict], framework: str, output_dir: Path) -> None:
    nodes = []
    for i, n in enumerate(raw_nodes, start=1):
        nodes.append(Node(
            node_id=str(n.get("node_id", f"n{i}")),
            name=n.get("name") or n.get("label") or n.get("text") or f"node_{i}",
            type=n.get("type", "Entity"),
            aliases=n.get("aliases", []),
            source_chunks=n.get("source_chunks", n.get("chunks", [])),
            framework=framework,
            dedup_mode="no_dedup",
        ))
    edges = []
    for i, e in enumerate(raw_edges, start=1):
        edges.append(Edge(
            edge_id=str(e.get("edge_id", f"e{i}")),
            source=str(e.get("source")),
            target=str(e.get("target")),
            relation=e.get("relation", "related_to"),
            source_chunks=e.get("source_chunks", e.get("chunks", [])),
            framework=framework,
            dedup_mode="no_dedup",
        ))
    output_dir.mkdir(parents=True, exist_ok=True)
    dump_json([n.to_dict() for n in nodes], output_dir / "nodes.json")
    dump_json([e.to_dict() for e in edges], output_dir / "edges.json")
