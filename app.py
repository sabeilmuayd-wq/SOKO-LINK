import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import re
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - Farmers Market",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== تخزين البيانات ====================
DATA_FOLDER = "soko_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PRODUCTS_FILE = os.path.join(DATA_FOLDER, "products.json")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
TRANSACTIONS_FILE = os.path.join(DATA_FOLDER, "transactions.json")
PRICES_FILE = os.path.join(DATA_FOLDER, "prices.json")

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# تهيئة بيانات تجريبية
if not os.path.exists(USERS_FILE):
    save_data(USERS_FILE, [
        {"id": "F001", "name": "علي حسن", "type": "farmer", "phone": "0777123456", "village": "Kiryandongo"},
        {"id": "F002", "name": "فاطمة محمد", "type": "farmer", "phone": "0777234567", "village": "Nyamoya"},
        {"id": "B001", "name": "جون كاماو", "type": "buyer", "phone": "0777345678", "company": "Kamau Traders"},
        {"id": "B002", "name": "سارة عثمان", "type": "buyer", "phone": "0777456789", "company": "Sarah Foods"},
    ])

# ==================== جلب أسعار السوق ====================
def get_market_prices():
    """أسعار السوق الحالية"""
    # في الإصدار القادم يمكن ربطها مع API حقيقي
    return {
        "🍌 موز": random.randint(2000, 3500),
        "🌽 ذرة": random.randint(1500, 2500),
        "🥜 فول": random.randint(3000, 4500)
    }

# ==================== تسجيل صفقة ====================
def record_transaction(farmer_id, buyer_id, product, quantity, price, total):
    transaction = {
        "id": str(uuid.uuid4())[:8],
        "farmer_id": farmer_id,
        "buyer_id": buyer_id,
        "product": product,
        "quantity": quantity,
        "price_per_kg": price,
        "total": total,
        "date": datetime.now().isoformat(),
        "status": "completed"
    }
    transactions = load_data(TRANSACTIONS_FILE)
    transactions.append(transaction)
    save_data(TRANSACTIONS_FILE, transactions)
    return transaction

# ==================== معالجة الأوامر ====================
def extract_number(text):
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    return None

def extract_product(text):
    text = text.lower()
    if "موز" in text or "banana" in text:
        return "🍌 موز"
    elif "ذرة" in text or "maize" in text or "corn" in text:
        return "🌽 ذرة"
    elif "فول" in text or "beans" in text or "bean" in text:
        return "🥜 فول"
    return None

def process_command(command, user_id, user_type):
    command = command.lower().strip()
    
    if "أضف" in command or "add" in command:
        product = extract_product(command)
        price = extract_number(command)
        numbers = re.findall(r'\d+', command)
        quantity = 100 if len(numbers) < 2 else int(numbers[1])
        
        if product and price and user_type == "farmer":
            product_data = {
                "id": str(uuid.uuid4())[:8],
                "product": product,
                "price": price,
                "quantity": quantity,
                "farmer_id": user_id,
                "date": datetime.now().isoformat()
            }
            products = load_data(PRODUCTS_FILE)
            products.append(product_data)
            save_data(PRODUCTS_FILE, products)
            return {"action": "add", "product": product, "price": price, "quantity": quantity}
    
    elif "شراء" in command or "buy" in command:
        product = extract_product(command)
        quantity = extract_number(command)
        if product and quantity and user_type == "buyer":
            return {"action": "buy", "product": product, "quantity": quantity}
    
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
    .price-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 5px solid #2ecc71;
    }
    .transaction-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3498db;
    }
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان ====================
st.markdown("""
<div class='main-header'>
    <h1>🌽 SOKO LINK 🎤</h1>
    <h3>ربط المزارعين بالتجار مباشرة</h3>
    <p>📊 أسعار السوق | 🤝 تسجيل الصفقات | 🎤 أوامر صوتية</p>
</div>
""", unsafe_allow_html=True)

# ==================== اختيار المستخدم ====================
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

users = load_data(USERS_FILE)

col1, col2 = st.columns(2)
with col1:
    farmer_names = [u["name"] for u in users if u["type"] == "farmer"]
    if farmer_names:
        selected_farmer = st.selectbox("👨‍🌾 اختر مزارع", farmer_names, key="farmer_select")
        if st.button("دخول كمزارع", key="farmer_btn"):
            for u in users:
                if u["name"] == selected_farmer:
                    st.session_state.user_id = u["id"]
                    st.session_state.user_type = "farmer"
                    st.session_state.user_name = u["name"]
                    st.rerun()

with col2:
    buyer_names = [u["name"] for u in users if u["type"] == "buyer"]
    if buyer_names:
        selected_buyer = st.selectbox("🛒 اختر تاجر", buyer_names, key="buyer_select")
        if st.button("دخول كتاجر", key="buyer_btn"):
            for u in users:
                if u["name"] == selected_buyer:
                    st.session_state.user_id = u["id"]
                    st.session_state.user_type = "buyer"
                    st.session_state.user_name = u["name"]
                    st.rerun()

