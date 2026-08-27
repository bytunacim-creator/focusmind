"""
FocusMind FastAPI uygulaması.
Bkz. orijinal talep §28 (API) ve §33 (Reproducibility).
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import os

from app.models.db_models import (
    Base, Session as SessionModel, DailyBehavior, ReactionTrial,
    AttentionTrial, TaskSwitchTrial,
)
from app.schemas.schemas import (
    SessionCreateIn, DailyBehaviorIn, ReactionTrialIn,
    AttentionTrialIn, TaskSwitchTrialIn,
)
from app.security.auth import get_auth_context, require_own_participant_data, \
    require_researcher, AuthContext

app = FastAPI(title="FocusMind API", version="1.0.0")

_frontend_origins = os.environ.get("FRONTEND_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if _frontend_origins == "*" else _frontend_origins.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine("sqlite:///./focusmind_dev.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/session")
def create_session(payload: SessionCreateIn, db=Depends(get_db),
                    auth: AuthContext = Depends(get_auth_context)):
    require_own_participant_data(payload.participant_id, auth)
    db_session = SessionModel(
        participant_id=payload.participant_id,
        session_date=payload.session_date,
        test_time=payload.test_time,
        device_type=payload.device_type,
        test_version=payload.test_version,
        is_demo=payload.is_demo,
        session_quality=None,
    )
    db.add(db_session)
    db.commit()
    return {"session_id": db_session.session_id, "is_demo": db_session.is_demo}


@app.post("/api/daily-behavior")
def submit_daily_behavior(payload: DailyBehaviorIn, db=Depends(get_db),
                           auth: AuthContext = Depends(get_auth_context)):
    # Orijinal talep §32: doğrulama Pydantic validator'larında zaten yapıldı
    existing = db.query(DailyBehavior).filter_by(session_id=payload.session_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Bu session için veri zaten gönderilmiş")
    db.add(DailyBehavior(**payload.model_dump()))
    db.commit()
    return {"status": "ok"}


@app.post("/api/reaction-trials")
def submit_reaction_trials(payloads: list[ReactionTrialIn], db=Depends(get_db),
                            auth: AuthContext = Depends(get_auth_context)):
    for p in payloads:
        # Duplicate submission kontrolü — orijinal talep §29.3
        existing = db.query(ReactionTrial).filter_by(trial_id=p.trial_id).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"trial_id {p.trial_id} zaten var")
        db.add(ReactionTrial(
            trial_id=p.trial_id,
            session_id=p.session_id,
            trial_index=p.trial_index,
            stimulus_timestamp=p.stimulus_timestamp,
            response_timestamp=p.response_timestamp,
            reaction_time=p.compute_reaction_time(),
            correct=p.correct,
            valid=p.compute_valid(),
            tab_hidden_flag=p.tab_hidden_flag,
            is_practice=p.is_practice,
        ))
    db.commit()
    return {"status": "ok", "n_trials": len(payloads)}


@app.post("/api/attention-trials")
def submit_attention_trials(payloads: list[AttentionTrialIn], db=Depends(get_db),
                             auth: AuthContext = Depends(get_auth_context)):
    for p in payloads:
        existing = db.query(AttentionTrial).filter_by(trial_id=p.trial_id).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"trial_id {p.trial_id} zaten var")
        db.add(AttentionTrial(
            trial_id=p.trial_id,
            session_id=p.session_id,
            stimulus_type=p.stimulus_type,
            response_timestamp=p.response_timestamp,
            correct=p.correct,
            error_type=p.error_type,
            valid=p.compute_valid(),
        ))
    db.commit()
    return {"status": "ok", "n_trials": len(payloads)}


@app.post("/api/task-switch-trials")
def submit_task_switch_trials(payloads: list[TaskSwitchTrialIn], db=Depends(get_db),
                               auth: AuthContext = Depends(get_auth_context)):
    for p in payloads:
        existing = db.query(TaskSwitchTrial).filter_by(trial_id=p.trial_id).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"trial_id {p.trial_id} zaten var")
        db.add(TaskSwitchTrial(
            trial_id=p.trial_id,
            session_id=p.session_id,
            rule_type=p.rule_type,
            is_switch_trial=p.is_switch_trial,
            reaction_time=p.compute_reaction_time(),
            correct=p.correct,
            valid=p.compute_valid(),
        ))
    db.commit()
    return {"status": "ok", "n_trials": len(payloads)}


@app.get("/api/research/dashboard")
def research_dashboard(db=Depends(get_db), auth: AuthContext = Depends(get_auth_context)):
    """Yalnızca researcher rolü — agregat/anonim gösterge paneli verisi.
    Bkz. PRIVACY.md §3. Canlı DB'den betimsel özet + varsa en son offline
    pipeline (scripts/run_analysis.py) çıktısı. Her ikisi de is_demo/warning
    bayrağını taşır — asla 'araştırma bulgusu' olarak sunulmaz."""
    require_researcher(auth)
    import pandas as pd
    from app.analytics.statistics import (
        compute_reaction_time_summary, compute_switch_cost_ies,
        compute_sustained_attention_score,
    )

    total_sessions = db.query(SessionModel).count()
    demo_sessions = db.query(SessionModel).filter_by(is_demo=True).count()

    sessions = db.query(SessionModel).all()
    sessions_df = pd.DataFrame([{
        "session_id": s.session_id, "participant_id": s.participant_id, "is_demo": s.is_demo,
    } for s in sessions])

    per_session_summary = []
    if not sessions_df.empty:
        reaction_df = pd.DataFrame([{
            "session_id": t.session_id, "reaction_time": t.reaction_time,
            "correct": t.correct, "valid": t.valid,
        } for t in db.query(ReactionTrial).all()])
        switch_df = pd.DataFrame([{
            "session_id": t.session_id, "is_switch_trial": t.is_switch_trial,
            "reaction_time": t.reaction_time, "correct": t.correct, "valid": t.valid,
        } for t in db.query(TaskSwitchTrial).all()])
        attention_df = pd.DataFrame([{
            "session_id": t.session_id, "error_type": t.error_type, "valid": t.valid,
        } for t in db.query(AttentionTrial).all()])

        merged = sessions_df.copy()
        if not reaction_df.empty:
            merged = merged.merge(compute_reaction_time_summary(reaction_df),
                                   on="session_id", how="left")
        if not switch_df.empty:
            merged = merged.merge(compute_switch_cost_ies(switch_df),
                                   on="session_id", how="left")
        if not attention_df.empty:
            merged = merged.merge(compute_sustained_attention_score(attention_df),
                                   on="session_id", how="left")
        per_session_summary = json.loads(merged.to_json(orient="records"))

    # En son offline pipeline (scripts/run_analysis.py) çıktısı — varsa
    analysis_dir = os.path.join(os.path.dirname(__file__), "..", "..", "research", "analysis")
    offline_run = None
    metadata_path = os.path.join(analysis_dir, "run_metadata.json")
    comparison_path = os.path.join(analysis_dir, "ml_model_comparison.csv")
    if os.path.exists(metadata_path):
        with open(metadata_path) as f:
            offline_run = {"run_metadata": json.load(f)}
        if os.path.exists(comparison_path):
            offline_run["ml_model_comparison"] = pd.read_csv(comparison_path).to_dict(
                orient="records")

    return {
        "is_demo_notice": (
            "Bu panelde is_demo=true olarak işaretli oturumlar bulunabilir. "
            "Bu veriler gerçek araştırma bulgusu DEĞİLDİR — bkz. docs/ETHICS_AND_CONSENT.md."
        ),
        "counts": {
            "total_sessions": total_sessions,
            "demo_sessions": demo_sessions,
            "real_research_sessions": total_sessions - demo_sessions,
        },
        "per_session_summary": per_session_summary,
        "offline_pipeline_run": offline_run,
    }


@app.get("/api/research/summary")
def research_summary(db=Depends(get_db), auth: AuthContext = Depends(get_auth_context)):
    """Yalnızca researcher rolü — agregat/anonim özet. Bkz. PRIVACY.md §3."""
    require_researcher(auth)
    total_sessions = db.query(SessionModel).count()
    demo_sessions = db.query(SessionModel).filter_by(is_demo=True).count()
    real_sessions = total_sessions - demo_sessions
    return {
        "total_sessions": total_sessions,
        "demo_sessions": demo_sessions,
        "real_research_sessions": real_sessions,
        "warning": (
            "DEMO/SYNTHETIC DATA dahildir. Yalnızca real_research_sessions > 0 "
            "ve etik/izin süreci tamamlanmışsa 'araştırma sonucu' olarak sunulabilir."
        ) if demo_sessions > 0 else None,
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "DEMO_MODE — bkz. docs/ETHICS_AND_CONSENT.md"}
