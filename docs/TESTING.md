# FocusMind — TESTING.md

## 1. Katmanlar ve Komutlar

| Katman | Araç | Komut |
|---|---|---|
| Backend birim/entegrasyon | pytest | `pytest backend/tests` |
| Frontend bileşen | Vitest + RTL | `npm run test` |
| E2E | Playwright | `npx playwright test` |
| Lint | ruff / eslint | `npm run lint`, `ruff check backend/` |
| Analiz pipeline yeniden çalıştırma | — | `python scripts/run_analysis.py` |

## 2. Zorunlu Test Senaryoları (Orijinal Talep §29 — Birebir Karşılık)

1. **Geçersiz trial:** RT < 150ms veya tab_hidden=true → `valid=false` olarak
   işaretlenir, analiz dışı bırakılır. (`test_reaction_trial_validation.py`)
2. **Eksik veri:** `daily_behavior` alanlarından biri boşsa, session yine
   kaydedilir (zorunlu alan değildir); mixed-effects model eksik veriyle
   çalışabilmelidir — bu bir birim testiyle doğrulanır.
3. **Duplicate submission:** Aynı `trial_id` ikinci kez POST edilirse
   `409 Conflict` döner, veri iki kez yazılmaz.
4. **Participant isolation:** `participant` rolündeki bir kullanıcı başka bir
   `participant_id`'nin verisini GET edemez → `403 Forbidden`.
5. **Researcher authorization:** `researcher` rolü ham `participant_id`↔kimlik
   eşlemesini içeren hiçbir uca erişemez; yalnızca agregat uçlara erişebilir.
6. **Data leakage (ML):** `test_groupkfold_no_participant_overlap` — her CV
   fold'unda train/test participant kümeleri ayrık olmalı (bkz. ML_METHODOLOGY.md §2).
7. **Invalid timestamp:** `response_timestamp < stimulus_timestamp` gibi
   fizyolojik olarak imkânsız değerler backend'de reddedilir (`422`).
8. **Outlier handling:** RESEARCH_PROTOCOL.md §6'daki eşiklerin (RT<150ms,
   RT>2000ms, oturum geçerli-trial oranı <%70) doğru uygulandığını doğrulayan
   testler.

## 3. Demo/Gerçek Veri Ayrım Testi (Ek — Kritik)
```python
def test_demo_data_never_labeled_as_research_result():
    """is_demo=true olan session'lardan üretilen analiz çıktıları
    API yanıtında is_demo=true bayrağını taşımalı; frontend bu bayrağı
    görmeden 'araştırma sonucu' başlığı gösteremez."""
```

## 4. CI Gate
`test_groupkfold_no_participant_overlap` ve participant-isolation testleri
**kırmızı ise build başarısız sayılır** — bunlar bilimsel/etik açıdan
"nice to have" değil, zorunlu kapılardır.
