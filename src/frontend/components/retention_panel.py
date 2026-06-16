
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_retention_panel(df):
    st.subheader("💪 Advanced Retention Strength Scoring Panel")
    st.markdown("Deep dive into customer health metrics, synthetic retention scores, and underlying driver correlations.")

    # --- 0. BACKGROUND DATA PREPARATION ---
    temp = df.copy()

    # Calculate Synthetic Retention Score
    temp["Retention_Score"] = (
        0.30 * temp["engagement_score"]
        + 0.25 * temp["Loyalty_Ratio"]
        + 0.20 * temp["Relationship_Intensity_Score"]
        + 0.15 * temp["Customer_Satisfaction_Score"]
        + 0.10 * temp["Switching_Cost_Index"]
    )

    # Ensure Status is a cleanly mapped string for plots
    temp["Status"] = temp["Exited"].map({0: "Retained", 1: "Churned"})

    # Bin Retention Scores into standard categories
    bins = [0, 0.4, 0.6, 0.8, 1.0]
    labels = ["Low Risk (0.0-0.4)", "Medium Risk (0.4-0.6)", "High Health (0.6-0.8)", "Elite Health (0.8-1.0)"]
    # Fallback to handle scores if they scale outside standard 0-1 ranges
    max_score = max(temp["Retention_Score"].max(), 1.0)#Retention_Score
    min_score = min(temp["Retention_Score"].min(), 0.0)
    
    temp["Retention_Category"] = pd.cut(
        temp["Retention_Score"], 
        bins=[min_score, 0.4, 0.6, 0.8, max_score], 
        labels=labels, 
        include_lowest=True
    )

    # --- 1. CORE FORMULA WEIGHTS & SUMMARY ---
    with st.expander("ℹ️ View Retention Score Computation Model Weights", expanded=False):
        w1, w2, w3, w4, w5 = st.columns(5)
        w1.metric("Engagement Score", "30%", help="Base activity profile tracking")
        w2.metric("Loyalty Ratio", "25%", help="Tenure and account history depth")
        w3.metric("Relationship Intensity", "20%", help="Product cross-sell interactions")
        w4.metric("Satisfaction Score", "15%", help="Direct customer sentiment survey feedback")
        w5.metric("Switching Cost Index", "10%", help="Financial/Operational exit barriers")

    st.write("---")

    # --- ROW 1: CORE DISTRIBUTIONS & SEGMENTS ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # ⭐⭐⭐ 1. Retention Score Distribution
        fig_dist = px.histogram(
            temp,
            x="Retention_Score",
            color="Status",
            title="<b>Retention Score Distribution</b>",
            labels={"Retention_Score": "Calculated Retention Score", "count": "Customer Count"},
            barmode="overlay",
            color_discrete_map={"Retained": "#2E7D32", "Churned": "#D32F2F"},
            opacity=0.75
        )
        fig_dist.update_layout(title_x=0.05, legend_title_text="Customer Status")
        st.plotly_chart(fig_dist, use_container_width=True)

    with row1_col2:
        # ⭐⭐⭐ 2. Churn Rate by Retention Category
        cat_churn = temp.groupby("Retention_Category", observed=False)["Exited"].mean().reset_index()
        cat_churn["Churn Rate (%)"] = cat_churn["Exited"] * 100
        
        fig_cat = px.bar(
            cat_churn,
            x="Retention_Category",
            y="Churn Rate (%)",
            title="<b>Churn Rate by Retention Category</b>",
            labels={"Retention_Category": "Retention Tier Breakdown"},
            color="Churn Rate (%)",
            color_continuous_scale="RdYlGn_r",
            text_auto=".1f"
        )
        fig_cat.update_layout(title_x=0.05, showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)


    # --- ROW 2: ADVANCED MATRIX RELATIONSHIPS ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # ⭐⭐⭐ 3. CLV vs Retention Scatter
        # Dynamically checks if CLV exists, falls back cleanly to EstimatedSalary if missing
        clv_col = "CLV" if "CLV" in temp.columns else ("EstimatedSalary" if "EstimatedSalary" in temp.columns else temp.columns[2])
        
        fig_scatter = px.scatter(
            temp.sample(min(2000, len(temp))), # Sampling avoids UI lagging on heavy datasets
            x="Retention_Score",
            y=clv_col,
            color="Status",
            opacity=0.6,
            title=f"<b>Value Matrix: {clv_col} vs Retention Score</b>",
            labels={"Retention_Score": "Retention Score", clv_col: f"Customer Value Vector ({clv_col})"},
            color_discrete_map={"Retained": "#2E7D32", "Churned": "#D32F2F"}
        )
        fig_scatter.update_layout(title_x=0.05, legend_title_text="Status")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with row2_col2:
        # ⭐⭐⭐ 4. Correlation Heatmap
        corr_cols = [
            "Retention_Score", "engagement_score", "Loyalty_Ratio", 
            "Relationship_Intensity_Score", "Customer_Satisfaction_Score", "Switching_Cost_Index"
        ]
        # Filter down dynamically to columns present in df
        valid_corr_cols = [c for c in corr_cols if c in temp.columns]
        corr_matrix = temp[valid_corr_cols].corr()

        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="<b>Feature Correlation Matrix</b>",
            labels=dict(color="Correlation")
        )
        fig_heat.update_layout(title_x=0.05)
        st.plotly_chart(fig_heat, use_container_width=True)


    # --- ROW 3: DEEP CROSS-SEGMENT BREAKDOWNS ---
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        # ⭐⭐⭐ 5. Retention by Engagement Segment (or dynamic substitute)
        eng_col = "Engagement_Segment" if "Engagement_Segment" in temp.columns else "Product_Segment"
        if eng_col in temp.columns:
            fig_box1 = px.box(
                temp,
                x=eng_col,
                y="Retention_Score",
                color="Status",
                title=f"<b>Retention Across {eng_col.replace('_',' ')} Tiers</b>",
                color_discrete_map={"Retained": "#2E7D32", "Churned": "#D32F2F"}
            )
            fig_box1.update_layout(title_x=0.05, boxmode="group")
            st.plotly_chart(fig_box1, use_container_width=True)
        else:
            st.info("Add an 'Engagement_Segment' column to visualize categorical boxplots.")

    with row3_col2:
     
     st.markdown("##### ⭐ Retention by Customer Value Segment / Clusters")

    # Mapping to your exact dataset column name 'cluster_id'
    if "cluster_id" in temp.columns:
        cluster_col = "cluster_id"
    # Fallback options based on your column list
    elif "customer_value_segment" in temp.columns:
        cluster_col = "customer_value_segment"
    elif "Engagement_Segment" in temp.columns:
        cluster_col = "Engagement_Segment"
    else:
        cluster_col = None

    if cluster_col:
        # Group and calculate mean retention
        cluster_avg = (
            temp.groupby(cluster_col)["Retention_Score"]
            .mean()
            .reset_index()
            .sort_values(by="Retention_Score")
        )
        
        # Convert cluster_id to string if it's numeric so the chart treats it as discrete categories
        if cluster_col == "cluster_id":
            cluster_avg[cluster_col] = cluster_avg[cluster_col].astype(str)

        fig_cluster = px.bar(
            cluster_avg,
            x="Retention_Score",
            y=cluster_col,
            orientation='h',
            title=f"<b>Average Retention Score by {cluster_col}</b>",
            color="Retention_Score",
            color_continuous_scale="Cividis"  # Clean, high-contrast continuous palette
        )
        fig_cluster.update_layout(title_x=0.05, showlegend=False)
        st.plotly_chart(fig_cluster, use_container_width=True)
    else:
        st.info("Add 'cluster_id' or a segmented group attribute to view grouping baselines.")

    # --- ROW 4: FEATURE IMPORTANCE / CONTRIBUTION MODEL ---
    st.write("---")
    st.markdown("### 📊 Feature Contribution / Importance to Retention Model")
    
    # Structural breakdown mapping static model coefficient vectors
    feature_importance = pd.DataFrame({
        "Model Driver Component": [
            "Engagement Score", "Loyalty Ratio", 
            "Relationship Intensity Score", "Customer Satisfaction Score", "Switching Cost Index"
        ],
        "Mathematical Framework Weight": [0.30, 0.25, 0.20, 0.15, 0.10]
    }).sort_values(by="Mathematical Framework Weight", ascending=True)

    fig_importance = px.bar(
        feature_importance,
        x="Mathematical Framework Weight",
        y="Model Driver Component",
        orientation="h",
        title="<b>Retention Score Component Weights (Impact Multipliers)</b>",
        text_auto=".2f",
        color="Mathematical Framework Weight",
        color_continuous_scale="Blues"
    )
    fig_importance.update_layout(title_x=0.01, showlegend=False, xaxis=dict(tickformat=".0%"))
    st.plotly_chart(fig_importance, use_container_width=True)


  # --- ROW 5: CRITICAL DRILL-DOWN ACTIONABLE TRACKING ---
    st.markdown("### 🔍 Risk Profile Drill-Down Matrix (Top 20 At-Risk Accounts)")
    st.markdown("*Visualizing the highest-priority accounts ordered by immediate churn risk.*")

    # 1. Filter, isolate, and sort your target subset
    drill_down_df = temp[[
        "CustomerId", "Retention_Score", "Loyalty_Ratio", 
        "Relationship_Intensity_Score", "Customer_Satisfaction_Score", "Status"
    ]].sort_values("Retention_Score", ascending=True).head(20).copy()

    # Convert CustomerId to a pure string configuration so Plotly treats it as a discrete label/axis categorical item
    drill_down_df["Customer ID String"] = "ID: " + drill_down_df["CustomerId"].astype(str)

    # 2. Build the horizontal risk tracking architecture
    fig_risk_drill = px.bar(
        drill_down_df,
        x="Retention_Score",
        y="Customer ID String",
        orientation="h",
        color="Status",
        title="<b>Top 20 At-Risk Accounts by Overall Health Index</b>",
        labels={
            "Retention_Score": "Overall Health Index (Lower = Higher Risk)",
            "Customer ID String": "Customer Reference"
        },
        # Explicit high-contrast tactical color maps
        color_discrete_map={"Retained": "#FFA500", "Churned": "#D9534F"},
        hover_data={
            "Customer ID String": False, # Hide redundant labels
            "Retention_Score": ":.3f",
            "Loyalty_Ratio": ":.2f",
            "Relationship_Intensity_Score": ":.2f",
            "Customer_Satisfaction_Score": ":.2f"
        },
        text="Retention_Score" # Renders the exact numeric risk value inside the visual elements
    )

    # 3. Apply professional visual canvas settings
    fig_risk_drill.update_traces(
        texttemplate='%{text:.2f}', 
        textposition='inside',
        marker_line_color='rgba(0,0,0,0)',
        marker_line_width=0
    )

    fig_risk_drill.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            range=[0, 1.05], 
            showgrid=True, 
            gridcolor="rgba(200,200,200,0.2)",
            side="top" # Places scale markers at top for quick glance reading
        ),
        yaxis=dict(
            autorange="reversed", # Forces the absolute lowest Retention Scores to stay locked at the top row position
            showgrid=False
        ),
        legend=dict(
            title_text="Current Account State",
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=120, r=20, t=60, b=40), # Give room for ID tags
        height=600 # Expanded structural viewport footprint so 20 discrete rows breathe cleanly
    )

    # 4. Compile directly to Streamlit container context
    st.plotly_chart(fig_risk_drill, use_container_width=True)