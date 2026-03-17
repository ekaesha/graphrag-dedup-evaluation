from pathlib import Path
import argparse
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from graphrag_dedup.adapters import normalize_export


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework", required=True, choices=["hirag", "lightrag", "fastrag"])
    parser.add_argument("--raw-nodes", required=True)
    parser.add_argument("--raw-edges", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    with open(args.raw_nodes, "r", encoding="utf-8") as f:
        raw_nodes = json.load(f)
    with open(args.raw_edges, "r", encoding="utf-8") as f:
        raw_edges = json.load(f)

    normalize_export(raw_nodes, raw_edges, args.framework, Path(args.output_dir))
    print(f"Normalized export written to {args.output_dir}")


if __name__ == "__main__":
    main()
