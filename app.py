import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - سوق المزارعين",
    page_icon="🌽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تحسين للهاتف
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 0.5rem;
    }
    .stButton button {
        width: 100%;
        height: 3rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 10px;
        background-color: #2ecc71;
        color: white;
    }
    h1 {
        font-size: 1.8rem !important;
        text-align: center;
        color: #27ae60;
        margin-bottom: 0.5rem;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .price {
        color: #27ae60;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== إعدادات التخزين ====================
DATA_FOLDER = "soko_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PRODUCTS_FILE = os.path.join(DATA_FOLDER, "products.json")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
ORDERS_FILE = os.path.join(DATA_FOLDER, "orders.json")

# التأكد من وجود الملفات
for file in [PRODUCTS_FILE, USERS_FILE, ORDERS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

# ==================== دوال مساعدة ====================
def load_data(filename):
    """تحميل البيانات من ملف JSON"""
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
    """حفظ البيانات في ملف JSON"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def generate_id():
    return str(uuid.uuid4())[:8].upper()

# تهيئة session state
if "user_type" not in st.session_state:
    st.session_state.user_type = "buyer"  # buyer or farmer
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_phone" not in st.session_state:
    st.session_state.user_phone = ""
if "user_village" not in st.session_state:
    st.session_state.user_village = ""

# ==================== العنوان الرئيسي ====================
st.markdown("""
<h1>🌽 SOKO LINK</h1>
<h4 style='text-align: center; color: #666;'>ربط المزارع بالتاجر مباشرة</h4>
<hr>
""", unsafe_allow_html=True)

# ==================== اختيار نوع المستخدم ====================
col1, col2 = st.columns(2)
with col1:
    if st.button("👨‍🌾 أنا مزارع", use_container_width=True):
        st.session_state.user_type = "farmer"
with col2:
    if st.button("🛒 أنا تاجر", use_container_width=True):
        st.session_state.user_type = "buyer"

st.markdown(f"**أنت الآن:** {'👨‍🌾 مزارع' if st.session_state.user_type == 'farmer' else '🛒 تاجر'}")

# ==================== تسجيل الدخول السريع ====================
with st.expander("📝 سجل دخولك (مرة واحدة)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("الاسم", value=st.session_state.user_name)
        if name:
            st.session_state.user_name = name
    with col2:
        phone = st.text_input("رقم الهاتف", value=st.session_state.user_phone)
        if phone:
            st.session_state.user_phone = phone
    
    village = st.text_input("القرية/المنطقة", value=st.session_state.user_village)
    if village:
        st.session_state.user_village = village

# ==================== التبويبات الرئيسية ====================
if st.session_state.user_type == "farmer":
    tab1, tab2, tab3 = st.tabs(["➕ إضافة منتج", "📋 منتجاتي", "📦 طلباتي"])
else:
    tab1, tab2, tab3 = st.tabs(["🔍 بحث عن منتجات", "📋 المنتجات", "📦 طلباتي"])

# ==================== TAB للمزارع: إضافة منتج ====================
if st.session_state.user_type == "farmer":
    with tab1:
        st.subheader("➕ إضافة منتج جديد")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.selectbox(
                "نوع المنتج",
                ["موز", "ذرة", "فول سوداني", "بصل", "طماطم", "بطاطا حلوة", "كسافا", "خضار", "فواكه", "أخرى"]
            )
            quantity = st.number_input("الكمية", min_value=1, step=1, value=100)
            unit = st.selectbox("الوحدة", ["كيلو", "صندوق", "حبة", "كيس", "طرد"])
            
        with col2:
            price = st.number_input("السعر للوحدة (شلن)", min_value=100, step=1000, value=5000)
            location = st.text_input("الموقع", value=st.session_state.user_village)
        
        description = st.text_area("وصف المنتج", placeholder="جودة طازجة، منتج عضوي، ...")
        
        if st.button("✅ نشر المنتج", type="primary", use_container_width=True):
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
                
                st.success("✅ تم نشر المنتج بنجاح!")
                st.balloons()
            else:
                st.error("❌ الرجاء إدخال اسمك ورقم هاتفك أولاً")

# ==================== TAB للمشتري: بحث عن منتجات ====================
if st.session_state.user_type == "buyer":
    with tab1:
        st.subheader("🔍 ابحث عن منتجات")
        
        products = load_data(PRODUCTS_FILE)
        available_products = [p for p in products if p.get("status") == "available"]
        
        if available_products:
            # فلترة حسب النوع
            product_types = list(set([p["product"] for p in available_products]))
            selected_type = st.selectbox("نوع المنتج", ["الكل"] + product_types)
            
            # فلترة حسب المنطقة
            locations = list(set([p.get("location", "غير معروف") for p in available_products]))
            selected_location = st.selectbox("المنطقة", ["الكل"] + locations)
            
            # تطبيق الفلترة
            filtered = available_products.copy()
            
            if selected_type != "الكل":
                filtered = [p for p in filtered if p["product"] == selected_type]
            
            if selected_location != "الكل":
                filtered = [p for p in filtered if p.get("location") == selected_location]
            
            st.markdown(f"**تم العثور على {len(filtered)} منتج**")
            
            # عرض المنتجات
            for product in filtered:
                with st.container():
                    st.markdown(f"""
                    <div class='product-card'>
                        <h4>{product['product']} - {product['quantity']} {product['unit']}</h4>
                        <p class='price'>{product['price']:,} شلن للوحدة</p>
                        <p>👨‍🌾 {product['farmer_name']} - {product.get('location', 'غير معروف')}</p>
                        <p>📞 {product['farmer_phone']}</p>
                        <p>{product.get('description', '')}</p>
                        <p>📅 {product['date'][:10]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🛒 أريد شراء هذا المنتج", key=f"buy_{product['id']}"):
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
                                "quantity": product["quantity"],
                                "unit": product["unit"],
                                "date": datetime.now().isoformat(),
                                "status": "pending"
                            }
                            
                            orders = load_data(ORDERS_FILE)
                            orders.append(order)
                            save_data(ORDERS_FILE, orders)
                            
                            st.success("✅ تم إرسال طلبك! المزارع سيتصل بك قريباً.")
                        else:
                            st.error("❌ الرجاء إدخال اسمك ورقم هاتفك أولاً")
        else:
            st.info("📭 لا توجد منتجات متاحة حالياً")

# ==================== TAB مشترك: عرض المنتجات ====================
with tab2:
    if st.session_state.user_type == "farmer":
        st.subheader("📋 منتجاتي")
        products = load_data(PRODUCTS_FILE)
        my_products = [p for p in products if p.get("farmer_name") == st.session_state.user_name]
        
        if my_products:
            for p in my_products:
                status_color = "🟢" if p.get("status") == "available" else "🔴"
                st.markdown(f"""
                {status_color} **{p['product']}** - {p['quantity']} {p['unit']} - {p['price']:,} شلن
                """)
        else:
            st.info("📭 لم تنشر أي منتج بعد")
    
    else:  # buyer
        st.subheader("📋 جميع المنتجات")
        products = load_data(PRODUCTS_FILE)
        available = [p for p in products if p.get("status") == "available"]
        
        if available:
            for p in available[:10]:
                st.markdown(f"""
                **{p['product']}** - {p['quantity']} {p['unit']} - {p['price']:,} شلن  
                👨‍🌾 {p['farmer_name']} - 📞 {p['farmer_phone']}
                """)
        else:
            st.info("📭 لا توجد منتجات")

# ==================== TAB الطلبات ====================
with tab3:
    st.subheader("📦 طلباتي")
    
    orders = load_data(ORDERS_FILE)
    
    if st.session_state.user_type == "farmer":
        my_orders = [o for o in orders if o.get("farmer_name") == st.session_state.user_name]
        if my_orders:
            for o in my_orders:
                status_emoji = "⏳" if o["status"] == "pending" else "✅" if o["status"] == "accepted" else "❌"
                st.markdown(f"""
                {status_emoji} **{o['product_name']}** - {o['quantity']} {o['unit']}  
                👤 المشتري: {o['buyer_name']} - 📞 {o['buyer_phone']}  
                """)
                
                if o["status"] == "pending":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ قبول", key=f"acc_{o['id']}"):
                            for ord in orders:
                                if ord["id"] == o["id"]:
                                    ord["status"] = "accepted"
                            save_data(ORDERS_FILE, orders)
                            st.rerun()
                    with col2:
                        if st.button(f"❌ رفض", key=f"rej_{o['id']}"):
                            for ord in orders:
                                if ord["id"] == o["id"]:
                                    ord["status"] = "rejected"
                            save_data(ORDERS_FILE, orders)
                            st.rerun()
        else:
            st.info("📭 لا توجد طلبات")
    
    else:  # buyer
        my_orders = [o for o in orders if o.get("buyer_name") == st.session_state.user_name]
        if my_orders:
            for o in my_orders:
                status_emoji = "⏳" if o["status"] == "pending" else "✅" if o["status"] == "accepted" else "❌"
                st.markdown(f"""
                {status_emoji} **{o['product_name']}** - {o['quantity']} {o['unit']}  
                👨‍🌾 المزارع: {o['farmer_name']} - 📞 {o['farmer_phone']}  
                الحالة: {o['status']}
                """)
        else:
            st.info("📭 لم ترسل أي طلب بعد")

# ==================== شريط جانبي ====================
with st.sidebar:
    st.markdown("### 👤 معلوماتك")
    st.markdown(f"**الاسم:** {st.session_state.user_name or 'غير مسجل'}")
    st.markdown(f"**الهاتف:** {st.session_state.user_phone or 'غير مسجل'}")
    st.markdown(f"**المنطقة:** {st.session_state.user_village or 'غير مسجل'}")
    
    st.markdown("---")
    st.markdown("### ℹ️ عن التطبيق")
    st.markdown("""
    **SOKO LINK** يربط المزارعين بالتجار مباشرة:
    - ✅ بدون وسطاء
    - ✅ عمولة 5% فقط
    - ✅ دفع آمن عبر Mobile Money
    """)
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    products = load_data(PRODUCTS_FILE)
    st.metric("منتجات متاحة", len([p for p in products if p.get("status") == "available"]))

# ==================== تذييل ====================
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>© 2026 SOKO LINK - سوق المزارعين</p>", unsafe_allow_html=True)
