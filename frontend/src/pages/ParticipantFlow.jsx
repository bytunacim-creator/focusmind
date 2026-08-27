import { useState } from "react";
import ReactionTimeTest from "../components/ReactionTimeTest.jsx";
import AttentionTest from "../components/AttentionTest.jsx";
import TaskSwitchTest from "../components/TaskSwitchTest.jsx";
import {
  createSession, submitDailyBehavior, submitReactionTrials,
  submitAttentionTrials, submitTaskSwitchTrials,
} from "../services/api.js";

const STEPS = [
  "consent", "daily-behavior", "reaction-time", "attention", "task-switch", "done",
];

const EMPTY_BEHAVIOR = {
  sleep_duration: "", screen_time: "", social_media_time: "",
  notification_count: "", study_time: "",
};

export default function ParticipantFlow({ auth }) {
  const [stepIndex, setStepIndex] = useState(0);
  const [sessionId, setSessionId] = useState(null);
  const [behavior, setBehavior] = useState(EMPTY_BEHAVIOR);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  const step = STEPS[stepIndex];

  function next() {
    setStepIndex((i) => Math.min(i + 1, STEPS.length - 1));
  }

  async function handleConsentContinue() {
    setBusy(true);
    setError(null);
    try {
      // Sistem RESEARCH_NOT_READY durumunda — bkz. README.md, docs/ETHICS_AND_CONSENT.md.
      // Bu nedenle üretilen tüm oturumlar is_demo=true olarak işaretlenir.
      const { session_id } = await createSession(auth, {
        participant_id: auth.participantId,
        session_date: new Date().toISOString().slice(0, 10),
        test_time: new Date().toTimeString().slice(0, 8),
        device_type: "desktop",
        test_version: "1.0.0",
        is_demo: true,
      });
      setSessionId(session_id);
      next();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleBehaviorSubmit(e) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const toNumberOrNull = (v) => (v === "" ? null : Number(v));
      await submitDailyBehavior(auth, {
        session_id: sessionId,
        sleep_duration: toNumberOrNull(behavior.sleep_duration),
        screen_time: toNumberOrNull(behavior.screen_time),
        social_media_time: toNumberOrNull(behavior.social_media_time),
        notification_count: toNumberOrNull(behavior.notification_count),
        study_time: toNumberOrNull(behavior.study_time),
      });
      next();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleReactionComplete(trials) {
    setError(null);
    try {
      const payload = trials.map((t) => ({ ...t, session_id: sessionId }));
      await submitReactionTrials(auth, payload);
      next();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleAttentionComplete(trials) {
    setError(null);
    try {
      const payload = trials.map((t) => ({ ...t, session_id: sessionId }));
      await submitAttentionTrials(auth, payload);
      next();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleTaskSwitchComplete(trials) {
    setError(null);
    try {
      const payload = trials.map((t) => ({ ...t, session_id: sessionId }));
      await submitTaskSwitchTrials(auth, payload);
      next();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 640, margin: "24px auto", fontFamily: "sans-serif" }}>
      <p>Katılımcı: {auth.participantId} — Adım {stepIndex + 1}/{STEPS.length}</p>
      {error && <p style={{ color: "#b91c1c" }}>Hata: {error}</p>}

      {step === "consent" && (
        <div>
          <h2>Bilgilendirme</h2>
          <p>
            Bu bir DEMO çalıştırmasıdır. Sistem şu anda RESEARCH_NOT_READY
            durumundadır; gerçek katılımcı verisi toplanmıyor. Üretilecek tüm
            veriler <code>is_demo=true</code> olarak işaretlenecektir.
          </p>
          <button onClick={handleConsentContinue} disabled={busy}>
            Anladım, Devam Et
          </button>
        </div>
      )}

      {step === "daily-behavior" && (
        <form onSubmit={handleBehaviorSubmit}>
          <h2>Günlük Kısa Form</h2>
          <p>
            <label>
              Dün gece kaç saat uyudunuz?{" "}
              <input type="number" step="0.1" value={behavior.sleep_duration}
                onChange={(e) => setBehavior({ ...behavior, sleep_duration: e.target.value })} />
            </label>
          </p>
          <p>
            <label>
              Bugün toplam ekran süreniz (dakika)?{" "}
              <input type="number" value={behavior.screen_time}
                onChange={(e) => setBehavior({ ...behavior, screen_time: e.target.value })} />
            </label>
          </p>
          <p>
            <label>
              Bugün sosyal medya süreniz (dakika)?{" "}
              <input type="number" value={behavior.social_media_time}
                onChange={(e) => setBehavior({ ...behavior, social_media_time: e.target.value })} />
            </label>
          </p>
          <p>
            <label>
              Bugün aldığınız bildirim sayısı?{" "}
              <input type="number" value={behavior.notification_count}
                onChange={(e) => setBehavior({ ...behavior, notification_count: e.target.value })} />
            </label>
          </p>
          <p>
            <label>
              Bugün ders çalışma süreniz (dakika)?{" "}
              <input type="number" value={behavior.study_time}
                onChange={(e) => setBehavior({ ...behavior, study_time: e.target.value })} />
            </label>
          </p>
          <button type="submit" disabled={busy}>Devam Et</button>
        </form>
      )}

      {step === "reaction-time" && (
        <div>
          <h2>Test 1/3 — Basit Reaksiyon Süresi</h2>
          <ReactionTimeTest onComplete={handleReactionComplete} />
        </div>
      )}

      {step === "attention" && (
        <div>
          <h2>Test 2/3 — Sürdürülen Dikkat (Go/No-Go)</h2>
          <AttentionTest onComplete={handleAttentionComplete} />
        </div>
      )}

      {step === "task-switch" && (
        <div>
          <h2>Test 3/3 — Görev Değiştirme</h2>
          <TaskSwitchTest onComplete={handleTaskSwitchComplete} />
        </div>
      )}

      {step === "done" && (
        <div>
          <h2>Teşekkürler!</h2>
          <p>Bugünkü oturumunuz tamamlandı (DEMO_MODE, is_demo=true).</p>
        </div>
      )}
    </div>
  );
}
