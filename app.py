import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import threading

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - Voice Edition",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== نظام الصوت ====================
def speak(text, language="en"):
    """تحويل النص إلى كلام"""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def listen():
    """الاستماع إلى الصوت وتحويله إلى نص"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 استمع... تحدث الآن")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en")
            return text.lower()
        except sr.WaitTimeoutError:
            st.warning("لم أسمع شيئاً")
            return ""
        except sr.UnknownValueError:
            st.warning("لم أفهم ما قلته")
            return ""
        except:
            return ""

# ==================== الأوامر الصوتية ====================
def process_voice_command(command):
    """معالجة الأوامر الصوتية"""
    command = command.lower()
    
    # إضافة منتج
    if "add" in command or "أضف" in command:
        # استخراج المعلومات
        words = command.split()
        product = None
        price = None
        quantity = None
        
        for i, word in enumerate(words):
            if word in ["banana", "موز", "bananas"]:
                product = "🍌 موز"
            elif word in ["maize", "ذرة", "corn"]:
                product = "🌽 ذرة"
            elif word in ["beans", "فول", "bean"]:
                product = "🥜 فول"
            elif word.isdigit():
                if price is None:
                    price = int(word)
                else:
                    quantity = int(word)
        
        if product and price:
            return {
                "action": "add_product",
                "product": product,
                "price": price,
                "quantity": quantity or 100
            }
    
    # بحث
    elif "search" in command or "بحث" in command:
        for word in ["banana", "موز", "maize", "ذرة", "beans", "فول"]:
            if word in command:
                return {"action": "search", "product": word}
    
    return {"action": "unknown"}

# ==================== تخزين البيانات ====================
DATA_FILE = "products.json"

def load_products():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_product(product):
    products = load_products()
    products.append(product)
    with open(DATA_FILE, 'w') as f:
        json.dump(products, f, indent=2)

# ==================== واجهة التطبيق ====================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    .voice-button {
        background-color: #3498db;
        color: white;
        font-size: 1.5rem;
        padding: 1rem;
        border-radius: 50px;
        text-align: center;
        cursor: pointer;
        margin: 1rem 0;
    }
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #2ecc71;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان ====================
st.markdown("""
<div class='main-header'>
    <h1>🌽 SOKO LINK 🎤</h1>
    <h3>Farmers Market | تحدث وأضف منتجك</h3>
    <p>🎤 Speak to add products | تكلم لإضافة المنتجات</p>
</div>
""", unsafe_allow_html=True)

# ==================== زر الصوت ====================
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🎤 اضغط وتحدث", use_container_width=True):
        st.session_state.voice_mode = True
        st.rerun()

# ==================== معالجة الصوت ====================
if st.session_state.voice_mode:
    st.markdown("### 🎤 استمع...")
    
    with st.spinner("جاري الاستماع..."):
        command = listen()
        
        if command:
            st.success(f"📝 سمعت: **{command}**")
            
            result = process_voice_command(command)
            
            if result["action"] == "add_product":
                product = {
                    "id": str(uuid.uuid4())[:8],
                    "product": result["product"],
                    "price": result["price"],
                    "quantity": result["quantity"],
                    "farmer": "Voice Farmer",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                save_product(product)
                st.success(f"✅ تم إضافة {result['product']} بسعر {result['price']} شلن!")
                st.balloons()
                
                # إشعار صوتي
                speak(f"Added {result['product']} at {result['price']} shillings")
                
            elif result["action"] == "search":
                st.info(f"🔍 جاري البحث عن {result['product']}...")
                speak(f"Searching for {result['product']}")
                
            else:
                st.warning("🤔 لم أفهم الأمر. جرب: 'add bananas 2000' أو 'search maize'")
                speak("I didn't understand. Try: add bananas 2000")
    
    if st.button("🔙 إلغاء", use_container_width=True):
        st.session_state.voice_mode = False
        st.rerun()

# ==================== إضافة منتج يدوي ====================
with st.expander("✍️ إضافة منتج يدوياً"):
    col1, col2 = st.columns(2)
    with col1:
        product = st.selectbox("المنتج", ["🍌 موز", "🌽 ذرة", "🥜 فول"])
        price = st.number_input("السعر (شلن)", min_value=100, step=500, value=2000)
    with col2:
        quantity = st.number_input("الكمية (كيلو)", min_value=1, value=100)
    
    if st.button("➕ إضافة منتج"):
        product_data = {
            "id": str(uuid.uuid4())[:8],
            "product": product,
            "price": price,
            "quantity": quantity,
            "farmer": st.session_state.get("farmer_name", "مزارع"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_product(product_data)
        st.success(f"✅ تم إضافة {product}")

# ==================== عرض المنتجات ====================
st.markdown("### 📋 المنتجات المتاحة")

products = load_products()

if products:
    for p in products[-5:]:  # آخر 5 منتجات
        st.markdown(f"""
        <div class='product-card'>
            <h3>{p['product']}</h3>
            <p>💰 السعر: {p['price']:,} شلن/كيلو</p>
            <p>📦 الكمية: {p['quantity']} كيلو</p>
            <p>👨‍🌾 {p['farmer']} | 📅 {p['date']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("لا توجد منتجات بعد. جرب إضافة منتج بالصوت أو يدوياً")

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("### 🎤 الأوامر الصوتية")
    st.markdown("""
    **بالعربية:**
    - "أضف موز 2000"
    - "أضف ذرة 1500 100"
    - "بحث موز"
    
    **In English:**
    - "add bananas 2000"
    - "add maize 1500 100"
    - "search bananas"
    """)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    st.metric("إجمالي المنتجات", len(products))
