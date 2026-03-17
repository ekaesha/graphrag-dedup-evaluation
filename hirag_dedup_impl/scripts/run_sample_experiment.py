from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd
import matplotlib.pyplot as plt

from graphrag_dedup.pipeline import ExperimentRunner


def main() -> None:
    config_path = ROOT / "config" / "experiment.yaml"
    input_root = ROOT / "data" / "sample_graphs"
    questions_path = ROOT / "data" / "questions" / "sample_questions.json"
    output_root = ROOT / "results" / "sample_run"
    output_root.mkdir(parents=True, exist_ok=True)

    runner = ExperimentRunner(config_path)
    runner.run(input_root=input_root, questions_path=questions_path, output_root=output_root)

    graph_df = pd.read_csv(output_root / "graph_metrics.csv")
    retrieval_df = pd.read_csv(output_root / "retrieval_metrics.csv")
    qa_df = pd.read_csv(output_root / "qa_metrics.csv")

    for metric_df, filename, metric_col in [
        (graph_df, "plot_nodes.png", "nodes"),
        (retrieval_df, "plot_recall5.png", "Recall@5"),
        (qa_df, "plot_rougel.png", "ROUGE-L"),
    ]:
        plt.figure(figsize=(8, 4))
        pivot = metric_df.pivot(index="framework", columns="mode", values=metric_col)
        pivot.plot(kind="bar")
        plt.ylabel(metric_col)
        plt.tight_layout()
        plt.savefig(output_root / filename, dpi=180)
        plt.close()

    print(f"Sample experiment completed. Results written to: {output_root}")


if __name__ == "__main__":
    main()
