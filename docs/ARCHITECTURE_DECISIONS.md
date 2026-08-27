# FocusMind — ARCHITECTURE_DECISIONS.md

## AD-1: Reaction-time testleri tamamen client-side çalışır
**Karar:** Uyaran sunumu ve yanıt zamanlaması backend'e hiçbir ağ çağrısı yapmadan,
tarayıcıda `requestAnimationFrame` + `performance.now()` ile yürütülür. Sonuçlar
test bitince toplu (`POST /api/reaction-trials`, tek istek, trial dizisi) gönderilir.
**Gerekçe:** Ağ gecikmesi RT ölçümüne karışırsa ölçüm geçersizleşir
(REFERENCES.md #8-11). Bu, bilimsel geçerliğin ön koşuludur, tercih değildir.

## AD-2: SQLite (dev) → PostgreSQL (prod), MLflow değil hafif JSON versiyonlama
**Karar:** Üretimde PostgreSQL+JSONB kullanılır ama MLflow/DVC gibi tam bir MLOps
yığını kurulmaz; `analysis_runs`/`model_runs` tablolarına `dataset_version`,
`code_version`, `parameters_json`, `metrics_json` yazılır.
**Gerekçe:** Lise projesi ölçeğinde tam MLOps gereksiz karmaşıklık ekler
(orijinal talep §40 ilkesi: "en havalı" değil, "bilimsel olarak uygun" araç).
Reprodüksiyon ihtiyacı, basit versiyon alanlarıyla karşılanabilir.

## AD-3: Gradient Boosting/derin modeller varsayılan olarak KAPALI
**Karar:** ML pipeline varsayılan olarak Mean Baseline → Linear → Ridge/Lasso →
(yalnızca n ≥ eşik ise) Random Forest sırasını izler; Gradient Boosting bir
"ileri seçenek" olarak kilitli/uyarılı sunulur.
**Gerekçe:** REFERENCES.md #17-19; küçük n'de karmaşık modeller overfitting riski
taşır ve yorumlanabilirliği düşürür.

## AD-4: Demo Mode, ayrı bir DB şeması değil, `is_demo` bayrağıyla aynı şemada
**Karar:** Sentetik veri gerçek veriyle aynı tablolara, `sessions.is_demo=true`
ile yazılır; ayrı bir demo veritabanı kurulmaz.
**Gerekçe:** Aynı analiz/ML kodunun demo ve gerçek veri üzerinde test edilmesini
sağlar (kod tekrarını önler), ama UI katmanında `is_demo=true` olan hiçbir kayıt
"araştırma sonucu" olarak etiketlenemez — bu kural API ve frontend'de çift kontrol
edilir (bkz. TESTING.md).

## AD-5: Basit rol modeli (participant / researcher), tam RBAC değil
**Karar:** İki rol: `participant` (yalnızca kendi session'larına yazar/okur),
`researcher` (yalnızca agregat/anonim uçlara okur, ham `participant_id`→kimlik
eşlemesine erişemez).
**Gerekçe:** Orijinal talebin §26 kısıtı; ölçekte tam bir yetkilendirme
matrisi (ör. Casbin) gereksizdir.

## AD-6: Frontend durum yönetimi — üçüncü parti kütüphane yerine React Context
**Karar:** Redux/Zustand yerine basit React Context + useReducer.
**Gerekçe:** Uygulamanın durum karmaşıklığı düşük (test akışı + sonuç ekranı);
ek kütüphane gereksiz bağımlılık ekler.
