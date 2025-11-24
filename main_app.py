# main_app.py - Simplified main file
import streamlit as st

st.set_page_config(
    page_title="Lucian Traders Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🔧 Lucian Traders Dashboard")
st.sidebar.markdown("---")

# Welcome page when no page is selected
st.title("🏭 Welcome to Lucian Traders Dashboard")
st.markdown("""
### Your All-in-One E-commerce Management Solution

**Navigate using the sidebar to:**
- 📦 **Meesho Product Manager** - Create product catalogs with image uploads
- 📈 **Trend Analysis** - Discover trending products across platforms

---            
**Features:**
✅ Direct image uploads to Imgur  
✅ Excel generation for Meesho  
✅ Trend analysis for manufacturing  
✅ Product research with direct links  
""")

st.sidebar.markdown("---")
st.sidebar.caption("Lucian Traders • E-commerce Management Tool")