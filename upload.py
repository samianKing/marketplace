import streamlit as st
from PIL import Image
import base64
import io

# --- App Config ---
st.set_page_config(page_title="Simple Marketplace", page_icon="🛍️", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #008b8b;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #ff7f50;
            font-size: 20px;
            margin-bottom: 40px;
        }
        .item-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .upload-section {
            background-color: #e0f7fa;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown('<div class="title">🛒 Sell It!</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload and showcase your items for sale easily</div>', unsafe_allow_html=True)

# --- Session to store uploaded items ---
if "items" not in st.session_state:
    st.session_state["items"] = []

# --- Upload Section ---
with st.container():
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📤 Upload Your Item")

    name = st.text_input("Item Name")
    price = st.number_input("Price ($)", min_value=0.0, step=0.5)
    description = st.text_area("Description", height=80)
    uploaded_file = st.file_uploader("Upload Item Image", type=["jpg", "jpeg", "png"])

    submit = st.button("Add Item")

    if submit:
        if name and price and uploaded_file:
            image = Image.open(uploaded_file)
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()

            st.session_state["items"].append({
                "name": name,
                "price": price,
                "desc": description,
                "image": img_base64
            })
            st.success(f"✅ '{name}' has been added successfully!")
        else:
            st.error("Please fill all fields and upload an image before submitting.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Display Uploaded Items ---
st.subheader("🧺 Items for Sale")

if st.session_state["items"]:
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state["items"]):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class="item-card">
                <img src="data:image/png;base64,{item['image']}" width="100%" style="border-radius:10px;">
                <h4 style="color:#008b8b; margin-top:10px;">{item['name']}</h4>
                <p style="color:#555;">{item['desc']}</p>
                <h5 style="color:#ff7f50;">${item['price']}</h5>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No items uploaded yet. Add your first item above! 🛍️")
