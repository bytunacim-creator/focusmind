"""
DEMO MODE sentetik veri üreticisi.

ÖNEMLİ: Bu modül orijinal talep §21'e uygun olarak yalnızca geliştirme/demo
amaçlıdır. Üretilen tüm session'lar is_demo=True olarak işaretlenir.
Bu veri ASLA "araştırma sonucu" olarak sunulamaz (bkz. PRIVACY.md §6).
"""
import numpy as np
import uuid
import datetime
from typing import List, Dict


def generate_synthetic_dataset(
    n_participants: int = 25,
    n_days_per_participant: int = 10,
    seed: int = 42,
) -> Dict[str, List[dict]]:
    """
    Gerçekçi ama TAMAMEN SENTETİK bir veri seti üretir.
    Küçük, gerçekçi bir within-person etki (ör. yüksek ekran süresi olan günlerde
    hafifçe daha yüksek RT) gömülüdür — bu SADECE demo/UI/pipeline testi içindir,
    gerçek bir bilimsel bulgu DEĞİLDİR.
    """
    rng = np.random.default_rng(seed)

    participants, sessions, daily_behavior = [], [], []
    reaction_trials, attention_trials, task_switch_trials = [], [], []

    age_bands = ["14-15", "16-17"]

    for p_idx in range(1, n_participants + 1):
        participant_id = f"P{p_idx:03d}"
        participants.append({
            "participant_id": participant_id,
            "age_band": rng.choice(age_bands),
            "gender": rng.choice(["F", "M", "belirtmek istemiyorum"]),
            "consent_status": "demo_synthetic",
        })

        # Katılımcıya özgü sabit (kişi-içi varyansı simüle etmek için) taban değerler
        base_rt = rng.normal(380, 40)  # ms
        base_sleep = rng.normal(7.2, 1.0)

        for day in range(n_days_per_participant):
            session_id = str(uuid.uuid4())
            session_date = datetime.date(2026, 1, 1) + datetime.timedelta(days=day)

            screen_time = max(0, rng.normal(220, 80))
            sleep_duration = max(3, min(11, base_sleep + rng.normal(0, 0.8)
                                         - 0.002 * max(0, screen_time - 180)))
            social_media_time = max(0, rng.normal(90, 40))
            notification_count = max(0, int(rng.normal(60, 25)))
            study_time = max(0, rng.normal(90, 45))

            sessions.append({
                "session_id": session_id,
                "participant_id": participant_id,
                "session_date": session_date.isoformat(),
                "test_time": "18:00:00",
                "device_type": rng.choice(["desktop", "mobile", "tablet"]),
                "test_version": "1.0.0-demo",
                "is_demo": True,
                "session_quality": "valid",
            })

            daily_behavior.append({
                "session_id": session_id,
                "sleep_duration": round(sleep_duration, 2),
                "screen_time": round(screen_time, 1),
                "screen_time_source": "self_report",
                "social_media_time": round(social_media_time, 1),
                "notification_count": notification_count,
                "study_time": round(study_time, 1),
            })

            # Küçük, gerçekçi bir "gün-içi" etki (yalnızca demo amaçlı)
            day_rt_shift = 0.05 * max(0, screen_time - 200) - 3.0 * max(0, sleep_duration - 7)
            n_trials = 50
            for t in range(n_trials):
                stim_ts = t * 2000.0
                rt = max(150, rng.normal(base_rt + day_rt_shift, 60))
                omission = rng.random() < 0.03
                reaction_trials.append({
                    "trial_id": str(uuid.uuid4()),
                    "session_id": session_id,
                    "trial_index": t,
                    "stimulus_timestamp": stim_ts,
                    "response_timestamp": None if omission else stim_ts + rt,
                    "reaction_time": None if omission else round(rt, 1),
                    "correct": not omission,
                    "valid": True,
                    "tab_hidden_flag": False,
                    "is_practice": False,
                })

            n_attention = 40
            for t in range(n_attention):
                is_nogo = rng.random() < 0.2
                if is_nogo:
                    commission = rng.random() < 0.15
                    attention_trials.append({
                        "trial_id": str(uuid.uuid4()),
                        "session_id": session_id,
                        "stimulus_type": "no_go",
                        "response_timestamp": 1.0 if commission else None,
                        "correct": not commission,
                        "error_type": "commission" if commission else None,
                        "valid": True,
                    })
                else:
                    omission = rng.random() < 0.05
                    attention_trials.append({
                        "trial_id": str(uuid.uuid4()),
                        "session_id": session_id,
                        "stimulus_type": "go",
                        "response_timestamp": None if omission else 1.0,
                        "correct": not omission,
                        "error_type": "omission" if omission else None,
                        "valid": True,
                    })

            n_switch = 32
            for t in range(n_switch):
                is_switch = t % 2 == 0
                switch_penalty = 40 if is_switch else 0
                rt = max(200, rng.normal(base_rt + 60 + switch_penalty, 70))
                task_switch_trials.append({
                    "trial_id": str(uuid.uuid4()),
                    "session_id": session_id,
                    "rule_type": "color" if t % 2 == 0 else "shape",
                    "is_switch_trial": is_switch,
                    "reaction_time": round(rt, 1),
                    "correct": rng.random() > 0.08,
                    "valid": True,
                })

    return {
        "participants": participants,
        "sessions": sessions,
        "daily_behavior": daily_behavior,
        "reaction_trials": reaction_trials,
        "attention_trials": attention_trials,
        "task_switch_trials": task_switch_trials,
    }


if __name__ == "__main__":
    data = generate_synthetic_dataset()
    print(f"Üretildi (DEMO/SYNTHETIC): {len(data['participants'])} katılımcı, "
          f"{len(data['sessions'])} oturum, "
          f"{len(data['reaction_trials'])} reaction trial")
