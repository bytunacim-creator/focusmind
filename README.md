# FocusMind

**Ergenlerde Dijital Davranışların Bilişsel Dikkat Performansıyla İlişkisinin
Davranışsal Veriler ve Makine Öğrenmesi Kullanılarak İncelenmesi**

TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projesi (Psikoloji ana alanı).

## ⚠️ Mevcut Durum: RESEARCH_NOT_READY

Bu sistem şu anda yalnızca **DEMO MODE** (tamamen sentetik veri) ile çalışır.
Gerçek katılımcı verisi toplanmadan önce `docs/ETHICS_AND_CONSENT.md` içindeki
izin zincirinin (MEB araştırma izni / kurum izni + veli onamı + katılımcı asenti)
eksiksiz tamamlanması zorunludur. Bkz. o belge için tam kontrol listesi.

## Proje Felsefesi

Bu bir "web sitesi" değil, bilimsel açıdan savunulabilir bir araştırma
platformudur. Sistem **hiçbir zaman**:
- psikolojik tanı koymaz,
- katılımcıları "sağlıklı/sağlıksız" diye sınıflandırmaz,
- gerçek olmayan veriyi araştırma sonucu gibi sunmaz.

## Belgeler (docs/)

| Belge | İçerik |
|---|---|
| PROJECT_PLAN.md | Amaç, araştırma soruları, mimari, ML stratejisi, roadmap |
| RESEARCH_PROTOCOL.md | Test tasarımları, güvenilirlik planı, outlier kuralları |
| DATA_DICTIONARY.md | Tüm veritabanı tablo/kolon tanımları |
| ETHICS_AND_CONSENT.md | İzin zinciri, veli onamı, kontrol listesi |
| PRIVACY.md | Gizlilik modeli, erişim kontrolü |
| ML_METHODOLOGY.md | Data leakage önleme, GroupKFold, kod örnekleri |
| ARCHITECTURE_DECISIONS.md | Teknik kararlar ve gerekçeleri |
| TESTING.md | Test stratejisi ve zorunlu senaryolar |
| TUBITAK_ALIGNMENT.md | Jüri kriterlerine göre dürüst öz-değerlendirme |

`research/references/REFERENCES.md` içinde tüm bilimsel iddiaların dayandığı
kaynaklar (TÜBİTAK resmi belgeleri + akademik literatür) listelenmiştir.

## Çalıştırma

```bash
# Backend testleri (data leakage testi dahil — kritik)
cd backend && pytest tests/ -v

# Uçtan uca analiz pipeline'ı (DEMO/SENTETİK veri ile)
python scripts/run_analysis.py
# Çıktılar: research/analysis/*.csv, run_metadata.json
```

## Kritik Kural

`is_demo=true` olan hiçbir veri/sonuç, "araştırma bulgusu" olarak sunulamaz.
Bu kural API (`/api/research/summary`) ve test seviyesinde
(`test_demo_sessions_are_flagged`) doğrulanmıştır.
