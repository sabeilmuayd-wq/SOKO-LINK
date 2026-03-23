import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import re

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

# ==================== معالجة الأوامر ====================
def extract_number(text):
    """استخراج الرقم من النص"""
    # البحث عن أرقام
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    return None

def extract_product(text):
    """استخراج اسم المنتج من النص"""
    text = text.lower()
    
    if "موز" in text or "banana" in text:
        return "🍌 موز"
    elif "ذرة" in text or "maize" in text or "corn" in text:
        return "🌽 ذرة"
    elif "فول" in text or "beans" in text or "bean" in text:
        return "🥜 فول"
    
    return None

def process_command(command):
    """معالجة الأمر"""
    command = command.lower().strip()
    
    # إضافة منتج
    if "أضف" in command or "add" in command:
        product = extract_product(command)
        price = extract_number(command)
        
        # البحث عن كمية ثانية إذا وجدت
        numbers = re.findall(r'\d+', command)
        quantity = 100  # افتراضي
        if len(numbers) >= 2:
            quantity = int(numbers[1])
        
        if product and price:
            return {
                "action": "add",
                "product": product,
                "price": price,
                "quantity": quantity
            }
    
    # بحث
    elif "بحث" in command or "search" in command:
        product = extract_product(command)
        if product:
            return {"action": "search", "product": product}
    
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
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #2ecc71;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان ====================
st.markdown("""
<div class='main-header'>
    <h1>🌽 SOKO LINK 🎤</h1>
    <h3>Farmers Market | تحدث وأضف منتجك</h3>
    <p>🎤 اكتب الأمر وجربه: <strong>"أضف موز 2000"</strong> أو <strong>"add bananas 2000"</strong></p>
</div>
""", unsafe_allow_html=True)

# ==================== المدخل الصوتي (كتابة) ====================
st.markdown("### 🎤 تحدث أو اكتب")

voice_input = st.text_input("أكتب الأمر هنا:", placeholder="مثال: أضف موز 2000 أو add bananas 2000")

if voice_input:
    result = process_command(voice_input)
    
    if result["action"] == "add":
        # حفظ المنتج
        product = {
            "id": str(uuid.uuid4())[:8],
            "product": result["product"],
            "price": result["price"],
            "quantity": result["quantity"],
            "farmer": st.session_state.get("farmer_name", "مزارع"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_product(product)
        
        st.markdown(f"""
        <div class='success-box'>
            ✅ <strong>تم إضافة المنتج!</strong><br>
            📦 {result['product']} - {result['quantity']} كيلو<br>
            💰 {result['price']:,} شلن/كيلو
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        
    elif result["action"] == "search":
        products = load_products()
        found = [p for p in products if result["product"] in p["product"]]
        
        if found:
            st.success(f"🔍 تم العثور على {len(found)} منتج")
            for p in found[-3:]:
                st.markdown(f"""
                <div class='product-card'>
                    <strong>{p['product']}</strong><br>
                    💰 {p['price']:,} شلن/كيلو | 📦 {p['quantity']} كيلو<br>
                    👨‍🌾 {p['farmer']} | 📅 {p['date']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"🔍 لا توجد منتجات من {result['product']}")
    
    elif result["action"] == "unknown":
        st.warning("🤔 لم أفهم الأمر. جرب:\n- 'أضف موز 2000'\n- 'add bananas 2000'\n- 'بحث موز'")

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
        st.rerun()

# ==================== عرض المنتجات ====================
st.markdown("### 📋 المنتجات المتاحة")

products = load_products()

if products:
    for p in products[-5:]:
        st.markdown(f"""
        <div class='product-card'>
            <strong>{p['product']}</strong><br>
            💰 السعر: {p['price']:,} شلن/كيلو<br>
            📦 الكمية: {p['quantity']} كيلو<br>
            👨‍🌾 {p['farmer']} | 📅 {p['date']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 لا توجد منتجات بعد. جرب إضافة منتج")

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("### 🎤 الأوامر الصوتية")
    st.markdown("""
    **اكتب أحد هذه الأوامر:**
    
    **بالعربية:**
    - `أضف موز 2000`
    - `أضف ذرة 1500`
    - `أضف فول 3000 50`
    - `بحث موز`
    
    **In English:**
    - `add bananas 2000`
    - `add maize 1500`
    - `add beans 3000 50`
    - `search bananas`
    """)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    st.metric("إجمالي المنتجات", len(products))
    
    # اسم المزارع
    farmer_name = st.text_input("👨‍🌾 اسم المزارع", value=st.session_state.get("farmer_name", ""))
    if farmer_name:
        st.session_state.farmer_name = farmer_name
