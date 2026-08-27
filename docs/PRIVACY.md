# FocusMind — PRIVACY.md

## 1. Privacy-by-Design İlkeleri
- **Minimum veri toplama:** Yalnızca araştırma sorusuna doğrudan hizmet eden
  veriler toplanır (bkz. DATA_DICTIONARY.md). Ad, telefon, e-posta, TC kimlik no
  hiçbir tabloda YOKTUR.
- **Pseudonymous ID:** `participant_id` (P001 formatı) rastgele/sıralı üretilir,
  gerçek kimlikle eşleşmesi yalnızca fiziksel/ayrı bir veli-onam kayıt defterinde
  tutulur (araştırma veritabanının dışında).
- **Amaç sınırlaması:** Toplanan veri yalnızca bu araştırma kapsamında
  kullanılır; başka bir amaçla (pazarlama, üçüncü taraf paylaşımı vb.)
  kullanılmaz.

## 2. Transport ve Depolama Güvenliği
- Tüm istemci-sunucu iletişimi HTTPS/TLS üzerinden yapılır.
- Şifreler (researcher hesapları için) bcrypt/argon2 ile hash'lenir, asla düz
  metin saklanmaz.
- Production veritabanı erişimi rol-tabanlı kısıtlanır; yalnızca proje
  sorumlusu (danışman öğretmen) ve öğrenci geliştirici tam erişime sahiptir.

## 3. Erişim Kontrolü
| Rol | Erişim |
|---|---|
| participant | Yalnızca kendi `participant_id`'sine ait session/trial verisi |
| researcher | Yalnızca agregat/anonimleştirilmiş istatistikler ve model çıktıları; ham `participant_id`↔kimlik eşlemesine erişemez |

## 4. Üçüncü Taraf Analitik Kullanılmaz
Google Analytics vb. üçüncü taraf izleme araçları kullanılmaz. Yalnızca
araştırma amacıyla toplanan, bu belgede tanımlanan veriler işlenir.

## 5. Veri Saklama ve Silme
- Araştırma tamamlandıktan ve rapor teslim edildikten sonra, veli onamında
  belirtilen süre sonunda (önerilen: 2 yıl, TÜBİTAK arşiv gereksinimleri
  saklı kalmak kaydıyla) ham veri silinir; yalnızca anonim/agregat istatistikler
  saklanabilir.
- Bir katılımcı/veli geri çekilme talebinde bulunursa, ilgili `participant_id`'ye
  ait tüm satırlar derhal silinir (ETHICS_AND_CONSENT.md §4).

## 6. Demo/Sentetik Veri Ayrımı
`is_demo=true` olan hiçbir kayıt gerçek kişiyle ilişkilendirilemez (zaten
üretilmiştir, gerçek katılımcıya ait değildir) ve UI'da her zaman "DEMO /
SENTETİK VERİ" etiketiyle gösterilir — bu aynı zamanda bir şeffaflık, hem de
gizlilik önlemidir (gerçek veriyle karıştırılmasını önler).
