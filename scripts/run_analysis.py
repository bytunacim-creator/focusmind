"""
python scripts/run_analysis.py

Uçtan uca analiz pipeline'ını çalıştırır: sentetik veri üret → istatistik →
ML (GroupKFold) → sonuçları research/analysis/ altına CSV olarak yazar.

UYARI: Varsayılan olarak DEMO_MODE=True çalışır. Gerçek veri üzerinde
çalıştırmak için gerçek bir veritabanından okuma eklenmelidir (bu iskelet
sürümünde kapsam dışıdır — bkz. Faz 4+).
"""
import sys
import os
import json
import subprocess
import uuid
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pandas as pd
import numpy as np

from app.services.synthetic_data import generate_synthetic_dataset
from app.analytics.statistics import (
    compute_reaction_time_summary, compute_switch_cost_ies,
    compute_sustained_attention_score, run_mixed_effects_model,
)
from app.ml.pipeline import evaluate_with_group_kfold

DEMO_MODE = True
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "research", "analysis")


def get_code_version() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "no-git-repo"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    run_id = str(uuid.uuid4())
    dataset_version = f"synthetic-{datetime.date.today().isoformat()}" if DEMO_MODE else "UNKNOWN"
    code_version = get_code_version()
    seed = 42

    print(f"[run_analysis] run_id={run_id} dataset_version={dataset_version} "
          f"code_version={code_version} DEMO_MODE={DEMO_MODE}")

    # 1) Veri
    data = generate_synthetic_dataset(n_participants=30, n_days_per_participant=10, seed=seed)
    sessions_df = pd.DataFrame(data["sessions"])
    behavior_df = pd.DataFrame(data["daily_behavior"])
    reaction_df = pd.DataFrame(data["reaction_trials"])
    attention_df = pd.DataFrame(data["attention_trials"])
    switch_df = pd.DataFrame(data["task_switch_trials"])

    assert sessions_df["is_demo"].all(), "DEMO_MODE dışı çalıştırma bu script'te desteklenmiyor"

    # 2) Betimsel + türetilmiş skorlar
    rt_summary = compute_reaction_time_summary(reaction_df)
    switch_summary = compute_switch_cost_ies(switch_df)
    attention_summary = compute_sustained_attention_score(attention_df)

    merged = (
        sessions_df[["session_id", "participant_id"]]
        .merge(behavior_df, on="session_id", how="left")
        .merge(rt_summary, on="session_id", how="left")
        .merge(switch_summary, on="session_id", how="left")
        .merge(attention_summary, on="session_id", how="left")
    )
    merged.to_csv(os.path.join(OUTPUT_DIR, "descriptive_statistics.csv"), index=False)
    print(f"[run_analysis] descriptive_statistics.csv yazıldı ({len(merged)} satır)")

    numeric_cols = ["sleep_duration", "screen_time", "social_media_time",
                     "notification_count", "study_time", "median_rt", "sd_rt",
                     "switch_cost_ies", "sustained_attention_score"]
    corr = merged[numeric_cols].corr(method="spearman")
    corr.to_csv(os.path.join(OUTPUT_DIR, "correlation_matrix.csv"))
    print("[run_analysis] correlation_matrix.csv yazıldı")

    # 3) Mixed-effects model (kişi-içi ayrıştırma ile)
    model_input = merged.dropna(subset=["median_rt", "screen_time"])
    mixed_result = run_mixed_effects_model(
        model_input, dependent_var="median_rt", predictor_var="screen_time",
        group_col="participant_id",
    )
    with open(os.path.join(OUTPUT_DIR, "regression_results.json"), "w") as f:
        json.dump(mixed_result, f, indent=2, default=str)
    print(f"[run_analysis] mixed-effects model tamamlandı: "
          f"n_obs={mixed_result['n_obs']}, n_groups={mixed_result['n_groups']}, "
          f"converged={mixed_result['converged']}")

    # 4) ML — GroupKFold ile leakage-free değerlendirme
    ml_input = merged.dropna(subset=["median_rt", "screen_time", "sleep_duration"])
    X = ml_input[["screen_time", "sleep_duration", "social_media_time",
                   "notification_count", "study_time"]].fillna(
        ml_input.mean(numeric_only=True)
    )
    y = ml_input["median_rt"].values
    groups = ml_input["participant_id"].values

    ml_results = evaluate_with_group_kfold(X, y, groups, n_splits=5, seed=seed)
    ml_comparison_rows = [
        {"model": name, **{k: v for k, v in r.items() if not isinstance(v, tuple)},
         "mae_ci_low": r["mae_ci95"][0], "mae_ci_high": r["mae_ci95"][1],
         "r2_ci_low": r["r2_ci95"][0], "r2_ci_high": r["r2_ci95"][1]}
        for name, r in ml_results.items()
    ]
    pd.DataFrame(ml_comparison_rows).to_csv(
        os.path.join(OUTPUT_DIR, "ml_model_comparison.csv"), index=False
    )
    print("[run_analysis] ml_model_comparison.csv yazıldı")
    for name, r in ml_results.items():
        print(f"  - {name}: MAE={r['mae']:.2f} (95% CI {r['mae_ci95'][0]:.2f}-"
              f"{r['mae_ci95'][1]:.2f}), R²={r['r2']:.3f}, cv={r['cv_strategy']}")

    # 5) Reprodüksiyon kaydı
    run_metadata = {
        "run_id": run_id,
        "dataset_version": dataset_version,
        "code_version": code_version,
        "random_seed": seed,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "is_demo": True,
        "warning": "DEMO/SYNTHETIC DATA — bu çıktı gerçek bir araştırma bulgusu DEĞİLDİR.",
    }
    with open(os.path.join(OUTPUT_DIR, "run_metadata.json"), "w") as f:
        json.dump(run_metadata, f, indent=2)

    print("\n" + "=" * 70)
    print("UYARI: Bu çalıştırma DEMO/SYNTHETIC veri kullanmıştır.")
    print("Gerçek araştırma sonucu olarak SUNULAMAZ.")
    print("Gerçek veri toplamadan önce docs/ETHICS_AND_CONSENT.md kontrol")
    print("listesinin tamamlanması ZORUNLUDUR.")
    print("=" * 70)


if __name__ == "__main__":
    main()
