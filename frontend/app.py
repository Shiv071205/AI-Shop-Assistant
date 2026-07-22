import streamlit as st
import requests

st.set_page_config(page_title="🛍️ Shop Assistant", layout="wide")

BACKEND_URL = "https://ai-shop-assistant-4uo2.onrender.com"

# ----------------------------
# Session State
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# Sidebar Chat
# ----------------------------
st.sidebar.title("💬 Shop Assistant Chat")
st.sidebar.write("Ask anything about our products.")

for msg in st.session_state.chat_history:
    if msg.startswith("User:"):
        st.sidebar.markdown(
            f"<p style='color:#1E88E5'><b>{msg}</b></p>",
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown(
            f"<p style='color:#2E7D32'><b>{msg}</b></p>",
            unsafe_allow_html=True,
        )

user_query = st.sidebar.text_input("Your Question")

if st.sidebar.button("Send"):
    if user_query.strip():
        try:
            res = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "query": user_query,
                    "history": st.session_state.chat_history,
                },
            )

            if res.status_code == 200:
                data = res.json()
                st.session_state.chat_history = data.get("history", [])
                st.rerun()
            else:
                st.sidebar.error("Chat request failed.")

        except Exception as e:
            st.sidebar.error(str(e))

# ----------------------------
# Main Page
# ----------------------------
st.title("🛒 Shop Product Catalog")
st.divider()

# ----------------------------
# Get Products
# ----------------------------
try:
    response = requests.get(f"{BACKEND_URL}/products")

    if response.status_code != 200:
        st.error("Unable to fetch products.")
        st.stop()

    data = response.json()

    # YOUR BACKEND RETURNS {"products":[...]}
    products = data.get("products", [])

    if len(products) == 0:
        st.warning("No products found.")
        st.stop()

except Exception as e:
    st.error(f"Backend Error : {e}")
    st.stop()

# ----------------------------
# Filters
# ----------------------------
brands = sorted(
    {
        p.get("ProductBrand", "")
        for p in products
        if p.get("ProductBrand")
    }
)

genders = sorted(
    {
        p.get("Gender", "")
        for p in products
        if p.get("Gender")
    }
)

st.subheader("🔍 Filter Products")

c1, c2, c3 = st.columns(3)

with c1:
    selected_brand = st.selectbox("Brand", ["All"] + brands)

with c2:
    selected_gender = st.selectbox("Gender", ["All"] + genders)

with c3:
    sort_order = st.selectbox(
        "Sort Price",
        ["Default", "Low to High", "High to Low"],
    )

filtered = products.copy()

if selected_brand != "All":
    filtered = [
        p
        for p in filtered
        if p.get("ProductBrand") == selected_brand
    ]

if selected_gender != "All":
    filtered = [
        p
        for p in filtered
        if p.get("Gender") == selected_gender
    ]

if sort_order == "Low to High":
    filtered = sorted(
        filtered,
        key=lambda x: float(x.get("Price", 0)),
    )

elif sort_order == "High to Low":
    filtered = sorted(
        filtered,
        key=lambda x: float(x.get("Price", 0)),
        reverse=True,
    )

# ----------------------------
# CSS
# ----------------------------
st.markdown(
    """
<style>

.product-card{
background:rgba(255,255,255,.05);
border-radius:15px;
padding:18px;
margin-bottom:18px;
border:1px solid #444;
box-shadow:0 4px 10px rgba(0,0,0,.2);
}

.product-title{
font-size:22px;
font-weight:bold;
color:#FFFFFF;
margin-bottom:8px;
}

.product-meta{
font-size:15px;
color:#DDDDDD;
margin-bottom:6px;
}

.product-desc{
font-size:14px;
color:#CCCCCC;
margin-top:10px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Display Products
# ----------------------------
cols = st.columns(2)

for i, product in enumerate(filtered):

    with cols[i % 2]:

        st.markdown(
            f"""
<div class="product-card">

<div class="product-title">
{product.get("ProductName","N/A")}
</div>

<div class="product-meta">
<b>Brand:</b> {product.get("ProductBrand","N/A")}
</div>

<div class="product-meta">
<b>Gender:</b> {product.get("Gender","N/A")}
</div>

<div class="product-meta">
<b>Price:</b> ₹{product.get("Price","N/A")}
</div>

<div class="product-meta">
<b>Color:</b> {product.get("PrimaryColor","N/A")}
</div>

<div class="product-desc">
{product.get("Description","No Description")}
</div>

</div>
""",
            unsafe_allow_html=True,
        )