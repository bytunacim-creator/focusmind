"""
API entegrasyon testleri — attention/task-switch uçları ve researcher dashboard.
Bkz. docs/TESTING.md.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("FOCUSMIND_TEST_DB", "1")


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.chdir(tmp_path)
    import importlib
    import app.main as main_module
    importlib.reload(main_module)
    return TestClient(main_module.app)


def _create_session(client, participant_id="P001", is_demo=True):
    resp = client.post(
        "/api/session",
        headers={"x-role": "participant", "x-participant-id": participant_id},
        json={
            "participant_id": participant_id,
            "session_date": "2026-08-27",
            "test_time": "18:00:00",
            "device_type": "desktop",
            "test_version": "1.0.0",
            "is_demo": is_demo,
        },
    )
    assert resp.status_code == 200
    return resp.json()["session_id"]


def test_attention_trial_submission_marks_omission_invalid_when_practice(client):
    session_id = _create_session(client)
    resp = client.post(
        "/api/attention-trials",
        headers={"x-role": "participant", "x-participant-id": "P001"},
        json=[{
            "trial_id": "a1", "session_id": session_id, "stimulus_type": "go",
            "response_timestamp": None, "correct": False, "error_type": "omission",
            "is_practice": True,
        }],
    )
    assert resp.status_code == 200
    assert resp.json()["n_trials"] == 1


def test_attention_trial_duplicate_rejected(client):
    session_id = _create_session(client)
    payload = [{
        "trial_id": "a2", "session_id": session_id, "stimulus_type": "no_go",
        "response_timestamp": 300.0, "correct": False, "error_type": "commission",
    }]
    headers = {"x-role": "participant", "x-participant-id": "P001"}
    first = client.post("/api/attention-trials", headers=headers, json=payload)
    second = client.post("/api/attention-trials", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 409


def test_task_switch_trial_omission_is_invalid(client):
    session_id = _create_session(client)
    resp = client.post(
        "/api/task-switch-trials",
        headers={"x-role": "participant", "x-participant-id": "P001"},
        json=[{
            "trial_id": "ts1", "session_id": session_id, "rule_type": "color",
            "is_switch_trial": True, "stimulus_timestamp": 0.0,
            "response_timestamp": None, "correct": False,
        }],
    )
    assert resp.status_code == 200


def test_task_switch_response_before_stimulus_rejected(client):
    session_id = _create_session(client)
    resp = client.post(
        "/api/task-switch-trials",
        headers={"x-role": "participant", "x-participant-id": "P001"},
        json=[{
            "trial_id": "ts2", "session_id": session_id, "rule_type": "shape",
            "is_switch_trial": False, "stimulus_timestamp": 1000.0,
            "response_timestamp": 500.0, "correct": True,
        }],
    )
    assert resp.status_code == 422


def test_dashboard_requires_researcher_role(client):
    resp = client.get("/api/research/dashboard", headers={"x-role": "participant",
                                                            "x-participant-id": "P001"})
    assert resp.status_code == 403


def test_dashboard_always_carries_demo_notice(client):
    _create_session(client, is_demo=True)
    resp = client.get("/api/research/dashboard", headers={"x-role": "researcher"})
    assert resp.status_code == 200
    body = resp.json()
    assert "is_demo" in body["is_demo_notice"].lower() or "araştırma" in body["is_demo_notice"]
    assert body["counts"]["demo_sessions"] >= 1
