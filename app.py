import streamlit as st
import pandas as pd
import io
import re

# Page Configuration
st.set_page_config(
    page_title="DataPolish | Smart CSV & Excel Cleaner",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 24px;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2563EB;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 600;
    }
    .stDownloadButton > button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px;
    }
    .stDownloadButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-header">📊 DataPolish: Automated Data Cleaning SaaS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload messy Excel or CSV exports to automatically clean, standardize, and transform into audit-ready reports.</div>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("📁 Upload & Settings")

upload_option = st.sidebar.radio("Data Source:", ["Upload My File", "Load Built-in Sample Dataset"])

df_raw = None

if upload_option == "Upload My File":
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
else:
    try:
        df_raw = pd.read_csv("sample_messy_data.csv")
        st.sidebar.success("Sample dataset loaded successfully!")
    except Exception as e:
        st.error(f"Could not load sample data: {e}")

if df_raw is not None:
    # Sidebar Cleaning Configurations
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛠️ Cleaning Operations")
    
    do_dedup = st.sidebar.checkbox("Remove Duplicate Rows", value=True)
    do_trim = st.sidebar.checkbox("Trim Extra Whitespaces", value=True)
    do_casing = st.sidebar.checkbox("Standardize Text (Title Case)", value=True)
    do_currency = st.sidebar.checkbox("Clean Currency & Numbers (Remove $, Rs, commas)", value=True)
    do_dates = st.sidebar.checkbox("Standardize Dates to YYYY-MM-DD", value=True)
    
    # Process Data
    df_clean = df_raw.copy()
    initial_rows = len(df_raw)
    
    # 1. Deduplication
    if do_dedup:
        df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    duplicates_removed = initial_rows - len(df_clean)
    
    # 2. Whitespace & Text Casing
    for col in df_clean.select_dtypes(include=["object"]).columns:
        if do_trim:
            df_clean[col] = df_clean[col].astype(str).str.strip()
        if do_casing:
            # Check if column is not an email
            if "email" not in col.lower() and "url" not in col.lower() and "link" not in col.lower():
                df_clean[col] = df_clean[col].astype(str).str.title()
            elif "email" in col.lower():
                df_clean[col] = df_clean[col].astype(str).str.lower()

    # 3. Currency and numeric cleaner
    if do_currency:
        for col in df_clean.columns:
            # Check if column looks like currency or price
            if any(term in col.lower() for term in ["price", "amount", "cost", "salary", "revenue", "rate", "fee"]):
                try:
                    df_clean[col] = (
                        df_clean[col]
                        .astype(str)
                        .str.replace("$", "", regex=False)
                        .str.replace("₹", "", regex=False)
                        .str.replace("Rs", "", regex=False)
                        .str.replace(",", "", regex=False)
                        .str.strip()
                    )
                    df_clean[col] = pd.to_numeric(df_clean[col], errors="ignore")
                except:
                    pass

    # 4. Dates
    if do_dates:
        for col in df_clean.columns:
            if "date" in col.lower() or "time" in col.lower() or "dob" in col.lower():
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col], format="mixed", errors="ignore")
                    if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                        df_clean[col] = df_clean[col].dt.strftime("%Y-%m-%d")
                except:
                    pass

    # Metrics Display
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{initial_rows}</div><div class="metric-lbl">Original Rows</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{len(df_clean)}</div><div class="metric-lbl">Cleaned Rows</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-val" style="color: {"#EF4444" if duplicates_removed > 0 else "#10B981"}">{duplicates_removed}</div><div class="metric-lbl">Duplicates Removed</div></div>', unsafe_allow_html=True)
    with col4:
        missing_count = int(df_clean.isna().sum().sum())
        st.markdown(f'<div class="metric-card"><div class="metric-val" style="color: #10B981">{len(df_clean.columns)}</div><div class="metric-lbl">Columns Cleaned</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Tabs
    tab1, tab2, tab3 = st.tabs(["✨ Cleaned Dataset", "🔍 Before vs After Diff", "📈 Analytics & Charts"])

    with tab1:
        st.subheader("Cleaned & Standardized Data")
        st.dataframe(df_clean, use_container_width=True)

    with tab2:
        st.subheader("Raw Source vs Cleaned Output")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Original Raw File:**")
            st.dataframe(df_raw.head(10), use_container_width=True)
        with c2:
            st.markdown("**Cleaned & Structured Output:**")
            st.dataframe(df_clean.head(10), use_container_width=True)

    with tab3:
        st.subheader("Visual Data Insights")
        # Find categorical column for chart
        cat_cols = df_clean.select_dtypes(include=["object"]).columns.tolist()
        num_cols = df_clean.select_dtypes(include=["number"]).columns.tolist()
        
        if len(cat_cols) > 0:
            primary_cat = cat_cols[0]
            for col in cat_cols:
                if any(k in col.lower() for k in ["product", "location", "city", "category", "service"]):
                    primary_cat = col
                    break
                    
            st.write(f"**Distribution by {primary_cat}:**")
            chart_data = df_clean[primary_cat].value_counts().reset_index()
            chart_data.columns = [primary_cat, "Count"]
            st.bar_chart(chart_data.set_index(primary_cat))
        else:
            st.info("No categorical text columns detected for bar chart visualization.")

    st.markdown("---")

    # Download Section
    st.subheader("📥 Export Cleaned Dataset")
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        # Excel buffer
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_raw.to_excel(writer, sheet_name="Raw_Data", index=False)
            df_clean.to_excel(writer, sheet_name="Clean_Data", index=False)
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Cleaned Excel (.xlsx)",
            data=excel_buffer,
            file_name="Cleaned_Data_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with d_col2:
        # CSV buffer
        csv_data = df_clean.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Download Cleaned CSV (.csv)",
            data=csv_data,
            file_name="Cleaned_Dataset.csv",
            mime="text/csv"
        )

else:
    st.info("👈 Please upload an Excel/CSV file or choose 'Load Built-in Sample Dataset' in the sidebar to begin.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
    "DataPolish SaaS Engine &copy; 2026 | Built by <strong>Onkar Hande</strong> (BCA / MCA) | "
    "<a href='https://onkarhande96.github.io' target='_blank' style='color: #2563EB;'>View Portfolio</a> • "
    "<a href='https://github.com/Onkarhande96' target='_blank' style='color: #2563EB;'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
