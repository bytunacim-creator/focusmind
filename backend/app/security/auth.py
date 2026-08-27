"""
Basit rol modeli — orijinal talep §26.
Tam bir RBAC kütüphanesi yerine iki rol: participant, researcher.
Bkz. docs/ARCHITECTURE_DECISIONS.md AD-5.
"""
from fastapi import Header, HTTPException, Depends
from typing import Optional


class AuthContext:
    def __init__(self, role: str, participant_id: Optional[str] = None):
        self.role = role
        self.participant_id = participant_id


def get_auth_context(
    x_role: str = Header(...),
    x_participant_id: Optional[str] = Header(default=None),
) -> AuthContext:
    if x_role not in ("participant", "researcher"):
        raise HTTPException(status_code=401, detail="Geçersiz rol")
    if x_role == "participant" and not x_participant_id:
        raise HTTPException(status_code=401, detail="participant_id gerekli")
    return AuthContext(role=x_role, participant_id=x_participant_id)


def require_own_participant_data(target_participant_id: str, auth: AuthContext):
    """Orijinal talep §26 — katılımcılar birbirinin verisini göremez."""
    if auth.role == "participant" and auth.participant_id != target_participant_id:
        raise HTTPException(
            status_code=403,
            detail="Başka bir katılımcının verisine erişim reddedildi",
        )


def require_researcher(auth: AuthContext):
    """Researcher panelinde ham kimlik eşlemesine erişimi engeller."""
    if auth.role != "researcher":
        raise HTTPException(status_code=403, detail="Yalnızca researcher rolü erişebilir")
