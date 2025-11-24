# pages/2_📈_Trend_Analysis.py
import streamlit as st
import time

# Import from utils
from utils.trend_analyzer import get_trending_products_with_links, show_trend_results

# Page configuration
st.set_page_config(
    page_title="Trend Analysis - Lucian Traders",
    page_icon="📈",
    layout="wide"
)

st.title("🛍️ E-commerce Trend Analyzer")
st.subheader("Discover trending apparel designs with direct product links")

st.markdown("""
### 🔍 Find Best-Selling Products

Use this tool to analyze popular apparel designs across major e-commerce platforms.
Get insights on:
- **Best-selling products with direct links** 
- **Popular colors & patterns**
- **Competitive pricing analysis**
- **Manufacturing recommendations**
""")

# Platform selection
col1, col2 = st.columns(2)

with col1:
    st.subheader("Target Platforms")
    selected_sites = st.multiselect(
        "Choose platforms to analyze:",
        ["Amazon Fashion", "Myntra", "Flipkart Fashion", "Nykaa Fashion", "Meesho Trends"],
        default=["Amazon Fashion", "Myntra"]
    )

with col2:
    st.subheader("Apparel Categories")
    categories = st.multiselect(
        "Select categories:",
        ["Women's Kurtis", "Men's T-Shirts", "Women's Dresses", "Men's Shirts", 
         "Ethnic Wear", "Western Wear", "Footwear", "Accessories"],
        default=["Women's Kurtis", "Women's Dresses"]
    )

# Analysis options
with st.expander("⚙️ Analysis Settings"):
    col3, col4 = st.columns(2)
    with col3:
        max_products = st.slider("Products to analyze per platform", 10, 100, 25)
        price_range = st.slider("Target price range (₹)", 100, 10000, (300, 2000))
    
    with col4:
        min_rating = st.slider("Minimum customer rating", 3.0, 5.0, 4.0)
        include_links = st.checkbox("Include product links", value=True, 
                                  help="Get direct links to best-selling products")

# Start analysis button
if st.button("🚀 Start Trend Analysis", type="primary", use_container_width=True):
    if not selected_sites:
        st.error("Please select at least one platform to analyze")
    elif not categories:
        st.error("Please select at least one category")
    else:
        with st.spinner("🕵️ Scanning e-commerce platforms for best-selling products..."):
            # Simulate analysis progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 25:
                    status_text.text(f"🔍 Scanning {selected_sites[0]}...")
                elif i < 50:
                    status_text.text(f"🔍 Analyzing {selected_sites[1] if len(selected_sites) > 1 else 'other platforms'}...")
                elif i < 75:
                    status_text.text("📊 Processing sales data...")
                else:
                    status_text.text("🔗 Collecting product links...")
                time.sleep(0.02)
            
            progress_bar.empty()
            status_text.empty()
            
            # Get trending products with links
            trending_products = get_trending_products_with_links(selected_sites, categories)
            show_trend_results(trending_products, include_links)

# Quick tips
with st.expander("💡 How to use this data for manufacturing"):
    st.markdown("""
    1. **Click product links** - Study best-selling items directly
    2. **Analyze customer reviews** - Understand what buyers love
    3. **Check product images** - See design details and styling
    4. **Compare pricing** - Find the optimal price points
    5. **Note materials & features** - Replicate successful elements
    """)