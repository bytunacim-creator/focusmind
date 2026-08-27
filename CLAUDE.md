# CLAUDE.md — FocusMind Proje Kuralları

## Proje Amacı
Ergen dijital davranış değişkenleri ile bilişsel dikkat performansı arasındaki
ilişkiyi, gözlemsel/tekrarlı-ölçüm verisiyle, nedensellik iddia etmeden incelemek.

## Bilimsel Dürüstlük Kuralları (İHLAL EDİLEMEZ)
- Sahte veri asla gerçek araştırma sonucu gibi sunulmaz.
- `is_demo=true` her zaman UI ve API yanıtlarında görünür kalır.
- "İstatistiksel olarak anlamlı" ifadesi yalnızca gerçek p-değeri hesaplandığında kullanılır.
- Model çıktıları nedensellik dili ile açıklanmaz ("X, Y'ye neden oldu" YASAK;
  "X, modelin tahmin gücüne katkı sağladı" DOĞRU).
- Katılımcı sayısı, model doğruluğu, p-değeri asla uydurulmaz.

## Gizlilik Kuralları
- Ad, telefon, e-posta, TC kimlik no hiçbir tabloda/formda toplanmaz.
- `participant_id` her zaman "P001" formatında, pseudonymous.
- Katılımcılar birbirinin verisini göremez (auth.py — require_own_participant_data).
- Researcher rolü ham kimlik eşlemesine erişemez.

## ML Kuralları
- Katılımcı-düzeyi veri sızıntısı ASLA olamaz → her CV işleminde `GroupKFold`
  + `groups=participant_id` zorunlu.
- Gradient Boosting / derin modeller varsayılan olarak KAPALI (küçük n riski).
- Her metrik yanında bootstrap %95 güven aralığı raporlanır.

## Araştırma Kısıtları
- Sistem `RESEARCH_NOT_READY` durumunda başlar; gerçek veri toplama, ancak
  docs/ETHICS_AND_CONSENT.md kontrol listesi tamamlandıktan sonra açılabilir.
- Reaction-time testleri ağdan tamamen izole, client-side, RAF tabanlı olmalı.

## Test Komutları
```bash
pytest backend/tests -v          # data leakage testi dahil — CI gate
python scripts/run_analysis.py   # uçtan uca pipeline (DEMO_MODE)
npm run test                     # frontend (Vitest)
npx playwright test              # E2E
```

## Yasak İfadeler (Rapor/UI Metninde)
- "AI öğrencinin psikolojik durumunu tespit ediyor" — YASAK
- Klinik tanı isimleri (depresyon, ADHD vb.) kullanıcıya atfen — YASAK
- "Bu değişken performans düşüşüne neden oluyor" — YASAK (nedensellik iddiası)
