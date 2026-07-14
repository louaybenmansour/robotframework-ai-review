"""
Calcule precision/rappel par LLM, par version de prompt, et par categorie
(bad/medium/good) a partir de results/comparaison.csv rempli manuellement.

Usage:
    python3 tools/compute_metrics.py
"""

import pandas as pd

CSV_PATH = "results/comparaison.csv"
LLMS = ["claude", "chatgpt", "gemini"]


def compute_for_subset(df_subset, label):
    total = len(df_subset)
    if total == 0:
        return
    print(f"\n--- {label} (n={total}) ---")
    for llm in LLMS:
        col_d = f"detecte_par_{llm}"
        col_fp = f"faux_positif_{llm}"
        if col_d not in df_subset.columns:
            continue
        vp = df_subset[col_d].sum()
        fp = df_subset[col_fp].sum()
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        rappel = vp / total if total > 0 else 0
        print(f"  {llm.upper():8s} precision={precision:.2f}  rappel={rappel:.2f}  (VP={vp} FP={fp})")


def main():
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        print(f"{CSV_PATH} est vide. Remplis-le d'abord avec tes observations.")
        return

    print("=== RESULTATS GLOBAUX ===")
    compute_for_subset(df, "Tous prompts confondus")

    if "prompt_version" in df.columns:
        print("\n=== PAR VERSION DE PROMPT ===")
        for pv in sorted(df["prompt_version"].unique()):
            compute_for_subset(df[df["prompt_version"] == pv], pv)

    if "category" in df.columns:
        print("\n=== PAR CATEGORIE DE SCRIPT ===")
        for cat in sorted(df["category"].unique()):
            compute_for_subset(df[df["category"] == cat], cat)


if __name__ == "__main__":
    main()
