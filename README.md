# 🎸 TONEX ONE AI Chatbot

**Ders:** MTH409 - Üretken Yapay Zeka ile Chatbot Geliştirme Temelleri  
**Öğrenci:** İbrahim Berk BALCI  
**No:** 090230737
---

## 📖 Proje Hakkında

Bu proje, **IK Multimedia TONEX ONE** gitar pedalı için geliştirilmiş, yapay zeka destekli bir teknik destek asistanıdır. 

Projenin temel amacı, **RAG** mimarisini kullanarak, Büyük Dil Modellerinin (LLM) teknik dokümanlara sadık kalarak cevap vermesini sağlamak ve "halüsinasyon" (yanlış bilgi üretme) problemini ortadan kaldırmaktır.

Video Demosu Linki:
https://drive.google.com/drive/folders/18-Wef_BaIezZsO3g1YJPK1LnV65wZcxk

---

## 🎛️ Cihaz Hakkında: Nedir Bu "TONEX ONE"?

**TONEX ONE**, IK Multimedia tarafından geliştirilen devrim niteliğinde mini bir GİTAR PEDALIdır.

* **Ne Yapar?** Gerçek gitar amfilerinin ve kabinlerinin birebir dijital kopyalarını (Tone Models) içinde saklar ve çalar.
* **Neden Chatbot Gerekiyor?** Cihazın üzerinde bir ekran yoktur ve sadece 3 küçük düğme bulunur. *Global Ayarlar, Noise Gate, EQ ayarları veya Resetleme* gibi işlemler karmaşık tuş kombinasyonları ve renkli LED kodları ile yapılır.
* **Çözüm:** Bu proje, kullanıcıların "Kırmızı ışık yanıp sönüyor, ne demek?" veya "Reset nasıl atarım?" gibi sorularına saniyeler içinde kullanım kılavuzundan (Manual) doğru cevabı verir.

---

## 🌟 Özellikler
* **Çoklu Model Desteği:** Kullanıcı, **Google Gemini 2.5 Flash** veya **Meta Llama 3.1 8B** (Groq) modelleri arasında seçim yapabilir.
* **RAG Mimarisi:** Cevaplar, PDF dokümanından (User Manual) üretilir.
* **Akıllı Red (Negative Constraint):** Dokümanda olmayan özellikler (örn. Bluetooth, Pil) sorulduğunda, model uydurmak yerine "Dokümanda bu özellikten bahsedilmemektedir" şeklinde yanıt verir.


## Notlar
* Modelin performansını test etmek için sorulan sorular, test-data dosyasında manuel_test_sablonu adlı excel dosyasında görülebilir.
---

## 📊 Performans ve Test Sonuçları

Proje, teknik soruları yanıtlama başarısı açısından **16 soruluk** bir test seti ile değerlendirilmiştir. Elde edilen metrikler, RAG sisteminin başarısını kanıtlamaktadır:

| Metrik | Gemini 2.5 Flash | Llama 3.1 8B |
| :--- | :---: | :---: |
| **Toplam Soru** | 16 | 16 |
| **Doğru Cevap (TP)** | 15 | 14 |
| **Yanlış/Eksik (FN/FP)**| 1 | 2 |
| **Precision** | **1.00** | 0.93 |
| **Recall** | **0.94** | 0.88 |
| **F1 Score** | **0.97** | 0.90 |

*Sonuç: Gemini 2.5 Flash modeli, F1 skoru (0.97) ve doğruluk oranı ile teknik destek görevlerinde daha yüksek performans göstermiştir.*

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları takip ediniz.

### 1. Gereksinimler
* Python 3.10 veya üzeri
* Google AI Studio API Anahtarı
* Groq API Anahtarı (Opsiyonel, Llama modeli için)

### 2. Klasör Yapısı
Projenin düzgün çalışması için dosyaların şu yapıda olduğundan emin olun:

```text
PROJE_ANA_DIZINI/
├── app/
│   └── chatbotv4.py                # Ana uygulama dosyası
│---TONEX_ONE_User_Manual_English.pdf  # RAG için kaynak doküman
├── requirements.txt                # Gerekli kütüphaneler
├── README.md                       # Proje dokümantasyonu
└── .env                            # API anahtarları (Gizli dosya)
```

### 3. Kurulum Adımları

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/tonex-one-chatbot.git](https://github.com/KULLANICI_ADINIZ/tonex-one-chatbot.git)
    cd tonex-one-chatbot
    ```

2.  **Sanal Ortam Oluşturun (Önerilen):**
    ```bash
    python -m venv venv
    # Windows için:
    venv\Scripts\activate
    # Mac/Linux için:
    source venv/bin/activate
    ```

3.  **Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Anahtarlarını Ayarlayın:**
    * Ana dizinde `.env` adında bir dosya oluşturun.
    * İçine aşağıdaki bilgileri girin:
    ```env
    GOOGLE_API_KEY=senin_google_api_keyin
    GROQ_API_KEY=senin_groq_api_keyin
    ```

### 4. Uygulamayı Başlatma

Terminalde ana dizindeyken şu komutu çalıştırın:
```bash
streamlit run app/chatbotv4.py
```
