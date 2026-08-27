"""
FocusMind veritabanı modelleri.
Bkz. docs/DATA_DICTIONARY.md için alan tanımları ve gerekçeler.
"""
from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Date, Time, ForeignKey, Text
)
from sqlalchemy.orm import declarative_base
import uuid
import datetime

Base = declarative_base()


def gen_uuid() -> str:
    return str(uuid.uuid4())


class Participant(Base):
    __tablename__ = "participants"

    participant_id = Column(String, primary_key=True)  # ör. "P001" — gerçek kimlik İÇERMEZ
    age_band = Column(String, nullable=False)  # ör. "14-15"
    gender = Column(String, nullable=True)
    consent_status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, default=gen_uuid)
    participant_id = Column(String, ForeignKey("participants.participant_id"), nullable=False)
    session_date = Column(Date, nullable=False)
    test_time = Column(Time, nullable=False)
    device_type = Column(String, nullable=False)
    test_version = Column(String, nullable=False)
    is_demo = Column(Boolean, nullable=False, default=False)  # ZORUNLU alan — bkz. PRIVACY.md
    session_quality = Column(String, nullable=True)  # "valid" / "low_quality"


class DailyBehavior(Base):
    __tablename__ = "daily_behavior"

    session_id = Column(String, ForeignKey("sessions.session_id"), primary_key=True)
    sleep_duration = Column(Float, nullable=True)  # saat
    screen_time = Column(Float, nullable=True)  # dakika
    screen_time_source = Column(String, nullable=True)  # "self_report" / "device_report"
    social_media_time = Column(Float, nullable=True)  # dakika
    notification_count = Column(Integer, nullable=True)
    study_time = Column(Float, nullable=True)  # dakika


class ReactionTrial(Base):
    __tablename__ = "reaction_trials"

    trial_id = Column(String, primary_key=True, default=gen_uuid)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    trial_index = Column(Integer, nullable=False)
    stimulus_timestamp = Column(Float, nullable=False)  # ms, performance.now()
    response_timestamp = Column(Float, nullable=True)
    reaction_time = Column(Float, nullable=True)  # ms
    correct = Column(Boolean, nullable=False)
    valid = Column(Boolean, nullable=False)
    tab_hidden_flag = Column(Boolean, nullable=False, default=False)
    is_practice = Column(Boolean, nullable=False, default=False)


class AttentionTrial(Base):
    __tablename__ = "attention_trials"

    trial_id = Column(String, primary_key=True, default=gen_uuid)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    stimulus_type = Column(String, nullable=False)  # "go" / "no_go"
    response_timestamp = Column(Float, nullable=True)
    correct = Column(Boolean, nullable=False)
    error_type = Column(String, nullable=True)  # "omission" / "commission" / null
    valid = Column(Boolean, nullable=False)


class TaskSwitchTrial(Base):
    __tablename__ = "task_switch_trials"

    trial_id = Column(String, primary_key=True, default=gen_uuid)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    rule_type = Column(String, nullable=False)  # "color" / "shape"
    is_switch_trial = Column(Boolean, nullable=False)
    reaction_time = Column(Float, nullable=True)
    correct = Column(Boolean, nullable=False)
    valid = Column(Boolean, nullable=False)


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    run_id = Column(String, primary_key=True, default=gen_uuid)
    dataset_version = Column(String, nullable=False)
    code_version = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    parameters_json = Column(Text, nullable=True)


class ModelRun(Base):
    __tablename__ = "model_runs"

    run_id = Column(String, primary_key=True, default=gen_uuid)
    analysis_run_id = Column(String, ForeignKey("analysis_runs.run_id"), nullable=False)
    model_type = Column(String, nullable=False)
    cv_strategy = Column(String, nullable=False)
    random_seed = Column(Integer, nullable=False)
    metrics_json = Column(Text, nullable=False)
