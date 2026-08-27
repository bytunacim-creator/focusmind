"""
ML pipeline — bkz. docs/ML_METHODOLOGY.md (kod örnekleri buradan üretilmiştir).
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
from sklearn.utils import resample
from typing import Dict, List, Tuple

MIN_SAMPLES_FOR_RF = 150
MIN_PARTICIPANTS_FOR_RF = 25


def get_candidate_models(n_observations: int, n_participants: int) -> Dict[str, object]:
    """Bkz. ML_METHODOLOGY.md §3 — model sırası ve eşikler."""
    models = {
        "mean_baseline": DummyRegressor(strategy="mean"),
        "linear_regression": LinearRegression(),
        "ridge": Ridge(alpha=1.0),
        "lasso": Lasso(alpha=0.1),
    }
    if n_observations >= MIN_SAMPLES_FOR_RF and n_participants >= MIN_PARTICIPANTS_FOR_RF:
        models["random_forest"] = RandomForestRegressor(
            n_estimators=200, max_depth=4, random_state=42
        )
    # Gradient Boosting kasıtlı olarak eklenmedi — bkz. ARCHITECTURE_DECISIONS.md AD-3
    return models


def bootstrap_ci(y_true: np.ndarray, y_pred: np.ndarray, participant_ids: np.ndarray,
                  metric_fn, n_boot: int = 1000, seed: int = 42) -> Tuple[float, float]:
    """Katılımcı-düzeyinde bootstrap %95 güven aralığı. Bkz. ML_METHODOLOGY.md §4."""
    rng = np.random.default_rng(seed)
    unique_ids = np.unique(participant_ids)
    scores = []
    for _ in range(n_boot):
        sampled_ids = rng.choice(unique_ids, size=len(unique_ids), replace=True)
        mask = np.isin(participant_ids, sampled_ids)
        if mask.sum() < 2:
            continue
        scores.append(metric_fn(y_true[mask], y_pred[mask]))
    return tuple(np.percentile(scores, [2.5, 97.5])) if scores else (np.nan, np.nan)


def evaluate_with_group_kfold(
    X: pd.DataFrame, y: np.ndarray, groups: np.ndarray, n_splits: int = 5, seed: int = 42
) -> Dict[str, dict]:
    """
    Katılımcı-farkında (leakage-free) çapraz doğrulama.
    ZORUNLU: groups=participant_id. Bkz. ML_METHODOLOGY.md §2.
    """
    n_participants = len(np.unique(groups))
    models = get_candidate_models(n_observations=len(X), n_participants=n_participants)
    gkf = GroupKFold(n_splits=min(n_splits, n_participants))

    results = {}
    for name, model in models.items():
        all_y_true, all_y_pred, all_groups = [], [], []
        for train_idx, test_idx in gkf.split(X, y, groups=groups):
            # Sızıntı kontrolü — bkz. tests/test_ml_leakage.py ile aynı mantık
            assert set(groups[train_idx]).isdisjoint(set(groups[test_idx])), \
                "Katılımcı sızıntısı tespit edildi!"
            model.fit(X.iloc[train_idx], y[train_idx])
            pred = model.predict(X.iloc[test_idx])
            all_y_true.extend(y[test_idx])
            all_y_pred.extend(pred)
            all_groups.extend(groups[test_idx])

        y_true_arr = np.array(all_y_true)
        y_pred_arr = np.array(all_y_pred)
        groups_arr = np.array(all_groups)

        mae = mean_absolute_error(y_true_arr, y_pred_arr)
        rmse = float(np.sqrt(mean_squared_error(y_true_arr, y_pred_arr)))
        r2 = r2_score(y_true_arr, y_pred_arr)

        mae_ci = bootstrap_ci(y_true_arr, y_pred_arr, groups_arr, mean_absolute_error)
        rmse_ci = bootstrap_ci(
            y_true_arr, y_pred_arr, groups_arr,
            lambda a, b: float(np.sqrt(mean_squared_error(a, b)))
        )
        r2_ci = bootstrap_ci(y_true_arr, y_pred_arr, groups_arr, r2_score)

        results[name] = {
            "mae": mae, "mae_ci95": mae_ci,
            "rmse": rmse, "rmse_ci95": rmse_ci,
            "r2": r2, "r2_ci95": r2_ci,
            "n_observations": len(y_true_arr),
            "n_participants": n_participants,
            "cv_strategy": f"GroupKFold(n_splits={gkf.n_splits})",
        }
    return results


def compute_permutation_importance(model, X_test: pd.DataFrame, y_test: np.ndarray,
                                    seed: int = 42) -> List[dict]:
    """Bkz. ML_METHODOLOGY.md §5. YASAK: nedensellik dili kullanmak."""
    result = permutation_importance(model, X_test, y_test, n_repeats=30, random_state=seed)
    importances = [
        {"feature": col, "importance_mean": float(m), "importance_std": float(s)}
        for col, m, s in zip(X_test.columns, result.importances_mean, result.importances_std)
    ]
    return sorted(importances, key=lambda d: d["importance_mean"], reverse=True)
