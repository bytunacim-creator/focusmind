# FocusMind — DATA_DICTIONARY.md

Durum: TASLAK — Faz 2 çıktısı.

## participants
| Kolon | Tip | Nullable | Birim/Format | Kaynak | Açıklama |
|---|---|---|---|---|---|
| participant_id | TEXT (PK) | Hayır | "P001" formatı | Sistem üretir | Gerçek kimlik içermez |
| age_band | TEXT | Hayır | ör. "14-15", "16-17" | Onam formu | Tam yaş değil, aralık — ek anonimleştirme |
| gender | TEXT | Evet | "F"/"M"/"belirtmek istemiyorum" | Katılımcı beyanı | Opsiyonel |
| consent_status | TEXT | Hayır | "veli_onami_alindi" vb. | Manuel giriş | Araştırmacı tarafından işaretlenir |
| created_at | TIMESTAMP | Hayır | ISO 8601 | Sistem | — |

## sessions
| Kolon | Tip | Nullable | Birim/Format | Kaynak | Açıklama |
|---|---|---|---|---|---|
| session_id | TEXT (PK) | Hayır | UUID | Sistem | — |
| participant_id | TEXT (FK) | Hayır | — | — | participants'a referans |
| session_date | DATE | Hayır | YYYY-MM-DD | Sistem | — |
| test_time | TIME | Hayır | HH:MM | Sistem (client saati) | Sirkadiyen kontrol değişkeni |
| device_type | TEXT | Hayır | "desktop"/"mobile"/"tablet" | User-Agent | RT hassasiyetini etkiler |
| test_version | TEXT | Hayır | ör. "1.0.0" | Sistem | Reprodüksiyon için |
| is_demo | BOOLEAN | Hayır | true/false | Sistem | Demo/sentetik veri işareti — ZORUNLU alan |
| session_quality | TEXT | Evet | "valid"/"low_quality" | Analiz pipeline | §6 RESEARCH_PROTOCOL kuralına göre hesaplanır |

## daily_behavior
| Kolon | Tip | Nullable | Birim | Kaynak | Açıklama |
|---|---|---|---|---|---|
| session_id | TEXT (FK) | Hayır | — | — | — |
| sleep_duration | FLOAT | Evet | saat | Self-report | Boş bırakılabilir |
| screen_time | FLOAT | Evet | dakika | Self-report / cihaz raporu | `source` alanıyla ayrım |
| screen_time_source | TEXT | Evet | "self_report"/"device_report" | Kullanıcı seçimi | Geçerlik karşılaştırması için |
| social_media_time | FLOAT | Evet | dakika | Self-report | — |
| notification_count | INTEGER | Evet | adet | Self-report | Kaba tahmin |
| study_time | FLOAT | Evet | dakika | Self-report | — |

## reaction_trials
| Kolon | Tip | Nullable | Birim | Açıklama |
|---|---|---|---|---|
| trial_id | TEXT (PK) | Hayır | UUID | — |
| session_id | TEXT (FK) | Hayır | — | — |
| trial_index | INTEGER | Hayır | 0-based | Sırayla |
| stimulus_timestamp | FLOAT | Hayır | ms (performance.now()) | — |
| response_timestamp | FLOAT | Evet | ms | Null ise omission |
| reaction_time | FLOAT | Evet | ms | response - stimulus |
| correct | BOOLEAN | Hayır | — | — |
| valid | BOOLEAN | Hayır | — | §3 RESEARCH_PROTOCOL kurallarına göre |
| tab_hidden_flag | BOOLEAN | Hayır | — | visibilitychange sırasında true |
| is_practice | BOOLEAN | Hayır | — | Pratik trial'lar analiz dışı |

## attention_trials
| Kolon | Tip | Nullable | Birim | Açıklama |
|---|---|---|---|---|
| trial_id | TEXT (PK) | Hayır | UUID | — |
| session_id | TEXT (FK) | Hayır | — | — |
| stimulus_type | TEXT | Hayır | "go"/"no_go" | — |
| response_timestamp | FLOAT | Evet | ms | Null ise yanıt yok |
| correct | BOOLEAN | Hayır | — | go'da yanıt=doğru, no_go'da yanıtsızlık=doğru |
| error_type | TEXT | Evet | "omission"/"commission"/null | — |
| valid | BOOLEAN | Hayır | — | — |

## task_switch_trials
| Kolon | Tip | Nullable | Birim | Açıklama |
|---|---|---|---|---|
| trial_id | TEXT (PK) | Hayır | UUID | — |
| session_id | TEXT (FK) | Hayır | — | — |
| rule_type | TEXT | Hayır | "color"/"shape" | O trial'da uygulanan kural |
| is_switch_trial | BOOLEAN | Hayır | — | Bir önceki trial'a göre kural değişti mi |
| reaction_time | FLOAT | Evet | ms | — |
| correct | BOOLEAN | Hayır | — | — |
| valid | BOOLEAN | Hayır | — | — |

## analysis_runs
| Kolon | Tip | Nullable | Açıklama |
|---|---|---|---|
| run_id | TEXT (PK) | Hayır | UUID |
| dataset_version | TEXT | Hayır | Veri setinin hash/versiyonu |
| code_version | TEXT | Hayır | Git commit hash |
| timestamp | TIMESTAMP | Hayır | — |
| parameters_json | TEXT (JSON) | Evet | Kullanılan tüm parametreler (outlier eşikleri vb.) |

## model_runs
| Kolon | Tip | Nullable | Açıklama |
|---|---|---|---|
| run_id | TEXT (PK) | Hayır | UUID |
| analysis_run_id | TEXT (FK) | Hayır | — |
| model_type | TEXT | Hayır | "ridge"/"random_forest" vb. |
| cv_strategy | TEXT | Hayır | "GroupKFold(n=5)" gibi açık string |
| random_seed | INTEGER | Hayır | Reprodüksiyon için |
| metrics_json | TEXT (JSON) | Hayır | MAE, RMSE, R², CI'ler |

## Genel Kurallar
- Hiçbir tabloda ad, telefon, e-posta, TC kimlik no alanı YOKTUR.
- `is_demo=true` olan hiçbir satır "araştırma sonucu" olarak dashboard'da
  gösterilemez; UI seviyesinde bu ayrım zorunlu kılınmalıdır.
