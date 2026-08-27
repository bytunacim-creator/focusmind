"""
Bkz. docs/TESTING.md — zorunlu test senaryoları.
Çalıştırma: pytest backend/tests
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import GroupKFold

from app.schemas.schemas import ReactionTrialIn
from app.ml.pipeline import evaluate_with_group_kfold
from app.services.synthetic_data import generate_synthetic_dataset


# --- 1. Geçersiz trial testi (RESEARCH_PROTOCOL.md §3) ---
def test_reaction_trial_too_fast_is_invalid():
    trial = ReactionTrialIn(
        trial_id="t1", session_id="s1", trial_index=0,
        stimulus_timestamp=0.0, response_timestamp=100.0,  # 100ms < 150ms eşiği
        correct=True,
    )
    assert trial.compute_valid() is False


def test_reaction_trial_tab_hidden_is_invalid():
    trial = ReactionTrialIn(
        trial_id="t2", session_id="s1", trial_index=1,
        stimulus_timestamp=0.0, response_timestamp=400.0,
        correct=True, tab_hidden_flag=True,
    )
    assert trial.compute_valid() is False


def test_reaction_trial_normal_is_valid():
    trial = ReactionTrialIn(
        trial_id="t3", session_id="s1", trial_index=2,
        stimulus_timestamp=0.0, response_timestamp=350.0,
        correct=True,
    )
    assert trial.compute_valid() is True


# --- 2. Invalid timestamp testi (orijinal talep §29.7, §32) ---
def test_response_before_stimulus_rejected():
    with pytest.raises(ValueError):
        ReactionTrialIn(
            trial_id="t4", session_id="s1", trial_index=3,
            stimulus_timestamp=1000.0, response_timestamp=500.0,  # imkansız
            correct=True,
        )


# --- 3. participant_id format testi (orijinal talep §9) ---
def test_participant_id_must_be_pseudonymous():
    from app.schemas.schemas import SessionCreateIn
    import datetime
    with pytest.raises(ValueError):
        SessionCreateIn(
            participant_id="Ahmet Yilmaz",  # gerçek isim — reddedilmeli
            session_date=datetime.date.today(),
            test_time=datetime.time(18, 0),
            device_type="desktop",
            test_version="1.0.0",
        )


# --- 4. Data leakage testi (orijinal talep §17, ML_METHODOLOGY.md §2) — KRİTİK ---
def test_groupkfold_no_participant_overlap():
    """Her fold'da train ve test participant_id kümeleri KESİNLİKLE ayrık olmalı."""
    n = 200
    rng = np.random.default_rng(0)
    groups = rng.integers(0, 20, size=n)  # 20 katılımcı, tekrarlı gözlemler
    X = pd.DataFrame({"feature": rng.normal(size=n)})
    y = rng.normal(size=n)

    gkf = GroupKFold(n_splits=5)
    for train_idx, test_idx in gkf.split(X, y, groups=groups):
        train_groups = set(groups[train_idx])
        test_groups = set(groups[test_idx])
        assert train_groups.isdisjoint(test_groups), "Katılımcı sızıntısı tespit edildi!"


def test_evaluate_with_group_kfold_runs_on_synthetic_data():
    """Uçtan uca: sentetik veri → GroupKFold pipeline hatasız çalışmalı."""
    data = generate_synthetic_dataset(n_participants=10, n_days_per_participant=5, seed=1)
    behavior_df = pd.DataFrame(data["daily_behavior"])
    sessions_df = pd.DataFrame(data["sessions"])[["session_id", "participant_id"]]
    merged = behavior_df.merge(sessions_df, on="session_id")

    X = merged[["screen_time", "sleep_duration"]].fillna(merged.mean(numeric_only=True))
    y = merged["study_time"].fillna(merged["study_time"].mean()).values
    groups = merged["participant_id"].values

    results = evaluate_with_group_kfold(X, y, groups, n_splits=3)
    assert "mean_baseline" in results
    assert "ridge" in results
    for name, r in results.items():
        assert r["n_participants"] == 10


# --- 5. Demo veri asla "araştırma sonucu" olarak etiketlenemez ---
def test_demo_sessions_are_flagged():
    data = generate_synthetic_dataset(n_participants=3, n_days_per_participant=2)
    assert all(s["is_demo"] is True for s in data["sessions"])
