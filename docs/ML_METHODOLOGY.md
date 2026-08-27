# FocusMind — ML_METHODOLOGY.md

## 1. Amaç
Davranışsal değişkenlerin bilişsel performansı ne ölçüde açıkladığını, katılımcı
düzeyinde veri sızıntısı olmadan, dürüstçe ölçmek. Amaç en yüksek doğruluk değildir.

## 2. Veri Sızıntısı (Data Leakage) — Zorunlu Kural

**YANLIŞ (asla yapılmaz):**
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# HATA: aynı participant_id'nin farklı günleri hem train hem test'e düşebilir
```

**DOĞRU:**
```python
from sklearn.model_selection import GroupKFold
import numpy as np

groups = df["participant_id"].values
gkf = GroupKFold(n_splits=5)

for train_idx, test_idx in gkf.split(X, y, groups=groups):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    assert set(groups[train_idx]).isdisjoint(set(groups[test_idx])), \
        "Katılımcı sızıntısı tespit edildi!"
```

**Zorunlu birim testi (tests/test_ml_leakage.py):**
```python
def test_groupkfold_no_participant_overlap():
    """Her fold'da train ve test participant_id kümeleri kesişmemeli."""
    for train_idx, test_idx in gkf.split(X, y, groups=groups):
        train_participants = set(groups[train_idx])
        test_participants = set(groups[test_idx])
        assert train_participants.isdisjoint(test_participants)
```
Bu test CI pipeline'ında her çalıştırmada geçmelidir; başarısız olursa build
kırılır.

## 3. Model Sırası ve Eşikler

```python
MIN_SAMPLES_FOR_RF = 150   # gözlem sayısı (satır), katılımcı değil
MIN_PARTICIPANTS_FOR_RF = 25

models_to_try = ["mean_baseline", "linear_regression", "ridge", "lasso"]
if n_observations >= MIN_SAMPLES_FOR_RF and n_participants >= MIN_PARTICIPANTS_FOR_RF:
    models_to_try.append("random_forest")
# gradient_boosting varsayılan olarak eklenmez; yalnızca açık --advanced bayrağıyla
```

## 4. Değerlendirme Metrikleri (Regresyon — birincil kullanım durumu)
- MAE, RMSE, R² — **her biri için bootstrap %95 güven aralığı** hesaplanır
  (katılımcı düzeyinde bootstrap — `resample(participant_ids)`).
- Nokta tahmini yalnız başına raporlanmaz.

```python
from sklearn.utils import resample

def bootstrap_ci(y_true, y_pred, participant_ids, metric_fn, n_boot=1000):
    scores = []
    unique_ids = np.unique(participant_ids)
    for _ in range(n_boot):
        sampled_ids = resample(unique_ids)
        mask = np.isin(participant_ids, sampled_ids)
        scores.append(metric_fn(y_true[mask], y_pred[mask]))
    return np.percentile(scores, [2.5, 97.5])
```

## 5. Açıklanabilirlik
```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=30, random_state=42)
# Rapor cümlesi: "Model açısından X değişkeni tahmin gücüne en yüksek katkıyı sağladı."
# YASAK cümle: "X değişkeni performans düşüşüne neden oldu."
```
SHAP yalnızca `n_participants >= 25` ve ağaç-tabanlı model kullanıldığında
opsiyonel olarak eklenir; küçük örneklemde ek karmaşıklık faydadan fazla yanıltıcı
kesinlik izlenimi verebilir.

## 6. Reprodüksiyon Kaydı
Her `python scripts/run_analysis.py` çalıştırması şunları `analysis_runs` /
`model_runs` tablolarına yazar: dataset_version (verinin hash'i), code_version
(git commit), random_seed, tüm hiperparametreler, tüm metrikler ve CI'ler.

## 7. Sınıflandırma Kullanımı — Sınırlı ve Gerekçeli
Sınıflandırma (ör. "düşük/yüksek dikkat" ikili ayrımı) yalnızca araştırma sorusu
gerçekten kategorik bir ayrımı gerektiriyorsa kullanılır. Bu projede birincil
kullanım durumu regresyondur (sürekli skorlar); sınıflandırma sadece ek/duyarlılık
analizi olarak sunulabilir, birincil bulgu olarak KULLANILMAZ (keyfi eşik değer
seçimi p-hacking riski taşır).
