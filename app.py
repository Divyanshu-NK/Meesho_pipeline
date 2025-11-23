# app.py  ← FIXED: No max_upload_size error, direct uploads for deployment

import streamlit as st
import openpyxl
from openpyxl.styles import PatternFill
import io
import requests
import base64
import time
from PIL import Image  # For previewing uploaded images

# ——————— Imgur upload (only if images uploaded) ———————
def upload_to_imgur(uploaded_file):
    url = "https://api.imgur.com/3/image"
    try:
        # Read bytes from uploaded file
        bytes_data = uploaded_file.read()
        payload = base64.b64encode(bytes_data)
        headers = {'Authorization': 'Client-ID 546c25a59c58ad7'}
        r = requests.post(url, headers=headers, data=payload)
        if r.status_code == 200:
            return r.json()['data']['link']
        else:
            st.warning(f"Upload failed for {uploaded_file.name}")
            return ""
    except Exception as e:
        st.error(f"Error uploading {uploaded_file.name}: {e}")
        return ""

# ——————— Generate Excel (with or without images) ———————
def generate_excel(rows_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    headers = ["Product Name","Variation","Meesho Price","MRP","GST %",
               "Image Link 1","Image Link 2","Image Link 3","Image Link 4","Image Link 5",
               "Seller SKU","Brand Name","Product ID","Description","HSN Code","Weight (g)","Keywords"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(1, c, h)
        cell.fill = PatternFill("solid", fgColor="FF0000" if c<=10 else "00FF00")
    for r, row in enumerate(rows_data, 2):
        for c, val in enumerate(row, 1):
            ws.cell(r, c, val)
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

# ——————— Initialize variants ———————
if 'variants' not in st.session_state:
    st.session_state.variants = [{"size": "M", "color": "Red"}]

# ——————— Streamlit UI ———————
st.set_page_config(page_title="Meesho Auto for Lucian Traders)", layout="wide")
st.title("Meesho Auto – Upload Images Directly")
st.markdown("**Fill form → (Optional) Upload up to 5 images → Click button → Get Excel with links!**")

# ——————— Optional Image Upload (at top for ease) ———————
uploaded_images = st.file_uploader(
    "Upload Product Images (Optional – up to 5 JPG/PNG)",
    type=['jpg', 'jpeg', 'png'],
    accept_multiple_files=True,
    help="Drag & drop or select files. They'll auto-upload to Imgur for public links."
)

# Preview uploaded images (if any)
if uploaded_images:
    st.info(f"Uploaded {len(uploaded_images)} image(s). Preview below:")
    cols = st.columns(min(5, len(uploaded_images)))
    for idx, img_file in enumerate(uploaded_images[:5]):
        with cols[idx]:
            # Reset file pointer for PIL preview
            img_file.seek(0)
            img = Image.open(img_file)
            st.image(img, caption=img_file.name, width=150)
    st.success("Images ready! They'll get public links in Excel.")

# ——————— Form (only product info) ———————
with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        product_id = st.text_input("Product ID*", "KURTI001")
        name = st.text_input("Product Name*", "Floral Cotton Kurti")
        brand = st.text_input("Brand", "Generic")
        price = st.number_input("Selling Price*", 100, 5000, 399)
        mrp = st.number_input("MRP*", price+1, 10000, 999)
        gst = st.number_input("GST %", 0, 28, 5)

    with col2:
        description = st.text_area("Description*", "Premium quality cotton kurti...")
        keywords = st.text_input("Keywords", "kurti, cotton, women, ethnic")
        hsn = st.text_input("HSN Code", "61091000")
        weight = st.number_input("Weight (g)", 100, 1000, 280)

    submitted = st.form_submit_button("Generate Meesho Excel (Images Optional)")

# ——————— Variants Editor (outside form – no errors) ———————
st.markdown("### Variants")
if st.button("Add Variant"):
    st.session_state.variants.append({"size": "", "color": ""})
    st.rerun()

for i in range(len(st.session_state.variants)):
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        st.session_state.variants[i]["size"] = st.text_input("Size", st.session_state.variants[i]["size"], key=f"s{i}")
    with col2:
        st.session_state.variants[i]["color"] = st.text_input("Color", st.session_state.variants[i]["color"], key=f"c{i}")
    with col3:
        if st.button("Remove", key=f"r{i}"):
            st.session_state.variants.pop(i)
            st.rerun()

# Clean empty variants
st.session_state.variants = [v for v in st.session_state.variants if v.get("size","").strip() and v.get("color","").strip()]
if not st.session_state.variants:
    st.session_state.variants = [{"size": "M", "color": "Red"}]

st.write("**Current variants:**")
for v in st.session_state.variants:
    st.write(f"• {v['size']} | {v['color']}")

# ——————— MAIN GENERATION (when button clicked) ———————
if submitted:
    if not st.session_state.variants:
        st.error("Add at least one variant")
    else:
        public_links = ["", "", "", "", ""]  # Default empty

        # ——— Optional: Upload images if provided ———
        if uploaded_images:
            st.info(f"Uploading {min(5, len(uploaded_images))} images to Imgur...")
            for idx, img_file in enumerate(uploaded_images[:5]):
                # Reset pointer for upload (after preview)
                img_file.seek(0)
                link = upload_to_imgur(img_file)
                if link:
                    public_links[idx] = link
                    st.success(f"Image {idx+1} ({img_file.name}): {link}")
                time.sleep(0.5)  # Rate limit
        else:
            st.info("No images uploaded → Excel has blank image links (add later)")

        # ——— Build Excel rows ———
        rows = []
        for var in st.session_state.variants:
            sku = f"{product_id}-{var['size']}-{var['color']}".upper()
            variation = f"{var['size']}|{var['color']}"
            row = [name, variation, price, mrp, gst,
                   public_links[0], public_links[1], public_links[2], public_links[3], public_links[4],
                   sku, brand, product_id, description, hsn, weight, keywords]
            rows.append(row)

        excel_file = generate_excel(rows)
        st.balloons()
        st.success(f"Excel ready with {len(rows)} variants!")
        st.download_button(
            label="Download Meesho Excel (Upload Now or Add Images Later)",
            data=excel_file,
            file_name=f"meesho_{product_id}_ready.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.caption("Works in deployed apps – upload images directly! Images optional.")