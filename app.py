import streamlit as st
import os
from dotenv import load_dotenv
import utils
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(
    page_title="Sigorta Acentesi - Sosyal Medya Asistanı",
    page_icon="🛡️",
    layout="centered"
)

# .env yükle
load_dotenv()

# Başlık
st.title("🛡️ Sigorta Acentesi İçerik Oluşturucu")
st.markdown("Yapay zeka desteği ile günlük Instagram içeriklerinizi saniyeler içinde hazırlayın.")

# API Key Kontrolü
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ OpenAI API anahtarı bulunamadı! Lütfen `.env` dosyasını kontrol edin.")
    st.stop()

# --- Session State Başlatma ---
if "ideas" not in st.session_state:
    st.session_state.ideas = []
if "selected_idea" not in st.session_state:
    st.session_state.selected_idea = None
if "generated_caption" not in st.session_state:
    st.session_state.generated_caption = None
if "generated_image_url" not in st.session_state:
    st.session_state.generated_image_url = None

# --- Bölüm 1: Konu Fikirleri ---
st.header("1. Konu Belirleme")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("💡 Yeni Konu Fikirleri Bul", use_container_width=True):
        with st.spinner("Yapay zeka sigorta trendlerini analiz ediyor..."):
            ideas = utils.generate_ideas()
            if ideas:
                st.session_state.ideas = ideas
                # Yeni fikirler gelince eski seçimleri temizle
                st.session_state.selected_idea = None
                st.session_state.generated_caption = None
                st.session_state.generated_image_url = None
                st.success("Fikirler bulundu!")
            else:
                st.error("Fikir üretilemedi. Lütfen tekrar deneyin.")

# Fikirleri Listeleme ve Seçim
if st.session_state.ideas:
    st.write("Aşağıdaki fikirlerden birini seçin:")

    selected = st.radio(
        "Günün Konusu:",
        st.session_state.ideas,
        index=0
    )

    # Seçim değiştiyse state güncelle
    if selected != st.session_state.selected_idea:
        st.session_state.selected_idea = selected
        # Yeni konu seçilince eski içeriği temizle
        st.session_state.generated_caption = None
        st.session_state.generated_image_url = None

    st.info(f"Seçilen Konu: **{selected}**")
else:
    st.info("Henüz bir konu fikri üretilmedi. Başlamak için butona tıklayın.")

# --- Bölüm 2: İçerik Oluşturma ---
if st.session_state.selected_idea:
    st.divider()
    st.header("2. İçerik Oluşturma")

    if st.button("✨ Metin ve Görsel Oluştur", use_container_width=True):
        with st.spinner("Yapay zeka çalışıyor... (Bu işlem 30-60 saniye sürebilir)"):
            # Metin oluştur
            caption = utils.generate_content(st.session_state.selected_idea)
            st.session_state.generated_caption = caption

            # Görsel oluştur
            image_url = utils.generate_image(st.session_state.selected_idea)
            st.session_state.generated_image_url = image_url

            if caption and image_url:
                st.success("İçerik başarıyla oluşturuldu!")
            else:
                st.error("Bir şeyler ters gitti. Lütfen tekrar deneyin.")

# --- Bölüm 3: Önizleme ve Kaydetme ---
if st.session_state.generated_caption and st.session_state.generated_image_url:
    st.divider()
    st.header("3. Önizleme ve Kayıt")

    col_img, col_txt = st.columns([1, 1])

    with col_img:
        st.image(st.session_state.generated_image_url, caption="Oluşturulan Görsel", use_column_width=True)

    with col_txt:
        st.text_area("Instagram Metni", value=st.session_state.generated_caption, height=400)

    # Kaydetme Butonu
    st.subheader("💾 Bilgisayara Kaydet")
    if st.button("Dosyaları Kaydet"):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Dosya isimlerini güvenli hale getir (boşlukları _ yap vs)
            safe_topic = "".join([c if c.isalnum() else "_" for c in st.session_state.selected_idea])[:20]
            base_filename = f"{timestamp}_{safe_topic}"

            save_dir = "olusturulan_icerikler"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Metni kaydet
            txt_path = os.path.join(save_dir, f"{base_filename}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(st.session_state.generated_caption)

            # Resmi indir ve kaydet
            img_path = os.path.join(save_dir, f"{base_filename}.png")
            img = utils.download_image(st.session_state.generated_image_url)
            if img:
                img.save(img_path)
                st.success(f"Dosyalar kaydedildi!\n\n📂 Konum: `{os.path.abspath(save_dir)}`")
                st.success(f"📝 Metin: `{txt_path}`")
                st.success(f"🖼️ Resim: `{img_path}`")
            else:
                st.error("Resim indirilemedi.")

        except Exception as e:
            st.error(f"Kaydetme sırasında hata: {e}")
