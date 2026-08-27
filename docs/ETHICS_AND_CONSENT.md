# FocusMind — ETHICS_AND_CONSENT.md

Durum: TASLAK — Faz 2 çıktısı.

## 1. Mevcut Durum

**Sistem şu anda `RESEARCH_NOT_READY` durumundadır.** Aşağıdaki izinler
tamamlanmadan gerçek katılımcı verisi toplanamaz ve toplanmış olsa bile
"araştırma sonucu" olarak sunulamaz. Bu süre zarfında sistem yalnızca
`DEMO MODE` (sentetik veri) ile çalıştırılabilir (bkz. PROJECT_PLAN.md, ileride
eklenecek DEMO_MODE bölümü).

## 2. Gerekli İzin Zinciri (REFERENCES.md #2, #3, #4)

### Adım 1 — Kurum İzni
- Araştırma bir MEB'e bağlı okulda, okulun öğrenci/öğretmen/veli paydaşlarıyla
  yürütülecekse: **arastirmaizinleri.meb.gov.tr** üzerinden "Araştırma Uygulama
  İzin Belgesi" alınır.
- MEB'e bağlı olmayan bir kurumda (özel kurs, dernek vb.) yürütülecekse: o
  kurumun kendi yönetiminden yazılı izin alınır.

### Adım 2 — Veli Onamı (18 Yaş Altı Katılımcılar İçin ZORUNLU)
- Türk Medeni Kanunu'nun velayet hükümleri gereği (KVKK'da çocuklara özel ayrı
  bir rejim tanımlanmadığından), açık rıza **veliden** alınır.
- Onam formu şunları içermelidir:
  - Araştırmanın amacı (sade dille, teşhis/tanı amacı olmadığı açıkça belirtilerek)
  - Toplanacak veri türleri (davranış anketi + bilişsel test performansı)
  - Verinin nasıl saklanacağı, kimlerin erişebileceği
  - Katılımın gönüllü olduğu ve istenildiği an çekilebileceği
  - Sonuçların yalnızca toplu/anonim biçimde raporlanacağı
  - Veli iletişim bilgisi ve sorular için başvuru kanalı

### Adım 3 — Katılımcı Asenti (Bilgilendirilmiş Onay — Öğrencinin Kendisinden)
- Veli onamına ek olarak, öğrencinin kendisine de yaşına uygun sadeleştirilmiş
  bir dille araştırma açıklanır ve katılmak isteyip istemediği sorulur
  ("asent" — çocuğun kendi rızası, veli onamının yerine geçmez, onu tamamlar).

### Adım 4 — Ölçek/Anket Telif İzinleri
- Kullanılacak günlük davranış anketi orijinal (bu projede özel olarak
  tasarlanmıştır) olduğu için üçüncü taraf telif sorunu yoktur. Eğer standart
  bir ölçek (ör. yayınlanmış bir ekran bağımlılığı ölçeği) eklenirse, o ölçeğin
  geliştiricisinden kullanım izni alınmalıdır.

### Adım 5 — Etik Kurul (Gerekiyorsa)
- Eğer proje bir üniversite/kurumla resmi iş birliği içinde yürütülüyorsa, o
  kurumun insan araştırmaları etik kurulundan onay gereklidir (5237 sayılı TCK
  m.90 ve 3359 sayılı Sağlık Hizmetleri Kanunu Ek m.10 çerçevesinde).
- Salt bir lise araştırma projesi olarak, resmi bir üniversite iş birliği
  yoksa, bu adım danışman öğretmen ve okul yönetimi onayı ile karşılanabilir;
  ancak nihai karar bölge koordinatörlüğüne danışılarak netleştirilmelidir.

## 3. Gizlilik Taahhütleri (PRIVACY.md ile Çapraz Referans)

- Katılımcıya ait ad, telefon, e-posta gibi doğrudan tanımlayıcı veri
  toplanmaz.
- `participant_id` ile gerçek kimlik arasındaki eşleştirme listesi (varsa,
  yalnızca veli onam takibi için), araştırma verisinden **fiziksel ve dijital
  olarak ayrı** saklanır ve yalnızca sorumlu öğretmen/öğrenciye erişim
  tanınır.
- Veriler yalnızca bu araştırma kapsamında kullanılır, üçüncü taraflarla
  paylaşılmaz.

## 4. Geri Çekilme Hakkı

Katılımcı (veya velisi) istediği an, sebep göstermeksizin araştırmadan
çekilebilir. Çekilme talebinde, o katılımcıya ait tüm veriler (`participant_id`
ile ilişkili tüm satırlar) analiz veri setinden çıkarılır ve silinir.

## 5. Kontrol Listesi (Rapor Ekine Konacak)

- [ ] MEB araştırma izni alındı / kurum izni alındı
- [ ] Tüm katılımcılar için veli onam formu imzalandı
- [ ] Tüm katılımcılardan asent alındı
- [ ] Kullanılan ölçekler için telif izni alındı (varsa)
- [ ] Danışman öğretmen/okul onayı belgelendi
- [ ] Tüm izin belgelerinin kopyası proje dosyasında saklandı

**Bu kontrol listesindeki maddeler tamamlanmadan sistem "production" moduna
alınamaz.**
