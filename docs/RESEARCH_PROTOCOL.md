# FocusMind — RESEARCH_PROTOCOL.md

Durum: TASLAK — Faz 2 çıktısı. Kod yazımından önce onaylanmalıdır.

## 1. Genel Tasarım

- **Desen:** Gözlemsel, çok-günlük tekrarlı ölçüm (within-subjects, longitudinal-lite).
- **Önerilen süre:** Katılımcı başına en az **7 ardışık gün** (mixed-effects modelin
  kişi-içi varyansı ayrıştırabilmesi için minimum pratik eşik; literatürde
  test-retest güvenilirlik çalışmaları 7-9 gün aralığı kullanmıştır — REFERENCES.md #16).
- **Katılımcı sayısı:** Gerçekçi hedef 20-40 lise öğrencisi (bkz. PROJECT_PLAN.md §7.4
  ve §13 — küçük n sınırlılığı raporda açıkça belirtilecektir).
- **Oturum sıklığı:** Günde 1 oturum, tercihen benzer saatte (sirkadiyen kontrol için
  `test_time` kaydedilir, zorunlu kısıtlama değildir).

## 2. Günlük Kısa Form (Davranış Anketi)

5 soru, ≤1 dakika:
1. Dün gece kaç saat uyudunuz? (sayısal, saat.dakika)
2. Bugün toplam ekran süreniz yaklaşık kaç dakikaydı? (cihazın kendi raporu varsa
   ondan kopyalanması teşvik edilir — self-report güvenilirliğini artırır)
3. Bugün sosyal medyada yaklaşık kaç dakika geçirdiniz?
4. Bugün yaklaşık kaç bildirim aldınız? (kaba tahmin kabul edilir; cihaz raporu
   varsa tercih edilir)
5. Bugün ders çalışmaya ayırdığınız süre yaklaşık kaç dakikaydı?

**Sınırlılık notu (rapora eklenecek):** Bu veriler self-report'tur ve hatıra dayalı
yanlılık (recall bias) taşıyabilir. Mümkünse Adım 2 ve 4 için katılımcıların
telefonlarının "Ekran Süresi / Dijital Denge" raporundan doğrudan kopyalama
yapmaları istenir; bu iki kaynağın (self-report vs cihaz raporu) karşılaştırılması
ek bir geçerlik kontrolü olarak STATISTICAL_ANALYSIS.md'de raporlanabilir.

## 3. Reaction Time (RT) Testi

- **Görev:** Basit RT (tek uyaran, tek tuş) — düşük bilişsel yük, hızlı uygulanabilir.
- **Trial sayısı:** 50 deneme + 5 pratik deneme (pratik veriler analiz dışı).
- **Uyaran-tepki aralığı (ISI):** 1500-3000ms arası rastgele (öngörülebilirliği
  önlemek için jitter).
- **Zaman aşımı:** 2000ms yanıt verilmezse "omission" olarak işaretlenir.
- **Teknik gereklilik:** `requestAnimationFrame` ile uyaran sunumu; `performance.now()`
  ile zaman damgası. `setTimeout`/`Date.now()` KULLANILMAZ (düşük hassasiyet).
- **Geçersizlik kuralları (invalid trial):**
  - `document.visibilityState !== 'visible'` sırasında geçen trial → invalid
  - RT < 150ms (fizyolojik olarak anlamsız hızlı, muhtemelen erken/tesadüfi tık) → invalid
  - RT > 2000ms → omission (invalid değil, ayrı kategori)
- **Skor:** Medyan RT (ortalama değil — sağa çarpık dağılım nedeniyle daha
  dayanıklı bir merkezi eğilim ölçüsü) + RT SD + CV (SD/medyan).

## 4. Sürdürülen Dikkat Testi (Go/No-Go)

- **Süre:** ~4 dakika, ~120 uyaran (REFERENCES.md #14-16 ile uyumlu kısa versiyon).
- **Go oranı:** %80 (sık "go", nadir "no-go" — dürtüsel yanıtı ortaya çıkarmak için
  klasik CPT tasarımı).
- **Ölçümler:**
  - `omission_errors`: kaçırılan "go" hedefleri
  - `commission_errors`: yanlışlıkla yanıtlanan "no-go" uyaranları
  - `median_RT` (yalnızca doğru "go" yanıtları için)
  - `RT_variability` (SD)
- **Bileşik `sustained_attention_score`:** Standardize edilmiş (z-skor) omission,
  commission ve RT-variability'nin ağırlıksız ortalaması (ters işaretli — düşük
  hata/varyans = yüksek skor). Ağırlıklandırma yapılmıyor çünkü örneklem küçükken
  ağırlık optimizasyonu overfitting riski taşır (bkz. PROJECT_PLAN.md §7.4).

## 5. Task-Switching Testi

- **Paradigma:** "Alternating runs" (Rogers & Monsell tipi, REFERENCES.md #13) —
  AABB deseninde önceden belirlenmiş sıra (cue-based değil, öngörülebilir sıra;
  lise düzeyinde uygulama basitliği için tercih edilmiştir).
- **Görevler:** Task A = renk yargısı (kırmızı/mavi), Task B = şekil yargısı
  (daire/kare). Bivalent uyaranlar (hem renk hem şekil bilgisi taşıyan).
- **Trial sayısı:** 64 deneme (32 switch + 32 repeat), + 8 pratik.
- **Birincil metrik:** Inverse Efficiency Score (IES) switch-cost
  (bkz. PROJECT_PLAN.md §2.3).
- **İkincil/betimsel metrikler:** ham RT switch-cost, ham doğruluk switch-cost
  (şeffaflık için ayrıca raporlanır, ana bulgu bunlara dayandırılmaz).

## 6. Outlier ve Veri Kalitesi Kuralları (Önceden Tanımlı — Analiz Öncesi Sabitlenir)

> Kural: Outlier kuralları veri toplandıktan SONRA, sonuçları "düzeltmek" amacıyla
> DEĞİL, veri toplanmadan ÖNCE belirlenir ve sabit kalır (p-hacking'i önlemek için).

- Oturum düzeyinde: Bir oturumda geçerli trial oranı %70'in altındaysa (ör. çok
  fazla invalid/omission), o oturum "düşük kalite" işaretlenir; birincil analizden
  çıkarılır ama veri silinmez (duyarlılık analizinde kullanılabilir).
- Trial düzeyinde: RT < 150ms veya RT > 2000ms kuralları (bkz. §3) sabit kalır.
- Katılımcı düzeyinde: 7 günden az geçerli oturumu olan katılımcı, mixed-effects
  modele dahil edilir (model eksik veriye dayanıklıdır) ama minimum oturum sayısı
  raporda belirtilir.

## 7. Güvenilirlik Analizi Planı

- **Split-half:** Her testin trial'ları tek/çift olarak ikiye bölünüp iki yarı
  arasındaki korelasyon Spearman-Brown formülüyle düzeltilir.
- **Test-retest:** Katılımcının ardışık iki günü arasındaki skor korelasyonu
  (ICC(2,1) önerilir — tekrarlı ölçüm için Pearson'dan daha uygun).
- **Rapor kuralı:** Güvenilirlik katsayısı .70'in altındaysa, o ölçümle yapılan
  korelasyon/regresyon bulguları "düşük ölçüm güvenilirliği nedeniyle sınırlı
  yorumlanmalıdır" notuyla sunulur — bu gizlenmez.

## 8. Neden Bu Yöntemler? (Kısa Gerekçe — jüri sorularına hazırlık)

| Seçim | Gerekçe |
|---|---|
| Medyan RT (ortalama değil) | RT dağılımları sağa çarpıktır; medyan aykırı değerlere dayanıklıdır |
| IES switch-cost | Salt RT farkı doğruluk-hız dengesini gizler (REFERENCES.md #12) |
| Mixed-effects model | Tekrarlı ölçümler bağımsız değildir; klasik korelasyon varsayımı ihlal edilir |
| GroupKFold (ML) | Katılımcı-düzeyi veri sızıntısını önler (REFERENCES.md #17-19) |
| Split-half + test-retest | Ölçüm aracının güvenilirliği kanıtlanmadan yorum yapılmamalı |
