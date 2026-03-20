import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import random
import string

# ==================== إعدادات الصفحة ====================
st.set_page_config(
    page_title="SOKO LINK - سوق المزارعات",
    page_icon="🌽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== رقم منصة SOKO LINK ====================
SOKO_PHONE = "0777123456"  # ضع رقم M-Pesa الخاص بك هنا

# ==================== دوال مساعدة ====================
def generate_payment_code():
    """توليد رمز فريد للدفع"""
    return "SOKO-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_id():
    return str(uuid.uuid4())[:8].upper()

# ==================== ملفات التخزين ====================
DATA_FOLDER = "soko_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PRODUCTS_FILE = os.path.join(DATA_FOLDER, "products.json")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
ORDERS_FILE = os.path.join(DATA_FOLDER, "orders.json")
TRANSACTIONS_FILE = os.path.join(DATA_FOLDER, "transactions.json")
PAYMENTS_FILE = os.path.join(DATA_FOLDER, "payments.json")

for file in [PRODUCTS_FILE, USERS_FILE, ORDERS_FILE, TRANSACTIONS_FILE, PAYMENTS_FILE]:
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

# ==================== نظام الترجمة ====================
if "language" not in st.session_state:
    st.session_state.language = "ar"

translations = {
    "ar": {
        "app_name": "🌽 سوكو لينك",
        "subtitle": "سوق المزارعات الأوغنديات",
        "welcome": "🇺🇬 مرحباً بك",
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
        "order_sent": "تم إرسال الطلب",
        "no_products": "لا توجد منتجات",
        "women": "👩🏾‍🌾 نساء أوغنديات يبعن منتجات بلدهن 🇺🇬",
        "contact_fee": "رسوم فتح التواصل",
        "unlock_farmer": "🔓 فتح معلومات المزارعة",
        "unlock_buyer": "🔓 فتح معلومات التاجرة",
        "hidden_info": "🔒 معلومات مخفية",
        "click_unlock": "اضغط لفتح المعلومات",
        "payment_code": "رمز الدفع",
        "send_with_code": "أرسل المبلغ مع هذا الرمز",
        "reference": "المرجع",
        "i_have_paid": "✅ لقد قمت بالدفع",
        "waiting_confirmation": "⏳ في انتظار التأكيد",
        "confirmed": "✅ تم التأكيد",
        "admin_panel": "🔧 لوحة التحكم",
        "pending_payments": "دفعات منتظرة للتأكيد",
        "confirm_payment": "تأكيد الدفع"
    },
    "en": {
        "app_name": "🌽 SOKO LINK",
        "subtitle": "Ugandan Women's Market",
        "welcome": "🇺🇬 Welcome",
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
        "order_sent": "Order sent",
        "no_products": "No products",
        "women": "👩🏾‍🌾 Ugandan women selling local products 🇺🇬",
        "contact_fee": "Contact fee",
        "unlock_farmer": "🔓 Unlock farmer info",
        "unlock_buyer": "🔓 Unlock buyer info",
        "hidden_info": "🔒 Hidden info",
        "click_unlock": "Click to unlock",
        "payment_code": "Payment code",
        "send_with_code": "Send payment with this code",
        "reference": "Reference",
        "i_have_paid": "✅ I have paid",
        "waiting_confirmation": "⏳ Waiting confirmation",
        "confirmed": "✅ Confirmed",
        "admin_panel": "🔧 Admin Panel",
        "pending_payments": "Pending Payments",
        "confirm_payment": "Confirm Payment"
    },
    "sw": {
        "app_name": "🌽 SOKO LINK",
        "subtitle": "Soko la Wanawake Uganda",
        "welcome": "🇺🇬 Karibu",
        "farmer": "👩🏾‍🌾 Mkulima",
        "trader": "🛒 Mfany
