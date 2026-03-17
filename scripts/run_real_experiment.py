from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from graphrag_dedup.pipeline import ExperimentRunner


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", required=True, help="Root with <framework>/no_dedup/nodes.json and edges.json")
    parser.add_argument("--questions", default=str(ROOT / "data" / "questions" / "sample_questions.json"))
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--config", default=str(ROOT / "config" / "experiment.yaml"))
    args = parser.parse_args()

    runner = ExperimentRunner(Path(args.config))
    runner.run(input_root=Path(args.input_root), questions_path=Path(args.questions), output_root=Path(args.output_root))
    print(f"Real experiment completed. Results written to: {args.output_root}")


if __name__ == "__main__":
    main()
