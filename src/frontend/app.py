# # import streamlit as st
# # import pandas as pd

# # from components.sidebar import render_sidebar, apply_filters
# # from components.engagement_overview import render_engagement_overview
# # from components.product_analysis import render_product_analysis
# # from components.high_value_detector import render_high_value_detector
# # from components.retention_panel import render_retention_panel
# # from pathlib import Path

# # import os
# # import pandas as pd
# # st.set_page_config(
# #     page_title="Customer Retention Intelligence Dashboard",
# #     page_icon="🏦",
# #     layout="wide"
# # )

# # # ----------------------------
# # # Load Data
# # # ----------------------------
# # @st.cache_data
# # def load_data():
# #     BASE_DIR = Path(__file__).resolve().parent 

# #     # 2. Move up to the project root directory (project_root/)
# #     PROJECT_ROOT = BASE_DIR.parents[1] 
    
# #     # 3. Explicitly point to your CSV file (change 'your_data.csv' to your actual file name)
# #     # If it's inside a 'data' folder, use: PROJECT_ROOT / 'data' / 'your_data.csv'
# #     # Option B: Wrapping the subpath string
# #     # file_path = PROJECT_ROOT / Path('src/data/processed/datasets/enriched_dataset_retention.csv')
   
# #     file_path = PROJECT_ROOT / Path('src/data/processed/datasets/enriched_final_dataset_finance.csv')

# #     return pd.read_csv(file_path)

# # df = load_data()

# # # ----------------------------
# # # Sidebar
# # # ----------------------------
# # filters = render_sidebar(df)
# # filtered_df = apply_filters(df, filters)

# # # ----------------------------
# # # Header
# # # ----------------------------
# # st.title("🏦 Customer Engagement & Retention Dashboard")

# # st.markdown(
# #     """
# #     Analyze customer engagement, product utilization,
# #     churn risk, and retention strength.
# #     """
# # )

# # st.markdown(
# #     """
# #     Bank Product Analytics | Created By Jyotirmai Tiwari | Client Bank:European Central Bank 
# #     """
# # )

# # # ----------------------------
# # # Tabs
# # # ----------------------------
# # tab1, tab2, tab3, tab4 = st.tabs([
# #     "📊 Engagement vs Churn",
# #     "📦 Product Utilization",
# #     "🎯 High-Value Risk",
# #     "💪 Retention Strength"
# # ])

# # with tab1:
# #     render_engagement_overview(filtered_df)

# # with tab2:
# #     render_product_analysis(filtered_df)

# # with tab3:
# #     render_high_value_detector(filtered_df, filters)

# # with tab4:
# #     render_retention_panel(filtered_df)
# import os
# from pathlib import Path
# import pandas as pd
# import streamlit as st

# from components.sidebar import render_sidebar, apply_filters
# from components.engagement_overview import render_engagement_overview
# from components.product_analysis import render_product_analysis
# from components.high_value_detector import render_high_value_detector
# from components.retention_panel import render_retention_panel

# # 1. Page Configuration
# st.set_page_config(
#     page_title="Customer Retention Intelligence Dashboard",
#     page_icon="🏦",
#     layout="wide"
# )

# # 2. Design Layout & Font Improvements (Injecting Clean Global UI Font Styles)
# st.markdown(
#     """
#     <style>
#         html, body, [class*="css"], .stText, p, li, h1, h2, h3, h4 {
#             font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif !important;
#         }
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 12px;
#         }
#         .stTabs [data-baseweb="tab"] {
#             padding-right: 16px;
#             padding-left: 16px;
#             font-weight: 600;
#         }
#     </style>
#     """, 
#     unsafe_allow_html=True
# )

# # 3. Load Data
# @st.cache_data
# def load_data():
#     BASE_DIR = Path(__file__).resolve().parent 
#     PROJECT_ROOT = BASE_DIR.parents[1] 
#     file_path = PROJECT_ROOT / Path('src/data/processed/datasets/enriched_final_dataset_finance.csv')
#     return pd.read_csv(file_path)

# df = load_data()

# # 4. Sidebar Elements
# filters = render_sidebar(df)
# filtered_df = apply_filters(df, filters)

# # 5. Header Section
# st.title("🏦 Customer Engagement & Retention Dashboard")

# st.markdown(
#     "Analyze customer engagement, product utilization, churn risk, and retention strength."
# )

# # Render requested header credits in blue color using Streamlit's native color syntax
# st.markdown(
#     ":blue[Bank Product Analytics | Created By Jyotirmai Tiwari | Client Bank: European Central Bank]"
# )
# st.markdown("---")

# # 6. Navigation Tabs
# tab1, tab2, tab3, tab4 = st.tabs([
#     "📊 Engagement vs Churn",
#     "📦 Product Utilization",
#     "🎯 High-Value Risk",
#     "💪 Retention Strength"
# ])

# with tab1:
#     render_engagement_overview(filtered_df)

# with tab2:
#     render_product_analysis(filtered_df)

# with tab3:
#     render_high_value_detector(filtered_df, filters)

# with tab4:
#     render_retention_panel(filtered_df)

