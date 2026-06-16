import streamlit as st

def render_sidebar(df):

    st.sidebar.header("Analysis Controls")

    # Engagement Filters

    engagement_segment = st.sidebar.multiselect(
        "Engagement Segment",
        sorted(df["Engagement_Segment"].dropna().unique()),
        default=sorted(df["Engagement_Segment"].dropna().unique())
    )

    engagement_level = st.sidebar.multiselect(
        "Engagement Level",
        sorted(df["Engagement_Level"].dropna().unique()),
        default=sorted(df["Engagement_Level"].dropna().unique())
    )

    active_member = st.sidebar.radio(
        "Active Member",
        ["All","Active","Inactive"]
    )

    # Product Slider
    product_max = st.sidebar.select_slider(
    "Number of Products",
    options=[1, 2, 3, 4],
    value=4
)

    product_range = (1, product_max)
    
#     min_products = int(df["NumOfProducts"].min())
#     max_products = int(df["NumOfProducts"].max())

#     product_max = st.sidebar.slider(
#     "Maximum Number of Products",
#     min_value=2,
#     max_value=max_products,
#     value=max_products
# )
#     product_range = (min_products, product_max)
   
    st.sidebar.divider()

    balance_threshold = st.sidebar.number_input(
        "Balance Threshold",
        value=100000
    )

    salary_threshold = st.sidebar.number_input(
        "Salary Threshold",
        value=100000
    )

    return {
        "EngagementSegment": engagement_segment,
        "EngagementLevel": engagement_level,
        "ActiveMember": active_member,
        "ProductRange": product_range,
        "BalanceThreshold": balance_threshold,
        "SalaryThreshold": salary_threshold
    }