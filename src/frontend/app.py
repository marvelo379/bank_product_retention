import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar, apply_filters
from components.engagement_overview import render_engagement_overview
from components.product_analysis import render_product_analysis
from components.high_value_detector import render_high_value_detector
from components.retention_panel import render_retention_panel
from pathlib import Path

import os
import pandas as pd
st.set_page_config(
    page_title="Customer Retention Intelligence Dashboard",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent 

    # 2. Move up to the project root directory (project_root/)
    PROJECT_ROOT = BASE_DIR.parents[1] 
    
    # 3. Explicitly point to your CSV file (change 'your_data.csv' to your actual file name)
    # If it's inside a 'data' folder, use: PROJECT_ROOT / 'data' / 'your_data.csv'
    # Option B: Wrapping the subpath string
    # file_path = PROJECT_ROOT / Path('src/data/processed/datasets/enriched_dataset_retention.csv')
   
    file_path = PROJECT_ROOT / Path('src/data/processed/datasets/enriched_final_dataset_finance.csv')

    return pd.read_csv(file_path)

df = load_data()

# ----------------------------
# Sidebar
# ----------------------------
filters = render_sidebar(df)
filtered_df = apply_filters(df, filters)

# ----------------------------
# Header
# ----------------------------
st.title("🏦 Customer Engagement & Retention Dashboard")

st.markdown(
    """
    Analyze customer engagement, product utilization,
    churn risk, and retention strength.
    """
)

# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Engagement vs Churn",
    "📦 Product Utilization",
    "🎯 High-Value Risk",
    "💪 Retention Strength"
])

with tab1:
    render_engagement_overview(filtered_df)

with tab2:
    render_product_analysis(filtered_df)

with tab3:
    render_high_value_detector(filtered_df, filters)

with tab4:
    render_retention_panel(filtered_df)