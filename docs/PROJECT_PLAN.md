# FocusMind — PROJECT_PLAN.md

**Durum:** TASLAK — onay bekliyor. Bu belge PHASE 1 (Araştırma) çıktısıdır.
Büyük çaplı implementasyon başlamadan önce proje sahibinin onayı gerekir.

---

## 0. Proje Amacı

Ergenlerde günlük dijital davranış değişkenleri (ekran süresi, bildirim yoğunluğu,
sosyal medya kullanımı, uyku süresi) ile bilişsel dikkat performansı (tepki süresi,
sürdürülen dikkat, görev değiştirme maliyeti) arasındaki **ilişkiyi** — nedensellik
iddia etmeksizin — davranışsal veri toplama, klasik istatistik ve makine öğrenmesi
kullanarak incelemek.

Sistem bir **tanı/teşhis aracı değil**, bir **araştırma enstrümanıdır**.

---

## 1. Araştırma Soruları ve Hipotezler

Kullanıcının belirttiği 7 alt araştırma sorusu (bkz. orijinal talep, Bölüm 3)
aynen korunmuştur. Her biri için **yönsüz** (non-directional) hipotez kurulmalıdır;
yön varsayımı yapılmamalıdır çünkü literatür (bkz. REFERENCES.md #20) etki
büyüklüklerinin küçük/mütevazı olduğunu ve yönün her zaman beklenen tarafta
çıkmayabileceğini göstermektedir.

**Genel H0 / H1 çerçevesi (her alt soru için tekrarlanır):**
- H0: Değişken X ile bilişsel ölçüm Y arasında (katılımcı içi ve katılımcılar arası
  varyans kontrol edildiğinde) anlamlı bir ilişki yoktur.
- H1: Değişken X ile Y arasında anlamlı bir ilişki vardır (yön önceden belirtilmez).

**Kritik kısıtlama:** Tasarım gözlemseldir (deneysel manipülasyon yoktur). Bu nedenle
raporlamada daima "X, Y ile ilişkilidir" denir; "X, Y'ye neden olur" denemez
(bkz. Bölüm 20, orijinal talep; REFERENCES.md #20).

---

## 2. Değişkenler

### 2.1 Bağımsız / Yordayıcı Değişkenler (günlük davranış)
| Değişken | Birim | Kaynak |
|---|---|---|
| sleep_duration | dakika | Günlük kısa form (self-report) |
| screen_time | dakika | Günlük kısa form |
| social_media_time | dakika | Günlük kısa form |
| notification_count | adet | Günlük kısa form (yaklaşık/algısal) |
| study_time | dakika | Günlük kısa form |

> **Not:** Bu değişkenler self-report'tur; cihaz düzeyinde ölçülmüyorsa bu bir
> **sınırlılık** olarak DATA_DICTIONARY.md ve rapor sonuçlarında açıkça belirtilmelidir.

### 2.2 Bağımlı Değişkenler (bilişsel performans)
| Değişken | Test | Hesaplama |
|---|---|---|
| reaction_time (median RT) | Basit/seçici RT görevi | Geçerli trial'ların medyanı |
| reaction_time_variability | RT görevi | SD veya CV (SD/mean RT) |
| omission_errors | Sürdürülen dikkat | Kaçırılan hedef sayısı |
| commission_errors | Sürdürülen dikkat | Hedef-olmayana yanlış yanıt sayısı |
| task_switch_cost | Task-switching | bkz. 2.3 |
| sustained_attention_score | Sürdürülen dikkat | Bileşik skor (bkz. RESEARCH_PROTOCOL.md) |

### 2.3 Task-Switch Cost Hesaplama (literatüre dayalı, REFERENCES.md #12-13)
Yalnızca RT farkı (switch RT − repeat RT) kullanmak doğruluk maliyetlerini gizler.
Bu nedenle **birincil metrik**: Inverse Efficiency Score (IES) = RT / doğruluk oranı,
switch ve repeat trial'lar için ayrı ayrı hesaplanır; switch_cost_IES = IES_switch −
IES_repeat. Ham RT switch-cost ve ham doğruluk switch-cost **ikincil/betimsel**
metrik olarak da raporlanır (şeffaflık için).

### 2.4 Kontrol Değişkenleri
- yaş (yaş grubu, tam doğum tarihi DEĞİL)
- cinsiyet (opsiyonel, katılımcı beyanına dayalı, doldurmama seçeneği ile)
- test_time (günün saati — sirkadiyen etkiler için)
- device_type (masaüstü/mobil/tablet — RT ölçüm hassasiyetini etkiler)
- test_version / protocol_version

---

## 3. Deney / Test Protokolü Özeti

Ayrıntılı protokol `RESEARCH_PROTOCOL.md` içinde. Özet:

1. **Günlük kısa form** (≤1 dakika, 5 soru)
2. **Reaction Time Testi** (~3 dk, ~40-60 geçerli trial hedefi)
3. **Sürdürülen Dikkat Testi (Go/No-Go tipi)** (~4-5 dk — literatürde önerilen kısa
   versiyonlar 3-6 dk aralığında, REFERENCES.md #14-16)
4. **Task-Switching Testi** (~4-5 dk, "alternating runs" paradigması — renk/şekil
   kuralları arasında geçiş)
5. **Sonuç ekranı** — araştırma amaçlı olduğuna dair açık uyarı

**Toplam oturum süresi:** ~12-15 dakika/gün — ergen katılımcı için makul, tükenme
etkisini (fatigue) sınırlamak amacıyla kritik.

### 3.1 Reaction Time Ölçüm Sınırlılıkları (REFERENCES.md #8-11)
- Tarayıcı tabanlı RT ölçümü ~10-100ms ek gecikme/varyans içerebilir.
- `requestAnimationFrame` kullanılmalı, `setTimeout` KULLANILMAMALI.
- Sekme arka plana alınırsa (`document.visibilityState`) trial **invalid**
  işaretlenmeli, silinmemeli (şeffaflık için ham veri korunur).
- API gecikmesi RT ölçümüne asla dahil edilmemeli — ölçüm tamamen client-side,
  veri toplu halde test sonunda gönderilmeli.

### 3.2 Güvenilirlik Değerlendirmesi
- **Split-half reliability**: Her testin trial'ları rastgele ikiye bölünüp
  korelasyon (Spearman-Brown düzeltmeli) hesaplanmalı.
- **Test-retest reliability**: Aynı katılımcının farklı günlerdeki skorları
  arasındaki korelasyon (ICC önerilir, basit Pearson değil — tekrarlı ölçüm).
- Güvenilirlik düşükse (ör. ICC < .5), bu **açıkça raporlanmalı**; düşük
  güvenilirlikli bir ölçümle güçlü korelasyon iddiası yapılmamalı.

---

## 4. İstatistiksel Analiz Pipeline

```
Veri temizleme (geçersiz trial/oturum filtreleme, kurallar önceden tanımlı)
   ↓
Betimsel istatistikler (ortalama, medyan, SD, çarpıklık)
   ↓
Dağılım incelemesi (Shapiro-Wilk / Q-Q; RT genelde sağa çarpık → log dönüşüm
   veya medyan kullanımı düşünülmeli)
   ↓
Korelasyon analizi (Pearson veya Spearman — dağılıma göre)
   ↓
**Tekrarlı ölçüm uyarısı**: Aynı katılımcının çoklu günlük gözlemi TEK BAŞINA
   Pearson korelasyonuyla analiz edilirse gözlemlerin bağımsızlığı varsayımı
   ihlal edilir (yanlış p-değerleri / şişirilmiş anlamlılık riski). Bu nedenle:
   → **Mixed-effects (multilevel) model** kullanılmalı: gözlemler (seviye 1)
     katılımcı içinde (seviye 2) iç içe (nested). R: `lme4::lmer`,
     Python: `statsmodels.MixedLM`.
   ↓
Etki büyüklükleri (Cohen's d, r², veya sabit etki katsayıları standardize edilmiş)
   ↓
Güven aralıkları (%95 CI, bootstrap veya parametrik)
   ↓
Makine öğrenmesi (sadece istatistiksel analiz tamamlandıktan sonra, tamamlayıcı olarak)
```

**"İstatistiksel olarak anlamlı" ifadesi yalnızca gerçek p-değeri hesaplandığında
kullanılır.** Sentetik/demo veri üzerinde ASLA kullanılmaz.

---

## 5. Yazılım Mimarisi

Kullanıcının önerdiği yapı büyük ölçüde korunmuştur; küçük gerekçeli sapmalar
`ARCHITECTURE_DECISIONS.md` içinde belgelenecektir. Öngörülen sapmalar:

- **Reaction-time testleri tamamen client-side (React state + Web Worker
  gerektirmeyen basit RAF döngüsü) çalışır**, sonuç toplu halde `POST` edilir.
  Ağ gecikmesinin RT'ye karışmaması için bu zorunludur (bkz. 3.1).
- Geliştirme aşamasında **SQLite**, ancak katılımcı/oturum ayrımı ve JSON alanlar
  (ör. ham trial dizileri) nedeniyle üretimde **PostgreSQL + JSONB** önerilir —
  kullanıcının planıyla uyumlu.
- ML tarafında **DVC veya basit dosya-tabanlı versiyonlama** (dataset_version,
  model_version) — TÜBİTAK ölçeğinde tam bir MLOps yığını (MLflow vb.) gereksiz
  karmaşıklık olur; bu nedenle hafif bir çözüm önerilir (gerekçe: Bölüm 40 —
  "gereksiz teknoloji ekleme" ilkesi).

Dizin yapısı kullanıcının Bölüm 8'de verdiği yapıyla birebir uyumludur.

---

## 6. Veri Modeli (Özet — ayrıntı DATA_DICTIONARY.md'de)

```
participants (participant_id PK, age_band, gender[nullable], created_at)
sessions (session_id PK, participant_id FK, session_date, device_type, test_version)
daily_behavior (session_id FK, sleep_duration, screen_time, social_media_time,
                notification_count, study_time)
reaction_trials (trial_id PK, session_id FK, stimulus_timestamp, response_timestamp,
                 reaction_time, correct, valid, tab_hidden_flag)
attention_trials (trial_id PK, session_id FK, stimulus_type[go/no-go],
                  response_timestamp, correct, valid)
task_switch_trials (trial_id PK, session_id FK, rule_type, is_switch_trial,
                    reaction_time, correct, valid)
analysis_runs (run_id PK, dataset_version, code_version, timestamp, parameters_json)
model_runs (run_id PK, analysis_run_id FK, model_type, cv_strategy, metrics_json,
            random_seed)
```

`participant_id` gerçek kimlik bilgisi İÇERMEZ (ör. "P001"). Ad/telefon/e-posta
şeması hiçbir tabloda YOKTUR (Bölüm 9-10 kısıtı).

---

## 7. Makine Öğrenmesi Stratejisi

### 7.1 Temel İlke
Amaç en yüksek doğruluk değil; **davranışsal değişkenlerin bilişsel performansı
ne ölçüde ve ne güvenilirlikte açıkladığını dürüstçe ölçmek.**

### 7.2 Model Sırası (baseline'dan karmaşığa)
1. Ortalama tahmin (mean baseline) — referans
2. Doğrusal regresyon
3. Ridge / Lasso (regularizasyon — küçük n için önemli)
4. Random Forest (yalnızca n yeterliyse)
5. Gradient Boosting (yalnızca n yeterliyse; **büyük ihtimalle bu projede
   kullanılmamalı** — bkz. 7.4)

### 7.3 Data Leakage — ZORUNLU KURAL
Aynı katılımcının farklı gün/oturumlarına ait satırlar **asla** hem train hem
test setine rastgele dağıtılmaz. `GroupKFold` / `GroupShuffleSplit`,
`groups=participant_id` ile kullanılır. Bu, REFERENCES.md #17-19'daki bulgularla
doğrudan gerekçelendirilmiştir: participant-level leakage, gerçekçi ~0.66
doğruluğu yapay olarak ~0.91'e şişirebilir. `ML_METHODOLOGY.md` içinde bu konu
somut kod örnekleriyle ayrıntılandırılacaktır.

### 7.4 Örneklem Büyüklüğü Dürüst Değerlendirmesi
Bir lise araştırma projesinde gerçekçi katılımcı sayısı muhtemelen **20-60 kişi**,
kişi başına birkaç gün tekrarlı ölçümle toplam **100-400 gözlem** civarındadır.
Bu ölçekte:
- Gradient Boosting / derin karmaşık modeller **önerilmez** — overfitting riski
  yüksek, yorumlanabilirlik düşüktür.
- Asıl bilimsel değer **klasik istatistik + basit/regularize edilmiş modellerden**
  gelecektir; ML burada "keşifçi ve tamamlayıcı" bir rol oynamalıdır, ana bulgu
  kaynağı DEĞİLDİR. Bu nokta jüri karşısında açıkça ifade edilmelidir (bkz. Bölüm G).

### 7.5 Açıklanabilirlik
Permutation importance (basit, model-agnostik) birincil yöntem. SHAP yalnızca
ağaç tabanlı modellerde ve n yeterliyse kullanılır; hesaplama maliyeti ve
yorumlama karmaşıklığı bu ölçekte SHAP'ı çoğu zaman gereksiz kılabilir.

**Yasak ifade:** "Bu değişken dikkat düşüşüne neden oluyor."
**İzinli ifade:** "Model açısından bu değişken tahmin gücüne daha yüksek katkı
sağladı."

---

## 8. Gizlilik Modeli (Özet — PRIVACY.md'de ayrıntı)

- Privacy-by-design: minimum veri toplama, pseudonymous participant_id.
- KVKK (6698 sayılı Kanun) çerçevesinde çocuklardan (18 yaş altı) veri işleme için
  ayrı bir rejim yoktur; TMK velayet hükümleri gereği **açık rıza veliden alınır**
  (REFERENCES.md #7). Katılımcının kendisinden de yaşına uygun "bilgilendirilmiş
  onay/asent" alınması önerilir.
- Ad, telefon, e-posta gibi doğrudan tanımlayıcılar toplanmaz.
- Transport encryption (HTTPS/TLS) zorunlu.
- Researcher rolü, participant'ların birbirinin verisini görmesini engeller;
  agregat/anonimleştirilmiş görünüm esastır.

---

## 9. Etik ve İzin Süreci (Özet — ETHICS_AND_CONSENT.md'de ayrıntı)

Gerçek katılımcı verisi toplanmadan önce **sırasıyla**:

1. MEB'e bağlı okul paydaşlarıyla çalışılacaksa: **arastirmaizinleri.meb.gov.tr**
   üzerinden Araştırma Uygulama İzin Belgesi (REFERENCES.md #2).
2. MEB dışı kurumda çalışılacaksa: ilgili kurumdan izin belgesi.
3. Tüm katılımcılar 18 yaş altıysa: **veli izin/onam belgesi** zorunlu
   (REFERENCES.md #2, #3).
4. Kullanılacak anket/ölçek geliştiricilerinden kullanım izni/telif hakkı.
5. İçerik itibarıyla gerekiyorsa (ör. üniversite/kurum iş birliği varsa) ilgili
   etik kuruldan onay (REFERENCES.md #4).

**Bu izinler tamamlanana kadar sistem `RESEARCH_NOT_READY` durumunda kalır ve
gerçek katılımcı verisi toplama modu "production" olarak sunulmaz** (Bölüm 38
kısıtı, aynen korunmuştur).

---

## 10. Test Stratejisi (Özet)

- Backend: `pytest` — özellikle geçersiz trial, eksik veri, duplicate submission,
  participant isolation, researcher authorization, data leakage (CV testleri),
  geçersiz timestamp, outlier handling.
- Frontend: `Vitest` + RTL — RT test bileşeninin zamanlama mantığı (mock RAF).
- E2E: `Playwright` — uçtan uca oturum akışı.
- ML pipeline testleri: GroupKFold'un gerçekten grup ayrımı yaptığını doğrulayan
  birim testi (kritik — bu olmadan leakage sessizce geri gelebilir).

---

## 11. TÜBİTAK Uyumluluk Ön Değerlendirmesi

Ayrıntı `TUBITAK_ALIGNMENT.md`'de; özet:

| Kriter | Ön Değerlendirme | Kanıt/Gereken |
|---|---|---|
| Özgün fikir öğrenciye mi ait? | **Doğrulanamaz** — bu bir süreç kanıtıdır, belgeyle değil, öğrencinin proje defteri/günlüğü ve jüri mülakatıyla kanıtlanır. | Proje süreç günlüğü tutulmalı |
| Yöntem amaca uygun mu? | **Kısmen evet** — ama örneklem büyüklüğü ML iddialarını sınırlayabilir | Bölüm 7.4 |
| Alan yazına dayalı mı? | **Evet** — REFERENCES.md ile desteklenmiş | — |
| Yaratıcılık / yeni bakış açısı | **Orta** — "ekran süresi–dikkat" ilişkisi çok çalışılmış bir alan (REFERENCES.md #20); özgünlük muhtemelen **yöntemde** (kendi geliştirilen web tabanlı çoklu-gün bilişsel test bataryası + ML boru hattı) aranmalı, sorunun kendisinde değil | Bkz. Bölüm F, aşağıda |
| Sonuçların kullanılabilirliği | Küçük n ile sınırlı genellenebilirlik; okul/veli için "farkındalık" çıktısı üretilebilir | — |

**Dürüst uyarı:** Salt "ekran süresi × dikkat" sorusu literatürde yoğun biçimde
çalışılmıştır ve etki büyüklükleri küçüktür (REFERENCES.md #20). Jüri özgünlüğü
muhtemelen *"okulun kendi öğrencilerinde, çok-günlük tekrarlı ölçüm + uygun
istatistik (mixed-effects) + participant-aware ML ile metodolojik olarak sağlam
bir küçük-ölçek araştırma modeli kurma"* yönünde değerlendirecektir — bu nedenle
metodolojik titizlik, bu projenin özgünlük iddiasının ana dayanağı olmalıdır.

---

## 12. Geliştirme Yol Haritası (13 Faz — kullanıcının sırasıyla)

Faz 1 (Araştırma) — **TAMAMLANDI** (bu belge + REFERENCES.md).
Faz 2-13 — onay sonrası, her faz sonunda ayrı rapor ile ilerlenecek.

**Önerilen ilk somut adım (onay verilirse):** Faz 2 (Bilimsel Protokol) — yani
`RESEARCH_PROTOCOL.md`, `DATA_DICTIONARY.md`, `ETHICS_AND_CONSENT.md` belgelerinin
tam metinlerinin yazılması — kod yazımından önce.

---

## 12.1 Rekabet Avantajı İçin Stratejik Kararlar (Jüri Değerlendirme Kriterlerine Dayalı)

Bölüm 11'deki dürüst değerlendirme ("soru düzeyinde orta özgünlük") göz önüne
alınarak, jürinin gerçekten aradığı unsurlara (Bölüm 3.6.7 — sadece durum tespiti
değil müdahale/çözüm önerisi; Önsöz — "özgün fikir", "yaratıcılık"; GENEL BİLGİLER
1.4 — bilimsel titizlik) dayanan üç somut karar eklenmiştir. Bunlar veri
uydurmadan, sadece tasarımı güçlendirerek özgünlüğü artırır:

**Karar 1 — Araştırma sorusunu "durum tespiti"nden "içi-kişi değişkenlik"e kaydırma.**
Literatürdeki çoğu ekran süresi–bilişsel performans çalışması **kişiler-arası**
(between-person) korelasyona dayanır (bkz. REFERENCES.md #20). FocusMind'ın çok
günlük tekrarlı ölçüm tasarımı, asıl özgün katkıyı **kişi-içi (within-person)**
soruya kaydırmaya izin verir: *"Aynı öğrencinin kendi ortalamasına göre, o gün
normalden fazla ekran süresi geçirdiğinde, o günkü dikkat performansı yine
kendi ortalamasına göre değişiyor mu?"* Bu, mixed-effects modelde ayrıştırılabilir
(within-person centering / person-mean centering tekniği). Bu açı, literatürde
lise projeleri düzeyinde nadiren görülür ve metodolojik özgünlük iddiasının
merkezi dayanağı olmalıdır.

**Karar 2 — "Sadece tespit değil, müdahale" ilkesini karşılayan hafif bir bileşen
ekleme.** Kullanım süresi boyunca toplanan verilerin ardından katılımcıya
(ve isterse veliye/öğretmene), **tanı koymayan, genel ve kişiselleştirilmemiş**
bir "dijital farkındalık özeti" gösterilebilir (ör. "Bu hafta ortalama uyku
süreniz X saatti; uyku hijyeni ile ilgili genel öneriler için ..."). Bu, klinik
iddia taşımaz, sadece rehberin özellikle vurguladığı "araştırma + uygulanabilir
çıktı" beklentisini karşılar. Bu bileşen **opsiyonel** olmalı ve asla bireysel
performans verisine dayalı psikolojik yorum içermemelidir.

**Karar 3 — Metodolojik titizliği projenin "başlığı" haline getirme.** Sunumda ve
raporda, projenin özgünlüğü açıkça şu cümleyle çerçevelenmelidir: *"Bu araştırmanın
katkısı, ekran süresinin dikkate 'etkisini keşfetmek' değil; lise düzeyinde nadiren
uygulanan, katılımcı-düzeyinde veri sızıntısından arındırılmış makine öğrenmesi
değerlendirmesi ve çok-günlük tekrarlı ölçüm için uygun istatistiksel modelleme
ile psikolojik araştırmanın nasıl güvenilir biçimde yürütülebileceğini
göstermektir."* Bu çerçeve, jürinin "yöntem uygun mu, bulgular amacı gerçekten
test ediyor mu" kriterine doğrudan hitap eder (bkz. Bölüm 37, orijinal talep).

---

## 13. Açık Riskler / Öğrenciye Dürüst Uyarılar

1. **Örneklem büyüklüğü riski**: Lise ortamında muhtemelen küçük n → ML modelleri
   zayıf/gürültülü sonuç verebilir. Bu bir *başarısızlık değil*, dürüstçe
   raporlanması gereken bir sınırlılıktır.
2. **Self-report davranış verisi** (ekran süresi vb.) genellikle cihaz-ölçümlü
   veriden daha az güvenilirdir; mümkünse ekran süresi için cihazın kendi
   "screen time" raporu istenip self-report ile karşılaştırılabilir (ek geçerlik
   kanıtı).
3. **Tekrarlı ölçüm + küçük n** kombinasyonu, klasik ML metriklerinin (özellikle
   RMSE/R²) güven aralıklarını geniş kılar; nokta tahminlerinin yanında MUTLAKA
   güven aralığı raporlanmalı.
4. **Özgünlük riski** (Bölüm 11) — yöntemsel katkı vurgulanmalı.
5. **Etik/izin süreci zaman alabilir** — MEB araştırma izni ve veli onamı süreci,
   proje takviminde erken başlatılmalı (Faz 10'u beklemeden, paralel yürütülmeli).
