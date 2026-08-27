import { useEffect, useState } from "react";
import { fetchResearchDashboard } from "../services/api.js";

function fmt(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  return typeof v === "number" ? v.toFixed(2) : String(v);
}

export default function ResearcherDashboard({ auth }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchResearchDashboard(auth).then(setData).catch((err) => setError(err.message));
  }, [auth]);

  if (error) return <p style={{ color: "#b91c1c" }}>Hata: {error}</p>;
  if (!data) return <p>Yükleniyor...</p>;

  const rows = data.per_session_summary ?? [];
  const offline = data.offline_pipeline_run;

  return (
    <div style={{ maxWidth: 960, margin: "24px auto", fontFamily: "sans-serif" }}>
      <h1>Researcher Dashboard</h1>
      <p style={{ background: "#fef3c7", padding: 8, borderRadius: 4 }}>
        {data.is_demo_notice}
      </p>

      <section>
        <h2>Özet</h2>
        <ul>
          <li>Toplam oturum: {data.counts.total_sessions}</li>
          <li>Demo (sentetik) oturum: {data.counts.demo_sessions}</li>
          <li>Gerçek araştırma oturumu: {data.counts.real_research_sessions}</li>
        </ul>
      </section>

      <section>
        <h2>Oturum Bazında Betimsel Özet (canlı veritabanı)</h2>
        {rows.length === 0 ? (
          <p>Henüz oturum verisi yok.</p>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table border="1" cellPadding="4" style={{ borderCollapse: "collapse", width: "100%" }}>
              <thead>
                <tr>
                  <th>participant_id</th>
                  <th>is_demo</th>
                  <th>median_rt</th>
                  <th>switch_cost_ies</th>
                  <th>sustained_attention_score</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.session_id}>
                    <td>{r.participant_id}</td>
                    <td>{String(r.is_demo)}</td>
                    <td>{fmt(r.median_rt)}</td>
                    <td>{fmt(r.switch_cost_ies)}</td>
                    <td>{fmt(r.sustained_attention_score)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section>
        <h2>Son Offline Pipeline Çalıştırması (scripts/run_analysis.py)</h2>
        {!offline ? (
          <p>
            Henüz bir pipeline çalıştırması bulunamadı. Terminalden{" "}
            <code>python scripts/run_analysis.py</code> çalıştırın.
          </p>
        ) : (
          <>
            <p>
              run_id: {offline.run_metadata.run_id} — dataset_version:{" "}
              {offline.run_metadata.dataset_version} — {offline.run_metadata.warning}
            </p>
            <table border="1" cellPadding="4" style={{ borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th>model</th>
                  <th>MAE</th>
                  <th>MAE 95% CI</th>
                  <th>R²</th>
                  <th>R² 95% CI</th>
                  <th>cv_strategy</th>
                </tr>
              </thead>
              <tbody>
                {(offline.ml_model_comparison ?? []).map((m) => (
                  <tr key={m.model}>
                    <td>{m.model}</td>
                    <td>{fmt(m.mae)}</td>
                    <td>[{fmt(m.mae_ci_low)}, {fmt(m.mae_ci_high)}]</td>
                    <td>{fmt(m.r2)}</td>
                    <td>[{fmt(m.r2_ci_low)}, {fmt(m.r2_ci_high)}]</td>
                    <td>{m.cv_strategy}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </section>
    </div>
  );
}
