/**
 * ReactionTimeTest.jsx
 *
 * KRİTİK: Bu bileşen test SIRASINDA hiçbir ağ isteği yapmaz.
 * Zamanlama tamamen requestAnimationFrame + performance.now() ile yürütülür.
 * Sonuçlar yalnızca test tamamlandığında toplu olarak onComplete callback'i
 * ile üst bileşene iletilir (üst bileşen bunu backend'e POST eder).
 *
 * Bkz. docs/RESEARCH_PROTOCOL.md §3, docs/ARCHITECTURE_DECISIONS.md AD-1.
 */
import { useState, useRef, useCallback, useEffect } from "react";

const N_TRIALS = 50;
const N_PRACTICE = 5;
const MIN_ISI_MS = 1500;
const MAX_ISI_MS = 3000;
const TIMEOUT_MS = 2000;
const MIN_VALID_RT_MS = 150; // RESEARCH_PROTOCOL.md §3 — fizyolojik olarak anlamsız hız eşiği

function randomIsi() {
  return MIN_ISI_MS + Math.random() * (MAX_ISI_MS - MIN_ISI_MS);
}

export default function ReactionTimeTest({ onComplete }) {
  const [phase, setPhase] = useState("instructions"); // instructions | running | done
  const [showStimulus, setShowStimulus] = useState(false);
  const trialsRef = useRef([]);
  const trialIndexRef = useRef(0);
  const stimulusOnsetRef = useRef(null);
  const tabHiddenRef = useRef(false);
  const timeoutHandleRef = useRef(null);
  const rafHandleRef = useRef(null);

  // Sekme arka plana alınırsa mevcut trial invalid işaretlenir (silinmez)
  useEffect(() => {
    function handleVisibilityChange() {
      if (document.visibilityState !== "visible") {
        tabHiddenRef.current = true;
      }
    }
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, []);

  const scheduleNextTrial = useCallback(() => {
    const isi = randomIsi();
    const isPractice = trialIndexRef.current < N_PRACTICE;

    rafHandleRef.current = setTimeout(() => {
      requestAnimationFrame(() => {
        stimulusOnsetRef.current = performance.now();
        tabHiddenRef.current = false;
        setShowStimulus(true);

        timeoutHandleRef.current = setTimeout(() => {
          recordTrial({ responseTimestamp: null, isPractice });
        }, TIMEOUT_MS);
      });
    }, isi);
  }, []);

  function recordTrial({ responseTimestamp, isPractice }) {
    clearTimeout(timeoutHandleRef.current);
    const stimulusTs = stimulusOnsetRef.current;
    const reactionTime = responseTimestamp != null ? responseTimestamp - stimulusTs : null;

    const trial = {
      trial_id: crypto.randomUUID(),
      trial_index: trialIndexRef.current,
      stimulus_timestamp: stimulusTs,
      response_timestamp: responseTimestamp,
      reaction_time: reactionTime,
      correct: reactionTime !== null,
      tab_hidden_flag: tabHiddenRef.current,
      is_practice: isPractice,
      // valid hesaplaması backend'de de tekrarlanır (tek kaynak backend olsun diye
      // burada sadece bilgi amaçlı gösterim için hesaplanabilir, gönderilmez)
    };

    trialsRef.current.push(trial);
    setShowStimulus(false);
    trialIndexRef.current += 1;

    const totalTrials = N_PRACTICE + N_TRIALS;
    if (trialIndexRef.current >= totalTrials) {
      finishTest();
    } else {
      scheduleNextTrial();
    }
  }

  function handleResponse() {
    if (!showStimulus) return; // erken tıklama — trial başlamadan yanıt sayılmaz
    const now = performance.now();
    const isPractice = trialIndexRef.current < N_PRACTICE;
    recordTrial({ responseTimestamp: now, isPractice });
  }

  function finishTest() {
    setPhase("done");
    const realTrials = trialsRef.current.filter((t) => !t.is_practice);
    onComplete(realTrials);
  }

  function startTest() {
    setPhase("running");
    trialIndexRef.current = 0;
    trialsRef.current = [];
    scheduleNextTrial();
  }

  if (phase === "instructions") {
    return (
      <div>
        <p>
          Ekranda daire belirdiğinde olabildiğince hızlı tıklayın/dokunun.
          Bu test araştırma amaçlıdır; sonuçlarınız başarı/başarısızlık olarak
          değerlendirilmez.
        </p>
        <button onClick={startTest}>Teste Başla</button>
      </div>
    );
  }

  if (phase === "running") {
    return (
      <div
        onClick={handleResponse}
        style={{ height: 300, display: "flex", alignItems: "center", justifyContent: "center" }}
      >
        {showStimulus ? (
          <div style={{ width: 80, height: 80, borderRadius: "50%", background: "#2b6cb0" }} />
        ) : (
          <p>Hazır olun...</p>
        )}
      </div>
    );
  }

  return <p>Test tamamlandı.</p>;
}
