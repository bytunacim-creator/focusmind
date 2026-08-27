import { useState } from "react";

export default function RoleSelect({ onParticipant, onResearcher }) {
  const [participantId, setParticipantId] = useState("P001");
  const [error, setError] = useState(null);

  function handleParticipantSubmit(e) {
    e.preventDefault();
    setError(null);
    try {
      onParticipant(participantId.trim());
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 480, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>FocusMind</h1>
      <p>
        Ergen dijital davranış değişkenleri ile bilişsel dikkat performansı
        arasındaki ilişkiyi inceleyen araştırma platformu (DEMO MODE).
      </p>

      <section style={{ marginTop: 24 }}>
        <h2>Katılımcı olarak devam et</h2>
        <form onSubmit={handleParticipantSubmit}>
          <label>
            Katılımcı ID (ör. P001):{" "}
            <input
              value={participantId}
              onChange={(e) => setParticipantId(e.target.value)}
            />
          </label>
          <button type="submit" style={{ marginLeft: 8 }}>
            Devam Et
          </button>
        </form>
        {error && <p style={{ color: "#b91c1c" }}>{error}</p>}
      </section>

      <section style={{ marginTop: 24 }}>
        <h2>Araştırmacı paneli</h2>
        <button onClick={onResearcher}>Researcher Dashboard'a Git</button>
      </section>
    </div>
  );
}
