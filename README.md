# SPEXRON ENGINE v2.0

Cheat Engine benzeri yüksek performanslı bellek tarayıcısı.

## Nasıl Çalıştırılır?

**`run.bat`** dosyasına çift tıkla → program açılır.

---

## Dosya Yapısı

```
📂 Proje Dizini
│
├── run.bat                  ← Buraya çift tıkla, program açılır
│
├── spexron_main.py          ← Giriş noktası (run.bat bunu çalıştırır)
├── spexron_gui.py           ← Ana pencere ve tüm UI mantığı
├── spexron_scanner.py       ← 64-bit bellek tarama motoru (Windows API)
├── spexron_processpicker.py ← Cheat Engine tarzı süreç seçim penceresi
├── spexron_localization.py  ← TR/EN tam dil paketi
│
└── SPEXRON (1).png          ← Logo dosyası (opsiyonel)
```

## Özellikler

- ✅ **Process Picker** — Tüm çalışan süreçlere bağlanabilir (sadece Warband değil)
- ✅ **Otomatik bağlanma YOK** — Program açılınca boş gelir, kendin seçersin
- ✅ **64-bit VirtualQueryEx taraması** — Gerçek adres uzayı taraması
- ✅ **9 farklı scan tipi** — Exact, Bigger, Smaller, Between, Unknown, Increased, Decreased, Changed, Unchanged
- ✅ **6 veri tipi** — 1/2/4/8 Byte, Float, Double
- ✅ **Cheat Engine tarzı değer editörü** — Çift tıkla → pencere açılır, Write Once / Apply+Freeze seçenekleri
- ✅ **Sağ tık menüsü** — Change Value, Freeze, Unfreeze, Edit Desc, Edit Type, Remove
- ✅ **Freeze (Dondurma) döngüsü** — Kilitli adresler 100ms'de bir yazılır
- ✅ **TR / EN** — Anında dil değiştirme
- ✅ **Gold (#FFD700) tema** — Premium dark mode arayüz