# # 7. Bottom Sticky Footer Layout
# st.markdown("---")
# st.markdown(
#     """
#     <style>
#         .custom-footer {
#             background-color: #f8fafc; 
#             padding: 22px; 
#             border-radius: 12px; 
#             text-align: center; 
#             color: #1e293b; 
#             font-family: 'Courier New', Courier, monospace; 
#             font-size: 0.9rem;
#             border: 1px solid #e2e8f0;
#             transition: all 0.3s ease-in-out;
#             box-shadow: 0 1px 3px rgba(0,0,0,0.02);
#         }
        
#         /* Interactive Hover Effects */
#         .custom-footer:hover {
#             background-color: #e2e8f0; 
#             border-color: #94a3b8;
#             box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
#             transform: translateY(-2px);
#         }
#     </style>

#     <div class="custom-footer">
#         <strong style="letter-spacing: 1px;">EUROPEAN BANK CHURN ANALYTICS DASHBOARD</strong><br>
#         <span style="color: #475569; font-weight: 500; display: inline-block; margin-top: 6px;">
#             Created by <strong>Jyotirmai Tiwari</strong> &nbsp;•&nbsp; 
#             Client: <strong>European Central Bank</strong> &nbsp;•&nbsp; 
#             Dataset: <strong>10,000 Customers</strong> &nbsp;•&nbsp; 
#             <strong>2026-27</strong>
#         </span>
#     </div>
#     """, 
#     unsafe_allow_html=True
# )

import os
from pathlib import Path
import pandas as pd
import streamlit as st

from components.sidebar import render_sidebar, apply_filters
from components.engagement_overview import render_engagement_overview
from components.product_analysis import render_product_analysis
from components.high_value_detector import render_high_value_detector
from components.retention_panel import render_retention_panel

# 1. Page Configuration
st.set_page_config(
    page_title="Customer Retention Intelligence Dashboard",
    page_icon="🏦",
    layout="wide"
)

# 2. Advanced Premium Layout & CSS Injection
st.markdown(
    """
    <style>
        /* Global Typography & Canvas Polish */
        html, body, [class*="css"], .stText, p, li, h1, h2, h3, h4 {
            font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif !important;
        }
        
        /* Main Application Background Tint for Depth */
        .main .block-container {
            background-color: #fcfdfe;
            padding-top: 2rem !important;
        }

        /* Institutional Hero Header Container */
        .hero-header-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            padding: 30px;
            border-radius: 16px;
            color: #ffffff;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
            margin-bottom: 25px;
            border-left: 6px solid #f59e0b; /* Executive Gold Accent Lip */
        }
        
        .hero-header-container h1 {
            color: #ffffff !important;
            margin: 0 0 8px 0 !important;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        
        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
            margin-bottom: 12px;
        }
        
        .hero-meta-badge {
            background-color: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #fbbf24;
            padding: 6px 14px;
            border-radius: 8px;
            display: inline-block;
            font-size: 0.88rem;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        /* High-Catch Tabs Nav Customization */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f1f5f9;
            padding: 6px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.2s ease;
            color: #475569 !important;
            background-color: transparent !important;
            border: none !important;
        }
        
        /* Active Tab Focus States */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #ffffff !important;
            color: #1e3a8a !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08) !important;
        }

        /* Tab Content Panel Outer Shell */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 24px;
            margin-top: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# 3. Load Data
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent 
    PROJECT_ROOT = BASE_DIR.parents[1] 
    file_path = PROJECT_ROOT / Path('src/data/processed/datasets/enriched_final_dataset_finance.csv')
    return pd.read_csv(file_path)

df = load_data()

# 4. Sidebar Elements
filters = render_sidebar(df)
filtered_df = apply_filters(df, filters)

# 5. Dynamic Structured Header Engine
st.markdown(
    """
    <div class="hero-header-container">
        <h1>🏦 Customer Engagement & Retention Dashboard</h1>
        <div class="hero-subtitle">
            Analyze enterprise-level asset distribution, localized product utilization matrix components, loss boundaries, and retention vectors.
        </div>
        <div class="hero-meta-badge">
            BANK PRODUCT ANALYTICS &nbsp;•&nbsp; BY JYOTIRMAI TIWARI &nbsp;•&nbsp; CLIENT: EUROPEAN CENTRAL BANK
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 6. Content Panels / Tabs layout
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

# 7. Interactive Adaptive Footer Engine
st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        .custom-footer {
            background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%); 
            padding: 24px; 
            border-radius: 14px; 
            text-align: center; 
            color: #334155; 
            font-family: 'Courier New', Courier, monospace; 
            font-size: 0.88rem;
            border: 1px solid #cbd5e1;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.01);
        }
        
        .custom-footer:hover {
            background: linear-gradient(90deg, #e2e8f0 0%, #cbd5e1 100%); 
            border-color: #64748b;
            box-shadow: 0 10px 20px rgba(15, 23, 42, 0.05);
            transform: translateY(-3px);
        }
    </style>

    <div class="custom-footer">
        <strong style="letter-spacing: 1.5px; color: #0f172a;">EUROPEAN BANK CHURN ANALYTICS DASHBOARD</strong><br>
        <span style="color: #475569; font-weight: 500; display: inline-block; margin-top: 8px;">
            Created by <strong style="color: #0f172a;">Jyotirmai Tiwari</strong> &nbsp;•&nbsp; 
            Client: <strong style="color: #0f172a;">European Central Bank</strong> &nbsp;•&nbsp; 
            Dataset: <strong style="color: #0f172a;">10,000 Customers</strong> &nbsp;•&nbsp; 
            <strong>2026-27</strong>
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)