import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random
from PIL import Image
import io
import base64

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - سوق المزارعين",
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

# التأكد من وجود الملفات
for file in [PRODUCTS_FILE, USERS_FILE, ORDERS_FILE, TRANSACTIONS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

# ==================== دوال مساعدة ====================
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return []
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
    st.session_state.language = "ar"  # ar, en, sw

translations = {
    "ar": {
        "app_name": "سوكو لينك",
        "subtitle": "ربط المزارعات والتجار مباشرة",
        "farmer": "👩‍🌾 مزارعة",
        "trader": "🛒 تاجرة",
        "you_are": "أنت الآن:",
        "register": "📝 سجل دخولك",
        "name": "الاسم",
        "phone": "رقم الهاتف",
        "village": "القرية/المنطقة",
        "add_product": "➕ إضافة منتج",
        "my_products": "📋 منتجاتي",
        "my_orders": "📦 طلباتي",
        "search": "🔍 بحث عن منتجات",
        "all_products": "📋 كل المنتجات",
        "product_type": "نوع المنتج",
        "quantity": "الكمية",
        "unit": "الوحدة",
        "price": "السعر",
        "location": "الموقع",
        "description": "وصف المنتج",
        "publish": "✅ نشر المنتج",
        "buy": "🛒 أريد شراء",
        "order_sent": "✅ تم إرسال الطلب! المزارعة ستتصل بك",
        "no_products": "📭 لا توجد منتجات",
        "pending": "⏳ معلق",
        "accepted": "✅ مقبول",
        "rejected": "❌ مرفوض",
        "accept": "✅ قبول",
        "reject": "❌ رفض",
        "commission": "💰 عمولة 5%",
        "pay": "💳 ادفع الآن",
        "total": "الإجمالي:",
        "welcome": "مرحباً بك في سوكو لينك"
    },
    "en": {
        "app_name": "SOKO LINK",
        "subtitle": "Connecting women farmers & traders directly",
        "farmer": "👩‍🌾 Woman Farmer",
        "trader": "🛒 Woman Trader",
        "you_are": "You are now:",
        "register": "📝 Register",
        "name": "Name",
        "phone": "Phone Number",
        "village": "Village/Location",
        "add_product": "➕ Add Product",
        "my_products": "📋 My Products",
        "my_orders": "📦 My Orders",
        "search": "🔍 Search Products",
        "all_products": "📋 All Products",
        "product_type": "Product Type",
        "quantity": "Quantity",
        "unit": "Unit",
        "price": "Price",
        "location": "Location",
        "description": "Description",
        "publish": "✅ Publish",
        "buy": "🛒 I want to buy",
        "order_sent": "✅ Order sent! The farmer will call you",
        "no_products": "📭 No products",
        "pending": "⏳ Pending",
        "accepted": "✅ Accepted",
        "rejected": "❌ Rejected",
        "accept": "✅ Accept",
        "reject": "❌ Reject",
        "commission": "💰 5% Commission",
        "pay": "💳 Pay Now",
        "total": "Total:",
        "welcome": "Welcome to SOKO LINK"
    },
    "sw": {
        "app_name": "SOKO LINK",
        "subtitle": "Kuunganisha wakulima na wafanyabiashara moja kwa moja",
        "farmer": "👩‍🌾 Mkulima Mwanamke",
        "trader": "🛒 Mfanyabiashara Mwanamke",
        "you_are": "Wewe ni:",
        "register": "📝 Jisajili",
        "name": "Jina",
        "phone": "Namba ya Simu",
        "village": "Kijiji/Eneo",
        "add_product": "➕ Ongeza Bidhaa",
        "my_products": "📋 Bidhaa Zangu",
        "my_orders": "📦 Maagizo Yangu",
        "search": "🔍 Tafuta Bidhaa",
        "all_products": "📋 Bidhaa Zote",
        "product_type": "Aina ya Bidhaa",
        "quantity": "Kiasi",
        "unit": "Kipimo",
        "price": "Bei",
        "location": "Mahali",
        "description": "Maelezo",
        "publish": "✅ Chapisha",
        "buy": "🛒 Nataka kununua",
        "order_sent": "✅ Agizo limetumwa! Mkulima atakupigia",
        "no_products": "📭 Hakuna bidhaa",
        "pending": "⏳ Inasubiri",
        "accepted": "✅ Imekubaliwa",
        "rejected": "❌ Imekataliwa",
        "accept": "✅ Kubali",
        "reject": "❌ Kataa",
        "commission": "💰 Kamisheni 5%",
        "pay": "💳 Lipa Sasa",
        "total": "Jumla:",
        "welcome": "Karibu SOKO LINK"
    }
}

def t(key):
    """دالة الترجمة"""
    return translations[st.session_state.language].get(key, key)

# ==================== زخرفة الخلفية ====================
def get_image_base64(image_path):
    """تحويل الصورة إلى base64 (للعرض)"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# خلفية مزخرفة (بدون صور خارجية)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .women-image {
        text-align: center;
        font-size: 3rem;
        padding: 1rem;
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
        margin: 1rem 0;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .price {
        color: #27ae60;
        font-weight: bold;
        font-size: 1.2rem;
        background: #e8f5e9;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        display: inline-block;
    }
    .woman-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        padding: 1rem;
        background: rgba(255,255,255,0.5);
        border-radius: 10px;
        margin-top: 2rem;
    }
    .language-btn {
        background: white;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ==================== العنوان الرئيسي ====================
st.markdown(f"""
<div class='main-header'>
    <h1>🌽 {t('app_name')}</h1>
    <h4>{t('subtitle')}</h4>
</div>
""", unsafe_allow_html=True)

# ==================== صورة نساء أوغنديات (محاكاة) ====================
st.markdown("""
<div class='women-image'>
    👩🏾‍🌾 👩🏿‍🌾 👩🏽‍🌾 
    <br>
    <span style='font-size: 1rem;'>"نساء أوغنديات يبعن منتجات بلدهن"</span>
    <br>
    <span style='font-size: 0.8rem; color: #666;'>🇺🇬 موز - ذرة - فول - خضار 🇺🇬</span>
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

# ==================== تهيئة session state ====================
if "user_type" not in st.session_state:
    st.session_state.user_type = "farmer"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""
if "user_village" not in st.session_state:
    st.session_state.user_village = ""

# ==================== اختيار نوع المستخدم ====================
st.markdown(f"### {t('welcome')}")
col1, col2 = st.columns(2)
with col1:
    if st.button(f"👩‍🌾 {t('farmer')}", use_container_width=True):
        st.session_state.user_type = "farmer"
with col2:
    if st.button(f"🛒 {t('trader')}", use_container_width=True):
        st.session_state.user_type = "trader"

st.markdown(f"**{t('you_are')}** {'👩‍🌾 ' + t('farmer') if st.session_state.user_type == 'farmer' else '🛒 ' + t('trader')}")

# ==================== تسجيل الدخول ====================
with st.expander(t('register'), expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(t('name'), value=st.session_state.user_name)
        if name:
            st.session_state.user_name = name
    with col2:
        phone = st.text_input(t('phone'), value=st.session_state.user_phone)
        if phone:
            st.session_state.user_phone = phone
    
    village = st.text_input(t('village'), value=st.session_state.user_village)
    if village:
        st.session_state.user_village = village

# ==================== التبويبات ====================
if st.session_state.user_type == "farmer":
    tab1, tab2, tab3 = st.tabs([t('add_product'), t('my_products'), t('my_orders')])
else:
    tab1, tab2, tab3 = st.tabs([t('search'), t('all_products'), t('my_orders')])

# ==================== TAB للمزارعة: إضافة منتج ====================
if st.session_state.user_type == "farmer":
    with tab1:
        st.subheader(t('add_product'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.selectbox(
                t('product_type'),
                ["🍌 موز", "🌽 ذرة", "🥜 فول سوداني", "🧅 بصل", "🍅 طماطم", "🍠 بطاطا", "🥬 خضار", "🍍 أناناس", "🥭 مانجو", "🍓 فواكه"]
            )
            quantity = st.number_input(t('quantity'), min_value=1, step=1, value=100)
            unit = st.selectbox(t('unit'), ["كيلو", "صندوق", "حبة", "كيس"])
            
        with col2:
            price = st.number_input(t('price') + " (UGX)", min_value=100, step=1000, value=5000)
            location = st.text_input(t('location'), value=st.session_state.user_village)
        
        description = st.text_area(t('description'), placeholder="منتج طازج من مزرعتي...")
        
        if st.button(t('publish'), type="primary", use_container_width=True):
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
                st.error("❌ " + t('name') + " و " + t('phone') + " مطلوبين")

# ==================== TAB للمتسوقة: بحث عن منتجات ====================
if st.session_state.user_type == "trader":
    with tab1:
        st.subheader(t('search'))
        
        products = load_data(PRODUCTS_FILE)
        available_products = [p for p in products if p.get("status") == "available"]
        
        if available_products:
            # فلترة
            product_types = list(set([p["product"] for p in available_products]))
            selected_type = st.selectbox(t('product_type'), ["الكل"] + product_types)
            
            locations = list(set([p.get("location", "غير معروف") for p in available_products]))
            selected_location = st.selectbox(t('location'), ["الكل"] + locations)
            
            filtered = available_products.copy()
            
            if selected_type != "الكل":
                filtered = [p for p in filtered if p["product"] == selected_type]
            
            if selected_location != "الكل":
                filtered = [p for p in filtered if p.get("location") == selected_location]
            
            st.markdown(f"**تم العثور على {len(filtered)} منتج**")
            
            for product in filtered:
                with st.container():
                    commission = int(product['price'] * 0.05)
                    total = product['price'] + commission
                    
                    st.markdown(f"""
                    <div class='product-card'>
                        <div style='display: flex; justify-content: space-between;'>
                            <h4>{product['product']} <span class='woman-badge'>👩‍🌾 {product['farmer_name']}</span></h4>
                        </div>
                        <p><strong>{t('quantity')}:</strong> {product['quantity']} {product['unit']}</p>
                        <p><strong>{t('price')}:</strong> <span class='price'>{product['price']:,} UGX</span></p>
                        <p><strong>{t('commission')}:</strong> {commission:,} UGX</p>
                        <p><strong>{t('total')}:</strong> <span style='color: #27ae60; font-weight: bold;'>{total:,} UGX</span></p>
                        <p><strong>{t('location')}:</strong> {product.get('location', 'غير معروف')}</p>
                        <p><strong>{t('description')}:</strong> {product.get('description', '')}</p>
                        <p><strong>📞 {t('phone')}:</strong> {product['farmer_phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"{t('buy')}", key=f"buy_{product['id']}"):
                            if st.session_state.user_name and st.session_state.user_phone:
                                order = {
                                    "id": generate_id(),
                                    "product_id": product["id"],
                                    "product_name": product["product"],
                                    "buyer_name": st.session_state.user_name,
                                    "buyer_phone": st.session_state.user_phone,
                                    "farmer_name": product["farmer_name"],
                                    "farmer_phone": product["farmer_phone"],
                                    "price": product["price"],
                                    "commission": commission,
                                    "total": total,
                                    "quantity": product["quantity"],
                                    "unit": product["unit"],
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
                                st.error("❌ " + t('name') + " و " + t('phone') + " مطلوبين")
                    with col2:
                        st.button(f"{t('pay')}", key=f"pay_{product['id']}")
        else:
            st.info(t('no_products'))

# ==================== TAB عرض المنتجات ====================
with tab2:
    if st.session_state.user_type == "farmer":
        st.subheader(t('my_products'))
        products = load_data(PRODUCTS_FILE)
        my_products = [p for p in products if p.get("farmer_name") == st.session_state.user_name]
        
        if my_products:
            for p in my_products:
                status = "🟢" if p.get("status") == "available" else "🔴"
                st.markdown(f"""
                {status} **{p['product']}** - {p['quantity']} {p['unit']} - {p['price']:,} UGX
                """)
        else:
            st.info(t('no_products'))
    
    else:
        st.subheader(t('all_products'))
        products = load_data(PRODUCTS_FILE)
        available = [p for p in products if p.get("status") == "available"]
        
        if available:
            for p in available[:10]:
                st.markdown(f"""
                **{p['product']}** - {p['quantity']} {p['unit']} - {p['price']:,} UGX  
                👩‍🌾 {p['farmer_name']} - 📞 {p['farmer_phone']}
                """)
        else:
            st.info(t('no_products'))

# ==================== TAB الطلبات مع خصم إلكتروني ====================
with tab3:
    st.subheader(t('my_orders'))
    
    orders = load_data(ORDERS_FILE)
    
    if st.session_state.user_type == "farmer":
        my_orders = [o for o in orders if o.get("farmer_name") == st.session_state.user_name]
        if my_orders:
            for o in my_orders:
                status_emoji = "⏳" if o["status"] == "pending" else "✅" if o["status"] == "accepted" else "❌"
                payment_emoji = "💳" if o.get("payment_status") == "paid" else "⏳"
                
                st.markdown(f"""
                {status_emoji} **{o['product_name']}** - {o['quantity']} {o['unit']}  
                👤 {o['buyer_name']} - 📞 {o['buyer_phone']}  
                💰 {t('commission')}: {o.get('commission', 0):,} UGX {payment_emoji}
                """)
                
                if o["status"] == "pending":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"{t('accept')}", key=f"acc_{o['id']}"):
                            for ord in orders:
                                if ord["id"] == o["id"]:
                                    ord["status"] = "accepted"
                            save_data(ORDERS_FILE, orders)
                            st.rerun()
                    with col2:
                        if st.button(f"{t('reject')}", key=f"rej_{o['id']}"):
                            for ord in orders:
                                if ord["id"] == o["id"]:
                                    ord["status"] = "rejected"
                            save_data(ORDERS_FILE, orders)
                            st.rerun()
        else:
            st.info(t('no_products'))
    
    else:  # trader
        my_orders = [o for o in orders if o.get("buyer_name") == st.session_state.user_name]
        if my_orders:
            for o in my_orders:
                status_emoji = "⏳" if o["status"] == "pending" else "✅" if o["status"] == "accepted" else "❌"
                payment_emoji = "💳" if o.get("payment_status") == "paid" else "⏳"
                
                st.markdown(f"""
                {status_emoji} **{o['product_name']}** - {o['quantity']} {o['unit']}  
                👩‍🌾 {o['farmer_name']} - 📞 {o['farmer_phone']}  
                💰 {t('total')}: {o.get('total', 0):,} UGX {payment_emoji}
                """)
                
                if o["status"] == "accepted" and o.get("payment_status") != "paid":
                    if st.button(f"{t('pay')}", key=f"pay_order_{o['id']}"):
                        for ord in orders:
                            if ord["id"] == o["id"]:
                                ord["payment_status"] = "paid"
                        save_data(ORDERS_FILE, orders)
                        
                        # تسجيل المعاملة
                        trans = {
                            "id": generate_id(),
                            "order_id": o["id"],
                            "amount": o["total"],
                            "commission": o["commission"],
                            "date": datetime.now().isoformat(),
                            "status": "completed"
                        }
                        trans_list = load_data(TRANSACTIONS_FILE)
                        trans_list.append(trans)
                        save_data(TRANSACTIONS_FILE, trans_list)
                        
                        st.success("✅ Payment successful! Commission recorded.")
                        st.balloons()
                        st.rerun()
        else:
            st.info(t('no_products'))

# ==================== شريط جانبي ====================
with st.sidebar:
    st.markdown("### 👩‍🌾 " + t('welcome'))
    st.markdown(f"**{t('name')}:** {st.session_state.user_name or '---'}")
    st.markdown(f"**{t('phone')}:** {st.session_state.user_phone or '---'}")
    st.markdown(f"**{t('village')}:** {st.session_state.user_village or '---'}")
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    products = load_data(PRODUCTS_FILE)
    orders = load_data(ORDERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)
    
    st.metric("منتجات متاحة", len([p for p in products if p.get("status") == "available"]))
    st.metric("طلبات نشطة", len([o for o in orders if o.get("status") == "pending"]))
    
    total_commission = sum([t.get("commission", 0) for t in transactions])
    st.metric("أرباحك", f"{total_commission:,} UGX")

# ==================== تذييل ====================
st.markdown(f"""
<div class='footer'>
    🌍 {t('app_name')} - {t('subtitle')} 🇺🇬<br>
    © 2026 جميع الحقوق محفوظة
</div>
""", unsafe_allow_html=True)
