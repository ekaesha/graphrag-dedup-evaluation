from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass
class Node:
    node_id: str
    name: str
    type: str = "Entity"
    aliases: List[str] = field(default_factory=list)
    source_chunks: List[str] = field(default_factory=list)
    framework: str = "unknown"
    dedup_mode: str = "no_dedup"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Edge:
    edge_id: str
    source: str
    target: str
    relation: str
    source_chunks: List[str] = field(default_factory=list)
    framework: str = "unknown"
    dedup_mode: str = "no_dedup"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
