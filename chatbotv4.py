import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

# Ortam değişkenlerini yükle (.env)
load_dotenv()

# Sayfa Ayarları
st.set_page_config(page_title="TONEX ONE AI", page_icon="🎸", layout="wide")

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Model Ayarları")
    st.markdown("LLM Modelini Seçiniz:")
    
    # Model Seçimi (Gemini vs Llama 3.1)
    model_choice = st.radio(
        "Aktif Model:",
        ("Gemini 2.5 Flash (Google)", "Llama 3.1 8B (Groq)"),
        index=0
    )
    
    st.info(f"Seçili Model: **{model_choice}**")
    
    # API Key Kontrolü
    if "Gemini" in model_choice and not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ GOOGLE_API_KEY eksik!")
    
    if "Llama" in model_choice and not os.getenv("GROQ_API_KEY"):
        st.error("⚠️ GROQ_API_KEY eksik! (.env dosyasını kontrol et)")

    st.markdown("---")
    st.caption("Eğitim Verisi: TONEX ONE User Manual")

# Ana Başlık
st.title("🎸 TONEX ONE - Teknik Destek Asistanı")
# Mevcut modeli başlık altında da gösterelim
st.markdown(f"Currently running on: **{model_choice}**")

# --- Vektör Veritabanı (Sabit - Gemini Embeddings) ---
@st.cache_resource
def setup_vector_store():
    if not os.path.exists("TONEX_ONE_User_Manual_English.pdf"):
        st.error("PDF dosyası bulunamadı! Lütfen dosya ismini kontrol edin.")
        return None
        
    loader = PyPDFLoader("TONEX_ONE_User_Manual_English.pdf")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(data)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        task_batch_limit=16 
    )
    
    vector_db = Chroma.from_documents(docs, embeddings)
    return vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

retriever = setup_vector_store()

# --- MODEL SEÇİM MANTIĞI ---
def get_llm(choice):
    # 1. Google Gemini 2.5 Flash
    if "Gemini" in choice:
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.3,
            max_tokens=500
        )
    
    # 2. Llama 3.1 8B (Groq Üzerinden)
    elif "Llama" in choice:
        return ChatOpenAI(
            model="llama-3.1-8b-instant",
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
            temperature=0.3,
            max_tokens=500
        )
    else:
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Seçilen modeli yükle
try:
    llm = get_llm(model_choice)
except Exception as e:
    st.error(f"Model yüklenirken hata oluştu: {e}")
    st.stop()

# --- SYSTEM PROMPT (Final: Akıllı, Güvenli ve Formatlı) ---
system_prompt = (
    "You are an expert technical support assistant for the IK Multimedia TONEX ONE pedal. "
    "Your task is to answer user questions strictly based on the provided context."
    
    "\n\n--- INSTRUCTIONS ---"
    "\n1. PRIORITY: Always search the context first. If the answer is found, explain it clearly."
    "\n2. FORMATTING: Use **bullet points** for lists and **numbered steps** for procedures to make the answer easy to read."
    "\n3. ABSENT FEATURES: If the user asks about a specific hardware feature (e.g., Bluetooth, Battery, WiFi) "
    "and the context is silent about it, respond: 'The manual does not mention [feature], which implies it is not supported.'"
    "\n4. UNKNOWN INFO: For other questions not found in the context, say: 'I cannot answer that based on the provided manual.'"
    "\n5. LANGUAGE: Respond in ENGLISH only."
    
    "\n\n--- INTENT HANDLING ---"
    "\n- If user says 'Hi', 'Hello', reply: 'Hello! I am your TONEX ONE assistant. How can I help you rock today?'"
    "\n- If user says 'Bye', reply: 'Goodbye! Keep shredding with your TONEX ONE!'"
    
    "\n\n--- CONTEXT ---"
    "\n{context}"
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{input}"),
    ]
)

# Zincirleri Oluşturma
if retriever:
    question_answering_chain = create_stuff_documents_chain(llm, prompt_template)
    rag_chain = create_retrieval_chain(retriever, question_answering_chain)
else:
    st.stop()

# --- SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# GEÇMİŞ MESAJLARI GÖSTER (Revize Edildi)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Eğer mesaj asistandan geliyorsa ve model bilgisi varsa, onu göster
        if message["role"] == "assistant" and "model" in message:
            st.caption(f"⚙️ Model: {message['model']}")
        
        st.markdown(message["content"])

# KULLANICI GİRİŞİ
if query := st.chat_input("Ask a question about TONEX ONE..."):
    
    # Kullanıcı mesajını kaydet
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner(f"Analyzing with {model_choice}..."):
        try:
            response = rag_chain.invoke({"input": query})
            answer = response["answer"]
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}. Lütfen API anahtarlarını kontrol edin."

    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer,
        "model": model_choice  # Hangi modelin cevap verdiğini kaydediyoruz
    })
    
    with st.chat_message("assistant"):
        st.caption(f"⚙️ Model: {model_choice}") # Anlık gösterim
        st.markdown(answer)