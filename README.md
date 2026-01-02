# 🎸 TONEX ONE AI Assistant (RAG Chatbot)

**Ders:** MTH409 - Üretken Yapay Zeka ile Chatbot Geliştirme Temelleri  
**Öğrenci:** İbrahim Berk BALCI  

---

## 📖 Proje Hakkında

Bu proje, **IK Multimedia TONEX ONE** gitar pedalı için geliştirilmiş, yapay zeka destekli bir teknik destek asistanıdır. 

Projenin temel amacı, **RAG (Retrieval-Augmented Generation)** mimarisini kullanarak, Büyük Dil Modellerinin (LLM) teknik dokümanlara sadık kalarak cevap vermesini sağlamak ve "halüsinasyon" (yanlış bilgi üretme) problemini ortadan kaldırmaktır.

### 🌟 Özellikler
* **Çoklu Model Desteği:** Kullanıcı, **Google Gemini 2.5 Flash** veya **Meta Llama 3.1 8B** (Groq) modelleri arasında seçim yapabilir.
* **RAG Mimarisi:** Cevaplar, sadece yüklenen PDF dokümanından (User Manual) üretilir.
* **Akıllı Red (Negative Constraint):** Dokümanda olmayan özellikler (örn. Bluetooth, Pil) sorulduğunda, model uydurmak yerine "Dokümanda bu özellikten bahsedilmemektedir" şeklinde yanıt verir.
* **Kullanıcı Dostu Arayüz:** Streamlit ile geliştirilmiş modern bir sohbet arayüzü sunar.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları takip ediniz.

### 1. Gereksinimler
* Python 3.10 veya üzeri
* Google AI Studio API Anahtarı
* Groq API Anahtarı (Opsiyonel, Llama modeli için)

### 2. Kurulum Adımları

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

### 3. Uygulamayı Başlatma

Terminalde şu komutu çalıştırın:
```bash
streamlit run chatbotv4.py