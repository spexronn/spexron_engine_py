# SPEXRON ENGINE 

Windows platformu için geliştirilmiş, yüksek performanslı ve modern arayüze sahip 64-bit bellek tarama ve manipülasyon motorudur. Düşük seviyeli Windows API çağrıları ile doğrudan sistem süreçlerinin belleğe müdahale edebilen bu araç; veri analizi, tersine mühendislik ve yazılım hata ayıklama süreçleri için tasarlanmıştır.

---

## 🚀 Öne Çıkan Özellikler

* **Gelişmiş Süreç Yönetimi (Process Picker):** Çalışan tüm sistem süreçlerini PID ve yürütülebilir dosya adlarıyla birlikte listeleyen, dinamik arama ve filtreleme destekli süreç seçim arayüzü.
* **64-Bit Hibrit Bellek Tarama:** `VirtualQueryEx` ve `ReadProcessMemory` API'leri yardımıyla taahhüt edilmiş (`MEM_COMMIT`) bellek bölgelerini hızlı ve güvenli bir şekilde tarayabilen arama motoru.
* **Kapsamlı Arama Seçenekleri (9 Farklı Tarama Tipi):**
  * Exact Value (Tam Değer)
  * Bigger Than (Daha Büyük)
  * Smaller Than (Daha Küçük)
  * Value Between (Değer Aralığı)
  * Unknown Initial Value (Bilinmeyen Başlangıç Değeri)
  * Increased Value (Artmış Değer)
  * Decreased Value (Azalmış Değer)
  * Changed Value (Değişmiş Değer)
  * Unchanged Value (Değişmemiş Değer)
* **Desteklenen Veri Tipleri:** `1 Byte`, `2 Bytes`, `4 Bytes`, `8 Bytes`, `Float` ve `Double` formatlarında arama ve düzenleme desteği.
* **Dinamik Değer Dondurma (Freeze) Döngüsü:** Adreslerin değerlerini sürekli kılmak için özelleştirilebilir aralıkta (varsayılan 100ms) otomatik olarak belleğe yazma işlemi uygulayan dondurma sistemi.
* **Entegre Speedhack Kontrolü:** Cheat Engine tarzında, 0.0x ile 500.0x hız aralığında kaydırılabilir (slider) arayüz ile sürece dinamik hız manipülasyonu uygulama yeteneği.
* **Premium Dark Mode Arayüzü:** Özel çizim kaydırma çubukları (scrollbar), dinamik durum çubukları ve modern animasyonlu slider bileşenleri içeren temiz ve profesyonel arayüz tasarımı.
* **Çift Dilli Yapı:** Türkçe ve İngilizce dilleri arasında çalışma anında (runtime) dinamik geçiş desteği.

---

## 🛠️ Nasıl Çalıştırılır?

Projenin başlatılması son derece basittir. Python veya bağımlılıkların sisteminizde kurulu olmasına gerek kalmadan otomatik kurulum yapabilen başlatıcıyı kullanabilirsiniz:

1. Proje ana dizininde bulunan **`run.bat`** dosyasına çift tıklayın.
2. Başlatıcı betik, sisteminizde uygun Python sürümünü kontrol eder, gerekli kütüphaneleri otomatik olarak kurar ve **Spexron Engine**'i başlatır.

---

##  Teknik Detaylar ve Güvenlik

* **Direct OS Calls:** Bellek tarama işlemleri Python'ın `ctypes` kütüphanesi üzerinden doğrudan `kernel32.dll` çağrıları (Windows API) kullanılarak gerçekleştirilir.
* **Güvenli Yazma:** Yazma işlemleri sırasında bellek koruma bayrakları (`VirtualProtectEx`) geçici olarak yazılabilir hale getirilir (`PAGE_EXECUTE_READWRITE`) ve işlem tamamlandığında orijinal durumuna geri döndürülerek çökme veya yetki hatalarının önüne geçilir.
* **Asenkron Yapı:** Arama ve tarama süreçleri ana arayüzü kilitlememesi için bağımsız iş parçacıklarında (threads) yürütülür, bu sayede büyük bellek boyutlarında dahi stabil bir arayüz deneyimi sunulur.
