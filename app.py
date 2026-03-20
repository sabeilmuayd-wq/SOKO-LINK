import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - سوق المزارعات",
    page_icon="🌽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== ملفات التخزين ====================
DATA_FOLDER = "soko_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PRODUCTS_FILE = os.path.join(DATA_FOLDER, "products.json")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
ORDERS_FILE = os.path.join(DATA_FOLDER, "orders.json")
TRANSACTIONS_FILE = os.path.join(DATA_FOLDER, "transactions.json")

for file in [PRODUCTS_FILE, USERS_FILE, ORDERS_FILE, TRANSACTIONS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except:
        return []

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def generate_id():
    return str(uuid.uuid4())[:8].upper()

# ==================== نظام الترجمة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"

translations = {
    "ar": {
        "app_name": "🌽 سوكو لينك",
        "subtitle": "سوق المزارعات الأوغنديات",
        "welcome": "🇺🇬 مرحباً بك في سوكو لينك",
        "farmer": "👩🏾‍🌾 مزارعة",
        "trader": "🛒 تاجرة",
        "you_are": "أنت الآن:",
        "register": "📝 التسجيل",
        "name": "الاسم",
        "phone": "الهاتف",
        "village": "القرية",
        "add_product": "➕ إضافة منتج",
        "my_products": "📋 منتجاتي",
        "my_orders": "📦 طلباتي",
        "search": "🔍 بحث",
        "all_products": "📋 كل المنتجات",
        "product_type": "المنتج",
        "quantity": "الكمية",
        "unit": "الوحدة",
        "price": "السعر",
        "location": "المنطقة",
        "description": "الوصف",
        "publish": "✅ نشر",
        "buy": "🛒 شراء",
        "pay": "💳 دفع",
        "commission": "💰 عمولتك",
        "total": "المجموع",
        "pending": "⏳ معلق",
        "accepted": "✅ مقبول",
        "rejected": "❌ مرفوض",
        "accept": "✅ قبول",
        "reject": "❌ رفض",
        "order_sent": "تم إرسال الطلب! المزارعة ستتصل بك",
        "no_products": "لا توجد منتجات",
        "women": "👩🏾‍🌾 نساء أوغنديات يبعن منتجات بلدهن 🇺🇬"
    },
    "en": {
        "app_name": "🌽 SOKO LINK",
        "subtitle": "Ugandan Women's Market",
        "welcome": "🇺🇬 Welcome to SOKO LINK",
        "farmer": "👩🏾‍🌾 Woman Farmer",
        "trader": "🛒 Woman Trader",
        "you_are": "You are:",
        "register": "📝 Register",
        "name": "Name",
        "phone": "Phone",
        "village": "Village",
        "add_product": "➕ Add Product",
        "my_products": "📋 My Products",
        "my_orders": "📦 My Orders",
        "search": "🔍 Search",
        "all_products": "📋 All Products",
        "product_type": "Product",
        "quantity": "Quantity",
        "unit": "Unit",
        "price": "Price",
        "location": "Location",
        "description": "Description",
        "publish": "✅ Publish",
        "buy": "🛒 Buy",
        "pay": "💳 Pay",
        "commission": "💰 Your Commission",
        "total": "Total",
        "pending": "⏳ Pending",
        "accepted": "✅ Accepted",
        "rejected": "❌ Rejected",
        "accept": "✅ Accept",
        "reject": "❌ Reject",
        "order_sent": "Order sent! The farmer will call you",
        "no_products": "No products",
        "women": "👩🏾‍🌾 Ugandan women selling local products 🇺🇬"
    },
    "sw": {
        "app_name": "🌽 SOKO LINK",
        "subtitle": "Soko la Wanawake Uganda",
        "welcome": "🇺🇬 Karibu SOKO LINK",
        "farmer": "👩🏾‍🌾 Mkulima",
        "trader": "🛒 Mfanyabiashara",
        "you_are": "Wewe ni:",
        "register": "📝 Jisajili",
        "name": "Jina",
        "phone": "Simu",
        "village": "Kijiji",
        "add_product": "➕ Ongeza Bidhaa",
        "my_products": "📋 Bidhaa Zangu",
        "my_orders": "📦 Maagizo Yangu",
        "search": "🔍 Tafuta",
        "all_products": "📋 Bidhaa Zote",
        "product_type": "Bidhaa",
        "quantity": "Kiasi",
        "unit": "Kipimo",
        "price": "Bei",
        "location": "Mahali",
        "description": "Maelezo",
        "publish": "✅ Chapisha",
        "buy": "🛒 Nunua",
        "pay": "💳 Lipa",
        "commission": "💰 Kamisheni yako",
        "total": "Jumla",
        "pending": "⏳ Inasubiri",
        "accepted": "✅ Imekubaliwa",
        "rejected": "❌ Imekataliwa",
        "accept": "✅ Kubali",
        "reject": "❌ Kataa",
        "order_sent": "Agizo limetumwa! Mkulima atakupigia",
        "no_products": "Hakuna bidhaa",
        "women": "👩🏾‍🌾 Wanawake Uganda wanauza bidhaa zao 🇺🇬"
    }
}

def t(key):
    return translations[st.session_state.language].get(key, key)

# ==================== تصميم الصفحة ====================
st.markdown(f"""
<style>
    /* الخلفية الرئيسية */
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }}
    
    /* تنسيق العنوان */
    .main-header {{
        text-align: center;
        padding: 2rem 1rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 3px solid #ffd700;
    }}
    .main-header h1 {{
        color: #2c3e50;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    .main-header h3 {{
        color: #e67e22;
        font-size: 1.3rem;
    }}
    
    /* شريط النساء الأوغنديات */
    .women-strip {{
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        padding: 1.5rem;
        border-radius: 50px;
        margin: 1.5rem 0;
        text-align: center;
        font-size: 2rem;
        border: 3px solid white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    .women-strip p {{
        color: white;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        text-shadow: 1px 1px 2px black;
    }}
    
    /* بطاقات المنتجات */
    .product-card {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #ffd700;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }}
    .product-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }}
    
    /* شارة المزارعة */
    .farmer-badge {{
        background: #e67e22;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 25px;
        display: inline-block;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }}
    
    /* سعر المنتج */
    .price-tag {{
        background: #27ae60;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        display: inline-block;
        font-weight: bold;
        font-size: 1.2rem;
    }}
    
    /* أزرار اللغات */
    .lang-btn {{
        background: white;
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 0.5rem;
        margin: 0.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }}
    .lang-btn:hover {{
        background: #ffd700;
        color: black;
    }}
    
    /* تذييل */
    .footer {{
        text-align: center;
        padding: 2rem;
        background: rgba(0,0,0,0.3);
        border-radius: 20px;
        margin-top: 3rem;
        color: white;
        border: 2px solid #ffd700;
    }}
</style>
""", unsafe_allow_html=True)

# ==================== العنوان الرئيسي ====================
st.markdown(f"""
<div class='main-header'>
    <h1>{t('app_name')}</h1>
    <h3>✨ {t('subtitle')} ✨</h3>
</div>
""", unsafe_allow_html=True)

# ==================== شريط النساء الأوغنديات ====================
st.markdown(f"""
<div class='women-strip'>
    👩🏾‍🌾 👩🏿‍🌾 👩🏽‍🌾 👩🏼‍🌾 👩🏻‍🌾
    <p>{t('women')}</p>
    🍌 🌽 🥜 🍠 🥭
</div>
""", unsafe_allow_html=True)

# ==================== اختيار اللغة ====================
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🇸🇦 عربي", use_container_width=True):
        st.session_state.language = "ar"
        st.rerun()
with col2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.language = "en"
        st.rerun()
with col3:
    if st.button("🇺🇬 Kiswahili", use_container_width=True):
        st.session_state.language = "sw"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ==================== اختيار نوع المستخدم ====================
st.markdown(f"<h2 style='text-align: center; color: white;'>{t('welcome')}</h2>", unsafe_allow_html=True)

if "user_type" not in st.session_state:
    st.session_state.user_type = "farmer"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""
if "user_village" not in st.session_state:
    st.session_state.user_village = ""

col1, col2 = st.columns(2)
with col1:
    if st.button(f"👩🏾‍🌾 {t('farmer')}", use_container_width=True):
        st.session_state.user_type = "farmer"
with col2:
    if st.button(f"🛒 {t('trader')}", use_container_width=True):
        st.session_state.user_type = "trader"

st.info(f"**{t('you_are')}** {'👩🏾‍🌾 ' + t('farmer') if st.session_state.user_type == 'farmer' else '🛒 ' + t('trader')}")

# ==================== تسجيل الدخول ====================
with st.expander(f"📝 {t('register')}", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(t('name'), value=st.session_state.user_name)
        st.session_state.user_name = name
    with col2:
        phone = st.text_input(t('phone'), value=st.session_state.user_phone)
        st.session_state.user_phone = phone
    
    village = st.text_input(t('village'), value=st.session_state.user_village)
    st.session_state.user_village = village

# ==================== التبويبات ====================
if st.session_state.user_type == "farmer":
    tab1, tab2, tab3 = st.tabs([t('add_product'), t('my_products'), t('my_orders')])
else:
    tab1, tab2, tab3 = st.tabs([t('search'), t('all_products'), t('my_orders')])

# ==================== إضافة منتج ====================
if st.session_state.user_type == "farmer":
    with tab1:
        st.markdown(f"<h3 style='color: white;'>{t('add_product')}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.selectbox(
                t('product_type'),
                ["🍌 موز", "🌽 ذرة", "🥜 فول", "🍅 طماطم", "🧅 بصل", "🍠 بطاطا", "🥬 خضار", "🍍 أناناس"]
            )
            quantity = st.number_input(t('quantity'), min_value=1, value=100)
            unit = st.selectbox(t('unit'), ["كيلو", "صندوق", "حبة"])
            
        with col2:
            price = st.number_input(t('price') + " (UGX)", min_value=100, step=1000, value=5000)
            location = st.text_input(t('location'), value=st.session_state.user_village)
        
        description = st.text_area(t('description'), placeholder="...")
        
        if st.button(f"{t('publish')} ✨", type="primary", use_container_width=True):
            if st.session_state.user_name and st.session_state.user_phone:
                product = {
                    "id": generate_id(),
                    "farmer_name": st.session_state.user_name,
                    "farmer_phone": st.session_state.user_phone,
                    "product": product_name,
                    "quantity": quantity,
                    "unit": unit,
                    "price": price,
                    "location": location or st.session_state.user_village,
                    "description": description,
                    "date": datetime.now().isoformat(),
                    "status": "available"
                }
                
                products = load_data(PRODUCTS_FILE)
                products.append(product)
                save_data(PRODUCTS_FILE, products)
                
                st.success(f"✅ {t('publish')}!")
                st.balloons()
            else:
                st.error(f"❌ {t('name')} + {t('phone')}")

# ==================== بحث للمشتري ====================
if st.session_state.user_type == "trader":
    with tab1:
        st.markdown(f"<h3 style='color: white;'>{t('search')}</h3>", unsafe_allow_html=True)
        
        products = load_data(PRODUCTS_FILE)
        available = [p for p in products if p.get("status") == "available"]
        
        if available:
            col1, col2 = st.columns(2)
            with col1:
                types = ["الكل"] + list(set([p["product"] for p in available]))
                selected_type = st.selectbox(t('product_type'), types)
            with col2:
                locs = ["الكل"] + list(set([p.get("location", "") for p in available if p.get("location")]))
                selected_loc = st.selectbox(t('location'), locs)
            
            filtered = available.copy()
            if selected_type != "الكل":
                filtered = [p for p in filtered if p["product"] == selected_type]
            if selected_loc != "الكل":
                filtered = [p for p in filtered if p.get("location") == selected_loc]
            
            st.markdown(f"**{len(filtered)} منتج**")
            
            for p in filtered:
                commission = int(p['price'] * 0.05)
                total = p['price'] + commission
                
                st.markdown(f"""
                <div class='product-card'>
                    <h3>{p['product']}</h3>
                    <span class='farmer-badge'>👩🏾‍🌾 {p['farmer_name']}</span>
                    <p>📞 {p['farmer_phone']}</p>
                    <p>📍 {p.get('location', 'N/A')}</p>
                    <p><span class='price-tag'>{p['price']:,} UGX</span></p>
                    <p>💰 {t('commission')}: {commission:,} UGX</p>
                    <p>💵 {t('total')}: {total:,} UGX</p>
                    <p>{p.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"{t('buy')}", key=f"buy_{p['id']}"):
                    if st.session_state.user_name and st.session_state.user_phone:
                        order = {
                            "id": generate_id(),
                            "product_id": p["id"],
                            "product_name": p["product"],
                            "buyer_name": st.session_state.user_name,
                            "buyer_phone": st.session_state.user_phone,
                            "farmer_name": p["farmer_name"],
                            "farmer_phone": p["farmer_phone"],
                            "price": p["price"],
                            "commission": commission,
                            "total": total,
                            "date": datetime.now().isoformat(),
                            "status": "pending",
                            "payment_status": "pending"
                        }
                        
                        orders = load_data(ORDERS_FILE)
                        orders.append(order)
                        save_data(ORDERS_FILE, orders)
                        
                        st.success(f"✅ {t('order_sent')}")
                        st.balloons()
                    else:
                        st.error(f"❌ {t('name')} + {t('phone')}")
        else:
            st.info(t('no_products'))

# ==================== عرض المنتجات ====================
with tab2:
    if st.session_state.user_type == "farmer":
        st.markdown(f"<h3 style='color: white;'>{t('my_products')}</h3>", unsafe_allow_html=True)
        products = load_data(PRODUCTS_FILE)
        my_products = [p for p in products if p.get("farmer_name") == st.session_state.user_name]
        
        if my_products:
            for p in my_products:
                st.markdown(f"""
                <div class='product-card'>
                    <h3>{p['product']}</h3>
                    <p>{p['quantity']} {p['unit']} - {p['price']:,} UGX</p>
                    <p>{'🟢 متاح' if p['status'] == 'available' else '🔴 مباع'}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t('no_products'))
    else:
        st.markdown(f"<h3 style='color: white;'>{t('all_products')}</h3>", unsafe_allow_html=True)
        products = load_data(PRODUCTS_FILE)
        available = [p for p in products if p.get("status") == "available"]
        
        if available:
            for p in available[:10]:
                st.markdown(f"""
                <div class='product-card'>
                    <h3>{p['product']}</h3>
                    <p>👩🏾‍🌾 {p['farmer_name']} - 📞 {p['farmer_phone']}</p>
                    <p>{p['quantity']} {p['unit']} - {p['price']:,} UGX</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t('no_products'))

# ==================== الطلبات ====================
with tab3:
    st.markdown(f"<h3 style='color: white;'>{t('my_orders')}</h3>", unsafe_allow_html=True)
    
    orders = load_data(ORDERS_FILE)
    
    if st.session_state.user_type == "farmer":
        my_orders = [o for o in orders if o.get("farmer_name") == st.session_state.user_name]
        if my_orders:
            for o in my_orders:
                st.markdown(f"""
                <div class='product-card'>
                    <h3>{o['product_name']}</h3>
                    <p>👤 {o['buyer_name']} - 📞 {o['buyer_phone']}</p>
                    <p>💰 {t('commission')}: {o.get('commission', 0):,} UGX</p>
                    <p>الحالة: {t(o['status'])}</p>
                """, unsafe_allow_html=True)
                
                if o["status"] == "pending":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(t('accept'), key=f"acc_{o['id']}"):
                            for ord in orders:
                                if ord["id"] == o["id"]:
                                    ord["status"] = "accepted"
                            save_data(ORDERS_FILE, orders)
                            st.rerun()
                    with col2:
                        if st.button(t('reject'), key=f"rej_{o['id']}"):
                            for ord in orders:
                                if ord["id"] == o["id"]:
                                    ord["status"] = "rejected"
                            save_data(ORDERS_FILE, orders)
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(t('no_products'))
    
    else:
        my_orders = [o for o in orders if o.get("buyer_name") == st.session_state.user_name]
        if my_orders:
            for o in my_orders:
                st.markdown(f"""
                <div class='product-card'>
                    <h3>{o['product_name']}</h3>
                    <p>👩🏾‍🌾 {o['farmer_name']} - 📞 {o['farmer_phone']}</p>
                    <p>💵 {t('total')}: {o.get('total', 0):,} UGX</p>
                    <p>الحالة: {t(o['status'])}</p>
                """, unsafe_allow_html=True)
                
                if o["status"] == "accepted" and o.get("payment_status") != "paid":
                    if st.button(f"{t('pay')} 💳", key=f"pay_{o['id']}"):
                        for ord in orders:
                            if ord["id"] == o["id"]:
                                ord["payment_status"] = "paid"
                        save_data(ORDERS_FILE, orders)
                        
                        trans = {
                            "id": generate_id(),
                            "order_id": o["id"],
                            "amount": o["total"],
                            "commission": o["commission"],
                            "date": datetime.now().isoformat()
                        }
                        trans_list = load_data(TRANSACTIONS_FILE)
                        trans_list.append(trans)
                        save_data(TRANSACTIONS_FILE, trans_list)
                        
                        st.success("✅ Payment successful!")
                        st.balloons()
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(t('no_products'))

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 20px;'>
        <h3>👩🏾‍🌾 {t('welcome')}</h3>
        <p><b>{t('name')}:</b> {st.session_state.user_name or '---'}</p>
        <p><b>{t('phone')}:</b> {st.session_state.user_phone or '---'}</p>
        <p><b>{t('village')}:</b> {st.session_state.user_village or '---'}</p>
        <hr>
        <h3>📊 إحصائيات</h3>
    """, unsafe_allow_html=True)
    
    products = load_data(PRODUCTS_FILE)
    orders = load_data(ORDERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)
    
    st.metric("منتجات متاحة", len([p for p in products if p.get("status") == "available"]))
    st.metric("طلبات نشطة", len([o for o in orders if o.get("status") == "pending"]))
    
    total_commission = sum([t.get("commission", 0) for t in transactions])
    st.metric("أرباحك", f"{total_commission:,} UGX")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== تذييل ====================
st.markdown(f"""
<div class='footer'>
    {t('app_name')} - {t('subtitle')}<br>
    🇺🇬 © 2026 جميع الحقوق محفوظة 🇺🇬
</div>
""", unsafe_allow_html=True)
