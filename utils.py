import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image

# .env dosyasını yükle
load_dotenv()

def get_client():
    """
    OpenAI istemcisini başlatır ve döner.
    API anahtarı yoksa None dönebilir veya hata fırlatabilir,
    ancak bu kontrolü app.py'ye bırakıyoruz.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def generate_ideas():
    """
    Sigorta acentesi için 3 farklı Instagram post konusu fikri üretir.
    """
    client = get_client()
    if not client:
        return ["Hata: API anahtarı bulunamadı."]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen yaratıcı bir sosyal medya uzmanısın. Bir sigorta acentesi için çalışıyorsun."},
                {"role": "user", "content": "Bir sigorta acentesi için Instagram'da paylaşılabilecek, ilgi çekici ve etkileşim alabilecek 3 farklı günlük konu başlığı öner. Sadece başlıkları listele, numaralandırarak ver (1., 2., 3. gibi). Ekstra açıklama yapma."}
            ],
            temperature=0.8,
            max_tokens=150
        )
        ideas_text = response.choices[0].message.content.strip()
        # Metni satırlara bölüp temizleyelim
        ideas = [line.strip() for line in ideas_text.split('\n') if line.strip()]
        return ideas
    except Exception as e:
        return [f"Hata oluştu: {str(e)}"]

def generate_content(topic):
    """
    Seçilen konu için Instagram post metni (caption) üretir.
    """
    client = get_client()
    if not client:
        return "Hata: API anahtarı bulunamadı."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir metin yazarısın. Sigorta acentesi için samimi ve güven veren bir dil kullanıyorsun."},
                {"role": "user", "content": f"'{topic}' konusu hakkında bir Instagram post metni yaz. \n\n- Samimi ve bilgilendirici olsun.\n- Emojiler kullan.\n- En alta popüler sigorta hashtag'leri ekle.\n- Türkçe olsun."}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"İçerik oluşturulurken hata oluştu: {str(e)}"

def generate_image(topic):
    """
    Seçilen konu için DALL-E 3 ile görsel oluşturur.
    Geriye görselin URL'sini döner.
    """
    client = get_client()
    if not client:
        print("Hata: API anahtarı bulunamadı.")
        return None

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A professional and creative instagram post image for an insurance agency about: {topic}. High quality, modern style, bright colors, no text on image.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Görsel hatası: {e}")
        return None

def download_image(image_url):
    """
    URL'deki resmi indirip PIL Image objesi olarak döner.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        print(f"İndirme hatası: {e}")
        return None
