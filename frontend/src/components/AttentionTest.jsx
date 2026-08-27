/**
 * AttentionTest.jsx — Sürdürülen dikkat (Go/No-Go) testi.
 *
 * Bkz. docs/RESEARCH_PROTOCOL.md §4: ~120 uyaran, %80 go / %20 no-go,
 * omission (kaçırılan go) ve commission (yanlış no-go yanıtı) hataları.
 *
 * ReactionTimeTest.jsx ile aynı ilke: test SIRASINDA ağ isteği yok,
 * zamanlama requestAnimationFrame + performance.now() ile yapılır.
 */
import { useState, useRef, useCallback, useEffect } from "react";

const N_TRIALS = 120;
const N_PRACTICE = 10;
const GO_PROBABILITY = 0.8;
const MIN_ISI_MS = 1000;
const MAX_ISI_MS = 1800;
const RESPONSE_WINDOW_MS = 1000;

function randomIsi() {
  return MIN_ISI_MS + Math.random() * (MAX_ISI_MS - MIN_ISI_MS);
}

function randomStimulusType() {
  return Math.random() < GO_PROBABILITY ? "go" : "no_go";
}

const TOTAL_TRIALS = N_PRACTICE + N_TRIALS;

export default function AttentionTest({ onComplete }) {
  const [phase, setPhase] = useState("instructions"); // instructions | running | done
  const [stimulus, setStimulus] = useState(null); // "go" | "no_go" | null
  const [trialsDone, setTrialsDone] = useState(0);
  const trialsRef = useRef([]);
  const trialIndexRef = useRef(0);
  const stimulusOnsetRef = useRef(null);
  const currentTypeRef = useRef(null);
  const respondedRef = useRef(false);
  const tabHiddenRef = useRef(false);
  const windowHandleRef = useRef(null);
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
        const stimulusType = randomStimulusType();
        currentTypeRef.current = stimulusType;
        respondedRef.current = false;
        tabHiddenRef.current = false;
        stimulusOnsetRef.current = performance.now();
        setStimulus(stimulusType);

        windowHandleRef.current = setTimeout(() => {
          finalizeTrial(null);
        }, RESPONSE_WINDOW_MS);
      });
    }, isi);
  }, []);

  function finalizeTrial(responseTimestamp) {
    clearTimeout(windowHandleRef.current);
    const isPractice = trialIndexRef.current < N_PRACTICE;
    const stimulusType = currentTypeRef.current;

    let correct;
    let errorType = null;
    if (stimulusType === "go") {
      correct = responseTimestamp !== null;
      if (!correct) errorType = "omission";
    } else {
      correct = responseTimestamp === null;
      if (!correct) errorType = "commission";
    }

    trialsRef.current.push({
      trial_id: crypto.randomUUID(),
      stimulus_type: stimulusType,
      response_timestamp: responseTimestamp,
      correct,
      error_type: errorType,
      is_practice: isPractice,
      tab_hidden_flag: tabHiddenRef.current,
    });

    setStimulus(null);
    trialIndexRef.current += 1;
    setTrialsDone(trialIndexRef.current);

    if (trialIndexRef.current >= N_PRACTICE + N_TRIALS) {
      finishTest();
    } else {
      scheduleNextTrial();
    }
  }

  function handleResponse() {
    if (respondedRef.current || stimulus === null) return;
    respondedRef.current = true;
    finalizeTrial(performance.now());
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
      clearTimeout(windowHandleRef.current);
    };
  }, []);

  if (phase === "instructions") {
    return (
      <div>
        <p>
          Ekranda <strong>yeşil daire</strong> gördüğünüzde hemen tıklayın/dokunun.
          <strong> Kırmızı kare</strong> gördüğünüzde HİÇBİR ŞEY YAPMAYIN. Bu test
          araştırma amaçlıdır; sonuçlarınız başarı/başarısızlık olarak değerlendirilmez.
        </p>
        <button onClick={startTest}>Teste Başla</button>
      </div>
    );
  }

  if (phase === "running") {
    return (
      <div>
        <p>Deneme {trialsDone + 1} / {TOTAL_TRIALS}</p>
        <div
          onClick={handleResponse}
          style={{ height: 300, display: "flex", alignItems: "center", justifyContent: "center" }}
        >
          {stimulus === "go" && (
            <div
              data-testid="go-stimulus"
              style={{ width: 80, height: 80, borderRadius: "50%", background: "#16a34a" }}
            />
          )}
          {stimulus === "no_go" && (
            <div
              data-testid="no-go-stimulus"
              style={{ width: 80, height: 80, background: "#dc2626" }}
            />
          )}
          {stimulus === null && <p>Hazır olun...</p>}
        </div>
      </div>
    );
  }

  return <p>Test tamamlandı.</p>;
}
