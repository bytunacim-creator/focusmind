/**
 * TaskSwitchTest.jsx — "Alternating runs" task-switching testi.
 *
 * Bkz. docs/RESEARCH_PROTOCOL.md §5: AABB deseninde önceden belirlenmiş sıra,
 * Task A = renk yargısı (kırmızı/mavi), Task B = şekil yargısı (daire/kare),
 * bivalent uyaranlar, 64 ana deneme (32 switch + 32 repeat) + 8 pratik.
 *
 * Sabit tuş eşlemesi: Buton 1 → kırmızı VEYA daire, Buton 2 → mavi VEYA kare.
 * Aktif kural (renk/şekil) ekranda gösterilir; yalnızca ilgili boyut geçerlidir.
 */
import { useState, useRef, useCallback, useEffect } from "react";

const N_PRACTICE = 8;
const N_TRIALS = 64;
const BLOCK_SIZE = 2; // AABB deseni
const MIN_ISI_MS = 800;
const MAX_ISI_MS = 1400;
const TIMEOUT_MS = 2500;

function buildRuleSequence(totalTrials) {
  const nBlocks = Math.ceil(totalTrials / BLOCK_SIZE);
  const sequence = [];
  for (let b = 0; b < nBlocks; b++) {
    const rule = b % 2 === 0 ? "color" : "shape";
    for (let i = 0; i < BLOCK_SIZE && sequence.length < totalTrials; i++) {
      sequence.push(rule);
    }
  }
  return sequence;
}

function randomStimulus() {
  return {
    color: Math.random() < 0.5 ? "red" : "blue",
    shape: Math.random() < 0.5 ? "circle" : "square",
  };
}

function randomIsi() {
  return MIN_ISI_MS + Math.random() * (MAX_ISI_MS - MIN_ISI_MS);
}

const COLOR_HEX = { red: "#dc2626", blue: "#2563eb" };

const TOTAL_TRIALS = N_PRACTICE + N_TRIALS;

export default function TaskSwitchTest({ onComplete }) {
  const [phase, setPhase] = useState("instructions"); // instructions | running | done
  const [showStimulus, setShowStimulus] = useState(false);
  const [currentRule, setCurrentRule] = useState(null);
  const [currentStimulus, setCurrentStimulus] = useState(null);
  const [trialsDone, setTrialsDone] = useState(0);

  const ruleSequenceRef = useRef(buildRuleSequence(N_PRACTICE + N_TRIALS));
  const trialsRef = useRef([]);
  const trialIndexRef = useRef(0);
  const stimulusOnsetRef = useRef(null);
  const tabHiddenRef = useRef(false);
  const respondedRef = useRef(false);
  const timeoutHandleRef = useRef(null);
  const isiHandleRef = useRef(null);

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
    isiHandleRef.current = setTimeout(() => {
      requestAnimationFrame(() => {
        const idx = trialIndexRef.current;
        const rule = ruleSequenceRef.current[idx];
        const stimulus = randomStimulus();
        respondedRef.current = false;
        tabHiddenRef.current = false;
        stimulusOnsetRef.current = performance.now();

        setCurrentRule(rule);
        setCurrentStimulus(stimulus);
        setShowStimulus(true);

        timeoutHandleRef.current = setTimeout(() => {
          finalizeTrial(null);
        }, TIMEOUT_MS);
      });
    }, isi);
  }, []);

  function isCorrectButton(rule, stimulus, button) {
    if (rule === "color") {
      return (button === 1 && stimulus.color === "red") ||
        (button === 2 && stimulus.color === "blue");
    }
    return (button === 1 && stimulus.shape === "circle") ||
      (button === 2 && stimulus.shape === "square");
  }

  function finalizeTrial(button) {
    clearTimeout(timeoutHandleRef.current);
    const idx = trialIndexRef.current;
    const isPractice = idx < N_PRACTICE;
    const rule = ruleSequenceRef.current[idx];
    const prevRule = idx > 0 ? ruleSequenceRef.current[idx - 1] : null;
    const isSwitchTrial = prevRule !== null && prevRule !== rule;

    const responseTimestamp = button !== null ? performance.now() : null;
    const correct = button !== null && isCorrectButton(rule, currentStimulus, button);

    trialsRef.current.push({
      trial_id: crypto.randomUUID(),
      rule_type: rule,
      is_switch_trial: isSwitchTrial,
      stimulus_timestamp: stimulusOnsetRef.current,
      response_timestamp: responseTimestamp,
      correct,
      is_practice: isPractice,
      tab_hidden_flag: tabHiddenRef.current,
    });

    setShowStimulus(false);
    trialIndexRef.current += 1;
    setTrialsDone(trialIndexRef.current);

    if (trialIndexRef.current >= N_PRACTICE + N_TRIALS) {
      finishTest();
    } else {
      scheduleNextTrial();
    }
  }

  function handleButton(button) {
    if (respondedRef.current || !showStimulus) return;
    respondedRef.current = true;
    finalizeTrial(button);
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

  useEffect(() => {
    return () => {
      clearTimeout(isiHandleRef.current);
      clearTimeout(timeoutHandleRef.current);
    };
  }, []);

  if (phase === "instructions") {
    return (
      <div>
        <p>
          Ekranda gösterilen kurala göre yanıt verin: kural <strong>RENK</strong> ise
          kırmızı için 1. butona, mavi için 2. butona basın. Kural <strong>ŞEKİL</strong>{" "}
          ise daire için 1. butona, kare için 2. butona basın. Aktif kural her zaman
          ekranda yazılı olacaktır.
        </p>
        <button onClick={startTest}>Teste Başla</button>
      </div>
    );
  }

  if (phase === "running") {
    return (
      <div style={{ textAlign: "center" }}>
        <p>Deneme {trialsDone + 1} / {TOTAL_TRIALS}</p>
        <p data-testid="rule-cue">
          {currentRule
            ? <>Kural: <strong>{currentRule === "color" ? "RENK" : "ŞEKİL"}</strong></>
            : "Hazırlanıyor..."}
        </p>
        <div
          style={{ height: 200, display: "flex", alignItems: "center", justifyContent: "center" }}
        >
          {showStimulus && currentStimulus && (
            <div
              data-testid="switch-stimulus"
              style={{
                width: 80,
                height: 80,
                background: COLOR_HEX[currentStimulus.color],
                borderRadius: currentStimulus.shape === "circle" ? "50%" : "0%",
              }}
            />
          )}
          {!showStimulus && <p>Hazır olun...</p>}
        </div>
        <button onClick={() => handleButton(1)}>Buton 1</button>
        <button onClick={() => handleButton(2)}>Buton 2</button>
      </div>
    );
  }

  return <p>Test tamamlandı.</p>;
}