if st.session_state.user_id:
    st.success(f"✅ مرحباً {st.session_state.user_name} - {'مزارع' if st.session_state.user_type == 'farmer' else 'تاجر'}")

# ==================== أسعار السوق ====================
st.markdown("### 📊 أسعار السوق اليوم")

market_prices = get_market_prices()

col1, col2, col3 = st.columns(3)
for i, (product, price) in enumerate(market_prices.items()):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div class='price-card'>
            <h3>{product}</h3>
            <h2>{price:,} شلن</h2>
            <small>سعر الكيلو</small>
        </div>
        """, unsafe_allow_html=True)

# ==================== المدخل الصوتي ====================
st.markdown("### 🎤 تحدث أو اكتب")

voice_input = st.text_input("أكتب الأمر هنا:", placeholder="مثال: أضف موز 2000 | شراء موز 50")

if voice_input and st.session_state.user_id:
    result = process_command(voice_input, st.session_state.user_id, st.session_state.user_type)
    
    if result["action"] == "add":
        st.success(f"✅ تم إضافة {result['product']} - {result['quantity']} كيلو بسعر {result['price']:,} شلن!")
        st.balloons()
    
    elif result["action"] == "buy":
        products = load_data(PRODUCTS_FILE)
        available = [p for p in products if result["product"] in p["product"]]
        if available:
            best = available[0]
            total = best["price"] * result["quantity"]
            transaction = record_transaction(
                best["farmer_id"], 
                st.session_state.user_id,
                result["product"], 
                result["quantity"], 
                best["price"], 
                total
            )
            st.success(f"✅ تم شراء {result['quantity']} كيلو {result['product']} بقيمة {total:,} شلن!")
            
            # إزالة المنتج من القائمة
            products.remove(best)
            save_data(PRODUCTS_FILE, products)
        else:
            st.warning(f"⚠️ لا يوجد {result['product']} متاح حالياً")
    
    elif result["action"] == "unknown":
        st.warning("🤔 لم أفهم الأمر. جرب: 'أضف موز 2000' أو 'شراء موز 50'")
elif voice_input and not st.session_state.user_id:
    st.warning("⚠️ يرجى اختيار مستخدم أولاً")

# ==================== عرض المنتجات المتاحة ====================
st.markdown("### 📦 المنتجات المتاحة")

products = load_data(PRODUCTS_FILE)
if products:
    for p in products:
        farmer = next((u for u in users if u["id"] == p["farmer_id"]), None)
        farmer_name = farmer["name"] if farmer else "مزارع"
        st.markdown(f"""
        <div class='product-card'>
            <strong>{p['product']}</strong><br>
            💰 {p['price']:,} شلن/كيلو | 📦 {p['quantity']} كيلو<br>
            👨‍🌾 {farmer_name} | 🕒 {p['date'][:16].replace('T', ' ')}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 لا توجد منتجات متاحة حالياً")

# ==================== سجل الصفقات ====================
st.markdown("### 📋 آخر الصفقات")

transactions = load_data(TRANSACTIONS_FILE)
if transactions:
    for t in transactions[-5:]:
        farmer = next((u for u in users if u["id"] == t["farmer_id"]), None)
        buyer = next((u for u in users if u["id"] == t["buyer_id"]), None)
        st.markdown(f"""
        <div class='transaction-card'>
            🍌 {t['product']} | {t['quantity']} كيلو | 💰 {t['total']:,} شلن<br>
            👨‍🌾 {farmer['name'] if farmer else 'مزارع'} → 🛒 {buyer['name'] if buyer else 'تاجر'}<br>
            🕒 {t['date'][:16].replace('T', ' ')}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 لا توجد صفقات بعد")

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown("### 📊 إحصائيات")
    st.metric("منتجات متاحة", len(products))
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_transactions = len([t for t in load_data(TRANSACTIONS_FILE) if t["date"].startswith(today)])
    st.metric("صفقات اليوم", today_transactions)
    
    total_sales = sum([t["total"] for t in load_data(TRANSACTIONS_FILE)])
    st.metric("إجمالي المبيعات", f"{total_sales:,} UGX")
    
    st.markdown("---")
    st.markdown("### 🎤 الأوامر الصوتية")
    st.markdown("""
    **للمزارع:**
    - `أضف موز 2000`
    - `أضف ذرة 1500 100`
    
    **للتاجر:**
    - `شراء موز 50`
    - `buy bananas 50`
    """)
    
    st.markdown("---")
    st.markdown("### 👥 المستخدمين")
    for u in users:
        st.markdown(f"- {u['name']} ({'مزارع' if u['type']=='farmer' else 'تاجر'})")
