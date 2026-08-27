/**
 * is_demo=true olan tüm ekranlarda görünür kalması ZORUNLU uyarı şeridi.
 * Bkz. CLAUDE.md — Bilimsel Dürüstlük Kuralları.
 */
export default function DemoBanner() {
  return (
    <div
      role="alert"
      style={{
        background: "#fef3c7",
        color: "#78350f",
        padding: "8px 16px",
        fontSize: 14,
        borderBottom: "1px solid #f59e0b",
      }}
    >
      ⚠️ DEMO MODE — is_demo=true — bu veriler sentetiktir ve gerçek bir araştırma
      bulgusu DEĞİLDİR. Bkz. docs/ETHICS_AND_CONSENT.md.
    </div>
  );
}
