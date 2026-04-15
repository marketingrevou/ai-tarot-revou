# AI Tarot — On-Screen Copy

---

## Screen 1 — Intention (Halaman Utama)

| Elemen | Copy |
|--------|------|
| Badge atas | AI TAROT |
| Subtitle | Ramalan Era AI |
| Headline | Era AI nyiapin apa buat kamu? 🔮 |
| Subheadline | Yuk intip nasib karirmu di zaman serba AI ini! |
| Label input | Profesimu |
| Placeholder input | Kamu kerja sebagai apa? |
| Error message | Isi dulu dong profesimu biar bisa mulai! 😅 |
| Tombol CTA | Mulai Ramalan! |

---

## Screen 2 — Pilih Kartu

| Elemen | Copy |
|--------|------|
| Badge header | AI Tarot |
| Headline | Pilih 3 kartu untuk ungkap jalanmu ✨ |
| Counter (kosong) | 0 dari 3 dipilih |
| Counter (terisi) | 1 dari 3 dipilih / 2 dari 3 dipilih / 3 dari 3 dipilih |
| Tombol (terkunci) | Lihat Interpretasi 🔒 |
| Tombol (aktif) | Lihat Interpretasi ✨ |
| Footer hint | Percaya aja sama instingmu, pilih yang terasa bener! 🃏 |

---

## Screen 3 — Reveal Kartu

| Elemen | Copy |
|--------|------|
| Label posisi kiri | Masa Lalu |
| Label posisi tengah | Sekarang |
| Label posisi kanan | Masa Depan |
| Summary (dinamis) | "[Kartu 1] di masa lalu, [Kartu 2] di masa kini, [Kartu 3] di masa depan." |
| Deskripsi (dinamis) | Kartu-kartumu udah bicara! [Kartu 1] membentuk fondasimu, [Kartu 2] jadi energi yang nemenin kamu sekarang, dan [Kartu 3] menerangi jalan ke depan. Yuk minta AI baca ramalanmu secara lengkap! 🌟 |
| Tombol CTA | BACA MASA DEPANKU! 🚀 |

---

## Screen 4 — AI Reading

| Elemen | Copy |
|--------|------|
| Badge header | AI Tarot |
| Judul section | Ramalanmu 🔮 |
| Loading state | Kartu-kartunya lagi ngomong… sabar ya! ✨ |
| Isi ramalan | *(digenerate oleh AI — 3 paragraf, dinamis)* |
| Tombol reset | Cabut Lagi! 🃏 |
| Error utama | Aduh, gagal ngambil ramalan nih 😓 |
| Error hint | Pastiin servernya udah jalan ya: `python server.py` |

---

## Nama Kartu (12 Kartu)

| # | Nama Kartu |
|---|-----------|
| 1 | The Automation |
| 2 | The Collaborator |
| 3 | The Disruptor |
| 4 | The Architect |
| 5 | The Learner |
| 6 | The Pioneer |
| 7 | The Connector |
| 8 | The Creator |
| 9 | The Strategist |
| 10 | The Innovator |
| 11 | The Guardian |
| 12 | The Visionary |

---

## AI Prompt (dikirim ke Claude)

```
Kamu adalah pembaca tarot era AI yang mistis tapi asik dan nyambung.
Penanya adalah seorang [PROFESI].

Mereka menarik tiga kartu:
- Masa Lalu: [KARTU 1]
- Sekarang: [KARTU 2]
- Masa Depan: [KARTU 3]

Berikan ramalan yang dalam, mistis, tapi juga praktis tentang perjalanan
karir mereka di era kecerdasan buatan.

Tulis tepat 3 paragraf yang dipisahkan dengan baris kosong. Gunakan bahasa
Indonesia yang santai, fun, dan casual — kayak ngobrol sama teman, tapi
tetap terasa magis dan bermakna. Sesuaikan dengan profesi dan kartu yang
ditarik. Jangan pakai header, bullet point, atau format markdown — cukup
tulisan biasa saja.
```
