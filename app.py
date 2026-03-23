import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import requests

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - Voice Edition",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

# ==================== تحويل الصوت إلى نص باستخدام API مجاني ====================
def transcribe_audio(audio_file):
    """إرسال الملف إلى API مجاني للتعرف على الكلام"""
    try:
        # استخدام API مجاني من Hugging Face (بديل)
        # أو استخدام خدمة تحويل الصوت إلى نص مدمجة
        return "add bananas 2000"  # مؤقتاً، نعيد أمراً وهمياً
    except:
        return ""

# ==================== معالجة الأوامر الصوتية ====================
def process_voice_command(command):
    """معالجة الأوامر الصوتية"""
    command = command.lower()
    
    # إضافة منتج
    if "add" in command or "أضف" in command:
        words = command.split()
        product = None
        price = None
        quantity = None
        
        # محاولة استخراج المنتج
        for word in words:
            if word in ["banana", "موز", "bananas"]:
                product = "🍌 موز"
            elif word in ["maize", "ذرة", "corn"]:
                product = "🌽 ذرة"
            elif word in ["beans", "فول", "bean"]:
                product = "🥜 فول"
            # محاولة استخراج السعر (أرقام)
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
    <p>🎤 اضغط الزر وتحدث (جرب: "أضف موز 2000")</p>
</div>
""", unsafe_allow_html=True)

# ==================== نموذج إدخال النص (بديل الصوت) ====================
st.markdown("### 🎤 تحدث أو اكتب")

# خيار: إدخال نصي (حتى يعمل التطبيق بدون ميكروفون)
voice_text = st.text_input("أو اكتب الأمر هنا:", placeholder="مثال: أضف موز 2000 أو add bananas 2000")

if voice_text:
    result = process_voice_command(voice_text)
    
    if result["action"] == "add_product":
        product = {
            "id": str(uuid.uuid4())[:8],
            "product": result["product"],
            "price": result["price"],
            "quantity": result["quantity"],
            "farmer": st.session_state.get("farmer_name", "مزارع"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_product(product)
        st.success(f"✅ تم إضافة {result['product']} بسعر {result['price']:,} شلن!")
        st.balloons()
        
    elif result["action"] == "search":
        st.info(f"🔍 جاري البحث عن {result['product']}...")
        
    elif result["action"] == "unknown":
        st.warning("🤔 لم أفهم الأمر. جرب: 'أضف موز 2000' أو 'add bananas 2000'")

# ==================== زر إضافة منتج يدوي ====================
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
    for p in products[-5:]:
        st.markdown(f"""
        <div class='product-card'>
            <h3>{p['product']}</h3>
            <p>💰 السعر: {p['price']:,} شلن/كيلو</p>
            <p>📦 الكمية: {p['quantity']} كيلو</p>
            <p>👨‍🌾 {p['farmer']} | 📅 {p['date']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("لا توجد منتجات بعد. جرب إضافة منتج")

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("### 🎤 الأوامر الصوتية (اكتبها)")
    st.markdown("""
    **بالعربية:**
    - `أضف موز 2000`
    - `أضف ذرة 1500 100`
    - `بحث موز`
    
    **In English:**
    - `add bananas 2000`
    - `add maize 1500 100`
    - `search bananas`
    """)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    st.metric("إجمالي المنتجات", len(products))
    
    # اسم المزارع
    farmer_name = st.text_input("👨‍🌾 اسم المزارع", value=st.session_state.get("farmer_name", ""))
    if farmer_name:
        st.session_state.farmer_name = farmer_name
