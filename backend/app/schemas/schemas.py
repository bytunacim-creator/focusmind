"""
Pydantic şemaları — backend/gelen veri doğrulama katmanı.
Bkz. docs/DATA_DICTIONARY.md ve orijinal talep §32 (Data Validation).
"""
from pydantic import BaseModel, field_validator
from typing import Optional
import datetime


class DailyBehaviorIn(BaseModel):
    session_id: str
    sleep_duration: Optional[float] = None
    screen_time: Optional[float] = None
    screen_time_source: Optional[str] = None
    social_media_time: Optional[float] = None
    notification_count: Optional[int] = None
    study_time: Optional[float] = None

    @field_validator("sleep_duration")
    @classmethod
    def sleep_must_be_plausible(cls, v):
        if v is not None and (v < 0 or v > 16):
            raise ValueError("sleep_duration 0-16 saat aralığında olmalıdır")
        return v

    @field_validator("screen_time", "social_media_time", "study_time")
    @classmethod
    def minutes_must_be_nonnegative_and_bounded(cls, v):
        if v is not None and (v < 0 or v > 1440):
            raise ValueError("dakika değeri 0-1440 aralığında olmalıdır")
        return v

    @field_validator("notification_count")
    @classmethod
    def notification_nonnegative(cls, v):
        if v is not None and v < 0:
            raise ValueError("notification_count negatif olamaz")
        return v


class ReactionTrialIn(BaseModel):
    trial_id: str
    session_id: str
    trial_index: int
    stimulus_timestamp: float
    response_timestamp: Optional[float] = None
    correct: bool
    tab_hidden_flag: bool = False
    is_practice: bool = False

    @field_validator("response_timestamp")
    @classmethod
    def response_after_stimulus(cls, v, info):
        stim = info.data.get("stimulus_timestamp")
        if v is not None and stim is not None and v < stim:
            # Orijinal talep §32: imkânsız timestamp kabul etme
            raise ValueError("response_timestamp, stimulus_timestamp'ten önce olamaz")
        return v

    def compute_reaction_time(self) -> Optional[float]:
        if self.response_timestamp is None:
            return None
        return self.response_timestamp - self.stimulus_timestamp

    def compute_valid(self) -> bool:
        """RESEARCH_PROTOCOL.md §3 — geçersizlik kuralları."""
        if self.tab_hidden_flag or self.is_practice:
            return False
        rt = self.compute_reaction_time()
        if rt is None:
            return True  # omission — invalid değil, ayrı kategori
        if rt < 150 or rt > 2000:
            return False
        return True


class SessionCreateIn(BaseModel):
    participant_id: str
    session_date: datetime.date
    test_time: datetime.time
    device_type: str
    test_version: str
    is_demo: bool = False

    @field_validator("participant_id")
    @classmethod
    def participant_id_format(cls, v):
        # Orijinal talep §9: gerçek isim değil, "P001" formatı
        if not v.startswith("P") or not v[1:].isdigit():
            raise ValueError("participant_id 'P001' formatında olmalıdır")
        return v


class AttentionTrialIn(BaseModel):
    """Sürdürülen dikkat (Go/No-Go) testi. Bkz. RESEARCH_PROTOCOL.md §4."""
    trial_id: str
    session_id: str
    stimulus_type: str  # "go" / "no_go"
    response_timestamp: Optional[float] = None
    correct: bool
    error_type: Optional[str] = None  # "omission" / "commission" / None
    is_practice: bool = False
    tab_hidden_flag: bool = False

    @field_validator("stimulus_type")
    @classmethod
    def stimulus_type_valid(cls, v):
        if v not in ("go", "no_go"):
            raise ValueError("stimulus_type 'go' veya 'no_go' olmalıdır")
        return v

    @field_validator("error_type")
    @classmethod
    def error_type_valid(cls, v):
        if v is not None and v not in ("omission", "commission"):
            raise ValueError("error_type 'omission', 'commission' veya null olmalıdır")
        return v

    def compute_valid(self) -> bool:
        """RESEARCH_PROTOCOL.md §6 — sekme arka planda/pratik deneme invalid."""
        return not (self.tab_hidden_flag or self.is_practice)


class TaskSwitchTrialIn(BaseModel):
    """Task-switching testi (alternating runs). Bkz. RESEARCH_PROTOCOL.md §5."""
    trial_id: str
    session_id: str
    rule_type: str  # "color" / "shape"
    is_switch_trial: bool
    stimulus_timestamp: float
    response_timestamp: Optional[float] = None
    correct: bool
    is_practice: bool = False
    tab_hidden_flag: bool = False

    @field_validator("rule_type")
    @classmethod
    def rule_type_valid(cls, v):
        if v not in ("color", "shape"):
            raise ValueError("rule_type 'color' veya 'shape' olmalıdır")
        return v

    @field_validator("response_timestamp")
    @classmethod
    def response_after_stimulus(cls, v, info):
        stim = info.data.get("stimulus_timestamp")
        if v is not None and stim is not None and v < stim:
            raise ValueError("response_timestamp, stimulus_timestamp'ten önce olamaz")
        return v

    def compute_reaction_time(self) -> Optional[float]:
        if self.response_timestamp is None:
            return None
        return self.response_timestamp - self.stimulus_timestamp

    def compute_valid(self) -> bool:
        """RESEARCH_PROTOCOL.md §6 — omission task-switch'te ayrı kategori değil, invalid sayılır."""
        if self.tab_hidden_flag or self.is_practice:
            return False
        return self.compute_reaction_time() is not None
