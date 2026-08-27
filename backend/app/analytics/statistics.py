"""
Klasik istatistik pipeline'ı.
Bkz. docs/PROJECT_PLAN.md §4 ve RESEARCH_PROTOCOL.md §8.

UYARI: Bu modülün "anlamlı" ifadesini kullanabilmesi için gerçek p-değeri
hesaplanmış olmalıdır. is_demo=True veri üzerinde bu fonksiyonlar çalıştırılabilir
(pipeline testi için) ama çıktı ASLA "araştırma bulgusu" olarak sunulmamalıdır —
çağıran kod bu bayrağı taşımak ve göstermek zorundadır.
"""
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf
from typing import Dict, Any


def compute_reaction_time_summary(reaction_trials_df: pd.DataFrame) -> pd.DataFrame:
    """Oturum başına medyan RT, SD, CV hesaplar (yalnızca valid & correct trial'lar)."""
    valid = reaction_trials_df[
        (reaction_trials_df["valid"]) & (reaction_trials_df["correct"])
        & (reaction_trials_df["reaction_time"].notna())
    ]
    summary = valid.groupby("session_id")["reaction_time"].agg(
        median_rt="median", sd_rt="std", n_valid_trials="count"
    ).reset_index()
    summary["cv_rt"] = summary["sd_rt"] / summary["median_rt"]
    return summary


def compute_switch_cost_ies(task_switch_df: pd.DataFrame) -> pd.DataFrame:
    """
    Inverse Efficiency Score tabanlı switch-cost.
    IES = mean(RT) / accuracy_rate, switch ve repeat için ayrı hesaplanır.
    Bkz. RESEARCH_PROTOCOL.md §5, REFERENCES.md #12.
    """
    valid = task_switch_df[task_switch_df["valid"]]

    def _ies(group):
        acc = group["correct"].mean()
        mean_rt = group.loc[group["correct"], "reaction_time"].mean()
        if acc == 0:
            return np.nan
        return mean_rt / acc

    results = []
    for session_id, g in valid.groupby("session_id"):
        ies_switch = _ies(g[g["is_switch_trial"]])
        ies_repeat = _ies(g[~g["is_switch_trial"]])
        results.append({
            "session_id": session_id,
            "ies_switch": ies_switch,
            "ies_repeat": ies_repeat,
            "switch_cost_ies": ies_switch - ies_repeat,
        })
    return pd.DataFrame(results)


def compute_sustained_attention_score(attention_df: pd.DataFrame) -> pd.DataFrame:
    """Standardize edilmiş bileşik skor. Bkz. RESEARCH_PROTOCOL.md §4."""
    valid = attention_df[attention_df["valid"]]

    def _agg(group):
        omissions = (group["error_type"] == "omission").sum()
        commissions = (group["error_type"] == "commission").sum()
        return pd.Series({"omission_errors": omissions, "commission_errors": commissions})

    per_session = valid.groupby("session_id").apply(_agg).reset_index()

    # z-skor standardizasyonu (örneklem içi); ters işaretli — düşük hata = yüksek skor
    for col in ["omission_errors", "commission_errors"]:
        mean, std = per_session[col].mean(), per_session[col].std()
        per_session[f"z_{col}"] = 0.0 if std == 0 else -(per_session[col] - mean) / std

    per_session["sustained_attention_score"] = (
        per_session["z_omission_errors"] + per_session["z_commission_errors"]
    ) / 2
    return per_session[["session_id", "omission_errors", "commission_errors",
                         "sustained_attention_score"]]


def within_person_center(df: pd.DataFrame, participant_col: str, value_col: str) -> pd.DataFrame:
    """
    Kişi-içi (within-person) merkezleme — PROJECT_PLAN.md §12.1 Karar 1'in
    istatistiksel temeli. Her gözlemi, o katılımcının kendi ortalamasından
    farkı olarak yeniden ifade eder.
    """
    df = df.copy()
    person_mean = df.groupby(participant_col)[value_col].transform("mean")
    df[f"{value_col}_within"] = df[value_col] - person_mean
    df[f"{value_col}_between"] = person_mean  # kişiler-arası bileşen, kontrol için
    return df


def run_mixed_effects_model(
    merged_df: pd.DataFrame,
    dependent_var: str,
    predictor_var: str,
    group_col: str = "participant_id",
) -> Dict[str, Any]:
    """
    Tekrarlı ölçüm için mixed-effects model (klasik Pearson korelasyonu YERİNE).
    Bkz. PROJECT_PLAN.md §4 — "tekrarlı ölçüm uyarısı".

    predictor_var, within_person_center ile ayrıştırılmış olmalıdır
    (ör. "screen_time_within" ve "screen_time_between" ayrı ayrı modele girer).
    """
    df = within_person_center(merged_df, group_col, predictor_var)
    formula = f"{dependent_var} ~ {predictor_var}_within + {predictor_var}_between"
    model = smf.mixedlm(formula, df, groups=df[group_col])
    result = model.fit()

    return {
        "formula": formula,
        "params": result.params.to_dict(),
        "pvalues": result.pvalues.to_dict(),
        "conf_int": result.conf_int().to_dict(),
        "n_obs": int(result.nobs),
        "n_groups": df[group_col].nunique(),
        "converged": result.converged,
    }


def split_half_reliability(trial_level_df: pd.DataFrame, session_col: str,
                            value_col: str) -> float:
    """
    Spearman-Brown düzeltmeli split-half güvenilirlik.
    Bkz. RESEARCH_PROTOCOL.md §7.
    """
    odd_even = trial_level_df.copy()
    odd_even["half"] = odd_even.groupby(session_col).cumcount() % 2
    pivoted = odd_even.groupby([session_col, "half"])[value_col].mean().unstack()
    if pivoted.shape[1] < 2 or pivoted.dropna().shape[0] < 3:
        return float("nan")
    r, _ = stats.pearsonr(pivoted[0].dropna(), pivoted[1].dropna())
    return (2 * r) / (1 + r)  # Spearman-Brown düzeltmesi
