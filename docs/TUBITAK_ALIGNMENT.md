# FocusMind — TUBITAK_ALIGNMENT.md

Her kriter, orijinal talebin Bölüm 37'sindeki üç ana eksene göre değerlendirilir.
**Hiçbir kriter varsayılan olarak "sağlanıyor" kabul edilmemiştir; her biri
kanıt veya açık eksiklik notuyla birlikte verilmiştir.**

## 1. Başarılabilirlik

| Alt kriter | Değerlendirme | Kanıt |
|---|---|---|
| Yöntem amaca uygun mu? | Kısmen evet | Mixed-effects model + GroupKFold, gözlemsel/tekrarlı-ölçüm verisine uygun; ancak örneklem küçükse ML bulguları sınırlı genellenebilir (açıkça raporlanacak) |
| Amaç açık mı? | Evet | PROJECT_PLAN.md §0, ölçülebilir alt sorular §1'de listelendi |
| Bulgular amacı gerçekten test ediyor mu? | Test edilebilir tasarım kuruldu | RESEARCH_PROTOCOL.md'deki her test, ilgili alt soruya doğrudan bağlanıyor |
| **Eksiklik** | Gerçek veri henüz yok | Etik/izin süreci tamamlanmadan bu kriter nihai olarak doğrulanamaz |

## 2. Yaratıcılık

| Alt kriter | Değerlendirme | Kanıt |
|---|---|---|
| Sorunun kendisi özgün mü? | **Hayır, orta düzeyde** | Ekran süresi-dikkat ilişkisi yoğun çalışılmış (REFERENCES.md #20) — dürüstçe kabul edilmeli |
| Yöntemde özgünlük var mı? | **Evet** | Kişi-içi (within-person) analiz açısı + katılımcı-farkında ML boru hattı, lise projesi ölçeğinde nadir (PROJECT_PLAN.md §12.1) |
| Farklı bir perspektif sunuluyor mu? | Evet | "Durum tespiti" yerine "metodolojik sağlamlık" vurgusu |

## 3. Sonuçların Kullanılabilirliği

| Alt kriter | Değerlendirme | Kanıt |
|---|---|---|
| Gerçek bir probleme katkı sağlar mı? | Sınırlı ama gerçek | Küçük n nedeniyle genellenebilirlik sınırlı; okul-içi farkındalık aracı olarak kullanılabilir |
| Uygulanabilir çıktı var mı? | Evet (opsiyonel bileşen) | Genel/tanı-koymayan dijital farkındalık özeti (PROJECT_PLAN.md §12.1 Karar 2) |

## 4. Genel Öz-Eleştiri (Jüri Sorabilecek Sorulara Hazırlık)

- **"Bu soru yeterince özgün mü?"** → Hayır tek başına değil; cevap yöntemde
  aranmalı, bu açıkça kabul edilmeli.
- **"Örneklem yeterli mi?"** → Muhtemelen ML için sınırlı; bu bir zayıflık
  olarak sunulmalı, gizlenmemelidir. Sunumda "bu ölçekte ne öğrenilebilir,
  ne öğrenilemez" ayrımı net yapılmalı.
- **"Neden makine öğrenmesi gerekli?"** → Zorunlu değil; katkısı sınırlı ve
  tamamlayıcı olarak sunulmalı, ana bulgu klasik istatistikten gelmelidir.
