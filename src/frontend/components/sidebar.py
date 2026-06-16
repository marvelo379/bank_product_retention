import streamlit as st


def render_sidebar(df):

    st.sidebar.header("🔍 Analysis Controls")

    engagement_segment = st.sidebar.multiselect(
        "Engagement Segment",
        options=sorted(df["Engagement_Segment"].dropna().unique()),
        default=sorted(df["Engagement_Segment"].dropna().unique())
    )

    engagement_level = st.sidebar.multiselect(
        "Engagement Level",
        options=sorted(df["Engagement_Level"].dropna().unique()),
        default=sorted(df["Engagement_Level"].dropna().unique())
    )

    active_member = st.sidebar.radio(
        "Active Member",
        ["All", "Active", "Inactive"]
    )

    st.sidebar.divider()

    product_range = st.sidebar.slider(
        "📦 Number of Products",
        min_value=int(df["NumOfProducts"].min()),
        max_value=int(df["NumOfProducts"].max()),
        value=(
            int(df["NumOfProducts"].min()),
            int(df["NumOfProducts"].max())
        )
    )

    st.sidebar.divider()

    balance_threshold = st.sidebar.number_input(
        "💰 Balance Threshold",
        value=100000
    )

    salary_threshold = st.sidebar.number_input(
        "💵 Salary Threshold",
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


def apply_filters(df, filters):

    temp = df.copy()

    temp = temp[
        temp["Engagement_Segment"].isin(
            filters["EngagementSegment"]
        )
    ]

    temp = temp[
        temp["Engagement_Level"].isin(
            filters["EngagementLevel"]
        )
    ]

    temp = temp[
        temp["NumOfProducts"].between(
            filters["ProductRange"][0],
            filters["ProductRange"][1]
        )
    ]

    if filters["ActiveMember"] == "Active":
        temp = temp[temp["IsActiveMember"] == 1]

    elif filters["ActiveMember"] == "Inactive":
        temp = temp[temp["IsActiveMember"] == 0]

    return temp