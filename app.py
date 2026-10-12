import streamlit as st
import sqlite3
import json
import uuid
import os
from datetime import datetime
from pathlib import Path

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "sodapop.db"

st.set_page_config(page_title="SodaPop | Fizzy happiness", page_icon="🥤", layout="wide", initial_sidebar_state="collapsed")

# ---------- Database ----------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

DRINKS = [
    ("classic-cola", "Classic Cola", "The timeless cola with a crisp, bubbly finish.", "Classics", 250, "🥤", "#ff5a5f", 1, "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?auto=format&fit=crop&w=900&q=85"),
    ("lemon-lime", "Lemon Lime Fizz", "Bright citrus and a sparkling, refreshing finish.", "Classics", 230, "🍋", "#b7e66b", 1, "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?auto=format&fit=crop&w=900&q=85"),
    ("orange-pop", "Orange Pop", "Sunny orange flavour with lively bubbles.", "Classics", 230, "🍊", "#ffb347", 1, "https://images.unsplash.com/photo-1547514701-42782101795e?auto=format&fit=crop&w=900&q=85"),
    ("berry-blast", "Berry Blast", "Sweet berry fizz with a colourful twist.", "Signature", 320, "🫐", "#a88bfa", 1, "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=900&q=85"),
    ("strawberry-spark", "Strawberry Spark", "Strawberry-inspired sparkle, served ice cold.", "Signature", 320, "🍓", "#ff91b5", 1, "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=900&q=85"),
    ("mango-bubble", "Mango Bubble", "Tropical mango flavour made for sunny days.", "Signature", 300, "🥭", "#ffd166", 1, "https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=900&q=85"),
    ("blue-raspberry", "Blue Raspberry Fizz", "A playful blue raspberry-inspired fizzy drink.", "Signature", 320, "🧊", "#80d8ff", 1, "https://images.unsplash.com/photo-1536935338788846bb9981813?auto=format&fit=crop&w=900&q=85"),
    ("vanilla-cola", "Vanilla Cola", "Smooth vanilla notes meet classic cola.", "Specials", 350, "✨", "#d7b8ff", 1, "https://images.unsplash.com/photo-1581636625402-29b2a704ef13?auto=format&fit=crop&w=900&q=85"),
    ("lime-mint", "Mint Lime Cooler", "Lime, mint, and a cool sparkling finish.", "Lemonades", 350, "🌿", "#9be7a5", 1, "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?auto=format&fit=crop&w=900&q=85"),
    ("classic-lemonade", "Classic Lemonade", "Fresh lemon flavour with a bright, tangy finish.", "Lemonades", 280, "🍋", "#ffe27a", 1, "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?auto=format&fit=crop&w=900&q=85"),
    ("strawberry-lemonade", "Strawberry Lemonade", "Sweet strawberry meets zesty lemonade.", "Lemonades", 330, "🍓", "#ff9ab7", 1, "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=900&q=85"),
    ("blueberry-lemonade", "Blueberry Lemonade", "A berry twist on a citrus favourite.", "Lemonades", 340, "🫐", "#a9a1ff", 1, "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=900&q=85"),
    ("watermelon-fizz", "Watermelon Fizz", "Juicy watermelon-inspired refreshment with bubbles.", "Fruit Fizz", 320, "🍉", "#ff8f9b", 1, "https://images.unsplash.com/photo-1527761939622-911a6c9c6c2c?auto=format&fit=crop&w=900&q=85"),
    ("pineapple-pop", "Pineapple Pop", "Tropical pineapple flavour with a fizzy lift.", "Fruit Fizz", 320, "🍍", "#ffd166", 1, "https://images.unsplash.com/photo-1587883012610-e3df17d41270?auto=format&fit=crop&w=900&q=85"),
    ("peach-fizz", "Peach Fizz", "Soft peach flavour in a sparkling cooler.", "Fruit Fizz", 330, "🍑", "#ffc4a3", 1, "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=85"),
    ("grape-spark", "Grape Spark", "Bold grape flavour with a bubbly finish.", "Fruit Fizz", 310, "🍇", "#c7a2ff", 1, "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=900&q=85"),
    # Newly Added Flavours
    ("green-apple-splash", "Green Apple Splash", "Tart, crisp green apple flavour with effervescent bubbles.", "Fruit Fizz", 310, "🍏", "#b5e7a0", 1, "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=900&q=85"),
    ("passionfruit-spark", "Passionfruit Spark", "Exotic and tangy passionfruit notes with extra fizz.", "Fruit Fizz", 340, "🧡", "#ffab76", 1, "https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=900&q=85"),
    ("cherry-cola-bliss", "Cherry Cola Bliss", "Classic cola infused with sweet black cherry syrup.", "Specials", 360, "🍒", "#ff6b81", 1, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=900&q=85"),
    ("tropical-sunset", "Tropical Sunset Mocktail", "A sparkling blend of orange, pineapple, and grenadine.", "Specials", 390, "🌅", "#ff9f43", 1, "https://images.unsplash.com/photo-1536935338788846bb9981813?auto=format&fit=crop&w=900&q=85"),
    ("cucumber-mint-cooler", "Cucumber Mint Cooler", "Super crisp cucumber, fresh mint, and sparkling soda.", "Lemonades", 330, "🥒", "#a8e6cf", 1, "https://images.unsplash.com/photo-1513558161293-cdaf765edfd7?auto=format&fit=crop&w=900&q=85"),
    ("ruby-pomegranate-fizz", "Ruby Pomegranate Fizz", "Rich pomegranate flavor with a tart, sparkling twist.", "Signature", 350, "🍷", "#e84393", 1, "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=900&q=85"),
    ("party-pack", "SodaPop Party Pack", "Four classic drinks for sharing with friends.", "Bundles", 850, "🎉", "#ffcf70", 1, "https://images.unsplash.com/photo-1536935338788846bb9981813?auto=format&fit=crop&w=900&q=85"),
    ("ultimate-fizz-bundle", "Ultimate Fizz Bundle", "Six assorted signature fruit fizz and lemonade drinks.", "Bundles", 1250, "🎁", "#fdcb6e", 1, "https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=900&q=85"),
]

def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, order_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL, customer_name TEXT NOT NULL, phone TEXT NOT NULL,
            address TEXT NOT NULL, payment_method TEXT NOT NULL, items_json TEXT NOT NULL,
            subtotal REAL NOT NULL, delivery_fee REAL NOT NULL, total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Received'
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS menu (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL,
            category TEXT NOT NULL, price REAL NOT NULL, emoji TEXT NOT NULL,
            color TEXT NOT NULL, available INTEGER NOT NULL DEFAULT 1, image_url TEXT DEFAULT ''
        )""")
        columns = [row[1] for row in conn.execute("PRAGMA table_info(menu)").fetchall()]
        if "image_url" not in columns:
            conn.execute("ALTER TABLE menu ADD COLUMN image_url TEXT DEFAULT ''")
        count = conn.execute("SELECT COUNT(*) FROM menu").fetchone()[0]
        if count == 0:
            conn.executemany("INSERT INTO menu (id,name,description,category,price,emoji,color,available,image_url) VALUES (?,?,?,?,?,?,?,?,?)", DRINKS)
        else:
            conn.executemany("INSERT OR IGNORE INTO menu (id,name,description,category,price,emoji,color,available,image_url) VALUES (?,?,?,?,?,?,?,?,?)", DRINKS)
            for drink in DRINKS:
                conn.execute("UPDATE menu SET image_url=? WHERE id=? AND (image_url IS NULL OR image_url='')", (drink[8], drink[0]))

def read_menu(available_only=True):
    with get_conn() as conn:
        query = "SELECT * FROM menu" + (" WHERE available=1" if available_only else "") + " ORDER BY category, name"
        return [dict(row) for row in conn.execute(query).fetchall()]

def read_orders():
    with get_conn() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()]

def money(value):
    return f"Rs {value:,.0f}"

def owner_password():
    env_password = os.environ.get("OWNER_PASSWORD")
    if env_password:
        return env_password
    try:
        secret_password = st.secrets.get("OWNER_PASSWORD")
        if secret_password:
            return str(secret_password)
    except Exception:
        pass
    return "sodapop123"

init_db()

# ---------- Style ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fredoka:wght@500;600;700&display=swap');
:root { --ink:#20213a; --muted:#77788f; --pink:#ff5b73; --orange:#ff9f43; --cream:#fffaf4; }
.stApp { background:#fffaf5; color:var(--ink); font-family:'DM Sans',sans-serif; }
.block-container { max-width:1240px; padding-top:1rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Fredoka',sans-serif !important; color:var(--ink); }
div[data-testid="stMetric"] { background:white; padding:18px; border:1px solid #f2e7e2; border-radius:18px; box-shadow:0 5px 18px #3b263b08; }
div.stButton > button { border-radius:12px; border:0; background:linear-gradient(100deg,#ff5b73,#ff8b61); color:white; font-weight:700; min-height:40px; transition:transform .15s ease; }
div.stButton > button:hover { color:white; transform:translateY(-1px); border:0; box-shadow:0 6px 16px #ff5b7330; }
div[data-testid="stFormSubmitButton"] button { background:linear-gradient(100deg,#ff5b73,#ff8b61); color:white; border-radius:12px; border:0; font-weight:700; }
.soda-logo { font-family:'Fredoka',sans-serif; font-size:2.25rem; font-weight:700; letter-spacing:-1px; color:#24233c; }
.soda-logo span { color:#ff5b73; }
.tagline { color:#85839a; margin-top:-7px; }
.hero { background:linear-gradient(115deg,#ffdfd5 0%,#ffe9b9 48%,#dff7ee 100%); border-radius:28px; padding:32px 34px; overflow:hidden; margin:12px 0 24px; box-shadow:0 8px 24px rgba(255, 91, 115, 0.1); }
.hero h1 { font-size:clamp(2.1rem,4vw,3.5rem); line-height:1.02; margin:0 0 12px; }
.hero p { max-width:510px; color:#55536b; font-size:1.05rem; }
.hero-bubbles { font-size:5rem; text-align:center; filter:drop-shadow(0 12px 8px #9b536222); }
.eyebrow { text-transform:uppercase; letter-spacing:2px; color:#e45169; font-size:.75rem; font-weight:700; }
.drink-card { background:white; border:1px solid #f2e7e2; border-radius:20px; padding:14px; box-shadow:0 6px 20px #39283d08; transition: transform 0.2s ease; }
.drink-card:hover { transform: translateY(-3px); box-shadow:0 10px 25px #39283d12; }
.drink-art { border-radius:16px; height:175px; overflow:hidden; margin-bottom:13px; background:#fff0ed; }
.drink-art img { width:100%; height:175px; object-fit:cover; display:block; }
.drink-name { font-family:'Fredoka',sans-serif; font-size:1.22rem; font-weight:600; }
.drink-desc { color:#85839a; font-size:.88rem; min-height:42px; }
.price { font-size:1.2rem; font-weight:700; color:#ff5b73; }
.pill { display:inline-block; padding:5px 10px; border-radius:99px; background:#fff0ed; color:#e45169; font-size:.72rem; font-weight:700; }
.info-strip { background:white; border:1px solid #f2e7e2; border-radius:18px; padding:16px; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.02); }
.footer { text-align:center; color:#9693a4; padding:28px 0 8px; font-size:.85rem; }
@media (max-width:700px) { .hero { padding:22px 18px; } .hero-bubbles { font-size:3rem; } .drink-art,.drink-art img { height:140px; } }
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "cart" not in st.session_state: st.session_state.cart = {}
if "page" not in st.session_state: st.session_state.page = "Shop"
if "last_order" not in st.session_state: st.session_state.last_order = None
if "tracked_order" not in st.session_state: st.session_state.tracked_order = None
if "owner_logged_in" not in st.session_state: st.session_state.owner_logged_in = False

menu = read_menu()

# ---------- Header and navigation ----------
st.markdown('<div class="soda-logo">Soda<span>Pop</span> 🥤</div><div class="tagline">A little fizz. A lot of happy.</div>', unsafe_allow_html=True)
st.write("")
cart_count = sum(x["qty"] for x in st.session_state.cart.values())
nav_items = [("Shop", "🛍️ Shop"), ("Menu", "🥤 Menu"), ("Cart", f"🛒 Cart ({cart_count})"), ("Track", "📦 Track Order"), ("Owner", "🔐 Admin")]
nav_cols = st.columns(5, gap="small")
for col, (page_key, label) in zip(nav_cols, nav_items):
    with col:
        if st.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.rerun()
st.markdown("---")

def cart_add(item, size, ice, qty, extra):
    key = f"{item['id']}|{size}|{ice}|{extra}"
    unit_price = float(item["price"]) + {"Regular": 0, "Large": 100, "Party size": 180}[size] + (50 if extra != "None" else 0)
    if key in st.session_state.cart:
        st.session_state.cart[key]["qty"] += qty
    else:
        st.session_state.cart[key] = {"key":key, "id":item["id"], "name":item["name"], "emoji":item["emoji"], "size":size, "ice":ice, "extra":extra, "qty":qty, "unit_price":unit_price}

def calculate_totals():
    subtotal = sum(v["qty"] * v["unit_price"] for v in st.session_state.cart.values())
    delivery = 150 if subtotal > 0 else 0
    return subtotal, delivery, subtotal + delivery

def render_drinks(drinks):
    if not drinks:
        st.info("No drinks found matching your criteria.")
        return
    for start in range(0, len(drinks), 3):
        cols = st.columns(3, gap="large")
        for col, item in zip(cols, drinks[start:start+3]):
            with col:
                image_url = item.get("image_url") or ""
                if image_url:
                    st.markdown(f'''<div class="drink-card"><div class="drink-art"><img src="{image_url}" alt="{item['name']}" onerror="this.style.display='none'"></div><div class="pill">{item['category']}</div><div class="drink-name">{item['emoji']} {item['name']}</div><div class="drink-desc">{item['description']}</div><div class="price">{money(item['price'])}</div></div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''<div class="drink-card"><div class="drink-art" style="display:flex;align-items:center;justify-content:center;font-size:4rem;background:{item['color']}25">{item['emoji']}</div><div class="pill">{item['category']}</div><div class="drink-name">{item['name']}</div><div class="drink-desc">{item['description']}</div><div class="price">{money(item['price'])}</div></div>''', unsafe_allow_html=True)
                with st.expander(f"Customize {item['name']}"):
                    size = st.selectbox("Size", ["Regular", "Large", "Party size"], key=f"size_{item['id']}")
                    ice = st.selectbox("Ice level", ["Regular ice", "Extra ice", "Light ice", "No ice"], key=f"ice_{item['id']}")
                    extra = st.selectbox("Extra flavour", ["None", "Lemon shot (+Rs 50)", "Mint shot (+Rs 50)"], key=f"extra_{item['id']}")
                    qty = st.number_input("Quantity", min_value=1, max_value=20, value=1, key=f"qty_{item['id']}")
                    if st.button("Add to cart +", key=f"add_{item['id']}", use_container_width=True):
                        cart_add(item, size, ice, int(qty), extra)
                        st.success(f"{item['name']} added to your cart!")

# ---------- Shop ----------
if st.session_state.page == "Shop":
    st.markdown('''<div class="hero"><div class="eyebrow">YOUR HAPPY PLACE FOR FIZZ</div><div style="display:grid;grid-template-columns:1.6fr 1fr;align-items:center;gap:12px"><div><h1>Pop open<br>something happy.</h1><p>Bright flavours, big bubbles, and ice-cold refreshment delivered right to your door.</p></div><div class="hero-bubbles">🥤 🍊 🫧</div></div></div>''', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    with a: st.markdown('<div class="info-strip">🧊<br><b>Made to refresh</b><br><small>Choose your ice level</small></div>', unsafe_allow_html=True)
    with b: st.markdown('<div class="info-strip">🚲<br><b>Doorstep delivery</b><br><small>Flat Rs 150 delivery</small></div>', unsafe_allow_html=True)
    with c: st.markdown('<div class="info-strip">💖<br><b>Good vibes only</b><br><small>Find your new favourite</small></div>', unsafe_allow_html=True)
    st.write("")
    st.markdown("## ⭐ Best sellers")
    featured = [x for x in menu if x["id"] in {"classic-cola", "strawberry-lemonade", "mango-bubble", "tropical-sunset"}]
    render_drinks(featured)
    if st.button("Explore the full menu →", use_container_width=True):
        st.session_state.page = "Menu"
        st.rerun()
    st.markdown('<div class="footer">Made with bubbles and good vibes · SodaPop</div>', unsafe_allow_html=True)

# ---------- Full menu ----------
elif st.session_state.page == "Menu":
    st.markdown("## 🥤 The SodaPop menu")
    st.caption("From classic colas to gourmet fruit fizzes, mocktails, and fresh lemonades.")
    search = st.text_input("Search drinks", placeholder="Try mango, cola, mojito, passionfruit…")
    categories = ["All drinks"] + sorted(set(item["category"] for item in menu))
    chosen_category = st.radio("Choose a category", categories, horizontal=True, label_visibility="collapsed")
    shown = [x for x in menu if (chosen_category == "All drinks" or x["category"] == chosen_category) and search.lower() in (x["name"] + " " + x["description"]).lower()]
    render_drinks(shown)

# ---------- Cart / checkout ----------
elif st.session_state.page == "Cart":
    st.markdown("## 🛒 Your cart")
    st.caption("Double-check your refreshing selections before checkout.")
    if not st.session_state.cart:
        st.info("Your cart is empty. Head to the Menu and add something fizzy!")
        if st.button("Browse drinks"):
            st.session_state.page = "Menu"; st.rerun()
    else:
        for key, item in list(st.session_state.cart.items()):
            with st.container(border=True):
                left, mid, right = st.columns([3, 2, 1])
                with left:
                    st.markdown(f"**{item['emoji']} {item['name']}**")
                    st.caption(f"{item['size']} · {item['ice']} · Extra: {item['extra']}")
                with mid:
                    st.write(f"{money(item['unit_price'])} × {item['qty']}")
                    new_qty = st.number_input("Quantity (0 removes item)", min_value=0, max_value=20, value=int(item["qty"]), key=f"cartqty_{key}")
                with right:
                    st.markdown(f"**{money(item['unit_price']*item['qty'])}**")
                    if st.button("Remove", key=f"remove_{key}"):
                        del st.session_state.cart[key]; st.rerun()
                if new_qty != item["qty"]:
                    if new_qty == 0: del st.session_state.cart[key]
                    else: st.session_state.cart[key]["qty"] = int(new_qty)
                    st.rerun()
        subtotal, delivery, total = calculate_totals()
        left, right = st.columns([1.2, 1])
        with right:
            with st.container(border=True):
                st.markdown("### Order summary")
                st.write("Subtotal", money(subtotal))
                st.write("Delivery", money(delivery))
                st.markdown(f"### Total: {money(total)}")
        with left:
            st.markdown("### 🚚 Delivery details")
            with st.form("checkout_form"):
                name = st.text_input("Full name")
                phone = st.text_input("Phone number", placeholder="03XX XXXXXXX")
                address = st.text_area("Delivery address", placeholder="House, street, area, city")
                payment = st.radio("Payment method", ["Cash on delivery", "Online payment (manual confirmation)"], help="Online payments are verified manually upon dispatch.")
                online_reference = st.text_input("Online payment reference (optional)", placeholder="Transaction ID, if already paid") if payment.startswith("Online") else ""
                notes = st.text_area("Order note (optional)", placeholder="Ring doorbell, extra napkins, etc.")
                submitted = st.form_submit_button(f"Place order · {money(total)}", use_container_width=True)
            if submitted:
                if not name.strip() or not phone.strip() or not address.strip():
                    st.error("Please enter your name, phone number, and delivery address.")
                elif len(phone.strip()) < 7:
                    st.error("Please enter a valid phone number.")
                else:
                    order_code = "SP" + uuid.uuid4().hex[:7].upper()
                    items_payload = []
                    for item in st.session_state.cart.values():
                        payload = dict(item)
                        if notes.strip(): payload["order_note"] = notes.strip()
                        if online_reference.strip(): payload["payment_reference"] = online_reference.strip()
                        items_payload.append(payload)
                    with get_conn() as conn:
                        conn.execute("INSERT INTO orders (order_code,created_at,customer_name,phone,address,payment_method,items_json,subtotal,delivery_fee,total,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (order_code, datetime.now().strftime("%Y-%m-%d %H:%M"), name.strip(), phone.strip(), address.strip(), payment, json.dumps(items_payload), subtotal, delivery, total, "Received"))
                    st.session_state.cart = {}
                    st.session_state.last_order = order_code
                    st.session_state.tracked_order = None
                    st.session_state.page = "Track"
                    st.rerun()

# ---------- Track order ----------
elif st.session_state.page == "Track":
    st.markdown("## 📦 Track your order")
    if st.session_state.last_order:
        st.success(f"Your latest order number is **{st.session_state.last_order}**. Save it to check progress later.")
    code = st.text_input("Enter your order number", value=st.session_state.last_order or "", placeholder="e.g. SP12AB34")
    if st.button("Find order"):
        match = next((o for o in read_orders() if o["order_code"].lower() == code.strip().lower()), None)
        st.session_state.tracked_order = match
        if not match: st.error("We couldn't find that order number. Check it and try again.")
    tracked = st.session_state.get("tracked_order")
    if tracked and code.strip().lower() == tracked["order_code"].lower():
        st.markdown(f"### Order {tracked['order_code']}")
        st.markdown(f"**Status:** `{tracked['status']}`")
        st.write(f"Placed: {tracked['created_at']}")
        st.write(f"Payment: {tracked['payment_method']}")
        for item in json.loads(tracked["items_json"]):
            st.write(f"{item['emoji']} {item['name']} · {item['size']} × {item['qty']} — {money(item['unit_price']*item['qty'])}")
        st.write(f"**Total: {money(tracked['total'])}**")
        st.caption("For privacy, share your order number only with people you trust.")

# ---------- Admin dashboard ----------
elif st.session_state.page == "Owner":
    st.markdown("## 🔐 SodaPop admin dashboard")
    st.caption("Manage incoming orders, menu items, and sales.")
    if not st.session_state.owner_logged_in:
        with st.form("owner_login"):
            password = st.text_input("Admin password", type="password")
            login = st.form_submit_button("Sign in", use_container_width=True)
        if login:
            if password == owner_password():
                st.session_state.owner_logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    else:
        _, logout_col = st.columns([4, 1])
        with logout_col:
            if st.button("Sign out", use_container_width=True):
                st.session_state.owner_logged_in = False; st.rerun()
        orders = read_orders()
        total_sales = sum(o["total"] for o in orders if o["status"] != "Cancelled")
        pending = sum(o["status"] in ["Received", "Preparing"] for o in orders)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Orders", len(orders)); m2.metric("Sales value", money(total_sales)); m3.metric("Needs attention", pending); m4.metric("Menu items", len(read_menu(False)))
        tab_orders, tab_menu = st.tabs(["📋 Orders", "🥤 Menu manager"])
        with tab_orders:
            if not orders: st.info("No orders yet. New orders will appear here.")
            for order in orders:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.markdown(f"**{order['order_code']} · {order['customer_name']}**")
                        st.caption(f"{order['created_at']} · {order['phone']}")
                        st.write(order["address"])
                    with c2:
                        for item in json.loads(order["items_json"]): st.write(f"{item['emoji']} {item['name']} × {item['qty']}")
                        st.caption(f"{order['payment_method']} · {money(order['total'])}")
                    with c3:
                        statuses = ["Received", "Preparing", "Ready", "Completed", "Cancelled"]
                        current = order["status"] if order["status"] in statuses else "Received"
                        new_status = st.selectbox("Status", statuses, index=statuses.index(current), key=f"status_{order['order_code']}")
                        if st.button("Save status", key=f"save_{order['order_code']}", use_container_width=True):
                            with get_conn() as conn: conn.execute("UPDATE orders SET status=? WHERE order_code=?", (new_status, order["order_code"]))
                            st.success("Status updated."); st.rerun()
        with tab_menu:
            items = read_menu(False)
            st.markdown("### Update a drink")
            if items:
                selected_id = st.selectbox("Select drink", [x["id"] for x in items], format_func=lambda i: next(x["name"] for x in items if x["id"] == i))
                selected = next(x for x in items if x["id"] == selected_id)
                with st.form("edit_menu"):
                    edit_name = st.text_input("Name", selected["name"])
                    edit_desc = st.text_area("Description", selected["description"])
                    category_options = ["Classics", "Signature", "Specials", "Lemonades", "Fruit Fizz", "Bundles"]
                    current_cat = selected["category"] if selected["category"] in category_options else "Classics"
                    edit_category = st.selectbox("Category", category_options, index=category_options.index(current_cat))
                    edit_price = st.number_input("Price (PKR)", min_value=1.0, value=float(selected["price"]), step=10.0)
                    edit_emoji = st.text_input("Emoji", selected["emoji"])
                    edit_image = st.text_input("Image URL", selected.get("image_url") or "")
                    edit_available = st.checkbox("Available for customers", value=bool(selected["available"]))
                    save_menu = st.form_submit_button("Save drink")
                if save_menu:
                    if not edit_name.strip(): st.error("Drink name cannot be empty.")
                    else:
                        with get_conn() as conn:
                            conn.execute("UPDATE menu SET name=?,description=?,category=?,price=?,emoji=?,image_url=?,available=? WHERE id=?", (edit_name.strip(), edit_desc.strip(), edit_category, edit_price, edit_emoji.strip() or "🥤", edit_image.strip(), int(edit_available), selected_id))
                        st.success("Drink updated."); st.rerun()
            st.markdown("### Add a new drink")
            with st.form("add_menu"):
                new_id = st.text_input("Unique ID (letters/numbers/hyphens)", placeholder="passionfruit-fizz")
                new_name = st.text_input("Drink name")
                new_desc = st.text_input("Description")
                n1, n2, n3 = st.columns(3)
                with n1: new_category = st.selectbox("Category", ["Classics", "Signature", "Specials", "Lemonades", "Fruit Fizz", "Bundles"], key="newcat")
                with n2: new_price = st.number_input("Price (PKR)", min_value=1.0, value=250.0, step=10.0, key="newprice")
                with n3: new_emoji = st.selectbox("Icon", ["🥤", "🍋", "🍊", "🫐", "🍓", "🥭", "🍉", "🍍", "🍑", "🍇", "🍏", "🍒", "🌅", "🥒", "🍷", "✨", "🌿", "🎉", "🎁"], key="newemoji")
                new_image = st.text_input("Image URL (optional)", placeholder="https://...")
                add_drink = st.form_submit_button("Add drink")
            if add_drink:
                clean_id = "".join(ch for ch in new_id.lower().strip() if ch.isalnum() or ch == "-")
                if not clean_id or not new_name.strip(): st.error("Enter a unique ID and drink name.")
                else:
                    try:
                        with get_conn() as conn:
                            conn.execute("INSERT INTO menu (id,name,description,category,price,emoji,color,available,image_url) VALUES (?,?,?,?,?,?,?,?,?)", (clean_id, new_name.strip(), new_desc.strip(), new_category, new_price, new_emoji, "#ffb347", 1, new_image.strip()))
                        st.success("Drink added."); st.rerun()
                    except sqlite3.IntegrityError: st.error("That ID already exists. Choose a different one.")

st.markdown("---")
st.caption("SodaPop · Prices in Pakistani Rupees (PKR). Online payment is manual in this version; payments are not collected automatically.")