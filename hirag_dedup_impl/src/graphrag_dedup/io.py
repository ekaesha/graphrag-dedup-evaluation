from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple, Dict, Any

from .schema import Node, Edge


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def load_graph(graph_dir: Path) -> Tuple[List[Node], List[Edge]]:
    nodes_raw = load_json(graph_dir / "nodes.json")
    edges_raw = load_json(graph_dir / "edges.json")
    nodes = [Node(**n) for n in nodes_raw]
    edges = [Edge(**e) for e in edges_raw]
    return nodes, edges


def save_graph(nodes: List[Node], edges: List[Edge], graph_dir: Path) -> None:
    graph_dir.mkdir(parents=True, exist_ok=True)
    dump_json([n.to_dict() for n in nodes], graph_dir / "nodes.json")
    dump_json([e.to_dict() for e in edges], graph_dir / "edges.json")


def load_questions(path: Path) -> List[Dict[str, Any]]:
    return load_json(path)
